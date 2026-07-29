"""
An ASCII Directory Tree View Generator - Pure Python with no dependencies.

Core ASCII Generator code is under MIT license. See,
https://github.com/BELECTRON13/dir-tree-generator/blob/main/LICENSE

The rest of the code here: GUI, supporting routines, etc. It totally freeware.

Note: There is a list of directories to ignore while traversing the directories.
It can be edited. Search for 'IGNORE_LIST' below.

Tested with Python 3.12 on Windows 7, 10 and 11.

Written July 29, 2026
"""
import tkinter as tk
from pathlib import Path, PurePath
from tkinter import filedialog, messagebox, ttk


#$ ===== ASCII Tree Generator Core =====
class TreeGen:
    """
    Core ASCII Tree Generation module is from the repository at,
        https://github.com/BELECTRON13/dir-tree-generator

    Reworked some errors in it and extended it for use here.
    Overall it works very well. Thanks Mohammad!  :-)

    Original license is MIT - Copyright (c) 2025 mohammadali
        https://github.com/BELECTRON13/dir-tree-generator/blob/main/LICENSE
    """
    def __init__(self)->None:
        self.IGNORE_LIST = ['.git', '__pycache__', '.mypy_cache', '.vscode']
        self.output_tree = []
        self.top_level = True

    def get_tree(self):
        return ''.join(self.output_tree)

    def generate_tree(self, directory, prefix='', ignore_list=None, max_depth=10, current_depth=0):
        if ignore_list is None:
            ignore_list = self.IGNORE_LIST

        directory = Path(directory) if isinstance(directory, str) else directory

        if not directory.exists() or not directory.is_dir():
            print('Error: The specified path is not valid directory.')
            self.output_tree = 'Error: The specified path is not valid directory.'
            return

        # Print the top level directory name first - only happens on first iteration
        if self.top_level:
            self.output_tree = directory.name + '\n'
            self.top_level = False

        if current_depth > max_depth:
            return

        try:
            items = sorted(list(directory.iterdir()), key=lambda x: (x.is_file(), x.name.lower()))

        except PermissionError:
            self.output_tree += f'{prefix} └─── [Permission Denied]' + '\n'
            return

        for index, item in enumerate(items):
            if next((sub for sub in ignore_list if sub in str(item)), None):
                continue

            is_last = index == len(items) - 1
            connector = '└── ' if is_last else '├── '

            line = prefix + connector + item.name
            self.output_tree += line + '\n'

            if item.is_dir():
                extention = '    ' if is_last else '│   '
                self.generate_tree(item,
                            prefix + extention,
                            ignore_list,
                            current_depth + 1,
                )



#$ ===== Helper Functions =====

def shorter_path(path, appx_len=20):
    """
    Breaks a long filepath into a smaller chunk for display purposes.

    Args:
        path (string): The full path + filename to shorten
        appx_len (int, optional): Approximate limit of the preamble string length.
        The return string WILL be longer than this.
        Defaults to 20.

    Returns:
        str: Shortened path string for display.

    """
    if not path:
        return path

    parts = list(PurePath(path).parts)

    path = PurePath(parts[0])
    for part in parts[1:-1]:
        path /= part
        if len(str(path)) >= appx_len:
            path /= ' ... '
            break
    if len(parts) > 1:
        path /= parts[-1]
    return path


