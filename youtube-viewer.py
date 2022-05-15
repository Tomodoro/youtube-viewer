pkgver = "0.1.0-alpha.7"
"""Youtube Viewer - %s

Copyright (C) 2022 Tomodoro *EMAIL REDACTED*

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published
by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

#-------------------------------------------------------
#  youtube-viewer
#  Created on: 14 February 2022
#  Latest edit on: 15 May 2022
#  https://github.com/Tomodoro/youtube-viewer
#-------------------------------------------------------

# youtube-viewer is a command line utility for streaming YouTube videos in mpv/vlc.

# Many thanks to the upstream project in which this program is based:
#   https://github.com/trizen/youtube-viewer
""" % pkgver

from youtubesearchpython import *
import os, re, sys, json, time, datetime
from shutil import which

pkgname = "youtube-viewer"

# Work in progress placeholder
alan = "Allan please add details"

#~~~~~~~~~~~~~~~~~~~~
# Configuration file
#~~~~~~~~~~~~~~~~~~~~

def config_file_write(file: str) -> None:
    """Writes the configuration file to given location
    """
    with open(file, 'w') as fp:
        fp.write('''{
    "ascii_mode": 1,
    "get_term_width": 1,
    "video_player_selected": "mpv",
    "video_players": {
        "mpv":
            {
                "arg": "--really-quiet --force-media-title=*TITLE* *VIDEO*",
                "cmd": "mpv",
                "fs": "--fullscreen",
                "novideo": "--no-video",
                "vol": "--volume=*VOL*",
                "nocache": "--no-cache"
            }
    },
    "youtube_video_url": "https://www.youtube.com/watch?v=",
    "youtube_playlist_url": "https://www.youtube.com/playlist?list="
}
''')

def config_file_check() -> None:
    """Makes sure the configuration file exists
    """
    
    appdata = os.getenv('APPDATA')
    data = os.path.join(appdata, pkgname)
    os.makedirs(data,exist_ok=True)

    config = os.path.join(data, pkgname+'.conf')

    if os.path.isfile(config):
        pass

    else:
        config_file_write(config)

    return config

#~~~~~~~~~~~
# Help text
#~~~~~~~~~~~

def halp() -> None:
    """Prints help of the program
    """

    print("""
# Base
[keywords]        : search for YouTube videos
[youtube-url]     : play a video by YouTube URL
:v(ideoid)=ID     : play videos by YouTube video IDs
[playlist-url]    : display videos from a playlistURL
:playlist=ID      : display videos from a playlistID

# Control
:n(ext)           : get the next page of results
:b(ack)           : get the next page of results

# Youtube
:i(nfo)=i         : display more information

# Others
:q, :quit, :exit  : close the application

# Extra
:h, :help         : prints this help
:vol=N            : set volume of the media player

NOTES:
 1. A stdin option is valid only if it begins with '=', ';' or ':'.
""")
    
    aga = input("=>> Press ENTER to continue...")
    print (aga)

#~~~~~~~~~~~~~~~
# Terminal size
#~~~~~~~~~~~~~~~

def terminal_width(opt: int) -> int:
    """Set the maximun width that the program output will take

    Reads the configuration file and checks get_term_width.

    If 1 (true), the output will adjust to the current terminal width
    If 0 (false), the output will be fixed to 70 chars
    """
    
    if int(opt) == 1:
        size = os.get_terminal_size()
        return int(size.columns)

    elif int(opt) == 0:
        return int(70)

    else:
        return int(70)

#~~~~~~~~~~~~~~
# Media player
#~~~~~~~~~~~~~~

def check_media_player(player: str) -> None:
    """Check existence of selected media player
    """

    if (which(player) is not None) is True: pass

    else: print("\n[!] Please install a supported video player! (e.g.: mpv)\n")

