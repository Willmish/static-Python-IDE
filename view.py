import tkinter as tk
import tkinter.scrolledtext as tkst
from typing import List


'''This is not my code, credit of:
https://stackoverflow.com/questions/16369470/tkinter-adding-line-number-to-text-widget'''
class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2,y,anchor="nw", text=linenum)
            i = self.textwidget.index("%s+1line" % i)


class ScrollText:
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(*args, **kwargs)


class View:
    def __init__(self, controller):
        self._root: tk.Tk = tk.Tk()
        self._scroll: tkst.ScrolledText = None
        #self._frame = tk.Frame(self._root)
        self.lineNo: TextLineNumbers = None
        self.controller = controller
        self._errorMessages: tkst.ScrolledText = None

    def runTCA(self) -> None:
        print("TCA running!")
        # Split the text into separate lines
        lines: List = self._scroll.get("1.0", tk.END).splitlines()
        self.controller.runTCA(lines)

    def saveFile(self) -> None:
        print(type(self._scroll.get("1.0", tk.END)))    # first parameter (in scroll.get): line.character
        f = open('programs/' + self.getFileName() + ".py", "w+")
        f.write(self._scroll.get("1.0", tk.END))
        f.close()

    def openFile(self) -> None:
        f = open(self.getFileName()+".py", "r+")
        self._scroll.delete("1.0", tk.END)
        self._scroll.insert(tk.END, f.read())
        # self._scroll.text = f.read()
        f.close()

    def openFileByName(self, name: str) -> None:
        f = open(name + ".py", "r")
        self._scroll.delete("1.0", tk.END)
        self._scroll.insert(tk.END, f.read())
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
    def tab(self, event: tk.Event) -> str:
        self._scroll.insert(tk.INSERT, 4*" ")
        # In order to prevent Tkinter from running
        # additional events
        return 'break'

    def createGUI(self):

        # Create the Toolbar:
        label = tk.Label(self._root, text="IDE", bg="#ffe211")
        label.pack(side=tk.TOP)
        saveButton = tk.Button(self._root, text="save", command=self.saveFile)
        saveButton.pack(side=tk.TOP)
        TCAButton =tk.Button(self._root, text="TCA", command=self.runTCA)
        TCAButton.pack(side=tk.TOP)
        openButton = tk.Button(self._root, text="open", command=self.openFile)
        openButton.pack(side=tk.TOP)
        # Create the text editor:
        self._scroll = tkst.ScrolledText(self._root, bg='black', foreground="white",
                                         insertbackground='white', selectbackground="blue", width=120, height=30)
        self._errorMessages = tkst.ScrolledText(self._root, width=130, height=10, state="disabled")
        #self.lineNo = TextLineNumbers(self._scroll.frame)
        # self.lineNo.attach(self._scroll)
        self._errorMessages.pack(side=tk.BOTTOM)
        self._scroll.pack(side=tk.BOTTOM)
        #self.lineNo.pack()
        # change tab to n spaces
        self._scroll.bind("<Tab>", self.tab)

    def addErrors(self, errors: List[str]):
        self._errorMessages['state'] = 'normal'
        self._errorMessages.delete("1.0", tk.END)
        for error in errors:
            self._errorMessages.insert(tk.END, error + '\n')
        self._errorMessages['state'] = 'disabled'

    def mainLoop(self):
        self._root.mainloop()
