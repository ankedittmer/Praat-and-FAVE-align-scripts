# Praat-and-FAVE-align-scripts
Praat and FAVE-align Python scripts for analysis of S and SH phonemes in american language.
These scripts need wav and corresponding textgrid files (with word-transcriptions in breath groups), and will result in a csv file with informations about the s/sh item used and the centre of gravity of s/sh (after a pre-emphasis).
Files should be named in the manner: Participant28reading.wav and Participant28reading.TextGrid.



# Preparations and instructions to run the centre of gravity script /MacOS
For this script python 2.7 is needed, be sure you have the right version of python installed. (if not sure, type “python --version” in your console)
## Install FAVE-align
### Install XCode

For compilation XCode is needed, open your terminal and type:

$ `xcode-select --install`

(If you’re using Ubuntu run sudo apt-get install libc6-i386 instead and if you also have a 64-bit system run sudo apt-get install gcc-multilib g++-multilib)


### Install HTK (Hidden Markov ToolKit)

HTK is needed for the aligner. Go to the [HTK website](http://htk.eng.cam.ac.uk/) and register. Click on 'Download' on the left panel, and then click on 'HTK source code (tar+gzip archive)' under ‘Stable release’ 'Linux/Unix downloads'.

Once this is downloaded, you may have to unpack the "tarball". With the terminal navigate to your downloads directory (cd ~/Downloads will probably work). Then unpack the tarball like so:

$ `tar -xvzf HTK-3.4.1.tar.gz`

Some browsers automatically unpack compressed files that they download. If you get an error when you execute the above command, try the following instead:

$ `tar -xvf HTK-3.4.1.tar`

Once you extract the application, navigate into the resulting directory:

$ `cd htk`

Once this is complete, the next step is to compile HTK. Execute the following commands inside the htk directory:

$ `export CPPFLAGS=-UPHNALG`               
$ `./configure --disable-hlmtools --disable-hslab`                  
$ `make clean`  # necessary if you're not starting from scratch, if you’re installing htk for the first time,
this will throw errors          
$ `make -j4 all`           
$ `sudo make -j4 install`         

(This will take a few minutes.)

### Install Homebrew

Homebrew is a tool to install software. To install it type in your terminal:

$ `ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`

and follow the instructions.

### Install SoX

SoX is needed for sound processing

$ `rew install sox`

(This may take a few minutes.)

### Install the actual aligner

FAVE-align lives on GitHub, a repository for open-source software. You may want to create an account there, and perhaps install 'GitHub.app', which makes it easier to interact with GitHub. But for the purposes of installing the aligner, all you need is the git command-line tool, which is part of Xcode (and so should already be installed). cd into your htk directory and type

$ `git clone https://github.com/JoFrhwld/FAVE.git`

## Install the centre of gravity scripts
Go into your FAVE -> FAVE-align directory:

$ `cd FAVE`             
$ `cd FAVE-align`

and download the scripts:

$ `git clone https://github.com/ankedittmer/Praat-and-FAVE-align-scripts.git`

copy all files that are in the new folder Praat-and-FAVE-align-scripts into the parent directory (htk -> FAVE -> FAVE-align). You don’t need the Praat-and-FAVE-align-scripts folder anymore and can delete it.

## Install Praat
Go to the praat website and download praat for macintosh [praat-website](http://www.fon.hum.uva.nl/praat/download_mac.html) and follow the instructions, it doesn’t matter where you install praat, but you have to remember the path.

## Set up the data/scripts
In your htk -> FAVE -> FAVE-align directory and create a folder named data. Copy all .wav and .TextGrid (with word-transcriptions sectioned in breath groups) files that you want to investigate in this directory. Be sure just to copy them, because the files in the data folder will be manipulated through the script.

Open the file main.py with a text editor. Under the section “# Set-up” edit the editor to one that is on your computer and change the praat directory to where ever you installed praat.

## Run the scripts

In your console maneuver into htk -> FAVE -> FAVE-align directory. Run the main script via

$ `python main.py`

After some time your text editor should pop up with all words that are out-of dictionary. One tab away from the written word transcribe them in Arpabet and delete the word context. You can delete word repetitions. Than save the changes and close the editor. If a word is in there because it is misspelled (raech instead of reach) transcribe it, as if it were correctly written.

Example:                 
BAMSIE   		 Bamsie             
BAMSIE   		 Bamsie the bear            
BAMSIE   		 said Lotta to Bamsie               
LOTTA'S   		 the sun was shining through the window and on the table was Lotta's very own cup                 
SCRATCHIER   		 it looked scratchier than ever              
SCRATCHIER   		 it looked scratchier than ever              
SCRATCHIER   		 scratchier than ever            
SNIFFLED   		 Lotta sniffled her nose stubbornly and said to herself          
SNIFFLED   		 Lotta sniffled her nose stubbornly and she said to herself       
SNIFFLED   		 sniffled her nose stubbornly and said

should become something like:     
BAMSIE  &nbsp;  B AH1 M S IY0      
LOTTA’S &nbsp;  L AO1 T AA0 S      
SCRATCHIER  &nbsp;  S K R AH1 T SH IY0 EH0    
SNIFFLED  &nbsp;  S N IY1 F L EH0 D, S N IY1 F EH0 L D    


When the script is done, the results are written in cog_outcome.txt.