def play(player: object, video: object, extra: str ="") -> None:
    """Plays the youtube link using the selected media player
    """
    
    nv = player.novideo
    fs = player.fullscreen
    vl = player.volume
    ch = player.nocache

    id       = video.vid_id
    title    = video.vid_title
    
    sep = " "
    program = cfg['video_player_selected']

    program_nv = lambda boolean: cfg['video_players'][program]['novideo']  if boolean else ""
    program_fs = lambda boolean: cfg['video_players'][program]['fs']       if boolean else ""
    program_ch = lambda boolean: cfg['video_players'][program]['nocache']  if boolean else ""

    program_cmd = cfg['video_players'][program]['cmd']
    program_arg = cfg['video_players'][program]['arg']
    program_vol = cfg['video_players'][program]['vol']

    url = cfg['youtube_video_url'] + id

    program_arg = program_arg.replace("*TITLE*", '"'+title+'"')
    program_arg = program_arg.replace("*VIDEO*", '"'+ url +'"')
    
    program_vol = program_vol.replace("*VOL*", str(vl))

    os.system( program_cmd + sep \
               + program_fs(fs) + sep \
               + program_nv(nv) + sep \
               + program_ch(ch) + sep \
               + program_vol + sep \
               + program_arg + sep \
               + extra )

#~~~~~~~~~~~~~~~~~~~~~~~
# Print formated output
#~~~~~~~~~~~~~~~~~~~~~~~

def diff_date(p: str) -> str:
    """Calculates difference of time between ISO8601 dates

    The function returns when it finds a difference greater than zero
    searching in the following order: YEAR, MONTH, DAY
    """
    
    p_year = p[0:4]
    p_month = p[5:7]
    p_day = p[8:10]

    t = datetime.datetime.now().isoformat()
    t_year = t[0:4]
    t_month = t[5:7]
    t_day = t[8:10]

    dif_year = int(t_year)-int(p_year)
    dif_month = int(t_month)-int(p_month)
    dif_day = int(t_day)-int(p_day)

    if dif_year != 0:
        return str(dif_year)+"y"

    elif dif_month != 0:
        return str(dif_month)+"m"

    elif dif_day != 0:
        return str(dif_day)+"d"

    else:
        return str("0d")
    
def publish_compact(p: str ) -> str:
    """Converts verbose published date text into abbreviature

    First removes the prefix "Streamed" and sufix words "ago"
    when created, then replaces the full words of time with
    abbreviatures using the following rules:

    year(s)   -> y
    month(s)  -> m
    week(s)   -> w
    day(s)    -> d
    hour(s)   -> h

    Everything below an hour is presented as <1h for easiness.
    """
    p = p.replace("Streamed ", "")
    p = p.replace(" ago", "")

    if re.search("years", p):
        return p.replace(" years", "y")

    elif re.search("year", p):
        return p.replace(" year", "y")

    elif re.search("months", p):
        return p.replace(" months", "m")

    elif re.search("month", p):
        return p.replace(" month", "m")

    elif re.search("weeks", p):
        return p.replace(" weeks", "w")

    elif re.search("week", p):
        return p.replace(" week", "w")

    elif re.search("days", p):
        return p.replace(" days", "d")

    elif re.search("day", p):
        return p.replace(" day", "d")

    elif re.search("hours", p):
        return p.replace(" hours", "h")

    elif re.search("hour", p):
        return p.replace(" hour", "h")

    else:
        return "<1h"

def views_compact(v: str) -> str:
    """Converts verbose views number into abbreviature

    First check the lenght of the string, then truncates it
    following the corresponding IS symbol:

    10^3  to 10^5   -> 1k to 100k
    10^6  to 10^9   -> 1M to 100M
    10^10 to 10^12  -> 1B to 100B

    Lenghts bellow 10^3 showed without alterations.
    Lenghts above 10^12 showed as "inf".
    
    """
    if (len(v) < 4):
        return v
    
    elif (len(v) >= 4) and (len(v) <= 6):
        return v[:-3]+"K"

    elif (len(v) >= 7) and (len(v) <= 9 ):
        return v[:-6]+"M"

    elif (len(v) >=10) and (len(v) <= 12):
        return v[:-9]+"B"

    else:
        return "inf"

