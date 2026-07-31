"""
An ASCII Directory Tree View Generator - Pure Python with no dependencies.

Core ASCII Generator code is under MIT license. See,
https://github.com/BELECTRON13/dir-tree-generator/blob/main/LICENSE

The rest of the code here: GUI, supporting routines, etc. It totally freeware.

Note: There is a list of directories to ignore while traversing the directories.
It can be edited. Search for 'IGNORE_LIST' below.

Tested with Python 3.12 on Windows 7, 10 and 11.

Versions:
First Written July 29, 2026
Added DPI Awareness and changed window scaling to match.
Made app TTK Bootstrap with light/dark theme (Thanks Copilot).
Made the directory text box readonly. - 31Jul26
"""

import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
from pathlib import Path, PurePath
from tkinter import filedialog, messagebox
import ctypes


# ===== Initial Window Geometry =====
WIN_WIDTH = 570
WIN_HEIGHT = 800
WIN_SF = 100


# ===== ASCII Tree Generator Core =====
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
        self.output_tree:list[str] = []
        self.top_level = True

    def get_tree(self):
        return ''.join(self.output_tree)

    def generate_tree(self, directory, prefix='', ignore_list=None, max_depth=10, current_depth=0):
        if ignore_list is None:
            ignore_list = self.IGNORE_LIST

        directory = Path(directory) if isinstance(directory, str) else directory

        if not directory.exists() or not directory.is_dir():
            self.output_tree = 'Error: The specified path is not valid directory.'
            return

        if self.top_level:
            self.output_tree = directory.name + '\n'
            self.top_level = False

        if current_depth > max_depth:
            return

        try:
            items = sorted(list(directory.iterdir()), key=lambda x: (x.is_file(), x.name.lower()))
        except PermissionError:
            self.output_tree += f'{prefix} └─── [Permission Denied]\n'
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
                self.generate_tree(item, prefix + extention, ignore_list, max_depth, current_depth + 1)


# ===== Helper Functions =====
def shorter_path(path, appx_len=20):
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


def set_dpi_awareness()->int:
    """
    Set the apps DPI awareness (if possible) - This works for Windows only
    Must be run before any windows are spawned.
    If Win 10 or 11, returns the current text scale factor. Else returns 100
    """
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2) # '2' scales across all windows.
        # print("Info: DPI Awareness set for Win 8.1, 10 or 11.")

        # Returns: 100, 125, 150, etc. Can be used later to help resize windows, etc.
        win_sf = ctypes.windll.shcore.GetScaleFactorForDevice(0)
        # print(f'Info: Current Text Scale Factor = {win_sf}.')
        return win_sf
    except:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
            return 100
            # print("info: DPI set for Win 7, 8")
        except:
            print('Info: DPI Awareness could not be set!')
            return 100


