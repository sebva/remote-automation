from fabric.operations import run, sudo


def hello():
    run("echo Hello world!")


def install_usual_packages():
    sudo("apt-get -yq update")
    sudo("apt-get -yq install tmux curl git build-essential mosh ca-certificates curl wget python python3")


def zsh():
    sudo("apt-get -yq update")
    sudo("apt-get -yq install zsh zsh-antigen wget")
    run("wget -O ~/.zshrc " +
        "https://gist.github.com/sebyx31/1adeaa10995e124b4166/raw/5fffc1a28fb070e107d414fff8605ac13ba2253b/.zshrc")
    user = run("whoami")
    sudo("chsh -s /bin/zsh " + user)