def ascii_workaround(v: str, c: str) -> tuple:
    """Removes all non-ascii chars from output

    v: video name
    c: channel name
    """
    
    v,c = v.encode("ascii", "ignore"),c.encode("ascii", "ignore")
    v,c = v.decode(),c.decode()

    return v,c

def video_list_display(vid_list: dict) -> None:

    print ("")
    upper = len(vid_list)
    for i in range(upper):
        item = vid_list[i]
        vid_number    = str(i+1)
        vid_title     = item['title']
        chl_title     = item['channel']['name']

        subitem = None

        if 'publishedTime' in item:
            published = item['publishedTime']
            
        else:
            published = "7 years ago"

        if 'viewCount' in item:
            if 'short' in item['viewCount']:
                vid_views  = item['viewCount']['short']
            else:
                vid_views = "7M views"
            
        else:
            vid_views = "7M views"

        duration = lambda string: "LIVE" if string is None else string

        if vid_views is None:
            if subitem is None:
                id = item['id']
                subitem = Video.getInfo(id)
                
            v = subitem['viewCount']['text']
            vid_views = views_compact(v)

        if published is None:
            if subitem is None:
                id = item['id']
                subitem = Video.getInfo(id)
                
            p = subitem['publishDate']
            if p is None:
                published = "ERR"
                
            else:
                published = diff_date(p)
                
        else:
            published = publish_compact(published)

        if int(cfg['ascii_mode']) == int(1):
            vid_title, chl_title = ascii_workaround(vid_title,chl_title)

        c_total = terminal_width(cfg['get_term_width'])

        c1 = int(3)
        c4 = int(4)
        c5 = int(5)
        c6 = int(8)

        c_fix = c1+c4+c5+c6
        c_dif = c_total-c_fix-int(5)

        if (c_dif%2) == 0:
            pass

        else:
            c_dif = c_dif - int(1)

        c3 = c_dif//5
        c2 = c_dif-c3-2

        print (vid_number.rjust(c1)+'.', end=" ")
        print (vid_title[0:(c2-1)].ljust(c2), end=" ")
        print (chl_title[0:(c3-1)].ljust(c3), end=" ")
        print (published.rjust(c4), end=" ")
        print (vid_views.replace(" views", "").rjust(c5), end=" ")
        print ((duration(item['duration'])).rjust(c6))

    print("")

#~~~~~~~~~~~~~~~~~
# Data organizers
#~~~~~~~~~~~~~~~~~

class SessionPlayerSettings:
    def __init__(slef, nv, fs, vol, nc):
        slef.novideo = nv
        slef.fullscreen = fs
        slef.volume = vol
        slef.nocache = nc

xset = SessionPlayerSettings(False,True,50,False)
        
class VideoListDisplay:
    def __init__(slef, a, b, c):
        slef.data  = a
        slef.list  = b
        slef.index = c

        slef.number    = None
        slef.title     = None
        slef.channel   = None
        slef.published = None
        slef.views     = None
        slef.duration  = None

class VideoInfoDisplay:
    def __init__(slef, vid_id):
        slef.vid_id    = vid_id
        slef.chl_id    = None

        slef.number    = None
        slef.vid_title = None
        slef.chl_title = None
        slef.published = None
        slef.vid_views = None
        slef.duration  = None
        slef.category  = None

        slef.description = None
        slef.url         = None

    def acquire_info(slef):
        
        info = Video.getInfo(slef.vid_id)

        duration = lambda string: \
                   time.strftime('%H:%M:%S', time.gmtime(int(string))) \
                   if  int(string) != 0 else "LIVE"

        slef.description = info['description']
        slef.url         = info['link']
        slef.vid_title   = info['title']
        slef.chl_title   = info['channel']['name']
        slef.chl_id      = info['channel']['id']
        slef.category    = info['category']
        slef.duration    = duration(info['duration']['secondsText'])
        slef.published   = info['publishDate']

    def display_info(slef):

        sep = ("\n"+('-' * terminal_width(cfg['get_term_width'])))
        
        print ("")    
        print ("=> Description", sep, slef.description, sep)
        print ("=> URL: %s" % slef.url, sep)
        print (("=>> "+slef.vid_title+" <<=\n").center(terminal_width(cfg['get_term_width'])))
        print ("-> Channel   : %s" % slef.chl_title)
        print ("-> ChannelID : %s" % slef.chl_id)
        print ("-> VideoID   : %s" % slef.vid_id)
        print ("-> Category  : %s" % slef.category)
        print ("-> Duration  : %s" % slef.duration)
        print ("-> Published : %s" % slef.published , sep)

