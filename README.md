# youtube-viewer (for Windows)
A lightweight application for searching and playing videos from YouTube.

All credits go to [`youtube-viewer`](https://github.com/trizen/youtube-viewer).

### youtube-viewer
* command-line interface to Youtube

![youtube-viewer](https://i.postimg.cc/HnbTypwG/Screenshot-5.png)

## Prerequisites
Python 3<br>
pip packages: youtube-search-python
```
pip3 install --user youtube-search-python
```

# Roadmap

- [ ] Complete functionality of the interactive help from Trizen
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
