import tkinter as tk
import time
import webbrowser
from PIL import Image,ImageTk
from tkinter import ttk
from datetime import datetime
from Scanner import Scanner
from Parser import Parser

class Init:
    def start(self):
        Root()

class Root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.resizable(0,0)
        self.title('LaLigaBot')
        self.mainFrame = tk.Frame(self)
        self.mainFrame.pack()
        Chat(self,self.mainFrame)
        self.mainloop()

class Chat(tk.Canvas):
    def __init__(self,root : tk.Tk,mainFrame : tk.Frame):
        super().__init__(root,bg = '#202C33')

        self.start()

        self.mainFrame = mainFrame
        self.mainFrame.pack_forget()

        self.root = root
        self.root.geometry('900x600')

        global images
        images = Image.open('Images/laligalogo.png')
        images = images.resize((60,60),Image.ANTIALIAS)
        images = ImageTk.PhotoImage(images)

        self.create_image(82,51,image = images)

        tk.Label(self,font = 'lucida 15 bold',bg = '#0060B2').place(width = 50,height = 30,x = 2, y = 40)
        tk.Label(self,text = 'La Liga Bot',font = 'lucida 15 bold',padx = 20, fg = 'white',bg = '#0060B2',anchor = 'w',justify = 'left').place(width = 786,height = 30,x = 112, y = 40)

        container = tk.Frame(self)
        container.place(x = 50,y = 100,width = 600,height = 400)

        self.canvas = tk.Canvas(container,bg = '#131B21')
        self.frameScroll = tk.Frame(self.canvas,bg = '#131B21')

        scroll = self.canvas.create_window((0,0),window = self.frameScroll,anchor = 'nw')

        def frameScrollConfiguration(e):
            self.canvas.configure(scrollregion = self.canvas.bbox('all'))

        def redimensionFrame(e):
            self.canvas.itemconfig(scroll,width = e.width)

        self.frameScroll.bind('<Configure>',frameScrollConfiguration)

        scrollbar = ttk.Scrollbar(container,orient = 'vertical',command = self.canvas.yview)
        self.canvas.configure(yscrollcommand = scrollbar.set)
        self.yview_moveto(1.0)

        scrollbar.pack(side = 'right',fill = 'y')

        self.canvas.bind('<Configure>',redimensionFrame)
        self.canvas.pack(fill = 'both',expand = True)

        errRep = tk.Button(self,text = 'Reporte de Errores',bg = '#1CB49C',fg = 'white',activebackground = '#1A9E8A',activeforeground = 'white',font='lucida 11 bold',borderwidth = 0,command = self.errorReport)
        errRep.place(width = 180,height = 30,x = 670,y = 100)

        clLErr = tk.Button(self,text = 'Limpiar Log de Errores',bg = '#1CB49C',fg = 'white',activebackground = '#1A9E8A',activeforeground = 'white',font='lucida 11 bold',borderwidth = 0,command = self.clearLogError)
        clLErr.place(width = 180,height = 30,x = 670,y = 140)

        tknRep = tk.Button(self,text = 'Reporte de Tokens',bg = '#1CB49C',fg = 'white',activebackground = '#1A9E8A',activeforeground = 'white',font='lucida 11 bold',borderwidth = 0,command = self.tokenReport)
        tknRep.place(width = 180,height = 30,x = 670,y = 180)

        clLTkn = tk.Button(self,text = 'Limpiar Log de Tokens',bg = '#1CB49C',fg = 'white',activebackground = '#1A9E8A',activeforeground = 'white',font='lucida 11 bold',borderwidth = 0,command = self.clearLogToken)
        clLTkn.place(width = 180,height = 30,x = 670,y = 220)

        usrGui = tk.Button(self,text = 'Manual de Usuario',bg = '#1CB49C',fg = 'white',activebackground = '#1A9E8A',activeforeground = 'white',font='lucida 11 bold',borderwidth = 0,command = self.openUsrGuide)
        usrGui.place(width = 180,height = 30,x = 670,y = 260)

        tcnGui = tk.Button(self,text = 'Manual Técnico',bg = '#1CB49C',fg = 'white',activebackground = '#1A9E8A',activeforeground = 'white',font='lucida 11 bold',borderwidth = 0,command = self.openTcnGuide)
        tcnGui.place(width = 180,height = 30,x = 670,y = 300)

        self.newMessage = tk.Text(self,font = 'lucida 10',highlightcolor = 'blue',highlightthickness = 0)
        self.newMessage.place(width = 600,height = 30,x = 50,y = 520)
        self.newMessage.focus_set()

        send = tk.Button(self,text = 'Enviar',bg = '#1CB49C',fg = 'white',activebackground = '#1A9E8A',activeforeground = 'white',font='lucida 11 bold',borderwidth = 0,command = self.sendMessage)
        send.place(width = 180,height = 30,x = 670,y = 520)

        contactFrame = tk.Frame(self.frameScroll,bg = '#d9d5d4')

        hour = tk.Label(contactFrame,bg = '#d9d5d4',text = datetime.now().strftime('%H:%M'),font = 'lucida 9 bold')
        hour.pack()

        contact = tk.Label(contactFrame,wraplength = 450,text = 'La Liga Bot Chat',font = 'lucida 10 bold',bg = 'orange')
        contact.pack(fill = 'x')

        contactFrame.pack(pady = 15,padx = 15,fill = 'x',expand = True,anchor = 'e')

        self.welcomeBot()
        self.pack(fill = 'both',expand = True)

    def sendMessage(self):
        pass

    def getMessage(self,message):
        messageFrame = tk.Frame(self.frameScroll,bg = '#131B21')
        messageFrame.columnconfigure(1,weight = 1)

        receivedMessage = tk.Label(messageFrame,wraplength = 450,fg = 'white',bg = '#202C33',text = message,font = 'lucida 9 bold',justify = 'left',anchor = 'w',padx = 5,pady = 5)
        receivedMessage.grid(row = 0,column = 1,padx = 2,sticky = 'w')

        hora = tk.Label(messageFrame,bg = '#131B21',fg = 'white',text = datetime.now().strftime('%H:%M'),font = 'lucida 7 bold',justify = 'left',anchor = 'w',padx = 5)
        hora.grid(row = 1,column = 1,padx = 2,sticky = 'w')

        messageFrame.pack(padx = 10,pady = 5,fill = 'x',expand = True,anchor = 'e')
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)

    def start(self):
        pass

    def errorReport(self):
        pass

    def clearLogError(self):
        pass

    def tokenReport(self):
        pass

    def clearLogToken(self):
        pass

    def openUsrGuide(self):
        pass

    def openTcnGuide(self):
        pass

    def welcomeBot(self):
        self.getMessage('Hola soy La Liga Bot\nPregúntame lo que sea de La Liga')