def test_field(inp):
    pass

#~~~~~~~~~~~~~~~~
# Input analyzer
#~~~~~~~~~~~~~~~~

def options_input(inp: str, display: object) -> object:

    #~~~~~~~~~~~~~~~~~~~
    # Catch basic input
    #~~~~~~~~~~~~~~~~~~~
    
    if inp == "":
        pass

    elif inp == "q" or inp == "quit" or inp == "exit":
        exit()

    elif inp == "h" or inp == "help":
        halp()

    elif inp[0:2] == "t=":
        test_field(inp.replace("t=", ""))
        exit()

    elif inp[0:4] == "vol=":
        number = inp.replace("vol=", "")

        if number.isdigit():
            vol = number
            if int(vol) > 100:
                vol = 100

        else:
            vol = xset.volume

        xset.volume = vol

    #~~~~~~~~~~~~~~
    # Base section
    #~~~~~~~~~~~~~~
    
    # :v(ideoid)=ID : play videos by YouTube video IDs
    elif inp[0:2] == "v=":
        id = inp.replace("v=", "")
        video = VideoInfoDisplay(id)
        video.acquire_info()
        video.display_info()
        play(xset, video)

    elif  inp[0:8] == "videoid=":
        id = inp.replace("videoid=", "")
        video = VideoInfoDisplay(id)
        video.acquire_info()
        video.display_info()
        play(xset, video)

    # :playlistid=ID : display videos from playlistID
    elif inp [0:9] == "playlist=":
        id = inp.replace("playlist=", "")
        playlist_result(id)

    #~~~~~~~~~~~~~~~~~
    # Control section
    #~~~~~~~~~~~~~~~~~
    
    # :n(ext) : get the next page of results
    elif inp == "n" or inp == "next":
        display.index += 1
        if display.index <= len(display.list)-1:
            video_list_display(display.list[display.index])

        else:
            # For search
            if type(display.data).__name__ == 'VideosSearch':
                display.data.next()
                display.list.append(display.data.result())

            # For playlist
            elif type(display.data).__name__ == 'Playlist':
                display.data.getNextVideos()
                display.list.append(display.data.videos)

            video_list_display(display.list[display.index])

    # :b(ack) - get the previous page of results
    elif inp == "b" or inp == "back":
        display.index -= 1
        if ( len(display.list) == 0 ) or ( display.index < 0 ):
            display.index += 1
            print ("\n[!] This is the first page.\n")

        else:
            video_list_display(display.list[display.index])

    #~~~~~~~~~~~~~~~~~
    # Youtube section
    #~~~~~~~~~~~~~~~~~
    
    # :i(nfo) : display more information
    elif inp[0:2] == "i=":
        number = inp.replace("i=", "")
        if number.isdigit() \
           and int(number) <= len(display.list[display.index]['result']) \
           and int(number) >= 0:
            id = display.list[display.index]['result'][int(number)-1]['id']
            video = VideoInfoDisplay(id)
            video.acquire_info()
            video.display_info()
            aga = input("\n=>> Press ENTER to continue...")
            print (aga)

        else:
            print ("\n[!] No video selected!")
            video_list_display(display.list[display.index])

    elif inp[0:5] == "info=":
        number = inp.replace("i=", "")
        if number.isdigit() \
           and int(number) <= len(display.list[display.index]['result']) \
           and int(number) >= 0:
            id = display.list[display.index]['result'][int(number)-1]['id']
            video = VideoInfoDisplay(id)
            video.acquire_info()
            video.display_info()
            aga = input("\n=>> Press ENTER to continue...")
            print (aga)

        else:
            print ("\n[!] No video selected!")
            video_list_display(display.list[display.index])

    # :page=i : jump to page i of results
    elif inp[0:5] == "page=":
        index = inp[5:]
        if  index.isdigit():
            if int(index)-1 <= len(display.list):
                display.index = int(index)-1
                video_list_display(display.list[display.index])

            else:
                print ("\n[!] %s is out of range.\n" % index)

        else:
            print ("\n[!] %s is not a number.\n" % index)
            return

    # Option not recognized
    #~~~~~~~~~~~~~~~~~~~~~~~
    else:
        print ("\n[!] Invalid option <%s>\n" % inp)

    return display

