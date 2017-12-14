'''
@title metGuidedMode
@author: Rebecca Coles
Updated on Dec 13, 2017
Created on Dec 13, 2017

metGuidedMode
Guided mode for DESI CI FIF metrology.

Modules:

'''

# Import #######################################################################################
import tkinter as tk
# Variables ####################################################################################
frameFont = ('consolas', '10')
################################################################################################

class metGuidedMode(tk.Frame):

    def __init__(self, master):
        '''
        Constructor
        '''
        super(metGuidedMode, self).__init__()
        self.master = master
        master.title("DESI CI Meterology Guided Mode")
        
    def guidedModeFrames(self):
        '''
        Guide the user through measuring all of the FIFs.
        '''
        #Create pages for all 22 FIFs
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        pages = list(range(0, 23)) #start page + FIF pages + conclusion page
        for page in (pages):
            frame = page(container, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(pages[0]) #start on the start page

    def show_frame(self, cont):
        '''
        Show page to user.
        '''
        frame = self.frames[cont]
        frame.tkraise()

class guidedModeWindow(tk.Tk):

    def __init__(self, *args, **kwargs):
        '''
        Constructor
        '''
        #Set up frame
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        #Set up page list
        pages = list(range(0, 23)) #start page + FIF pages + conclusion page
        for page in (pages):
            frame = page(container, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(pages[0]) #start on the start page

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page", font=frameFont)
        label.pack(pady=10,padx=10)

        button = tk.Button(self, text="Visit Page 1",
                            command=lambda: controller.show_frame(PageOne))
        button.pack()

        button2 = tk.Button(self, text="Visit Page 2",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=frameFont)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=frameFont)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack()