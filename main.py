from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfilenames
import tkinter.messagebox
import os
from PIL import Image

#Window to store the widget
class Window(Frame):
    def __init__(self,master) -> None:
        super().__init__(master)
        self.master = master

        #Setting the title of the master
        self.master.title("Image Compressor")
        self.master.geometry("500x300")

        #Initialising the variables
        self.dir = None
        self.quality = IntVar()

        #Create and pack the frame
        self.create_widgets()
        self.pack()
    
    def create_widgets(self) -> None:
        '''Creates the widgets within the frame'''

        #Creating all of the widgets
        self.main_label = Label(self,text = 'Img Compressor')
        self.browse_btn = Button(self,text = 'Browse Images', command = self.browse)
        self.quality_label = Label(self,text = 'Select Quality')
        self.quality_box = Entry(self,textvariable = self.quality, width = 10)
        self.start_btn = Button(self,text = 'Start Compression', command = self.compress_images)
        self.logger = Listbox(self, height = 8, width = 70, border = 0)
        self.instructions = Button(self,text = 'Instructions', command = self.show_instructions)
        self.openfolder = Button(self,text = 'Open output folder', command = self.outputfolder)

        #Packing all of the widgets
        self.main_label.grid(row = 0, column = 5, padx = 10, pady = 10)
        self.browse_btn.grid(row = 1, column = 1)
        self.quality_label.grid(row = 1, column = 6)
        self.quality_box.grid(row = 1, column = 7)
        self.start_btn.grid(row = 3, column = 5)
        self.logger.grid(row = 5,column = 1, columnspan = 7)
        self.instructions.grid(row = 1, column = 5)
        self.openfolder.grid(row = 4, column = 5)

    def log(self, string) -> None:
        '''Display the activity in the tkinter window'''
        self.logger.insert(END,string)

    def outputfolder(self):
        '''Open the folder where the resized image is output to'''
        #Check if the output folder is found
        if('Resized' not in os.listdir()):
            #Create the folder if it is not found
            os.mkdir('Resized')
        os.startfile("Resized")
        self.log("Opened output folder")
    
    def show_instructions(self) -> None:
        '''Displays the instruction to use the app'''
        self.i = \
        '''Instruction
        1. Browse the images that you will like to select
        2. Select the quality of the images to be resized
        3. Press the start button to start resizing

        Quality can only be between 1 and 100

        The output will be in the folder Resized at the
        same location as the program
        '''
        tkinter.messagebox.showinfo("Instructions",self.i)

    def browse(self) -> None:
        accepted = (('Image Files','.jpg'),('Image Files','.jfif'),('Image Files','png'))
        self.dir = askopenfilenames(parent = self.master, title = 'Choose an image file', filetypes = accepted)
        for name in self.dir:
            self.log("Selected " + getfilename(name))

    def compress_images(self) -> None:
        '''Compress the images and output them to a file'''
        #Check if the director is selected
        if(self.dir == None):
            tkinter.messagebox.showerror("Please select the images","Please select your images to be processed")
            return

        #If the quality selected is a number
        try:
            q = self.quality.get()
            
        except:
            tkinter.messagebox.showerror("Select a valid quality","Please select a valid quality")
            return

        #Check if the value is within range
        if(q<=0 or q > 100):
            tkinter.messagebox.showerror("Select a valid quality","Please select a valid quality, quality can only be between 0 and 100")
            return

        #Check if the folder to store the resized images is found
        if('Resized' not in os.listdir()):
            #Create the folder if it is not found
            os.mkdir('Resized')

        #Loop through the images that are in the item
        try:
            for f in self.dir:
                self.log('Compressing: ' + getfilename(f))
                with Image.open(f) as img:
                    img.save("Resized\\"+getfilename(f[:-4]) + "_resized.jpg", quality = q, optimize = True)

        except Exception as exp:
            #If there is an error log the error
            self.log("An Error occurred: " + str(exp))
            return

        #If not signal when done
        self.log("Compression complete")

def getfilename(path) -> str:
    '''Get the name of the file given a filename'''
    result = ''
    while(len(path) > 0 and path[-1] != '/'):
        result = path[-1] + result
        path = path[:-1]
    return result

def main()->None:
    '''Main function'''
    root = Tk()
    app = Window(root)
    root.mainloop()

if(__name__ == "__main__"):
    main()