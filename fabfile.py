from fabric import task


@task
def hello(c):
    c.run("echo Hello world!")


@task
def update_pkg_db(c):
    c.sudo("apt-get -yq update")


@task
def upgrade_pkgs(c):
    update_pkg_db(c)
    c.sudo("apt-get -yq dist-upgrade")


@task
def apt_install(c, packages):
    if isinstance(packages, list):
        packages = " ".join(packages)
    c.sudo("apt-get -yq install " + packages)


@task
def apt_purge(c, packages):
    if isinstance(packages, list):
        packages = " ".join(packages)
    c.sudo("apt-get -yq purge " + packages)


@task
def install_usual_packages(c):
    update_pkg_db(c)
    apt_install(c, "tmux curl git build-essential mosh ca-certificates curl wget python python3 htop tree traceroute lm-sensors")


@task
def zsh(c):
    update_pkg_db(c)
    apt_install(c, "zsh zsh-antigen wget")
    c.run("wget -O ~/.zshrc https://gist.github.com/sebva/1adeaa10995e124b4166/raw"
        "/5fffc1a28fb070e107d414fff8605ac13ba2253b/.zshrc")
    user = c.run("whoami").stdout
    c.sudo("chsh -s /bin/zsh " + user)
    c.sudo("curl -o /usr/share/zsh-antigen/antigen.zsh -sL https://git.io/antigen")


@task
def fish(c):
    update_pkg_db(c)
    apt_install(c, "fish")
    user = c.run("whoami").stdout
    c.sudo("chsh -s /usr/bin/fish " + user)


@task
def disable_ua(c):
    apt_purge(c, "ubuntu-advantage-tools")
    c.sudo("sed -i'' 's/ENABLED=1/ENABLED=0/' /etc/default/motd-news")


@task
def disable_swap(c):
    c.sudo("swapoff -a")
    c.sudo("systemctl mask swap.img.swap")
    c.sudo("sed -i'.bak' 's-/swap.img-# /swap.img-' /etc/fstab")
    c.run("free")


@task
def install_sgx(c, trusted_platform_services=True):
    update_pkg_db(c)
    # TODO Separate pkgs for trusted platform services
    apt_install(c,
        "--no-install-recommends ca-certificates build-essential ocaml automake autoconf libtool wget python "
        "libssl-dev libcurl4-openssl-dev protobuf-compiler libprotobuf-dev alien cmake uuid-dev libxml2-dev "
        "pkg-config")
    apt_install(c, "ocamlbuild", warn_only=True)
    with c.cd(c.run("mktemp -d")):
        c.run("wget -O - https://github.com/01org/linux-sgx-driver/archive/sgx_driver_2.0.tar.gz | tar -xz")
        with c.cd("linux-sgx-driver-sgx_driver_2.0"):
            c.run("make") and c.sudo("make install && depmod && modprobe isgx")

        if trusted_platform_services:
            c.run("wget --progress=dot:mega -O iclsclient.rpm "
                "http://registrationcenter-download.intel.com/akdlm/irc_nas/11414/iclsClient-1.45.449.12-1.x86_64.rpm")
            c.sudo("alien --scripts -i iclsclient.rpm")

            c.run("wget --progress=dot:mega -O - https://github.com/01org/dynamic-application-loader-host-interface"
                "/archive/7b49da96ee2395909d867234c937c7726550c82f.tar.gz | tar -xz")
            with c.cd("dynamic-application-loader-host-interface-7b49da96ee2395909d867234c937c7726550c82f"):
                c.run("cmake . -DCMAKE_BUILD_TYPE=Release && make -j $(nproc)")
                c.sudo("make install")

        c.run("wget --progress=dot:mega -O - https://github.com/01org/linux-sgx/archive/sgx_2.0.tar.gz | tar -xz")
        with c.cd("linux-sgx-sgx_2.0"):
            c.run("wget -O - https://gist.github.com/sebyx31/ce85d4d5aa724c600be7ce69ed4ec9a4/raw"
                "/6d58de3f7b99c8c9366e9bee429e47ebe0de8c8e/no-unused.patch | patch -p1")
            c.run("./download_prebuilt.sh 2> /dev/null && make -s -j$(nproc) sdk_install_pkg psw_install_pkg")
            c.sudo("./linux/installer/bin/sgx_linux_x64_sdk_2.0.40950.bin --prefix=/opt/intel && "
                 "./linux/installer/bin/sgx_linux_x64_psw_2.0.40950.bin")

