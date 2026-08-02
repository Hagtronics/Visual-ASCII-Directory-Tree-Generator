# Visual ASCII Folder Tree Generator
A Python3/Tkinter Windows app that generates ASCII folder tree views suitable for documentation. 
  
Also very useful when trying to find 'lost items' or where you 'stashed' files in your project directories.  
  
## Screenshot:  
![Screenshot](/images/screen_shot_2.PNG)  

## Usage:
Get the single source file and run it anywhere Python 3.12+ and ttkbootstrap are installed.  
(see the requirements.txt in the src folder)  
  
## Simple to use:  
1) Select the maximum number of levels to traverse.  
2) Select the folder to generate a tree view of, tree generation starts automatically.  
3) Press the 'Copy To Clipboard' button to place the generated tree on the clipboard.
Note: If you want to change the levels to traverse, just select a new number and then  
re-select the same folder again. A new Tree will be generated.  
   
Tested on windows 7, 10 and 11 with Python 3.12.  

## Notes:  
There is a list of folder names to 'ignore' while traversing the directories.  
It can be edited. Search for 'IGNORE_LIST' in the source code.  
Currently the default ignore list is: `IGNORE_LIST = ['.git', '__pycache__', '.mypy_cache', '.vscode']`  
  
## Based on:   
Core ASCII Tree Generation module is from the repository at,  
https://github.com/BELECTRON13/dir-tree-generator    
Reworked some errors in it and extended it for use here.  
Overall it works very well. Thanks Mohammad!  :-)  
Original license is MIT - Copyright (c) 2025 mohammadali  
https://github.com/BELECTRON13/dir-tree-generator/blob/main/LICENSE  

The rest of the GUI code, etc. here is freeware.  
  
