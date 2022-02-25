pkgver = "0.1.0-alpha.6"
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
#  Latest edit on: 25 February 2022
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

def config_dir() -> str:
    """Makes sure the configuration directory exists
    """
    
    appdata = os.getenv('APPDATA')
    data = os.path.join(appdata, pkgname)
    os.makedirs(data,exist_ok=True)

    return data

def config_file(data_dir: str) -> None:
    """Makes sure the configuration file exists
    """
    config = os.path.join(data_dir, pkgname+'.conf')

    if os.path.isfile(config):
        pass

    else:
        with open(config, 'w') as fp:
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
                "novideo": "--no-video"
            },
        "vlc":
            {
                "arg": "--quiet --play-and-exit --no-video-title-show --input-title-format=*TITLE* *VIDEO*",
                "cmd": "vlc",
                "fs": "--fullscreen",
                "novideo": "--novideo"
            }
    },
    "youtube_video_url": "https://www.youtube.com/watch?v="
}
''')
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

# Control
:n(ext)           : get the next page of results
:b(ack)           : get the next page of results

# Youtube
:i(nfo)=i         : display more information

# Others
:q, :quit, :exit  : close the application

# Extra
:h, :help         : prints this help
:(!)video         : disables|enables video window
:(!)fullscreen    : disables|enables fullscreen playback

NOTES:
 1. A stdin option is valid only if it begins with '=', ';' or ':'.
""")
    
    aga = input("=>> Press ENTER to continue...")
    print (aga)

#~~~~~~~~~~~~~~~
# Terminal size
#~~~~~~~~~~~~~~~

def terminal_width() -> int:
    """Set the maximun width that the program output will take

    Reads the configuration file and checks get_term_width.

    If 1 (true), the output will adjust to the current terminal width
    If 0 (false), the output will be fixed to 70 chars
    """
    opt = cfg['get_term_width']
    
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

def play(nv: bool, fs: bool, id: str, title: str, extra: str ="") -> None:
    """Plays the youtube link using the selected media player
    """

    sep = " "
    program = cfg['video_player_selected']

    program_nv = lambda boolean: cfg['video_players'][program]['novideo'] if boolean else ""
    program_fs = lambda boolean: cfg['video_players'][program]['fs']      if boolean else ""

    program_cmd = cfg['video_players'][program]['cmd']
    program_arg = cfg['video_players'][program]['arg']

    video = cfg['youtube_video_url'] + id

    program_arg = program_arg.replace("*TITLE*", '"'+title+'"')
    program_arg = program_arg.replace("*VIDEO*", '"'+video+'"')

    os.system( program_cmd + sep \
               + program_fs(fs) + sep \
               + program_nv(nv) + sep \
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
    """
    
    v = v.encode("ascii", "ignore")
    c = c.encode("ascii", "ignore")
    v = v.decode()
    c = c.decode()

    return v,c

def echo_VideosSearch_info(search: dict) -> None:
    """Print relevant information of the VideosSearch dictionary

    This function analizes the desired data to be aquired
    and prints it in a human legible way.

    If ['publishedTime'] is None on the VideosSearch dictionary, that
    means that the video is live, therefore a second dictionary must
    be obtain by calling Video.getInfo for that specific video. The
    output is obtained in an abbreviated form (e.g 5y) by calling an
    external function.

    TODO: Save the Video.getInfo dictionary to speed up selection.

    To double check it is live, ['isLiveNow'] is read. If it returns
    the bool "Ture" then the str "LIVE" is assigned to the variable.

    Live videos give a different dictionary, but for the search
    output it is only needed to extract ['publishDate'] and
    ['viewCount']['text']. The latter is a str of the number and it
    is converted to an abbreviated form (e.g. 15M) by calling
    and external function.

    KNOWN BUGS: UTF-8 chars like emojis will not display correctly on
                Windows PowerShell or Windows CMD and it will not ever
                work because of their limitations.

                A workaround is turned on by default that replaces
                those chars with ?.

                Although Windows Terminal can display all utf8 chars,
                they use two spaces instead of one and break columns
                of the search output.

                A workaround is planned in order to recognize emojis and
                substract one space per emoji in the overall width,
                but this would slow down the output as it reads char by
                char so it would not be enabled by default.
    """

    print ("")
    upper = len(search['result'])
    for i in range(upper):
        item = search['result'][i]
        vid_number    = str(i+1)
        vid_title     = item['title']
        chl_title     = item['channel']['name']
        published     = item['publishedTime']
        vid_views     = item['viewCount']['short']

        subitem = None

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

        c_total = terminal_width()

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
        c2 = c_dif-c3

        print (vid_number.rjust(c1)+'.', end=" ")
        print (vid_title[0:(c2-1)].ljust(c2), end=" ")
        print (chl_title[0:(c3-1)].ljust(c3), end=" ")
        print (published.rjust(c4), end=" ")
        print (vid_views.replace(" views", "").rjust(c5), end=" ")
        print ((duration(item['duration'])).rjust(c6))

    print("")

def echo_Videoget_info(id: str) -> None:
    """Print information of the video
    """

    info = Video.getInfo(id)

    sep = ("\n"+('-' * terminal_width()))

    duration = lambda string: \
               time.strftime('%H:%M:%S', time.gmtime(int(string))) \
               if  int(string) != 0 else "LIVE"
    
    print ("")    
    print ("=> Description", sep, info['description'], sep)
    print ("=> URL: %s" % info['link'], sep)
    print (("=>> "+info['title']+" <<=\n").center(terminal_width()))
    print ("-> Channel   : %s" % info['channel']['name'])
    print ("-> ChannelID : %s" % info['channel']['id'])
    print ("-> VideoID   : %s" % info['id'])
    print ("-> Category  : %s" % info['category'])
    print ("-> Duration  : %s" % duration(info['duration']['secondsText']))
    print ("-> Published : %s" % info['publishDate'] , sep)

#~~~~~~~~~~~
# Main loop
#~~~~~~~~~~~
configJson  = config_file( config_dir() )
cfg   = json.load( open(configJson) )

def rick() -> None:
    print ('\033[1A> Rick Astley - Never Gonna Give You Up (Official Music Video)')
    echo_Videoget_info('dQw4w9WgXcQ')
    play(True, True, "dQw4w9WgXcQ", "")

first_prompt = "=>> Search for YouTube videos (:h for help) \n> "

def main(PS1):
    check_media_player(cfg['video_player_selected'])
    search = None
    search_list = []
    search_index = 0
    novideo = False
    fullscreen = False

    if len(sys.argv) > 1 and sys.argv[1] == "--version":
        print("Youtube Viewer (for Windows) %s" % pkgver)
        exit()
    
    while True:
        inp = input(PS1)

        # Catch empty input
        #~~~~~~~~~~~~~~~~~~~
        if inp == "":
            if len(search_list) == 0:
                rick()
                continue

            else:            
                echo_VideosSearch_info(search_list[search_index])

        # All this first chars are valid for options input
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        elif inp[0] == ":" or inp[0] == ";" or inp[0] == "=":
            inp = inp[1:]

            # Catch empty input
            #~~~~~~~~~~~~~~~~~~~
            if inp == "":
                rick()
                continue

            # Base section
            #~~~~~~~~~~~~~~

            # :v(ideoid)=ID : play videos by YouTube video IDs
            elif inp[0:2] == "v=":
                id = inp.replace("v=", "")
                echo_Videoget_info(id)
                play(novideo, fullscreen, id, "")

            elif  inp[0:8] == "videoid=":
                id = inp.replace("videoid=", "")
                echo_Videoget_info(id)
                play(novideo, fullscreen, id, "")

            # :playlist=ID : display videos from a playlistID (pending)

            # Control section
            #~~~~~~~~~~~~~~~~~
            
            # :n(ext) : get the next page of results
            elif inp == "n" or inp == "next":
                search_index += 1
                if search_index <= len(search_list)-1:
                    echo_VideosSearch_info(search_list[search_index])

                else:
                    search.next()
                    search_list.append(search.result())
                    echo_VideosSearch_info(search_list[search_index])

            # :b(ack) - get the previous page of results
            elif inp == "b" or inp == "back":
                search_index -= 1
                if len(search_list) == 0:
                    search_index += 1
                    rick()
                    continue                   

                elif search_index < 0:
                    search_index += 1
                    print ("\n[!] This is the first page.\n")
                    continue

                else:
                    echo_VideosSearch_info(search_list[search_index])

            # Actions section
            #~~~~~~~~~~~~~~~~~

            # :login : will prompt you for login (pending)
            # :logout : will delete the authentication key (pending)

            # Youtube section
            #~~~~~~~~~~~~~~~~~

            # :i(nfo) : display more information
            elif inp[0:2] == "i=":
                number = inp.replace("i=", "")
                if number.isdigit() \
                   and int(number) <= len(search_list[search_index]['result']) \
                   and int(number) >= 0:
                    id = search_list[search_index]['result'][int(number)-1]['id']
                    echo_Videoget_info(id)
                    aga = input("\n=>> Press ENTER to continue...")
                    print (aga)

                else:
                    print ("\n[!] No video selected!")
                    echo_VideosSearch_info(search_list[search_index])

            elif inp[0:5] == "info=":
                number = inp.replace("i=", "")
                if number.isdigit() \
                   and int(number) <= len(search_list[search_index]['result']) \
                   and int(number) >= 0:
                    id = search_list[search_index]['result'][int(number)-1]['id']
                    echo_Videoget_info(id)
                    aga = input("\n=>> Press ENTER to continue...")
                    print (aga)

                else:
                    print ("\n[!] No video selected!")
                    echo_VideosSearch_info(search_list[search_index])

            # :page=i : jump to page i of results
            elif inp[0:5] == "page=":
                index = inp[5:]
                if  index.isdigit():
                    if int(index)-1 <= len(search_list):
                        search_index = int(index)-1
                        echo_VideosSearch_info(search_list[search_index])

                    else:
                        print ("\n[!] %s is out of range.\n" % index)

                else:
                    print ("\n[!] %s is not a number.\n" % index)
                    continue

            # :beg :end : jump to first or last page of results

            # Playing section
            #~~~~~~~~~~~~~~~~~

            # Others section
            #~~~~~~~~~~~~~~~~
            
            # :q, :quit, :exit  : close the application
            elif inp == "q" or inp == "quit" or inp == "exit":
                exit()

            # Extra section
            #~~~~~~~~~~~~~~~~

            # :h, :help : prints this help
            elif inp == "h" or inp == "help":
                halp()

            # (!)video - disables|enables video window
            elif inp == "!video":
                novideo = True
                echo_VideosSearch_info(search_list[search_index])

            elif inp == "video":
                novideo = False
                echo_VideosSearch_info(search_list[search_index])

            # (!)fullscreen - disables|enables fullscreen playback
            elif inp == "!fullscreen":
                fullscreen = False
                echo_VideosSearch_info(search_list[search_index])

            elif inp == "fullscreen":
                fullscreen = True
                echo_VideosSearch_info(search_list[search_index])

            # Option not recognized
            #~~~~~~~~~~~~~~~~~~~~~~~
            else:
                print ("\n[!] Invalid option <%s>\n" % inp)

        # Playing section (non-option)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        elif inp.isdigit() and len(search_list) !=0:
            if int(inp) != 0 \
               and int(inp) <= len(search_list[search_index]['result']):
                id = search_list[search_index]['result'][int(inp)-1]['id']
                echo_Videoget_info(id)
                title = search_list[search_index]['result'][int(inp)-1]['title']
                play(novideo, fullscreen, id, title)

            else:    
                print ("\n[!] No video selected!")
                echo_VideosSearch_info(search_list[search_index])                

        # Base section (non-option)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        # Catch URL (pending recognize video or playlist)
        elif inp[:4] == "http":
            # [youtube-url] : play a video by YouTube URL
            # [playlist-url] : display videos from a playlistURL
            id = inp.replace(cfg['youtube_video_url'], "")
            echo_Videoget_info(id)
            play(novideo, fullscreen, id, "")

        # [keywords] : search for YouTube videos
        else:
            search = VideosSearch(inp)
            search_list = []
            search_index = 0
            search_list.append(search.result())
            echo_VideosSearch_info(search_list[search_index])

        PS1 = "=>> Select one or more videos to play (:h for help)\n> "

if __name__ == "__main__":
    try:
        main(first_prompt)
        
    except KeyboardInterrupt:
        pass
    
    finally:
        pass
