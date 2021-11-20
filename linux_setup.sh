#!/bin/bash

set -ex

pip_setup() {

    # pip2:
    # curl -O https://bootstrap.pypa.io/pip/2.7/get-pip.py | python

    # pip3:
    # curl -O https://bootstrap.pypa.io/get-pip.py | python

    if [ "$(pip config list | grep -c mirrors.aliyun.com)" -eq 0 ]; then
        if [ -d "${HOME}/miniconda3/" ]; then
            source "${HOME}/miniconda3/bin/activate" base
        fi
        pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
        pip config set global.trusted-host mirrors.aliyun.com
    fi
}

install_docker() {

    if [ "$(dpkg --list | grep -c docker-ce)" -eq 0 ]; then
        curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun

        sudo mkdir -p /etc/docker
        sudo tee /etc/docker/daemon.json <<-EOF
{
    "registry-mirrors": [
        "https://oq1auek6.mirror.aliyuncs.com",
        "https://hub-mirror.c.163.com",
        "https://mirror.baidubce.com"
    ],
    "insecure-registries": [
        "192.168.1.229"
    ]
}
EOF

        sudo getent group docker || groupadd docker
        sudo usermod -aG docker $USER
        sudo service docker start

        if [ "$(ps -ef | grep "systemd " | grep -cv grep)" -eq 0 ]; then
            sudo service docker restart
        else
            sudo systemctl daemon-reload
            sudo systemctl restart docker
        fi
    fi

}

install_tmux() {
    sudo apt install -y tmux
    if [ ! -d "${HOME}/.tmux" ]; then
        cd
        git clone --depth=1 https://github.com/gpakosz/.tmux.git
        ln -s -f .tmux/.tmux.conf
        cp .tmux/.tmux.conf.local .
    fi
}

install_zsh() {
    sudo apt install -y zsh

    zsh="$(which zsh)"
    sudo chsh -s "$zsh" "$USER"
    export SHELL="$zsh"

    if [ ! -d "${HOME}/.oh-my-zsh/lib/" ]; then
        if [ ! -f "ohmyzsh_install.sh" ]; then
            curl -fsSL -o ohmyzsh_install.sh https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh
        fi
        sh ohmyzsh_install.sh --unattended
    fi

    if [ ! -d "${HOME}/.oh-my-zsh/custom/themes/powerlevel10k" ]; then
        git clone --depth=1 https://github.com/romkatv/powerlevel10k.git "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}"/themes/powerlevel10k

        # ZSH_THEME="powerlevel10k/powerlevel10k" in ~/.zshrc
        sed -i 's/^\(ZSH_THEME\).*/\1="powerlevel10k\/powerlevel10k"/' ~/.zshrc
    fi

    if [ ! -d "${HOME}/.oh-my-zsh/custom/plugins/zsh-autosuggestions" ]; then
        git clone --depth=1 git://github.com/zsh-users/zsh-autosuggestions "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}"/plugins/zsh-autosuggestions

        add_plugin_to_zsh "zsh-autosuggestions"
    fi
}

install_miniconda() {

    if [ ! -d "${HOME}/miniconda3/" ]; then
        if [ ! -f "Miniconda3-latest-Linux-x86_64.sh" ]; then
            wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
        fi
        bash Miniconda3-latest-Linux-x86_64.sh -b
    fi

    if [ "$(cat ${HOME}/.zshrc | grep -c 'conda initialize')" -eq 0 ]; then
        ~/miniconda3/bin/conda init zsh
    fi

    if [ ! -f ~/.condarc ]; then
        tee ~/.condarc <<-EOF
channels:
  - defaults
show_channel_urls: true
default_channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
custom_channels:
  conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  msys2: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  bioconda: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  menpo: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  simpleitk: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
EOF
    fi
}

add_plugin_to_zsh() {
    plugin_name="$1"
    if [ "$(cat ~/.zshrc | grep -c $plugin_name)" -eq 0 ]; then
        allPlugins=$(grep ^plugins= ~/.zshrc | cut -d '(' -f2 | cut -d ')' -f1)
        allPlugins="${allPlugins} $plugin_name"
        sed -i 's/^plugins=.*/plugins=('"${allPlugins}"')/' ~/.zshrc
    fi
}

