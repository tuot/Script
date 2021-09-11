#!/bin/bash
set -e

PROCESSOR=10
FFMPEG_LOCATION=ffmpeg/bin/ffmpeg.exe
PROXY="socks5://127.0.0.1:7890"
url="https://www.youtube.com/watch?v=gn64M16gl2E&list=PL61FGHPfT-kBZi18paeyzM1RPrkD1tItG"
download_archive=archive.txt

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
        FFMPEG_LOCATION=$(which ffmpeg)
        sudo apt install -y ffmpeg
    fi
}

download() {
    playlist_length=$(youtube-dl --proxy "$PROXY" -J --flat-playlist "$url" | python -c 'import json,sys;obj=json.load(sys.stdin);print(len(obj["entries"]))')

    internal=$(("$playlist_length" / "$PROCESSOR"))
    for ((start = 1; start <= playlist_length; start++)); do
        end=$((start + internal))
        if [ $end -gt $playlist_length ]; then
            end=$playlist_length
        fi
        download_mp3 "$start-$end" &
        pids[${start}]=$!
        start=$end
    done

    # wait for all pids
    for pid in ${pids[*]}; do
        wait $pid
    done
}

download_mp3() {
    counter=1
    error_limt=5

    playlist_items="$1"
    echo "Download $playlist_items"
    while true; do
        EXIT_CODE=0
        youtube-dl --proxy $PROXY \
            --download-archive $download_archive \
            --extract-audio --embed-thumbnail --audio-format mp3 \
            -o "mp3/%(title)s.%(ext)s" \
            --playlist-items "$playlist_items" \
            --ffmpeg-location "$FFMPEG_LOCATION" \
            "$url" || EXIT_CODE=$?

        if [ ! $EXIT_CODE -eq 0 ]; then
            counter=$((counter + 1))
            echo "$counter" >>log.txt
            if [[ "$counter" -gt "$error_limt" ]]; then
                exit 0
            fi
        else
            exit 0
        fi
    done
    echo "DONE"
}

exit_all() {
    for pid in ${pids[*]}; do
        kill -9 $pid
    done
    exit 0
}

main() {
    trap exit_all SIGINT
    install_dependence
    download
}

main
