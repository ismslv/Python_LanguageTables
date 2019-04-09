#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.simpledialog as simpledialog
import tkinter.ttk as ttk
from collections import namedtuple

#pyinstaller Main.py -n Langear -i Icon.ico --add-data Data;Data --noconsole --windowed

class ExampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        """ t = SimpleTable(self, 10,2)
        t.pack(side="top", fill="x") """

        self.menubar = tk.Menu()
        self.menubar.add_command(label="New book", command=self.OnNewBook)
        self.menubar.add_command(label="Open book", command=self.OnOpenBook)
        self.menubar.add_command(label="Add page", command=self.OnAddPage, state="disabled")
        self.menubar.add_command(label="Add line", command=self.AddLine, state="disabled")
        self.menubar.add_command(label="Save book", command=self.OnSave, state="disabled")
        self.menubar.add_command(label="Quit", command=frame.quit)
        self.bind('<Control-l>', self.KeyNewLine)

        self.config(menu=self.menubar)

        self.currentBook = None

    def KeyNewLine(self, e):
        self.AddLine("")

    def OnOpenLibrary(self):
        file = filedialog.askopenfilename(initialdir="/",
                                          title="Select Library file",
                                          filetypes=[("library files","*.fmlib")])
        if (file != None and file != ""):
            self.OpenLibrary(file)
    
    def OpenLibrary(self, libname):
        file1 = open(libname, "r", encoding="utf-8")
        data = file1.readlines()
        for line in data:
            d = line.split('=')
            if (len(d) == 2):
                if (d[0].strip() == "languages"):
                    self.libLangs = d[1].split(',')
                    for ll in self.libLangs:
                        ll = ll.strip

    def OnNewBook(self):
        file = filedialog.asksaveasfilename(initialdir="/",
                                            title="Select Book name and place",
                                            filetypes=[("book files","*.fmbook")])
        if (file != None and file != ""):
            self.NewBook(file)
    
    def NewBook(self, newname):
        newname += ".fmbook"
        file = open(newname,"w+", encoding="utf-8")
        file.close()
        self.OpenBook(file.name)

    def OnOpenBook(self):
        file = filedialog.askopenfilename(initialdir="/",
                                          title="Select Book file",
                                          filetypes=[("book files","*.fmbook")])
        if (file != None and file != ""):
            self.OpenBook(file)

    def OpenBook(self, bookfile):
        if (self.currentBook != None and self.table != None):
            self.CloseBook()
        self.currentBook = bookfile
        file1 = open(bookfile, "r", encoding="utf-8")
        ids = file1.readlines()
        self.bookIds = list()
        for line in ids:
            self.bookIds.append(line.strip())
        file1.close()
        self.currentDir = directory = os.path.split(bookfile)[0]
        self.filename = os.path.split(bookfile)[1].split('.')
        os.chdir(directory)
        self.pages = list()
        self.table = SimpleTable(self)
        num = 0
        for file_ in glob.glob(self.filename[0] + "_*.fmpage"):
            langid = os.path.split(file_)[1].split('.')[0].split('_')[1]
            self.pages.append((langid, file_, self.OpenPage(file_)))
            num += 1
            self.table.AddColumn(num, self.pages[num-1])
        self.table.pack(side="top", fill="x")
        if (len(self.pages) > 0):
            self.menubar.entryconfig("Save book", state = "normal")
        else:
            self.menubar.entryconfig("Save book", state = "disabled")
        self.menubar.entryconfig("Add page", state = "normal")
        self.menubar.entryconfig("Add line", state = "normal")
    
    def CloseBook(self):
        self.currentBook = None
        self.table.Destroy()
        self.table = None
            
    def OpenPage(self, file):
        file1 = open(file, "r", encoding="utf-8")
        data = self.PageToGrid(file1)
        file1.close()
        return data
    
    def OnAddPage(self):
        newlang = simpledialog.askstring("Enter new file name (code)", self)
        if (newlang != None):
            self.AddPage(newlang)
            self.menubar.entryconfig("Save book", state = "normal")

    def AddPage(self, name):
        newname = self.currentDir + "/" + self.filename[0] + "_" + name + ".fmpage"
        file = open(newname,"w+", encoding="utf-8")
        arr = list()
        for i in range(len(self.bookIds)):
            if (i > 0):
                file.write("\n")
            file.write(self.bookIds[i])
            file.write("\n")
            arr.append((self.bookIds[i], ""))
        file.close()
        data = (name, newname, arr)
        self.pages.append(data)
        self.table.AddColumn(len(self.pages), data)

    def OnOpen(self):
        file = filedialog.askopenfilename(initialdir="/",
                                          title="Select Book file",
                                          filetypes=[("book files","*.fmpage")])
        self.currentFile = file
        file1 = open(file, "r", encoding="utf-8")
        data = self.PageToGrid(file1)
        file1.close()
        self.table = SimpleTable(self)
        self.table.pack(side="top", fill="x")
    
    def OnSave(self):
        file = open(self.currentBook,"w+", encoding="utf-8")
        for y in range(0, len(self.bookIds)):
            if (y > 0):
                file.write("\n")
            self.bookIds[y] = self.table._widgets[y + 1][0].get()
            file.write(self.bookIds[y])
        file.close()
        for i in range(len(self.pages)):
            self.SavePage(i)
        
    def SavePage(self, num):
        file = open(self.pages[num][1],"w+", encoding="utf-8")
        for y in range(0, len(self.bookIds)):
            if (y > 0):
                file.write("\n")
            file.write(self.bookIds[y] + "\n")
            file.write(self.table._widgets[y + 1][num + 1].get())
        file.close()
    
    def PageToGrid(self, page):
        lines = page.readlines()
        qTotal = len(lines)
        if (qTotal % 2 == 1):
            lines.append("")
            qTotal += 1
        arr = list()
        for i in range(0,qTotal,2):
            arr.append([lines[i].strip(), lines[i + 1].strip()])
        return arr
    
    def AddLine(self, newid = None):
        if (newid == None):
            newid = simpledialog.askstring("Enter new id", self)
        if (newid != None):
            self.bookIds.append(newid)
            self.table.AddRow(newid)

