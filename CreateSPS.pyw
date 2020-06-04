from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilenames, asksaveasfilename
from tkinter.messagebox import showinfo
import tkinter.font
import zlib, base64, tempfile, io

class Converter:

    # Root window
    root = Tk()

    # Set icon for root window
    try:
        root.iconphoto(True, PhotoImage(file='./icon.png'))
    except:
        ICON = zlib.decompress(base64.b64decode('eJxjYGAEQgEBBiDJwZDBy'
        'sAgxsDAoAHEQCEGBQaIOAg4sDIgACMUj4JRMApGwQgF/ykEAFXxQRc='))
        _, ICON_PATH = tempfile.mkstemp()
        with open(ICON_PATH, 'wb') as icon_file:
            icon_file.write(ICON)
        root.iconbitmap(default=ICON_PATH)
        pass

    # GUI attributes
    windowWidth = 665
    windowHeight = 495
    entryWidth = 60
    entryFont = tkinter.font.Font(family = "helvetica", size = 10)

    # Create GUI Widgets
    mainContainer = Frame(root)
    leftContainer = Frame(mainContainer)
    rightContainer = Frame(mainContainer)
    leftTopContainer = Frame(leftContainer)
    leftBottomContainer = Frame(leftContainer)
    leftBottomTopContainer = Frame(leftBottomContainer)
    fileScrollbar = Scrollbar(leftTopContainer)
    fileList = Listbox(leftTopContainer, yscrollcommand = fileScrollbar.set)
    sortButton = Button(leftBottomTopContainer)
    topContainer = Frame(rightContainer)
    formInfoButton = Button(topContainer)
    openButton = Button(topContainer)
    keywordLabel = Label(rightContainer)
    keywordEntry = Entry(rightContainer)
    titleLabel = Label(rightContainer)
    titleEntry = Entry(rightContainer)
    descLabel = Label(rightContainer)
    descEntry = Text(rightContainer)
    saveButton = Button(rightContainer)

    # Variables
    defaultKeywords = "Verse, Chorus, Куплет, Припев"
    openedFilenames = None
    saveFilename = ""

    def __init__(self):

        # Set window title
        self.root.title("CreateSPS")

        # Calculate values to center window on screen
        pxFromLeft = (self.root.winfo_screenwidth() / 2) - (self.windowWidth / 2)
        pxFromTop = (self.root.winfo_screenheight() / 2) - (self.windowHeight / 2)

        # Center window on screen
        self.root.geometry("%dx%d+%d+%d" %  (self.windowWidth,
                                             self.windowHeight,
                                             pxFromLeft,
                                             pxFromTop))

        # Make the window non-resizeable
        self.root.resizable(0, 0)

        # Configure widgets
        ## Formatting info button
        self.formInfoButton.configure(text = "Formatting info",
                                      font = self.entryFont,
                                      command = self.showFormattingInfo)
        
        ## Open button
        self.openButton.configure(text = "Open song files",
                                  font = self.entryFont,
                                  command = self.openFiles)
        ## Keyword label and entry
        self.keywordLabel.configure(text = "Keywords for verses & chorus:",
                                    font = self.entryFont)
        self.keywordEntry.insert(END, self.defaultKeywords)
        self.keywordEntry.configure(width = self.entryWidth,
                                    font = self.entryFont)
        ## Title label and entry
        self.titleLabel.configure(text = "Songbook Title:",
                                  font = self.entryFont)
        self.titleEntry.configure(width = self.entryWidth,
                                  font = self.entryFont)
        ## Description label and entry
        self.descLabel.configure(text = "Songbook Description (optional):",
                                 font = self.entryFont)
        self.descEntry.configure(width = self.entryWidth,
                                 font = self.entryFont,
                                 height = 8)
        ## Save button
        self.saveButton.configure(text = "Save as songbook",
                                  font = self.entryFont,
                                  command = self.saveFile)

        ## Scrollbar
        self.fileScrollbar.config(command = self.fileList.yview)

        ## File list
        self.fileList.configure(height = 20,
                                font = self.entryFont)

        ## Sort button
        self.sortButton.configure(text = "Sort by title",
                                  font = self.entryFont,
                                  width = 10,
                                  command = self.sortList)

        # Pack widgets into main window
        self.mainContainer.pack(side = TOP,
                                padx = 20,
                                pady = 10)

        self.leftContainer.pack(side = LEFT,
                                padx = 10)

        self.rightContainer.pack(side = RIGHT,
                                 padx = 10)

        self.leftTopContainer.pack(side = TOP)

        self.leftBottomContainer.pack(side = TOP)
        
        self.leftBottomTopContainer.pack(side = TOP,
                                         pady = 8)

        self.fileScrollbar.pack(side = RIGHT,
                           fill = Y)

        self.fileList.pack(side = LEFT)


        self.topContainer.pack(side = TOP,
                               pady = 20)

        self.formInfoButton.pack(side = LEFT,
                                 padx = 10)

        self.openButton.pack(side = RIGHT,
                             padx = 10)

        self.keywordLabel.pack(side = TOP,
                               pady = 5)

        self.keywordEntry.pack(side = TOP,
                               pady = 10)

        self.titleLabel.pack(side = TOP,
                             pady = 5)

        self.titleEntry.pack(side = TOP,
                             pady = 10)

        self.descLabel.pack(side = TOP,
                            pady = 5)

        self.descEntry.pack(side = TOP,
                            pady = 10)

        self.saveButton.pack(side = TOP,
                             pady = 10)

        self.sortButton.pack(side = BOTTOM)

    def openFiles(self):

        opened_filenames_str = askopenfilenames(defaultextension=".txt",
                                        filetypes=[("Text Documents","*.txt"),])
        if (opened_filenames_str != ""):
            self.openedFilenames = self.root.tk.splitlist(opened_filenames_str)
            self.updateFileList()

    def saveFile(self):
        if (self.verifyInputs()):
            self.saveFilename = asksaveasfilename(initialfile='songbook.sps',
                                                  defaultextension=".sps",
                                                  filetypes=[("softProjector Songbook","*.sps"),
                                                             ("All Files","*.*")])

            if (self.saveFilename != ""):
                songbook_text = self.createSongbook()
                with io.open(self.saveFilename, "w+", encoding="utf-8") as songbook_file:
                    songbook_file.write(songbook_text)
                showinfo("Done", "Songbook created.")

    def verifyInputs(self):

        if (self.openedFilenames == None):
            showinfo("Error", "No song files opened.")
            return False

        keywords = self.keywordEntry.get().rstrip()
        if (keywords == ""):
            showinfo("Error", "No keywords given.")
            return False

        title = self.titleEntry.get().rstrip()
        if (title == ""):
            showinfo("Error", "Please enter a title.")
            return False

        return True

    def createSongbook(self):

        songbook_text = ""

        # The id doesn't matter since it's changed by softProjecter when you import the songbook
        songbook_id = "##1\n"
        songbook_text += songbook_id

        songbook_title = self.titleEntry.get()
        songbook_title = "##" + songbook_title + "\n"
        songbook_text += songbook_title

        description = self.descEntry.get("1.0", END)
        # Removes the extra "\n" tkinter adds when getting the description
        description = description[:(len(description) - 1)]
        description = description.replace("\n", "@%")
        description = "##" + description + "\n"
        songbook_text += description

        keywords_str = self.keywordEntry.get()
        keywords_str = keywords_str.replace(" ", "")
        keywords = keywords_str.split(",")

        for song_index, song_filename in enumerate(self.openedFilenames):
            song_index += 1

            with io.open(song_filename, "r", encoding="utf-8") as song_file:
                song_text = song_file.read().lstrip()

            # Use first line of lyrics as each song's title
            song_title_start = song_text.find("\n") + 1
            song_title_end = song_text.find("\n", song_title_start)
            song_title = song_text[song_title_start:song_title_end]
            # Remove punctuation and extra whitespace
            chars = ".,!?-\""
            for char in chars:
                if char in song_title:
                    song_title = song_title.replace(char, "")
                    
            song_title = song_title.replace("  ", " ")

            for keyword in keywords:

                # Search for keywords using all uppercase text
                word_location = song_text.upper().find(keyword.upper())
                while (word_location != -1):
                    
                    # Unless it's the first keyword, insert "@S" before each one
                    if(word_location != 0):
                        song_text = song_text[:(word_location - 2)] + "@$" + song_text[word_location:]
                        
                    word_location = song_text.upper().find(keyword.upper(), (word_location + 1))

            # Removes duplicate newlines
            duplicate_location = song_text.find("\n\n")
            while (duplicate_location != -1):
                song_text = song_text.replace("\n\n", "\n")
                duplicate_location = song_text.find("\n\n")

            # Replaces newlines with "@%"
            song_text = song_text.replace("\n", "@%")

            # Combines all song file elements
            song_text = str(song_index) + "#$#" + song_title + "#$#0#$##$##$##$#" + song_text + "#$##$##$#\n"

            # Removes "\n" from the last song
            if (song_filename == self.openedFilenames[len(self.openedFilenames) - 1]):
                song_text = song_text.replace("\n", "")

            songbook_text += song_text

        return songbook_text

    def showFormattingInfo(self):

        showinfo("Song formatting", "Songs must be formatted as:\n( [ ] = optional )\n\nKeyword [additional text]\n[Lyrics for line 1]\n[Lyrics for line 2]\n[etc.]\n\nBasically the same way as in softProjector\n\nThe first line of the first stanza of\neach song will be the song's title")

    def sortList(self):
        unsorted_list = list(self.openedFilenames)
        sort_key = []

        for filename in unsorted_list:
            filenamestart = filename.rfind("/") + 1
            filenameend = filename.rfind(".")
            filename = filename[filenamestart:filenameend]
            sort_key.append(filename)
            
        for index, key in enumerate(sort_key):
            try:
                sort_key[index] = int(key)
            except:
                pass

        sorted_list = [x for _,x in sorted(zip(sort_key,unsorted_list))]

        self.openedFilenames = tuple(sorted_list)
        self.updateFileList()


    def updateFileList(self):
        self.fileList.delete(0, END)
        for filename in self.openedFilenames:
            filenamestart = filename.rfind("/") + 1
            filename = filename[filenamestart:]
            self.fileList.insert(END, filename)

    def run(self):

        self.root.mainloop()

    def quit(self):

        self.root.destroy()

CreateSPS = Converter()
CreateSPS.run()
