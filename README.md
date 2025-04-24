## How it Works
Your media should be organized by disc. Run the python script and it will ask you to enter a page from thediscdb.com, and then the location of your media. The script will use information from the provided thediscdb.com page you used and rename your media files in a Plex-friendly format. The script will try to figure out the matching file/name by referencing the length of each video file. If there are multiple files with the same length, the script will then attempt to match by file size. If the script finds multiple video files with the same length and file size, those files won't be renamed. Files that don't have a match won't be renamed, and the script will let you know if any files couldn't be found. For example, if you reference a disc that has 10 titles but the script only sees 8 files in the folder, it will let you know which files it couldn't find. 

Currently the script can handle movies, televsion shows, and extras. Based on the URL, the script can determine if you're trying to rename a movie or TV show. The script can also handle multiple movie versions. If there's a directors cut and theatrical cut in the same folder, it will rename those according to the Plex convention for multiple versions of a movie. The script should also be able to add 1080p or 4k to the file name.

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

## Pull Requests
This script was made using ChatGPT. I'm able to get my hands a little dirty in scripting but I am not a programmer. I'm making revisions as I see problems arise. I am not a developer though and my knowledge is a little limited in programming in python. Or programming. But I'll do my best to review any pull requests and merge in fixes. I'm open to suggestions.
