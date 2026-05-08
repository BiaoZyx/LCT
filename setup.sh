#!/bin/bash
echo Now, the pwd is $pwd, if the script doesn\'t work, please choose the currect project\'s path. 
if [ sudo -i ]; 
	sudo cp ./dist/LCT-v1.3.py /usr/local/bin/lct
	echo Success! 
else
	echo Are you root or a sudoer? 
