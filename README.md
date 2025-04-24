## How to Use
The following instructions should work on Linux, possibly MacOS. Download the discdb_rename.py file. Open up a terminal window, navigate to the folder with the script, and then just use the command ```python3 dbdisc_rename.py``` and the script will work. 

For example if the script is in /home/user/discdb_rename.py, you can open up a terminal window and type in 

```
cd /home/user
```

Then run the command

```
python3 dbdisc_rename.py
```

You may need to run the following command to install all dependencies for the script to work:

```
sudo apt update &&
sudo apt install python3 python3-pip ffmpeg **
pip3 install requests beautifulsoup4
```

# Problems with script finding file location
If the script throws an error when specifying the file location, you can put the script file in the folder with your files. Then, when it asks for the location just put "." with no quotation marks. The period just signifies it will look for files in the same folder with the script file. So if you put the script in /media/myfiles/discdb_rename.py and your media files are in /media/myfiles/ then the script will look for files in /media/myfiles if you enter "." for the location.
