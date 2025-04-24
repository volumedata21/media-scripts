# How it Works
This script uses information from [thediscdb.com](https://thediscdb.com/) to rename files in a media-server friendly format from discs burned by MakeMKV. It attempts to rename files based on the length of each file. If multiple files have the same length it then tries by file size. If that doesn't work, it does not rename the files. The script was mostly done using ChatGPT and my very limited Python knowledge.

# Features:
* Rename files based on Plex naming standards
* Works with movies and television series.
* Works with extras
* Works with multiple movie versions, IE director's cut and theatrical release.

# Important
### Organize by Disc
Before running the script, make sure your media is organized by disc. If renaming files from *Miami Vice, season 3, disc 1*, make sure those files are in a seperate folder from *Miami Vice, season 3, disc 2*. Having files from multiple discs in the same folder can increase chance of naming errors.
### File Types
The script assumes files are MKV files from the disc. If you compressed files it may be able to determine correct names based on length, but not file size. It is recommended to compress **after** renaming. 


# How to Use
The following instructions should work on Linux. If using MacOS, you can get it working using Brew to download python/ffmpeg/beautifulsoup4.

You can either download the discdb_rename.py file, or just make a text file and name it discdb_rename.py and copy the text from my file into yours. Open up a terminal window, navigate to the folder with the script, and then just use the command ```python3 dbdisc_rename.py``` and the script will run. 

For example if the script is in ```/home/user/discdb_rename.py```, you can open up a terminal window and type in 

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

It will ask you to enter a page from https://thediscdb.com/ and then for the location of your media files. If, for example, you were renaming files from *Miami Vice, Season 2, Disc 1*, just specify the URL for that disc from thediscdb when it asks for the URL.

# Problems with script finding file location
If the script throws an error when specifying the file location, you can put the script file in the folder with your files. Then, when it asks for the location just put ```.``` and nothing else. The period signifies it will look for files in the same folder with the script file. If you put the script in ```/media/myfiles/discdb_rename.py``` then the script will look for files in ```/media/myfiles``` if you enter ```.``` for the location.

In my experience this can occur when specifying a location that's not on the local machine, like an SMB mount.

# Pull Requests
I'm able to get my hands a little dirty in scripting but I am not a programmer. I'm making revisions as I see problems arise. I am not a developer though and my knowledge is a little limited in programming in python. Or programming. But I'll do my best to review any pull requests and merge in fixes. I'm open to suggestions.
