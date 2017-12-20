# dihdahdotpy
Little implementation of a Morse code generator in CLI.


**usage:** dihdahdotpy [-h] [-m [MSG] | -f FILENAME | -w [WIKI [WIKI ...]]]<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[-lang LANG] [-s WPM] [--save | --reset]

A digital Morse code operator and trainer

**optional arguments:**  
&nbsp;&nbsp;&nbsp;-h, --help            show this help message and exit  
&nbsp;&nbsp;&nbsp;-m [MSG]              The message to translate in morse code  
&nbsp;&nbsp;&nbsp;-f FILENAME           The message to translate is stored in a text file  
&nbsp;&nbsp;&nbsp;-w [WIKI [WIKI ...]]  Read the definition from wikipedia.org of a given word  
&nbsp;&nbsp;&nbsp;-lang [LANG]          Choose the language for wikipedia.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
Ex. for french :  "fr". Default language : "en"  
&nbsp;&nbsp;&nbsp;-s [WPM]              Set speed of transmission in words per minutes  
&nbsp;&nbsp;&nbsp;--save                Save values of passed parameters in .conf file  
&nbsp;&nbsp;&nbsp;--reset               Reset conf file to default values  

-------------------------------------------------------------------------------

Only support Posix for now.