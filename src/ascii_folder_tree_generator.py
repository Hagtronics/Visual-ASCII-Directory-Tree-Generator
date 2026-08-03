"""
An ASCII Folder Tree View Generator - Pure Python with no dependencies.

Core ASCII Generator code is under MIT license. See,
https://github.com/BELECTRON13/dir-tree-generator/blob/main/LICENSE

The rest of the code here: GUI, supporting routines, etc. are totally freeware.

Note: There is a list of directories to ignore while traversing the directories.
It can be edited. Search for 'IGNORE_LIST' below.

Tested with Python 3.12 on Windows 7, 10 and 11.

First Written July 29, 2026
"""
import ctypes
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

#$ ===== The Master Folder Ignore List =====
IGNORE_LIST = ['.git', '__pycache__', '.mypy_cache', '.vscode', '.ipynb_checkpoints']


#$ ===== ASCII Tree Generator Core =====
class TreeGen:
    """
    Core ASCII Tree Generation module is from the repository at,
        https://github.com/BELECTRON13/dir-tree-generator

    Extended it for use here. Overall it works very well. Thanks Mohammad!  :-)

    Original license is MIT - Copyright (c) 2025 mohammadali
        https://github.com/BELECTRON13/dir-tree-generator/blob/main/LICENSE
    """
    def __init__(self)->None:
        self.output_tree = []
        self.top_level = True

    def get_tree(self):
        return ''.join(self.output_tree)

    def generate_tree(self, directory, prefix='', ignore_list=None, max_depth=0, current_depth=0):
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
                            max_depth,
                            current_depth + 1,
                )


#$ ===== Helper Functions =====
def set_dpi_awareness()->None:
    """
    Set the apps DPI awareness (if possible) - This works for Windows only
    Must be run before any windows are spawned.
    """
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2) # '2' scales across all windows.
        # print("Info: DPI Awareness set for Win 8.1, 10 or 11.")

        # Returns: 100, 125, 150, etc. Can be used later to help resize windows, etc.
        # win_sf = ctypes.windll.shcore.GetScaleFactorForDevice(0)
        # print(f'Info: Current Text Scale Factor = {win_sf}.')
    except:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
            # print("info: DPI set for Win 7, 8")
        except:
            print('Info: DPI Awareness could not be set!')


def center_window(window):
    """ Center tk Window on screen """
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")



#$ ===== TkInter Main Window GUI =====
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('ASCII Folder Tree View Generator')
        self.geometry('640x700')
        self.minsize(640, 700)
        center_window(self)

        self._build_ui()
        self._connect_slots()
        self._configure_resizing()

        self.selected_diectory = ''

        # Optionally pick a theme here
        # for windows, valid themes are: ('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
        #style = ttk.Style()
        #style.theme_use('vista')

    #$ ===== Build UI =====
    def _build_ui(self):

        # Main window grid behavior
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)
        self.grid_rowconfigure(0, minsize=0)
        self.grid_rowconfigure(2, minsize=0)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        # Row 0: Folder selection + Levels
        self.btnSelectDir = ttk.Button(self, text='Select Folder', width=30)
        self.btnSelectDir.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        self.label = ttk.Label(self, text='Levels To Traverse:')
        self.label.grid(row=0, column=1, padx=10, pady=10, sticky='e')

        self.spnLevels = ttk.Spinbox(self, from_=0, to=999)
        self.spnLevels.grid(row=0, column=3, padx=10, pady=10, sticky='e')
        self.spnLevels.set(10)

        # Row 1: Text Box with Scrollbars
        self.txtFrame = ttk.Frame(self)
        self.txtFrame.grid(row=1, column=0, columnspan=4, padx=10, pady=(0,0), sticky='nsew')

        # Text frame grid behavior
        self.txtFrame.rowconfigure(0, weight=1)   # text expands
        self.txtFrame.rowconfigure(1, weight=0)   # horizontal scrollbar stays fixed
        self.txtFrame.columnconfigure(0, weight=1)

        self.txtTreeView = tk.Text(self.txtFrame, wrap='none')
        self.txtTreeView.grid(row=0, column=0, sticky='nsew')

        self.txtTreeView.insert('1.0', 'No Tree View Generated Yet...')

        self.scrollY = ttk.Scrollbar(self.txtFrame, orient='vertical',
                                    command=self.txtTreeView.yview)
        self.scrollY.grid(row=0, column=1, sticky='ns')

        self.scrollX = ttk.Scrollbar(self.txtFrame, orient='horizontal',
                                    command=self.txtTreeView.xview)
        self.scrollX.grid(row=1, column=0, sticky='ew')

        self.txtTreeView.configure(yscrollcommand=self.scrollY.set,
                                xscrollcommand=self.scrollX.set)

        # Row 2: Copy + Exit
        self.btnCopy = ttk.Button(self, text='Copy Tree To Clipboard', width=30)
        self.btnCopy.grid(row=2, column=0, padx=10, pady=(10,10), sticky='w')

        self.btnExit = ttk.Button(self, text='Exit')
        self.btnExit.grid(row=2, column=3, padx=10, pady=(10,10), sticky='e')


    #$ ===== Connect Slots =====
    def _connect_slots(self):
        self.btnSelectDir.configure(command=self.slot_select_dir)
        self.btnCopy.configure(command=self.slot_copy)
        self.btnExit.configure(command=self.slot_exit)


    #$ ===== Construct App Window as Resizable =====
    def _configure_resizing(self):
        # Make columns expand
        self.columnconfigure(0, weight=0)   # buttons
        self.columnconfigure(1, weight=1)   # entry + spinbox
        self.columnconfigure(2, weight=1)   # generate button
        self.columnconfigure(3, weight=1)   # generate button


    #$ ===== Slots (Callbacks) =====
    def slot_select_dir(self):
        path = filedialog.askdirectory()
        if path:
            p = Path(path)
            if (not path) or (not p.exists()) or (not p.is_dir()):
                messagebox.showwarning('Warning', 'Please select a valid directory first.')
                return

            tg = TreeGen()
            self.txtTreeView.delete('1.0', tk.END)
            self.txtTreeView.insert('1.0', 'Working...')
            self.txtTreeView.update()

            tg.generate_tree(
                path,
                max_depth=int(self.spnLevels.get()),
                ignore_list=IGNORE_LIST,
                )

            self.txtTreeView.delete('1.0', tk.END)
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
    set_dpi_awareness()
    app = MainWindow()
    app.mainloop()
