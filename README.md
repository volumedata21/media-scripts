## How to Use
The following instructions should work on Linux, possibly MacOS. You can either download the discdb_rename.py file, or just make a text file and name it discdb_rename.py and copy the text from my file into yours. Open up a terminal window, navigate to the folder with the script, and then just use the command ```python3 dbdisc_rename.py``` and the script will run. 

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

It will ask you to enter a page from https://thediscdb.com/ and then for the location of your media files. If, for example, you were renaming files from Miami Vice, Season 2, Disc 1, just specify that URL from thediscdb when it asks for the URL.

# Problems with script finding file location
If the script throws an error when specifying the file location, you can put the script file in the folder with your files. Then, when it asks for the location just put "." with no quotation marks. The period just signifies it will look for files in the same folder with the script file. So if you put the script in /media/myfiles/discdb_rename.py and your media files are in /media/myfiles/ then the script will look for files in /media/myfiles if you enter "." for the location.