# ===== Main Window (Bootstrap) =====
class MainWindow(tb.Window):
    def __init__(self):
        super().__init__(themename='flatly')   # Windows‑11‑style theme (light)

        self.title('ASCII Directory Tree View Generator')
        # self.geometry('800x800')
        self.geometry(str(WIN_WIDTH) + 'x' + str(WIN_HEIGHT))
        self.minsize(640, 480)

        self.selected_diectory = ''

        self._build_ui()
        self._connect_slots()
        self._configure_resizing()

    # ===== Build UI =====
    def _build_ui(self):

        # --- Top Row: Directory Selection ---
        self.btnSelectDir = tb.Button(self, text='Select Directory', bootstyle=PRIMARY)
        self.btnSelectDir.grid(row=0, column=0, padx=14, pady=12, sticky='w')

        self.txtDirPath = tb.Entry(self)
        self.txtDirPath.grid(row=0, column=1, columnspan=3, padx=14, pady=12, sticky='nsew')
        self.txtDirPath.insert(0, 'No Directory Selected...')
        self.txtDirPath.config(state='readonly')

        # --- Row 1: Levels + Generate ---
        self.label = tb.Label(self, text='Levels To Traverse:')
        self.label.grid(row=1, column=0, padx=14, pady=12, sticky='w')

        self.spnLevels = tb.Spinbox(self, from_=1, to=100)
        self.spnLevels.grid(row=1, column=1, padx=14, pady=12, sticky='w')
        self.spnLevels.set(10)

        self.btnGenerate = tb.Button(self, text='Generate Tree View', bootstyle=PRIMARY)
        self.btnGenerate.grid(row=1, column=2, columnspan=2, padx=14, pady=12, sticky='nsew')

        # --- Row 2: Text Frame ---
        self.txtFrame = tb.Frame(self)
        self.txtFrame.grid(row=2, column=0, columnspan=4, padx=14, pady=12, sticky='nsew')

        self.txtFrame.rowconfigure(0, weight=1)
        self.txtFrame.columnconfigure(0, weight=1)

        self.txtTreeView = tk.Text(self.txtFrame, wrap='none')
        self.txtTreeView.grid(row=0, column=0, sticky='nsew')
        self.txtTreeView.insert('1.0', 'No Tree View Generated Yet...')

        self.scrollY = tb.Scrollbar(self.txtFrame, orient='vertical', command=self.txtTreeView.yview)
        self.scrollY.grid(row=0, column=1, sticky='ns')

        self.scrollX = tb.Scrollbar(self.txtFrame, orient='horizontal', command=self.txtTreeView.xview)
        self.scrollX.grid(row=1, column=0, sticky='ew')

        self.txtTreeView.configure(yscrollcommand=self.scrollY.set, xscrollcommand=self.scrollX.set)

        # --- Row 3: Copy + Exit + Theme Toggle ---
        self.btnCopy = tb.Button(self, text='Copy Tree To Clipboard', bootstyle=INFO)
        self.btnCopy.grid(row=3, column=0, padx=14, pady=12, sticky='w')

        self.btnToggleTheme = tb.Button(self, text='Toggle Dark/Light', bootstyle=INFO)
        self.btnToggleTheme.grid(row=3, column=1, padx=14, pady=12, sticky='w')

        self.btnExit = tb.Button(self, text='Exit', bootstyle=DANGER)
        self.btnExit.grid(row=3, column=3, padx=14, pady=12, sticky='e')

    # ===== Connect Slots =====
    def _connect_slots(self):
        self.btnSelectDir.configure(command=self.slot_select_dir)
        self.btnGenerate.configure(command=self.slot_generate)
        self.btnCopy.configure(command=self.slot_copy)
        self.btnExit.configure(command=self.slot_exit)
        self.btnToggleTheme.configure(command=self.slot_toggle_theme)

    # ===== Resizing =====
    def _configure_resizing(self):
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.rowconfigure(2, weight=1)

    # ===== Slots =====
    def slot_select_dir(self):
        path = filedialog.askdirectory()
        if path:
            self.txtDirPath.config(state='normal')
            self.txtDirPath.delete(0, tk.END)
            adj_len = int(15*(WIN_SF/100))
            self.txtDirPath.insert(0, str(shorter_path(path, appx_len=adj_len)))
            self.txtDirPath.config(state='readonly')

            self.selected_diectory = path

            self.txtTreeView.delete('1.0', tk.END)
            self.txtTreeView.insert('1.0', 'No Tree View Generated Yet...')

    def slot_generate(self):
        p = Path(self.selected_diectory)
        if (not self.selected_diectory) or (not p.exists()) or (not p.is_dir()):
            messagebox.showwarning('Warning', 'Please select a directory first.')
            return

        tg = TreeGen()
        tg.generate_tree(self.selected_diectory, max_depth=int(self.spnLevels.get()))

        self.txtTreeView.delete('1.0', tk.END)
        self.txtTreeView.insert('1.0', tg.get_tree())

    def slot_copy(self):
        text = self.txtTreeView.get('1.0', tk.END).strip()
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)

    def slot_toggle_theme(self):
        current = self.style.theme.name
        if 'dark' in current.lower():
            self.style.theme_use('flatly')   # light
        else:
            self.style.theme_use('darkly')   # dark

    def slot_exit(self):
        self.destroy()


# ===== Main =====
if __name__ == '__main__':

    # Scale app if possible
    WIN_SF = set_dpi_awareness()
    if WIN_SF == 125:
        WIN_WIDTH = 690
    elif WIN_SF == 150:
        WIN_WIDTH = 790

    app = MainWindow()
    app.mainloop()
