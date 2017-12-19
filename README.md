# dihdahdotpy
Little implementation of a Morse code generator in CLI.


usage: dihdahdotpy [-h] [-m [MSG]] [-f FILENAME] [-w [WIKI [WIKI ...]]]
                   [-lang [LANG]] [-s [WPM]] [--save] [--reset]

A digital Morse code operator and trainer

optional arguments:
  -h, --help            show this help message and exit
  -m [MSG]              The message to translate in morse code
  -f FILENAME           The message to translate is stored in a text file
  -w [WIKI [WIKI ...]]  Read the definition from wikipedia.org of a given word
  -lang [LANG]          Choose the language for wikipedia. Ex. for french :
                        "fr". Default language : "en"
  -s [WPM]              Set speed of transmission in words per minutes
  --save                Save values of passed parameters in .conf file
  --reset               Reset conf file to default values

-------------------------------------------------------------------------------

Only support Posix for now.