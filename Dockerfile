FROM debian:latest

RUN apt-get update && apt-get install -y \
    ffmpeg \
    ffmpegthumbnailer \
    exiftool \
    strace \
    lsof \
    tcpdump \
    grep \
    && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["/bin/bash"]
