from tkinter import Frame, Tk, Label, Button, W, StringVar, Entry, messagebox, ttk
import requests
import urllib.request
import os
import hashlib
import math

threadapi = 'https://a.4cdn.org/{0}/thread/{1}.json'
imageapi = 'https://i.4cdn.org/{0}/{1}{2}'
boardsapi = 'https://a.4cdn.org/boards.json'

if os.name == 'nt':
    imagedirname = 'Pictures'
else:
    imagedirname = 'images'

userdir = os.path.expanduser("~")
imgcollectiondir = '4chan'
imagedir = os.path.join(userdir, imagedirname)
collectiondir = os.path.join(imagedir, imgcollectiondir)

class Window(Frame):

    def __init__(self, master=None):

        Frame.__init__(self, master)               
        self.master = master
        self.init_window()
        self.load_boards()
    
    def format_bytes(self, bytes_num):
        sizes = [ "B", "KB", "MB", "GB", "TB" ]
    
        i = 0
        dblbyte = bytes_num
    
        while (i < len(sizes) and  bytes_num >= 1024):
                dblbyte = bytes_num / 1024.0
                i = i + 1
                bytes_num = bytes_num / 1024
    
        return str(round(dblbyte, 2)) + " " + sizes[i]

    def on_field_change(self, index, value, op):
        print(self.boardstring.get())
        self.boarddescriptiontext['text'] = list(filter(lambda x: x['board'] == self.boardstring.get(), self.boards))[0]['title']
    
    def load_boards(self):
        boardsjson = requests.get(boardsapi).json()
        boardsjson = boardsjson['boards']
        self.boards = list(map(lambda x: {'title': x['title'], 'board': x['board']}, boardsjson))
        self.boardstextbox.grid(row=self.boardstextboxrow, column=1, pady=self.pady)
        self.boardstextbox['values'] = list(map(lambda x: x['board'] , self.boards))
        self.boardstextbox.current(0)
        #self.boarddescriptiontext
        self.loadingboards.grid_forget()
        self.boarddescriptiontext.grid(row=self.boarddescriptiontextrow, column=1, pady=math.floor(self.pady/5))

    def init_window(self):   
        self.master.title("4chdo")  
        self.titleFont = 'helvetica 10 bold'
        self.subFont = 'helvetica 10'
        self.italicFont = 'helvetica 10 italic'
        self.bgColor = '#f0f0f0'
        self.padx = 55
        self.pady = 5
        rowcount = 0
        boxWidth = 20

        self.grid(padx=self.padx, pady=self.pady * 3)

        ######################## UI ########################
        ############### ENTRY ONE ###############

        text = Label(self, text="Board:", font=self.titleFont)
        text.grid(row=rowcount, column=1, pady=self.pady)

        rowcount += 1

        self.boardstring = StringVar()
        self.boardstring.trace('w', self.on_field_change)
        #self.boardstextbox = Entry(self, textvariable=self.boardstring, width=boxWidth)
        self.boardstextbox = ttk.Combobox(self, values=([]), width=boxWidth-3, textvariable=self.boardstring, state='readonly')
        #self.boardstextbox.current(0)
        self.boardstextbox.focus_set()
        self.boardstextboxrow = rowcount

        self.loadingboards = Label(self, text="Loading list...", font=self.subFont)
        self.loadingboardsrow = rowcount
        self.loadingboards.grid(row=self.loadingboardsrow, column=1, pady=self.pady)

        rowcount += 1

        self.boarddescriptiontext = Label(self, text='', font=self.italicFont)
        self.boarddescriptiontextrow = rowcount

        rowcount += 1

        ############### ENTRY TWO ###############

        text = Label(self, text="Thread:", font=self.titleFont)
        text.grid(row=rowcount, column=1, pady=self.pady)
        rowcount += 1

        self.threadstring = StringVar()
        textbox = Entry(self, textvariable=self.threadstring, width=boxWidth)
        textbox.focus_set()
        textbox.grid(row=rowcount, column=1, pady=self.pady)
        rowcount += 1

        ############### PADDING ###############

        text = Label(self, text="", font=self.titleFont)
        text.grid(row=rowcount, column=1, pady=5)
        rowcount += 1

        ############### INFO LABELS ###############

        self.infotext = Label(self, text='Info:', font=self.titleFont)
        self.infotextrow = rowcount
        rowcount += 1

        self.threadtexttext = 'Thread: {0}'
        self.threadtext = Label(self, text=self.threadtexttext, font=self.subFont)
        self.threadtextrow = rowcount
        rowcount += 1

        self.imagestexttext = 'No of Images: {0}'
        self.imagestext = Label(self, text=self.imagestexttext, font=self.subFont)
        self.imagestextrow = rowcount
        rowcount += 1

        self.sizetexttext = 'Total size: {0}'
        self.sizetext = Label(self, text=self.sizetexttext, font=self.subFont)
        self.sizetextrow = rowcount
        rowcount += 1

        ############### PADDING ###############

        self.lowpadding = Label(self, text="", font=self.titleFont)
        self.lowpaddingrow = rowcount
        rowcount += 1

        ############### MAIN BUTTONS ###############

        self.viewbutton = Button(self, text="Check thread",command=lambda: self.view_thread(), height = 1, width = boxWidth - 3)
        self.viewbutton.grid(row=rowcount, column=1, pady=self.pady)
        rowcount += 1

        self.downloadbutton = Button(self, text="Download images",command=lambda: self.download_images(), height = 1, width = boxWidth - 3)
        self.downloadbuttonrow = rowcount
        rowcount += 1

        #quitButton = Button(self, text="Close",command=self.client_exit, height = 1, width = boxWidth - 3)
        #quitButton.grid(row=rowcount, column=1, pady=pady)

        ############### PROGRESSBAR ###############

        self.progressbar = ttk.Progressbar(self, orient='horizontal', length = 100, mode='determinate')
        self.progressbarrow = rowcount

        rowcount += 1

        ##########################

    
    def client_exit(self):
        exit()

    def view_thread(self):
        #print(self.boards)

        self.selectedboard = self.boardstring.get()
        self.selectedthread = self.threadstring.get()
        
        if self.selectedboard == '' or self.selectedthread == '':
            messagebox.showinfo("Error", "Both Board and Thread must be specified")
            return
        
        self.lowpadding.grid(row=self.lowpaddingrow, column=1, pady=5)
        self.downloadbutton.grid(row=self.downloadbuttonrow, column=1, pady=self.pady)
        self.infotext.grid(row=self.infotextrow, column=1, pady=math.floor(self.pady/4))

        jsonres = requests.get( threadapi.format(self.selectedboard, self.selectedthread) )

        if jsonres.status_code != 200:
            messagebox.showinfo("Error", "Could not find thread or contact server. Please confirm that the thread number is correct and try again")
            return
        
        jsonres = jsonres.json()
        jsonres = jsonres['posts']

        self.threadtext['text'] = self.threadtexttext.format(self.selectedthread)
        self.threadtext.grid(row=self.threadtextrow, column=1, pady=math.floor(self.pady/4))

        self.posts = list(filter(lambda x: 'tim' in x, jsonres))

        self.imagestext['text'] = self.imagestexttext.format(len(self.posts))
        self.imagestext.grid(row=self.imagestextrow, column=1, pady=math.floor(self.pady/4))

        self.totalfilesize = 0
        for f in self.posts:
            self.totalfilesize = self.totalfilesize + f['fsize']
        
        self.sizetext['text'] = self.sizetexttext.format(self.format_bytes(self.totalfilesize))
        self.sizetext.grid(row=self.sizetextrow, column=1, pady=math.floor(self.pady/4))

    
    def download_images(self):

        if not os.path.exists(imagedir):
            os.makedirs(imagedir)

        if not os.path.exists(collectiondir):
            os.makedirs(collectiondir)
        
        threaddir = os.path.join(collectiondir, self.selectedthread)

        if not os.path.exists(threaddir):
            os.makedirs(threaddir)
        
        self.progressbar.grid(row=self.progressbarrow, column=1, pady=self.pady)
        
        postcounter = 0
        for post in self.posts:
            print('Filename: {0}'.format(post['filename']))
            print('URL: {0}'.format( imageapi.format( self.selectedboard, post['tim'], post['ext'] ) ))
            print('')
            localfile = os.path.join( threaddir, post['filename'] + post['ext'] )
            if os.path.isfile(localfile):
                onlinechecksum = hashlib.md5(requests.get( imageapi.format( self.selectedboard, post['tim'], post['ext'] ) ).content).hexdigest()
                localchecksum = hashlib.md5(open(localfile,'rb').read()).hexdigest()
                if onlinechecksum != localchecksum:
                    counter = 1
                    while True:
                        filecheck = os.path.join( threaddir, '{0}({1}){2}'.format(post['filename'], counter, post['ext']) )
                        if not os.path.isfile( filecheck ):
                            open(
                                filecheck, 'wb'
                            ).write(
                                requests.get(
                                    imageapi.format( self.selectedboard, post['tim'], post['ext'] )
                                ).content
                            )
                            break
                        else:
                            counter = counter + 1
                else:
                    pass
            else:
                open(
                    localfile, 'wb'
                ).write(
                    requests.get(
                        imageapi.format( self.selectedboard, post['tim'], post['ext'] )
                    ).content
                )
            postcounter = postcounter + 1
            self.progressbar['value'] = math.floor(postcounter / len(self.posts) * 100 )
            
        self.progressbar.grid_forget()




root = Tk()
root.title('4chdo')

root.resizable(False, False)
root.iconbitmap('favicon.ico')

#root.geometry("300x750")

app = Window(root)
root.mainloop()