#$ ===== TkInter Main Window GUI =====
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('ASCII Directory Tree View Generator')
        self.geometry('500x650')
        self.minsize(500, 650)

        self._build_ui()
        self._connect_slots()
        self._configure_resizing()

        self.selected_diectory = ''

    #$ ===== Build UI =====
    def _build_ui(self):

        # Row 0: Directory selection
        self.btnSelectDir = ttk.Button(self, text=' Select Directory: ')
        self.btnSelectDir.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        self.txtDirPath = ttk.Entry(self)
        self.txtDirPath.grid(row=0, column=1, columnspan=3, padx=10, pady=10, sticky='nsew')
        self.txtDirPath.insert(0, 'No Directory Selected...')

        # Row 1: Levels + Generate
        self.label = ttk.Label(self, text='Levels To Traverse:')
        self.label.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        self.spnLevels = ttk.Spinbox(self, from_=1, to=999)
        self.spnLevels.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        self.spnLevels.set(10)

        self.btnGenerate = ttk.Button(self, text='Generate Tree View')
        self.btnGenerate.grid(row=1, column=2, columnspan=2, padx=10, pady=10, sticky='nsew')


        # Text Box with Scrollbars
        self.txtFrame = ttk.Frame(self)
        self.txtFrame.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')

        # Configure grid inside the frame
        self.txtFrame.rowconfigure(0, weight=1)
        self.txtFrame.columnconfigure(0, weight=1)

        # Text widget
        self.txtTreeView = tk.Text(self.txtFrame, wrap='none')
        self.txtTreeView.grid(row=0, column=0, sticky='nsew')
        self.txtTreeView.insert('1.0', 'No Tree View Generated Yet...')

        # Vertical scrollbar
        self.scrollY = ttk.Scrollbar(self.txtFrame, orient='vertical',
                                     command=self.txtTreeView.yview)
        self.scrollY.grid(row=0, column=1, sticky='ns')

        # Horizontal scrollbar
        self.scrollX = ttk.Scrollbar(self.txtFrame, orient='horizontal',
                                     command=self.txtTreeView.xview)
        self.scrollX.grid(row=1, column=0, sticky='ew')

        # Connect scrollbars
        self.txtTreeView.configure(yscrollcommand=self.scrollY.set,
                                   xscrollcommand=self.scrollX.set)

        # Row 3: Copy + Exit
        self.btnCopy = ttk.Button(self, text='Copy Tree To Clipboard')
        self.btnCopy.grid(row=3, column=0, padx=10, pady=10, sticky='w')

        self.btnExit = ttk.Button(self, text='Exit')
        self.btnExit.grid(row=3, column=3, padx=10, pady=10, sticky='e')


    #$ ===== Connect Slots =====
    def _connect_slots(self):
        self.btnSelectDir.configure(command=self.slot_select_dir)
        self.btnGenerate.configure(command=self.slot_generate)
        self.btnCopy.configure(command=self.slot_copy)
        self.btnExit.configure(command=self.slot_exit)


    #$ ===== Construct App Window as Resizable =====
    def _configure_resizing(self):
        # Make columns expand
        self.columnconfigure(0, weight=0)   # buttons
        self.columnconfigure(1, weight=1)   # entry + spinbox
        self.columnconfigure(2, weight=1)   # generate button
        self.columnconfigure(3, weight=1)   # generate button

        # Make row 2 (text area) expand
        self.rowconfigure(2, weight=1)


    #$ ===== Slots (Callbacks) =====
    def slot_select_dir(self):
        path = filedialog.askdirectory()
        if path:
            self.txtDirPath.delete(0, tk.END)
            self.txtDirPath.insert(0,str(shorter_path(path, appx_len=20)))
            self.selected_diectory = path

            # Another directory selected, so delete the current tree view
            self.txtTreeView.delete('1.0', 'end')
            self.txtTreeView.insert('1.0', 'No Tree View Generated Yet...')


    #$ ===== Callback functions =====
    def slot_generate(self):
        print(f'dir = {self.selected_diectory}')
        p = Path(self.selected_diectory)
        if (not self.selected_diectory) or (not p.exists()) or (not p.is_dir()):
            messagebox.showwarning('Warning', 'Please select a directory first.')
            return

        tg = TreeGen()
        tg.generate_tree(
            self.selected_diectory,
            max_depth=int(self.spnLevels.get()),
            )
        self.txtTreeView.delete('1.0', 'end')
        self.txtTreeView.insert('1.0', tg.get_tree())


    def slot_copy(self):
        text = self.txtTreeView.get('1.0', tk.END).strip()
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)
            # messagebox.showinfo('Copied', 'Tree text copied to clipboard.')


    def slot_exit(self):
        self.destroy()


#$ ===== Tk Main Loop =====
if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()