def catch_keywords(inp: str, search_display: object) -> object:

    vid_results = VideosSearch(inp)
    search_display.data = vid_results
    search_display.list = []
    search_display.index = 0
    search_display.list.append(search_display.data.result()['result'])
    video_list_display(search_display.list[search_display.index])

    return search_display

def playlist_result(id: str) -> object:

    playlist_display = VideoListDisplay(None, [], 0)
    playlist_display.data = Playlist(cfg['youtube_playlist_url'] + id)
    playlist_display.list.append(playlist_display.data.videos)
    return playlist_display

def catch_url(inp: str, display: object) -> object:

    # This is a video
    if re.search("watch", inp):
        videoid = inp.replace(cfg['youtube_video_url'], "")

        # In-video playlist detected
        if re.search("list", videoid):
            sub_str = "&list="
            playlistid = videoid[(videoid.index(sub_str)+len(sub_str)):]
            display = playlist_result(playlistid)
            video_list_display(display.list[display.index])

        else:
            video = VideoInfoDisplay(videoid)
            video.acquire_info()
            video.display_info()
            play(xset, video)

    # This is a playlist
    elif re.search("playlist", inp):
        playlistid = inp.replace(cfg['youtube_playlist_url'], "")
        display = playlist_result(playlistid)
        video_list_display(display.list[display.index])

    return display


def playing_output(inp: str, display: object) -> None:
    
    if int(inp) != 0 \
       and int(inp) <= len(display.list[display.index]):
        
        id = display.list[display.index][int(inp)-1]['id']
        video = VideoInfoDisplay(id)
        video.acquire_info()
        video.display_info()
        play(xset, video)

    else:
        print ("\n[!] No video selected!")
        video_list_display(display.list[display.index])

#~~~~~~~~~~~
# Main loop
#~~~~~~~~~~~
configJson  = config_file_check()
cfg   = json.load( open(configJson) )

first_prompt = "=>> Search for YouTube videos (:h for help) \n> "

def main(PS1):
    
    check_media_player(cfg['video_player_selected'])
    display = VideoListDisplay(None, [], 0)

    if len(sys.argv) > 1 and sys.argv[1] == "--version":
        print("Youtube Viewer (for Windows) %s" % pkgver)
        exit()
    
    while True:
        inp = input(PS1)

        # Catch empty input
        #~~~~~~~~~~~~~~~~~~~
        if inp == "":
            if len(display.list) == 0: continue
            else: video_list_display(display.list[display.index])

        # Playing section (non-option)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        elif inp.isdigit() and len(display.list) !=0:
            playing_output(inp, display)
        
        # Options input
        #~~~~~~~~~~~~~~~
        elif inp[0] == ":" or inp[0] == ";" or inp[0] == "=":
            display = options_input(inp[1:], display)

        # [youtube-url] : play a video by Youtube URL
        # [playlist-url] : display videos form a playlistURL
        elif inp[:4] == "http":
            display = catch_url(inp, display)

        # [keywords] : search for YouTube videos
        else:
            display = catch_keywords(inp, display)

        PS1 = "=>> Select one or more videos to play (:h for help)\n> "

if __name__ == "__main__":
    try:
        main(first_prompt)
        
    except KeyboardInterrupt:
        pass
    
    finally:
        pass
