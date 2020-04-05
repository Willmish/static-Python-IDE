import tkinter as tk
import tkinter.scrolledtext as tkst
from typing import List



# This is a scrollable text widget
class ScrollText(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.text: tk.Text = tk.Text(self, bg='#2b2b2b', foreground="#d1dce8", insertbackground='white',
                                     selectbackground="blue", width=120, height=30)

        self.scrollbar: tk.Scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scrollbar.set)

        self.numberLines: TextLineNumbers = TextLineNumbers(self, width=40, bg='#313335')
        self.numberLines.attach(self.text)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.numberLines.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
        self.text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.text.bind("<Key>", self.onPressDelay)
        self.text.bind("<Button-1>", self.numberLines.redraw)
        self.scrollbar.bind("<Button-1>", self.onScrollPress)
        self.text.bind("<MouseWheel>", self.onPressDelay)
        # change tab to n spaces
        self.text.bind("<Tab>", self.tab)

    def onScrollPress(self, *args) -> None:
        self.scrollbar.bind("<B1-Motion>", self.numberLines.redraw)

    def onScrollRelease(self, *args) -> None:
        self.scrollbar.unbind("<B1-Motion>", self.numberLines.redraw)

    def onPressDelay(self, *args) -> None:
        self.after(2, self.numberLines.redraw)

    def get(self, *args, **kwargs):
        return self.text.get(*args, **kwargs)

    def insert(self, *args, **kwargs):
        return self.text.insert(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.text.delete(*args, **kwargs)

    def index(self, *args, **kwargs):
        return self.text.index(*args, **kwargs)

    def redraw(self):
        self.numberLines.redraw()

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
        self.insert(tk.INSERT, 4 * " ")
        # In order to prevent Tkinter from running
        # additional events
        return 'break'


'''THIS CODE IS CREDIT OF Bryan Oakley (With minor visual modifications on my side): 
https://stackoverflow.com/questions/16369470/tkinter-adding-line-number-to-text-widget'''


class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs, highlightthickness=0)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=linenum, fill="#606366")
            i = self.textwidget.index("%s+1line" % i)


'''END OF Bryan Oakley's CODE'''


class View:
    PLATFORM = None

    def __init__(self, controller):
        self._root: tk.Tk = tk.Tk()
        self._scroll: ScrollText = None
        # self._frame = tk.Frame(self._root)
        self.controller = controller
        self._errorMessages: tkst.ScrolledText = None

    def getScrollData(self, startIndex: str, endIndex: str) -> str:
        return self._scroll.get(startIndex, endIndex)

    def getErrorMsgData(self, startIndex: str, endIndex: str) -> str:
        return self._errorMessages.get(startIndex, endIndex)

    def deleteAllInfoScroll(self) -> None:
        self._scroll.delete("1.0", tk.END)

    def deleteAllInfoErrorMsg(self) -> None:
        self._errorMessages.delete("1.0", tk.END)

    def insertIntoScroll(self, location: str, data: str):
        self._scroll.insert(location, data)

    def insertIntoErrorMsg(self, location: str, data: List[str]):
        self._errorMessages.insert(location, data)

    def runTCA(self) -> None:
        print("TCA running!")
        # Split the text into separate lines
        lines: List = self.getScrollData("1.0", tk.END).splitlines()
        self.controller.runTCA(lines)

    def saveFile(self) -> None:
        # print(type(self._scroll.get("1.0", tk.END)))    # first parameter (in scroll.get): line.character
        try:
            f = open('programs/' + self.getFileName() + ".py", "w+")
            f.write(self.getScrollData("1.0", tk.END))
            f.close()
            self._scroll.redraw()
        except FileNotFoundError:
            print("No such file or directory")

    def openFile(self) -> None:
        try:
            f = open(self.getFileName() + ".py", "r+")
            self.deleteAllInfoScroll()
            self.insertIntoScroll(tk.END, f.read())
            # self._scroll.text = f.read()
            f.close()
            self._scroll.redraw()
        except FileNotFoundError:
            print("No such file or directory")

    def openFileByName(self, name: str) -> None:
        f = open(name + ".py", "r")
        self._scroll.delete("1.0", tk.END)
        self._scroll.insert(tk.END, f.read())
        f.close()
        self._scroll.redraw()

    @staticmethod
    def getFileName() -> str:
        return input("Specify filename:")

    def createGUI(self):
        self._root.configure(background='#3c3f41')
        # Create the Toolbar:
        topFrame = tk.Frame(self._root, bg='#3c3f41')
        # label = tk.Label(topFrame, text="IDE", bg="#ffe211")
        # label.pack(side=tk.TOP)
        saveButton = tk.Button(topFrame, text="save", command=self.saveFile, bg='#4a4d4f', fg="#d1dce8")
        saveButton.pack(side=tk.LEFT, padx=(5, 5), pady=(5, 5))
        TCAButton = tk.Button(topFrame, text="TCA", command=self.runTCA, bg='#4a4d4f', fg="#d1dce8")
        TCAButton.pack(side=tk.LEFT, padx=(5, 5), pady=(5, 5))
        openButton = tk.Button(topFrame, text="open", command=self.openFile, bg='#4a4d4f', fg="#d1dce8")
        openButton.pack(side=tk.LEFT, padx=(5, 5), pady=(5, 5))
        # Create the text editor:
        self._root.title('ShymIDE')

        topFrame.pack(side=tk.TOP, pady=(0, 5), fill=tk.X, expand=True, anchor='n')

        self._scroll = ScrollText(self._root, bg='#3c3f41')
        self._errorMessages = tkst.ScrolledText(self._root, width=130, height=10, state="disabled", bg='#2b2b2b',
                                                fg='#d1dce8')

        # fill - tells the manager how to expand - only use the space in the x, y or both directions
        # expand - assign additional space to a slave if the master is resized
        self._scroll.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=(10, 10), anchor='n')
        self._errorMessages.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=(15, 15), pady=(15, 5), anchor='n')

    def addErrors(self, errors: List[str]):
        self._errorMessages['state'] = 'normal'
        self._errorMessages.delete("1.0", tk.END)
        for error in errors:
            self._errorMessages.insert(tk.END, error + '\n')
        self._errorMessages['state'] = 'disabled'

    def addMessage(self, msg: str) -> None:
        self._errorMessages.configure(state='normal')
        self.deleteAllInfoErrorMsg()
        self.insertIntoScroll(tk.END, msg)
        self._errorMessages.configure(state='disabled')

    def getInputFromConsole(self) -> str:
        self._errorMessages.configure(state='normal')
        # TODO wait for enter press
        self._errorMessages.configure(state='disabled')

    def mainLoop(self):
        self._root.after(200, self._scroll.redraw)
        self._root.mainloop()
