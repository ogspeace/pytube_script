# v1.7
#- additional printing of links on queue.
# v1.6
#- printing links and titles that were not downloaded because of an error
# v1.5
#- for some reason stream sorting is inverted! changed download target from .first() to .last()
# v1.4
#- added createDirDatestamp function which creates a directory with the date stamp as title for current downloaded batch
# v1.3
#- added progress bar adapted from pytube documentation
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
import os, pytube, sys, datetime, urllib

dir_name = os.path.dirname(os.path.realpath(__file__))

def print_stdout(s):
    print(s)
    sys.stdout.flush()

def createDirDatestamp():
    today = datetime.datetime.now()
    title = today.strftime('%Y-%m-%d')
    if not os.path.exists(dir_name+"/vids_dir/"+title):
        os.makedirs(dir_name+"/vids_dir/"+title)
    return title

def get_terminal_size():
    rows, columns = os.popen('stty size', 'r').read().split()
    return int(rows), int(columns)

def display_progress_bar(bytes_received, filesize, ch='*', scale=0.55):
    _, columns = get_terminal_size()
    max_width = int(columns * scale)

    filled = int(round(max_width * bytes_received / float(filesize)))
    remaining = max_width - filled
    bar = ch * remaining + ' ' * filled
    percent = round(100 - round(100.0 * bytes_received / float(filesize), 1), 1)
    text = ' > |{bar}| {percent} % downloaded \r'.format(bar=bar, percent=percent)
    sys.stdout.write(text)
    sys.stdout.flush()

def progress_Check(stream = None, chunk = None, file_handle = None, remaining = None):
    file_size = stream.filesize
    bytes_received = file_size - remaining
    display_progress_bar(remaining, file_size)


t = open(dir_name+"/to_dl.txt","r")
toDL_list = t.readlines()
cnt = 1
not_downloaded = {}
if not os.path.exists(dir_name+"/vids_dir/"):
    os.makedirs(dir_name+"/vids_dir/")
for v in toDL_list:
    try:
        title = createDirDatestamp()
        yt = YouTube(v.strip(), on_progress_callback=progress_Check)
        print_stdout("[%s] Downloading video : '%s'. . .\n link: < %s > "%(cnt,yt.title,v))
        yt_filt = yt.streams.filter(progressive=True, file_extension='mp4')
        for x in yt_filt.all():
            print(x)
        yt_filt.last().download(dir_name+"/vids_dir/"+title+"/")
        print_stdout("[%s] successfully downloaded video '%s'!"%(cnt,yt.title))
        print_stdout("\n==============")
    except pytube.exceptions.RegexMatchError as regerr:
        print("encountered {}~error cannot download {} ... skipping".format(regerr, yt.title))
        not_downloaded[yt.title] = v
        pass
    except urllib.error.HTTPError as HE:
        print("encountered {}~error cannot download {} ... skipping".format(HE, yt.title))
        not_downloaded[yt.title] = v
        pass
    except Exception as e:
        print("encountered {}~unique error cannot download {} ... skipping".format(e, yt.title))
        not_downloaded[yt.title] = v
        pass
    finally:
        cnt += 1
t.close()


if sys.platform == "linux":
    command = "sudo rm %s/to_dl.txt && sudo touch %s/to_dl.txt"%(dir_name,dir_name)
else: #windows
    command = "rm to_dl.txt && touch to_dl.txt"
os.system(command)

print('was not able to download the following titles:')
for title, link in not_downloaded.items():
    print("title : {} | link : {}".format(title, link))

print('reprinting links:')
for link in not_downloaded.values():
    print("{}".format(link))