install_pyenv() {

    sudo apt-get update
    sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
        libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
        libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

    PYENV_ROOT="${HOME}/.pyenv"
    if [ ! -d "$PYENV_ROOT" ]; then
        git clone https://github.com/pyenv/pyenv.git "${PYENV_ROOT}"

        # echo 'export PYENV_ROOT="$HOME/.pyenv"' >>~/.profile
        # echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >>~/.profile
        # echo 'eval "$(pyenv init --path)' >>~/.profile

        echo 'export PYENV_ROOT="$HOME/.pyenv"' >>~/.zprofile
        echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >>~/.zprofile
        echo 'eval "$(pyenv init --path)"' >>~/.zprofile

        echo 'eval "$(pyenv init -)"' >>~/.zshrc
    fi

    if [ ! -d "${HOME}/.pyenv/plugins/pyenv-virtualenv" ]; then
        git clone https://github.com/pyenv/pyenv-virtualenv.git "${PYENV_ROOT}/plugins/pyenv-virtualenv"
        echo 'eval "$(pyenv virtualenv-init -)"' >>~/.zshrc
    fi

    # zsh add plugin
    add_plugin_to_zsh "pyenv"
}

config_network() {

    if [ "$(uname -a | grep -c WSL)" -eq 1 ]; then
        sudo tee /etc/wsl.conf <<-EOF
[network]
generateResolvConf = false
EOF

        sudo rm /etc/resolv.conf
        sudo tee /etc/resolv.conf <<-EOF
nameserver 114.114.114.114
nameserver 8.8.8.8
nameserver 1.1.1.1
EOF

    elif [ "$(uname -a | grep -c Debian)" -eq 1 ]; then
        if ! systemctl list-units --full -all | grep -Fq resolvconf.service; then
            sudo apt update
            sudo apt install -y resolvconf
            sudo systemctl enable resolvconf.service
            sudo systemctl start resolvconf.service
            sudo systemctl -l --no-pager status resolvconf.service

            sudo tee /etc/resolvconf/resolv.conf.d/head <<-EOF
nameserver 114.114.114.114
nameserver 8.8.8.8
nameserver 1.1.1.1
EOF
            sudo resolvconf --enable-updates
            sudo resolvconf -u
        fi

    else
        if [ "$(cat /etc/resolv.conf | grep -c 8.8.8.8)" -eq 0 ]; then
            sudo sed -i 's/^#DNS=/DNS=114.114.114.114 8.8.8.8 1.1.1.1/' /etc/systemd/resolved.conf

            if [ -f "/run/systemd/resolve/resolv.conf" ]; then
                sudo mv /etc/resolv.conf /etc/resolv.conf.bak
                sudo ln -s /run/systemd/resolve/resolv.conf /etc/resolv.conf
            fi
            sudo service systemd-resolved restart
        fi
    fi

}

config_mount() {

    if [ "$(vmware-hgfsclient)" ]; then
        echo "Will Mount"
        # sudo vmhgfs-fuse .host:/ /mnt/hgfs -o subtype=vmhgfs-fuse,allow_other
        if [ "$(cat /etc/fstab | grep -c vmhgfs-fuse)" -eq 0 ]; then
            # option 1
            # cmd = "vmhgfs-fuse    /mnt    fuse    defaults,allow_other    0   0"
            # optoin 2
            cmd=".host:/    /mnt   fuse.vmhgfs-fuse    defaults,allow_other 0   0"
            sudo sed -i '$a'"$cmd" /etc/fstab
            sudo mount -a
        fi
    fi

}

config_mirrors() {
    if [ "$(cat /etc/apt/sources.list | grep -c mirrors.aliyun.com)" -eq 0 ]; then
        file_url="https://raw.githubusercontent.com/tuot/Script/main/mirrors_update.sh"
        if [ "$(dpkg --list | grep -wc wget)" -ne 0 ]; then
            wget -qO- "${file_url}" | sudo bash -s aliyun
        elif [ "$(dpkg --list | grep -wc curl)" -ne 0 ]; then
            curl -kLso- "${file_url}" | sudo bash -s aliyun
        else
            sudo apt update &&
                sudo apt install -y wget
            config_mirrors
        fi
    fi
}

common_config() {
    sudo sed -i 's/^# \(set bell-style none\)/\1/' /etc/inputrc
}

main() {

    common_config
    config_mirrors
    config_mount

    sudo apt update &&
        sudo apt install -y vim git wget curl

    config_network
    install_docker
    install_zsh
    install_tmux
    install_miniconda
    pip_setup

    echo "Completed........."
}

main
