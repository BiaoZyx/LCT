#!/bin/bash
echo Now, the pwd is $(pwd), if the script doesn\'t work, please choose the currect project\'s path. 
if command sudo -v ;then 
  sudo cp ./dist/LCT-v1.3 /usr/local/bin/lct
  echo Success! 
else
  echo Are you root or a sudoer? 
fi
