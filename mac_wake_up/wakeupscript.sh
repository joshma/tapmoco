#!/bin/bash

ping -c 1 -W 10 google.com &>/dev/null
until [ $? -eq 0 ]; do
sleep 1
ping -c 1 -W 10 google.com &>/dev/null
done


response=$(curl http://www.tapmo.co/user/me@joshma.com/loc/1/status)

until [ $response == 1 ]; do
response=$(curl http://www.tapmo.co/user/me@joshma.com/loc/1/status)
done

echo $response

if [ $response == 1 ]; then
/usr/bin/osascript <<AppleScript
   tell application "System Events" 
   	keystroke "**password**"
      keystroke return 
   end tell
AppleScript
say -v Vicki "Hello there Android"
else
echo "Fuck off"
fi
exit 0