# v1.2
#- future proofed script: added create vids_dir output directory if directory didn't exist
#- added print_stdout method to force print/output
#- modified ending commands - to cater to other operating systems outside linux
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

def print_stdout(s):
    print(s)
    sys.stdout.flush()


def get_terminal_size():
    rows, columns = os.popen('stty size', 'r').read().split()
    return int(rows), int(columns)

def display_progress_bar(bytes_received, filesize, ch='*', scale=0.55):
    _, columns = get_terminal_size()
    max_width = int(columns * scale)

    filled = int(round(max_width * bytes_received / float(filesize)))
    remaining = max_width - filled
    bar = ch * filled + ' ' * remaining
    percent = round(100.0 * bytes_received / float(filesize), 1)
    text = ' > |{bar}| {percent} \r'.format(bar=bar, percent=percent)
    sys.stdout.write(text)
    sys.stdout.flush()

def progress_Check(stream = None, chunk = None, file_handle = None, remaining = None):
    file_size = stream.filesize
    bytes_received = file_size - remaining
#    percent = (100*(file_size-remaining))/file_size
    display_progress_bar(remaining, file_size)
#    print_stdout("%.2f downloaded"%percent)

dir_name = os.path.dirname(os.path.realpath(__file__))

t = open(dir_name+"/to_dl.txt","r")
toDL_list = t.readlines()
cnt = 1
if not os.path.exists(dir_name+"/vids_dir/"):
    os.makedirs(dir_name+"/vids_dir/")
for v in toDL_list:
    try:
        yt = YouTube(v.strip(), on_progress_callback=progress_Check)
        print_stdout("[%s] Downloading video : '%s'. . ."%(cnt,yt.title))
        yt_filt = yt.streams.filter(progressive=True, file_extension='mp4')
        for x in yt_filt.all():
            print(x)
        yt_filt.first().download(dir_name+"/vids_dir/")
        print_stdout("[%s] successfully downloaded video '%s'!"%(cnt,yt.title))
        print_stdout("\n==============")
    except Exception as e:
        print_stdout(e)
    cnt += 1
t.close()


if sys.platform == "linux":
    command = "sudo rm %s/to_dl.txt && sudo touch %s/to_dl.txt"%(dir_name,dir_name)
else: #windows
    command = "rm to_dl.txt && touch to_dl.txt"
os.system(command)
