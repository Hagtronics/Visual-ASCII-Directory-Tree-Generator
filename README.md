# Visual-ASCII-Directory-Tree-Generator
A Python3/Tkinter app that generates ASCII directory tree views suitable for documentation. 
  
Also very useful when trying to find 'lost items' or where you 'stashed' files in your project directories.  
  
## Screenshot:  
![Screenshot](/images/screen_shot.PNG)  

## Usage:
Get the single source file and run it anywhere Python 3.12+ is installed. No other dependencies.  
  
##Simple to use:  
1) Select the directory to generate a tree view of.  
2) Select the maximum number of levels to traverse.  
3) Press the 'Generate' button.  
4) Press the 'Copy To Clipboard' button to place the generated tree on the clipboard.  
   
Tested on windows 7, 10 and 11 with Python 3.12.  

##Notes:  
There is a list of directory names to 'ignore' while traversing the directories.  
It can be edited. Search for 'IGNORE_LIST' in the source code.  
Currently the default ignore list is: `IGNORE_LIST = ['.git', '__pycache__', '.mypy_cache', '.vscode']`  
  
##Based on:   
Core ASCII Tree Generation module is from the repository at,  
https://github.com/BELECTRON13/dir-tree-generator    
Reworked some errors in it and extended it for use here.  
Overall it works very well. Thanks Mohammad!  :-)  
Original license is MIT - Copyright (c) 2025 mohammadali  
https://github.com/BELECTRON13/dir-tree-generator/blob/main/LICENSE  

The rest of the GUI code, etc. is freeware.  
  
