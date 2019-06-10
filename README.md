# pytube_script
pytube script to DL yt vids. tested on windows and linux (rasbian, debian, *ubuntu) devices.

## prerequisites:
1. sudo pip3 install pytube
2. sudo touch to_dl.txt

## usage
1. copy youtube video urls from address bar.
2. paste youtube urls to to_dl.txt
3. execute sudo python3 get_file.py
4. once video's downloaded, these are found in vids_dir/ directory.

## disclaimer
1. should you get a regex error, or 's' output, just reattempt the process all over again.
2. to_dl.txt gets refreshed (deleted and re-touched) once the script is finished.
