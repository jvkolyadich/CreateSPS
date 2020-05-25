from tkinter import *
from tkinter.filedialog import askopenfilenames, asksaveasfilename
from tkinter.messagebox import showinfo
import tkinter.font
import io

class Converter:

    # Root window
    root = Tk()

    # Set icon for root window
    try:
        root.iconphoto(True, PhotoImage(file='./icon.png'))
    except:
        pass

    # GUI attributes
    windowWidth = 600
    windowHeight = 450
    entryWidth = 60
    entryFont = tkinter.font.Font(family = "helvetica", size = 10)

    # Create GUI Widgets
    topContainer = Frame(root)
    formInfoButton = Button(topContainer)
    openButton = Button(topContainer)
    keywordLabel = Label(root)
    keywordEntry = Entry(root)
    titleLabel = Label(root)
    titleEntry = Entry(root)
    descLabel = Label(root)
    descEntry = Text(root)
    saveButton = Button(root)

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
                                      command = self.showFormattingInfo)
        
        ## Open button
        self.openButton.configure(text = "Open song files",
                                  command = self.openFiles)
        ## Keyword label and entry
        self.keywordLabel.configure(text = "Keywords for verses & chorus:")
        self.keywordEntry.insert(END, self.defaultKeywords)
        self.keywordEntry.configure(width = self.entryWidth,
                                    font = self.entryFont)
        ## Title label and entry
        self.titleLabel.configure(text = "Songbook Title:")
        self.titleEntry.configure(width = self.entryWidth,
                                  font = self.entryFont)
        ## Description label and entry
        self.descLabel.configure(text = "Songbook Description (optional):")
        self.descEntry.configure(width = self.entryWidth,
                                 font = self.entryFont,
                                 height = 8)
        ## Save button
        self.saveButton.configure(text = "Save as songbook",
                                  command = self.saveFile)

        # Pack widgets into main window
        self.topContainer.pack(side = TOP, pady = 20)
        self.formInfoButton.pack(side = LEFT, padx = 10)
        self.openButton.pack(side = RIGHT, padx = 10)
        self.keywordLabel.pack(side = TOP, pady = 5)
        self.keywordEntry.pack(side = TOP, pady = 10)
        self.titleLabel.pack(side = TOP, pady = 5)
        self.titleEntry.pack(side = TOP, pady = 10)
        self.descLabel.pack(side = TOP, pady = 5)
        self.descEntry.pack(side = TOP, pady = 10)
        self.saveButton.pack(side = TOP, pady = 10)

    def openFiles(self):

        opened_filenames_str = askopenfilenames(defaultextension=".txt",
                                        filetypes=[("Text Documents","*.txt"),])
        if (opened_filenames_str != ""):
            self.openedFilenames = self.root.tk.splitlist(opened_filenames_str)

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
                    songbook_file.close()
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

        song_index = 0

        for song_filename in self.openedFilenames:

            song_index += 1

            with io.open(song_filename, "r", encoding="utf-8") as song_file:

                song_text = song_file.read().lstrip()
                song_file.close()

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
        
    def run(self):

        self.root.mainloop()

    def quit(self):

        self.root.destroy()

CreateSPS = Converter()
CreateSPS.run()
