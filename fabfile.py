from fabric.context_managers import cd
from fabric.decorators import runs_once
from fabric.operations import run, sudo
from fabric.state import env

env.use_ssh_config = True


def hello():
    run("echo Hello world!")


@runs_once
def update_pkg_db():
    sudo("apt-get -yq update")


def upgrade_pkgs():
    update_pkg_db()
    sudo("apt-get -yq dist-upgrade")


def apt_install(packages):
    if isinstance(packages, list):
        packages = " ".join(packages)
    sudo("apt-get -yq install " + packages)


def install_usual_packages():
    update_pkg_db()
    apt_install("tmux curl git build-essential mosh ca-certificates curl wget python python3")


def zsh():
    update_pkg_db()
    apt_install("zsh zsh-antigen wget")
    run("wget -O ~/.zshrc https://gist.github.com/sebyx31/1adeaa10995e124b4166/raw"
        "/5fffc1a28fb070e107d414fff8605ac13ba2253b/.zshrc")
    user = run("whoami")
    sudo("chsh -s /bin/zsh " + user)


def install_sgx(trusted_platform_services=True):
    update_pkg_db()
    # TODO Separate pkgs for trusted platform services
    apt_install(
        "--no-install-recommends ca-certificates build-essential ocaml automake autoconf libtool wget python "
        "libssl-dev libcurl4-openssl-dev protobuf-compiler libprotobuf-dev alien cmake uuid-dev libxml2-dev "
        "pkg-config ocamlbuild")
    with cd(run("mktemp -d")):
        run("wget -O - https://github.com/01org/linux-sgx-driver/archive/sgx_driver_2.0.tar.gz | tar -xz")
        with cd("linux-sgx-driver-sgx_driver_2.0"):
            run("make") and sudo("make install && depmod && modprobe isgx")

        if trusted_platform_services:
            run("wget --progress=dot:mega -O iclsclient.rpm "
                "http://registrationcenter-download.intel.com/akdlm/irc_nas/11414/iclsClient-1.45.449.12-1.x86_64.rpm")
            sudo("alien --scripts -i iclsclient.rpm")

            run("wget --progress=dot:mega -O - https://github.com/01org/dynamic-application-loader-host-interface"
                "/archive/7b49da96ee2395909d867234c937c7726550c82f.tar.gz | tar -xz")
            with cd("dynamic-application-loader-host-interface-7b49da96ee2395909d867234c937c7726550c82f"):
                run("cmake . -DCMAKE_BUILD_TYPE=Release && make -j $(nproc)")
                sudo("make install")

        run("wget --progress=dot:mega -O - https://github.com/01org/linux-sgx/archive/sgx_2.0.tar.gz | tar -xz")
        with cd("linux-sgx-sgx_2.0"):
            run("wget -O - https://gist.github.com/sebyx31/ce85d4d5aa724c600be7ce69ed4ec9a4/raw"
                "/6d58de3f7b99c8c9366e9bee429e47ebe0de8c8e/no-unused.patch | patch -p1")
            run("./download_prebuilt.sh 2> /dev/null && make -s -j$(nproc) sdk_install_pkg psw_install_pkg")
            sudo("./linux/installer/bin/sgx_linux_x64_sdk_2.0.40950.bin --prefix=/opt/intel && "
                 "./linux/installer/bin/sgx_linux_x64_psw_2.0.40950.bin")
