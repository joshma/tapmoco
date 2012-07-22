#!/bin/bash

#hard code username and password here

username="delian"
password="test"

/usr/bin/osascript <<AppleScript
   tell application "System Events" 
      delay 3.0 
      keystroke "$password" 
      delay 3.0 
      keystroke tab 
      keystroke return 
   end tell
AppleScript

exit 0