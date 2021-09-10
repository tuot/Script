#!/bin/bash
set -e

FFMPEG_LOCATION=ffmpeg/bin/ffmpeg.exe
PROXY="socks5://127.0.0.1:7890"
url="https://www.youtube.com/watch?v=gn64M16gl2E&list=PL61FGHPfT-kBZi18paeyzM1RPrkD1tItG"

if [ $(uname -s | grep -c "MINGW") -ne 0 ]; then
    OS="Win"
elif [ $(uname -s | grep -c "Linux") -ne 0 ]; then
    OS="Linux"
fi

install_dependence() {
    pip install youtube-dl

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
        sudo apt install -y ffmpeg
    fi
}

download_mp3() {
    counter=1
    count_limt=1
    while true; do
        EXIT_CODE=0
        if [ $OS == "Win" ]; then
            youtube-dl --proxy $PROXY \
                --download-archive archive.txt \
                --extract-audio --embed-thumbnail --audio-format mp3 \
                -o "mp3/%(title)s.%(ext)s" \
                --ffmpeg-location $FFMPEG_LOCATION \
                $url || EXIT_CODE=$?
        else
            youtube-dl --proxy $PROXY \
                --download-archive archive.txt \
                --extract-audio --embed-thumbnail --audio-format mp3 \
                -o "mp3/%(title)s.%(ext)s" \
                $url || EXIT_CODE=$?
        fi

        if [ ! $EXIT_CODE -eq 0 ]; then
            counter=$((counter + 1))
            if [[ "$counter" -gt "$count_limt" ]]; then
                exit 0
            fi
        fi
    done
}

install_dependence
download_mp3