class SimpleTable(tk.Frame):
    def __init__(self, parent):
        # use black background so it "peeks through" to 
        # form grid lines
        tk.Frame.__init__(self, parent, background="black")
        self._widgets = []
        for row in range(len(parent.bookIds) + 1):
            current_row = []
            label = tk.Entry(self)
            label.grid(row=row, column=0, sticky="nsew", padx=1, pady=1)
            if (row == 0):
                label.insert(0, "Id")
                label.config(state = "readonly")
            else:
                label.insert(0, parent.bookIds[row - 1])
                #label.config(state = "readonly")
            current_row.append(label)
            self._widgets.append(current_row)

        self.grid_columnconfigure(0, weight=1)

    def Destroy(self):
        for r in self._widgets:
            for c in r:
                c.pack_forget()
                c.grid_forget()
                c.destroy()
        self.pack_forget()
        self.destroy()

    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)
    
    def AddRow(self, name):
        current_row = []
        for x in range(len(self._widgets[0])):
            label = tk.Entry(self)
            label.grid(row=len(self._widgets), column=x, sticky="nsew", padx=1, pady=1)
            if (x == 0):
                label.insert(0, name)
                #label.config(state = "readonly")
            else:
                label.insert(0, "")
            current_row.append(label)
        self._widgets.append(current_row)

    def AddColumn(self, num, columnData):
        for row in range(len(columnData[2]) + 1):
            label = tk.Entry(self)
            label.grid(row=row, column=num, sticky="nsew", padx=1, pady=1)
            if (row == 0):
                label.insert(0, columnData[0])
                label.config(state = "readonly")
            else:
                label.insert(0, columnData[2][row - 1][1])
            self._widgets[row].append(label)
            #self._widgets.append(current_row)
        
        self.grid_columnconfigure(num, weight=1)

if __name__ == "__main__":
    DictItem = namedtuple('DictItem', 'id val')
    app = ExampleApp()
    app.version = "0.001"
    app.title("Langear by FMLHT, v" + app.version)
    #app.geometry("600x800")
    app.iconphoto(True, tk.PhotoImage(file='Data/Images/Icon.png'))
    app.mainloop()