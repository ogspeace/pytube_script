# v1.2
#- future proofed script: added create vids_dir output directory if directory didn't exist
# v1.1
#- downloads multiple vids based on text file listing (to_dl.txt)
#- included status messages
#
# v1.0
#-downloaded 1 vid only
#
# by: Ogs Ablazo
from pytube import YouTube
import os, sys

dir_name = os.path.dirname(os.path.realpath(__file__))

t = open(dir_name+"/to_dl.txt","r")
toDL_list = t.readlines()
cnt = 1
if not os.path.exists(dir_name+"/vids_dir/"):
    os.makedirs(dir_name+"/vids_dir/")
for v in toDL_list:
    try:
        yt = YouTube(v.strip())
        print("[%s] Downloading video : '%s'. . ."%(cnt,yt.title))
        yt_filt = yt.streams.filter(progressive=True, file_extension='mp4')
        for x in yt_filt.all():
            print(x)
        yt_filt.first().download(dir_name+"/vids_dir/")
        print("[%s] successfully downloaded video '%s'!"%(cnt,yt.title))
        print("\n==============")
    except Exception as e:
        pass
    cnt += 1
t.close()
os.system("sudo rm %s/to_dl.txt"%dir_name)
os.system("sudo touch %s/to_dl.txt"%dir_name)
