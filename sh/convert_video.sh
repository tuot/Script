#!/bin/bash
set -e

FFMPEG_LOCATION=ffmpeg/bin/ffmpeg.exe

if [ $(uname -s | grep -c "MINGW") -ne 0 ]; then
    OS="Win"
elif [ $(uname -s | grep -c "Linux") -ne 0 ]; then
    OS="Linux"
fi

install_dependence() {
    if [ $OS == "Win" ]; then
        ffmpeg_file=ffmpeg-release-essentials.7z
        if [ ! -f $FFMPEG_LOCATION ]; then
            if [ ! -f $ffmpeg_file ]; then
                curl -LO https://www.gyan.dev/ffmpeg/builds/$ffmpeg_file
            fi
            Bandizip $ffmpeg_file
            ls -d ffmpeg*/ | cut -f1 -d'/' | xargs -I '{}' mv '{}' ffmpeg
        fi
    else
        FFMPEG_LOCATION=$(which ffmpeg)
        sudo apt install -y ffmpeg
    fi
}

convert_video() {
    file=$1
    new_file="${file%.*}.mp4"

    "$FFMPEG_LOCATION" -hide_banner -i "$file" \
        -c:v libx264 \
        -crf 23 \
        -vf scale=1280:720 \
        -an \
        "$new_file"
}

main() {

    URL="$1"
    if [ -z "$URL" ]; then
        echo "Please input url!!!"
        exit 1
    fi
    echo "Url is : $URL"
    install_dependence
    convert_video "$URL"
}

main "$@"
