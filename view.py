from tkinter import *
import tkinter.scrolledtext as tkst
from typing import List


class View:
    def __init__(self, controller):
        self._root: Tk = Tk()
        self._scroll: tkst.ScrolledText = None
        self.controller = controller

    def runTCA(self) -> None:
        print("TCA running!")
        # Split the text into separate lines
        lines: List = self._scroll.get("1.0", END).splitlines()
        self.controller.runTCA(lines)

    def saveFile(self) -> None:
        print(type(self._scroll.get("1.0", END)))    # first parameter (in scroll.get): line.character
        f = open('programs/' + self.getFileName() + ".py", "w+")
        f.write(self._scroll.get("1.0", END))
        f.close()

    def openFile(self) -> None:
        f = open(self.getFileName()+".py", "r+")
        self._scroll.delete("1.0", END)
        self._scroll.insert(END, f.read())
        # self._scroll.text = f.read()
        f.close()

    def openFileByName(self, name: str) -> None:
        f = open(name + ".py", "r")
        self._scroll.delete("1.0", END)
        self._scroll.insert(END, f.read())
        f.close()

    @staticmethod
    def getFileName() -> str:
        return input("Specify filename:")

    '''Original code of: https://stackoverflow.com/users/5321910/joey
    import tkinter as tk

    _root = tk.Tk()
    text = tk.Text(_root)
    text.pack()

    def tab(arg):
        print("tab pressed")
        text.insert(tk.INSERT, " " * 4)
        return 'break'
    
    text.bind("<Tab>", tab)
    _root.mainloop()
    '''
    # My version of a similar function:
    def tab(self, event: Event) -> str:
        self._scroll.insert(INSERT, 4*" ")
        # In order to prevent Tkinter from running
        # additional events
        return 'break'

    def createGUI(self):

        # Create the Toolbar:
        label = Label(self._root, text="IDE", bg="#ffe211")
        label.pack(side=TOP)
        saveButton = Button(self._root, text="save", command=self.saveFile)
        saveButton.pack(side=TOP)
        TCAButton = Button(self._root, text="TCA", command=self.runTCA)
        TCAButton.pack(side=TOP)
        openButton = Button(self._root, text="open", command=self.openFile)
        openButton.pack(side=TOP)
        # Create the text editor:
        self._scroll = tkst.ScrolledText(self._root, bg='black', foreground="white",
                                         insertbackground='white', selectbackground="blue")
        self._scroll.pack(side=BOTTOM)
        # change tab to n spaces
        self._scroll.bind("<Tab>", self.tab)

    def mainLoop(self):
        self._root.mainloop()
