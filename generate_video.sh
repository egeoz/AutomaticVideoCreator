#!/bin/bash

OUTPUT_FOLDER=$1
SOUND=$2
IMAGES=$3

ffmpeg -ss 0 -t 4 -i sounds/$SOUND.mp3 -vcodec copy -af "volume=-10dB" $OUTPUT_FOLDER/intro_sound.mp3
ffmpeg -loop 1 -framerate 1/11 -i images/$IMAGES/%d.jpg -i $OUTPUT_FOLDER/tts.mp3 -c:v libx264 -c:a copy -shortest $OUTPUT_FOLDER/slideshow.mp4
ffmpeg -loop 1 -ss 0 -t 4 -i $OUTPUT_FOLDER/cover.png -i $OUTPUT_FOLDER/intro_sound.mp3 -c:v libx264 -c:a copy -shortest $OUTPUT_FOLDER/intro.mp4

ffmpeg -f concat -safe 0 -i $OUTPUT_FOLDER/file_list.txt -c copy $OUTPUT_FOLDER/output.mp4

