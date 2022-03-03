#!/bin/sh
# Linux(Distribution) MacOS SunOS AIX

OS=$(uname -s)
REV=$(uname -r)
MACH=$(uname -m)

GetVersionFromFile() {
    VERSION="$(tr "\n" ' ' "$1" <cat | sed s/.*VERSION.*=\ //)"
}

GetOSVersion() {
    if [ "${OS}" = "SunOS" ]; then
        OS=Solaris
        ARCH=$(uname -p)
        OSSTR="${OS} ${REV}(${ARCH} $(uname -v)"
        echo ${OSSTR}
        return

    elif [ "${OS}" = "AIX" ]; then
        OSSTR="${OS} $(oslevel) ($(oslevel -r)"
        echo ${OSSTR}
        return

    elif [ "${OS}" = "Linux" ]; then
        KERNEL=$(uname -r)
        if [ -f /etc/redhat-release ]; then
            DIST='RedHat'
            PSUEDONAME=$(sed s/.*\(// </etc/redhat-release | sed s/\)//)
            REV=$(sed s/.*release\ // </etc/redhat-release | sed s/\ .*//)
        elif [ -f /etc/SuSE-release ]; then
            DIST=$(tr "\n" ' ' </etc/SuSE-release | sed s/VERSION.*//)
            REV=$(tr "\n" ' ' </etc/SuSE-release | sed s/.*=\ //)
        elif [ -f /etc/mandrake-release ]; then
            DIST='Mandrake'
            PSUEDONAME=$(sed s/.*\(// </etc/mandrake-release | sed s/\)//)
            REV=$(sed s/.*release\ // </etc/mandrake-release | sed s/\ .*//)
        elif [ -f /etc/debian_version ]; then
            if [ "$(awk -F= '/DISTRIB_ID/ {print $2}' /etc/lsb-release)" = "Ubuntu" ]; then
                DIST="Ubuntu"
            else
                DIST="Debian $(cat /etc/debian_version)"
                REV=""
            fi
        elif [ -f /etc/arch-release ]; then
            DIST="Arch"
        fi
        if [ -f /etc/UnitedLinux-release ]; then
            DIST="${DIST}[$(tr "\n" ' ' </etc/UnitedLinux-release | sed s/VERSION.*//)]"
        fi
        OSSTR="${OS} ${DIST} ${REV}(${PSUEDONAME} ${KERNEL} ${MACH})"
        echo ${OSSTR}
        return

    elif [ "${OS}" == "Darwin" ]; then
        type -p sw_vers &>/dev/null
        [ $? -eq 0 ] && {
            OS=$(sw_vers | grep 'ProductName' | cut -f 2)
            VER=$(sw_vers | grep 'ProductVersion' | cut -f 2)
            BUILD=$(sw_vers | grep 'BuildVersion' | cut -f 2)
            OSSTR="Darwin ${OS} ${VER} ${BUILD}"
        } || {
            OSSTR="MacOSX"
        }
        echo ${OSSTR}
        return

    fi

    # F0ck wind0ws. G0 t0 he11!
    echo "Your platform ($(uname -a)) is not supported."
    exit 1

}

GetOSVersion2() {
    os=$(uname -s)
    dist_name='unknown'
    dist_version='unknown'

    case "${os}" in
    'Linux')
        lsb_release_path=$(which lsb_release 2>/dev/null)
        if [ "${lsb_release_path}x" != "x" ]; then
            dist_name=$(${lsb_release_path} -i | cut -d ':' -f2)
            dist_version=$(${lsb_release_path} -r | cut -d ':' -f2 | sed 's/\t *//g')
        else
            if [ -r '/etc/debian_version' ]; then
                if [ -r '/etc/dpkg/origins/ubuntu' ]; then
                    dist_name='ubuntu'
                else
                    dist_name='debian'
                fi
                dist_version=$(cat /etc/debian_version | sed s/.*\///)
            elif [ -r '/etc/mandrake-release' ]; then
                dist_name=$(cat /etc/mandrake-release | sed s/.*\(// | sed s/\)//)
                dist_version=$(cat /etc/mandrake-release | sed 's/.*release\ //' | sed 's/\ .*//')
            elif [ -r '/etc/redhat-release' ]; then
                if [ -r '/etc/asplinux-release' ]; then
                    dist_name='asplinux'
                    dist_version=$(cat /etc/asplinux-release | sed 's/.*release\ //' | sed 's/\ .*//')
                elif [ -r '/etc/altlinux-release' ]; then
                    dist_name='altlinux'
                    dist_version=$(cat /etc/altlinux-release | sed 's/.*Linux\ //' | sed 's/\ .*//')
                else
                    if [ "$(cat /etc/redhat-release | grep -i 'Red Hat Enterprise')x" != "x" ]; then
                        dist_name='rhel'
                    else
                        dist_name=$(cat /etc/redhat-release | cut -d ' ' -f1)
                    fi
                    dist_version=$(cat /etc/redhat-release | sed 's/.*release\ //' | sed 's/\ .*//')
                fi
            elif [ -r '/etc/arch-release' ]; then
                dist_name='archlinux'
                dist_version=$(cat /etc/arch-release)
            elif [ -r '/etc/SuSe-release' ]; then
                dist_name='opensuse'
                dist_version=$(cat /etc/SuSe-release | grep 'VERSION' | sed 's/.*=\ //')
            elif [ -r '/etc/sles-release' ]; then
                dist_name='sles'
                dist_version=$(cat /etc/SuSe-release | grep 'VERSION' | sed 's/.*=\ //')
            elif [ -r '/etc/slackware-version' ]; then
                if [ -r '/etc/zenwalk-version' ]; then
                    dist_name='zenwalk'
                    dist_version=$(cat /etc/zenwalk-version)
                elif [ -r '/etc/slax-version' ]; then
                    dist_name='slax'
                    dist_version=$(cat /etc/slax-version | cut -d ' ' -f2)
                else
                    dist_name=$(cat /etc/slackware-version | cut -d ' ' -f1)
                    dist_version=$(cat /etc/slackware-version | cut -d ' ' -f2)
                fi
            fi
        fi
        ;;
    'OpenBSD' | 'NetBSD' | 'FreeBSD' | 'SunOS')
        dist_name=$os
        if [ "$dist_name" = "SunOS" ]; then
            dist_name='solaris'
        fi
        dist_version=$(uname -r | sed 's/-.*//')
        ;;
    'Darwin')
        dist_name='macos'
        dist_version=$(sw_vers -productVersion)
        ;;
    esac

    dist_name=$(echo $dist_name | tr '[:upper:]' '[:lower:]')
    echo "$dist_name $dist_version"
}

GetOSVersion
GetOSVersion2
