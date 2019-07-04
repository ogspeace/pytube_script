#v1.0 - downloads playlists from youtube
#Ogs Ablazo
from pytube import Playlist
import os,sys

dir_name = os.path.dirname(os.path.realpath(__file__))

inp = sys.argv[1]
playlist = Playlist(inp)
print('Number of videos in playlist: %s' % len(playlist.video_urls))
playlist.download_all(dir_name+"/playlist/")
