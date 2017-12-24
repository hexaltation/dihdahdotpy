# dihdahdotpy
Little implementation of a Morse code generator in CLI.


**usage:** dihdahdotpy [-h] [-m [MSG] | -f FILENAME | -w [WIKI [WIKI ...]]]<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[-lang [LANG]] [-s WPM] [-rec [REC]] [-sound [SOUND]]
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[-d [DEST]] [--save | --reset]

A digital Morse code operator and trainer

**optional arguments:**  
&nbsp;&nbsp;&nbsp;-h, --help            `show this help message and exit`  
&nbsp;&nbsp;&nbsp;-m [MSG]              `the message to translate in morse code`  
&nbsp;&nbsp;&nbsp;-f FILENAME           `the message to translate is stored in a text file`  
&nbsp;&nbsp;&nbsp;-w [WIKI [WIKI ...]]  `read the definition from wikipedia.org of a given 
word`  
&nbsp;&nbsp;&nbsp;-lang [LANG]          `choose the language for wikipedia`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
`Ex. for french :  "fr". Default language : "en"`  
&nbsp;&nbsp;&nbsp;-s [WPM]              `set speed of transmission in words per minutes`  
&nbsp;&nbsp;&nbsp;-rec [REC]            `set True to save message as wave file`  
&nbsp;&nbsp;&nbsp;-sound [SOUND]        `set True to Audio Stream Output`  
&nbsp;&nbsp;&nbsp;-d [DEST]             `set destination directory of wave file`  
&nbsp;&nbsp;&nbsp;--save                `save values of passed parameters in .conf file`  
&nbsp;&nbsp;&nbsp;--reset               `reset conf file to default values`  

-------------------------------------------------------------------------------

Only support Posix for now.