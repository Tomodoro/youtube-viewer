# youtube-viewer (for Windows)
A lightweight application for searching and playing videos from YouTube

All credits go to Trizen's [`youtube-viewer`](https://github.com/trizen/youtube-viewer).

### youtube-viewer
* command-line interface to Youtube

![youtube-viewer](https://i.postimg.cc/HnbTypwG/Screenshot-5.png)

## Prerequisites
**Program**: mpv (recommended)<br>
**Program**: yt-dlp<br>
**Program**: Python 3<br>
**Program**: vlc (alternative to mpv)<br>

pip packages: youtube-search-python
```
pip3 install --user youtube-search-python
```


All* programs can be easily installed with [Chocolatey](https://chocolatey.org/) and get automatically added to PATH.

## Known issues
1. *VLC must be added to path manually.

~~2. VLC gets pushed to the background with `:!video` and it must be closed from Task Manager.~~

2. VLC will always show GUI, even with `!video` option.
3. VLC *needs* that `youtube-dl` is available on PATH, even if it is `yt-dlp` renamed.
4. json module from python cannot handle backslashes, therefore the full path of vlc excecutable cannot be set there

# Roadmap

- [x] Implement `:back` function
    - [x] Save result pages into array
- [ ] Implement multiple-select reproduction
    - [ ] Save input into array
    - [ ] Apply regex on input
    - [ ] Save videos into array
- [ ] Differentiate "first prompt" mode from "complete" mode.
- [ ] Save local watched videos into text file
    - [ ] Set colors to output
    - [ ] Use a different color for watched videos
    - [ ] Put this setting on configuration file
- [ ] Add support for playlists
    - [ ] Differentiate `watch?v=` from `playlist?list=`
- [ ] Complete functionality of the interactive help from Trizen

(Complete help)

```
# Base
[keywords]        : search for YouTube videos ---------------------------> Done!
[youtube-url]     : play a video by YouTube URL -------------------------> Done!
:v(ideoid)=ID     : play videos by YouTube video IDs --------------------> Done!
[playlist-url]    : display videos from a playlistURL
:playlist=ID      : display videos from a playlistID

# Control
:n(ext)           : get the next page of results ------------------------> Done!
:b(ack)           : get the previous page of results --------------------> Done!

# Actions
:login            : will prompt you for login
:logout           : will delete the authentication key

# YouTube
:i(nfo)=i,i       : display more information ----------------------------> Partial, only accepts one argument.
:d(ownload)=i,i   : download the selected videos
:c(omments)=i     : display video comments
:r(elated)=i      : display related videos
:u(ploads)=i      : display author's latest uploads
:pv=i :popular=i  : display author's popular uploads
:A(ctivity)=i     : display author's recent activity
:p(laylists)=i    : display author's playlists
:s=i  :save=i     : save a video ID in a local playlist (see -lp)
:rm=i :remove=i,i : remove a saved video from the local playlist
:sc=i             : save author's channel ID to file (see -lc)
:ps=i :s2p=i,i    : save videos to a post-selected playlist
:sub(scribe)=i    : subscribe to author's channel
:unsub(scribe)=i  : unsubscribe from author's channel
:(dis)like=i      : like or dislike a video
:fav(orite)=i     : favorite a video
:autoplay=i       : autoplay mode, starting from video i
:page=i           : jump to page i of results --------------------------> Done!
:beg :end         : jump to first or last page of results

# Playing
<number>          : play the corresponding video -----------------------> Done!
3-8, 3..8         : same as 3 4 5 6 7 8
8-3, 8..3         : same as 8 7 6 5 4 3
8 2 12 4 6 5 1    : play the videos in a specific order
10..              : play all the videos onwards from 10
:q(ueue)=i,i,...  : enqueue videos for playing them later
:pq, :play-queue  : play the enqueued videos (if any)
:anp, :nnp        : auto-next-page, no-next-page
:play=i,i,...     : play a group of selected videos
:regex='RE'       : play videos matched by a regex (/i)
:kregex=KEY,RE    : play videos if the value of KEY matches the RE

# Others
:r(eturn)         : return to previous page of results
:refresh          : refresh the current list of results
:dv=i             : display the data structure of result i
-argv -argv2=v    : apply some arguments (e.g.: -u=google)
:reset, :reload   : restart the application
:q, :quit, :exit  : close the application ------------------------------> Done!

NOTES:
 1. You can specify more options in a row, separated by spaces.
 2. A stdin option is valid only if it begins with '=', ';' or ':'. ----> Done!
 3. Quoting a group of space separated keywords or option-values,
    the group will be considered a single keyword or a single value.

** Examples:
:regex='\w \d' -> play videos matched by a regular expression.
:info=1        -> show extra information for the first video.
:d18-20,1,2    -> download the selected videos: 18, 19, 20, 1 and 2.
3 4 :next 9    -> play the 3rd and 4th videos from the current
                  page, go to the next page and play the 9th video.
```

(First prompt help)
```
# Base
[keywords]        : search for YouTube videos
[youtube-url]     : play a video by YouTube URL
:v(ideoid)=ID     : play videos by YouTube video IDs
[playlist-url]    : display videos from a playlistURL
:playlist=ID      : display videos from a playlistID

# Actions
:login            : will prompt you for login
:logout           : will delete the authentication key

# Others
:r(eturn)         : return to previous page of results
:refresh          : refresh the current list of results
:dv=i             : display the data structure of result i
-argv -argv2=v    : apply some arguments (e.g.: -u=google)
:reset, :reload   : restart the application
:q, :quit, :exit  : close the application

NOTES:
 1. You can specify more options in a row, separated by spaces.
 2. A stdin option is valid only if it begins with '=', ';' or ':'.
 3. Quoting a group of space separated keywords or option-values,
    the group will be considered a single keyword or a single value.

** Example:
    To search for playlists, insert: -p keywords
```

# Future of the project

There main reasons this project exists are:
1. I like youtube-viewer, but upstream does not provide support for Windows.
2. I tried to install Trizen's youtube-viewer on Strawberry Perl (Windows) and failed.
3. I mostly open Youtube videos with mpv by copying the url to the terminal.
4. I prefer to skip the web browser thing all togheter and search the video from the terminal.

For the program to get a beta release it must provide all upstream features, it does not matter if the code is messy or not optimized.
Once the last part gets arranged the program should finally hit 0.1.0 (and who knows what the future awaits!).

At the moment of writing this repository is more like a storage for the code than an active development branch, so I will not hang around very ofter.
HOWEVER if you really like this project and would like to see it thrive, please open a pull request with your contribution.

If I don't show up (I sometimes get really busy and disapear for almost a year) and that halts the development,
feel free to fork it. I don't care if someone else takes over from here, I only want this to exists. Just respect the licence.

Regards, Tomodoro
