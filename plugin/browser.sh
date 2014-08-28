#!/bin/bash

# due to some issues with LIRC / UBUNTU / XBMC, hitting play button actually causes this script to be executed again
# till that is fixed, I am at least going to reduce the problem by bailing out if chrome is already running.
CHROME_STARTED=`ps -ef | grep google-chrome-unstable | grep -v "grep" | wc -l`
if [ $CHROME_STARTED -gt 0 ]; then
	exit 1;
fi

# lets find out if irxevent and xdotool actually exist before we try to call them.
command -v irxevent >/dev/null 2>&1
IRXEVENT=$?
command -v xdotool >/dev/null 2>&1
XDOTOOL=$?

if [ $IRXEVENT -eq 0 ]; then
	killall irxevent >/dev/null 2>&1
fi

# http://stackoverflow.com/questions/59895/can-a-bash-script-tell-what-directory-its-stored-in
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# This is the html 5 player url
url="https://www.youtube.com/embed/$1?autoplay=1&autohide=1"

# notice the ampersand to send google chrome into back ground so that the script continues and we execute the xdotool below
/usr/bin/google-chrome-unstable --start-maximized --disable-translate --disable-new-tab-first-run --no-default-browser-check --no-first-run "$url" &
CHROME_PID=$!

if [ $IRXEVENT -eq 0 ]; then
	# run irxevent as a daemon so that we can call xdotool
	irxevent -d $DIR/youtube.lirc &
else
	echo "irxevent is not installed, can't do remote control"	
fi

if [ $XDOTOOL -eq 0 ]; then
	# no point sleeping if xdotool is not installed.
	sleep 5
	# the 800 800 is just to ensure the mouse is in middle of video but not on any controls by accident
	xdotool search "Google Chrome" windowactivate --sync mousemove 800 800 click --repeat 2 1 >/dev/null 2>&1
else
	echo "xdotool is not installed, can't do full screen"
fi

# wait for google-chrome to be killed before killing irxevent below.  This only works if we execute irxevent as a daemon, otherwise
# the script would never finish.
wait $CHROME_PID

if [ $IRXEVENT -eq 0 ]; then
	killall irxevent >/dev/null 2>&1
fi
