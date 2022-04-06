import os
import tkinter as tk
import tkinter.ttk as ttk
import pygubu.builder.tkstdwidgets
import pygubu.builder.ttkstdwidgets
from tkinter.filedialog import askopenfile
from tkinter import messagebox
import PyPDF2
from googletrans import Translator
import pygubu

try:
    CDIR = os.path.abspath(os.path.dirname(__file__))
except NameError:
    CDIR = os.path.dirname(os.path.abspath(sys.argv[0]))
#PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_UI = os.path.join(CDIR, "referencing.ui")

class ReferencingApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(CDIR)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object('frame1', master)
        builder.connect_callbacks(self)
    

    def browse(self):
    
        path = os.getcwd()
        file = askopenfile(mode='rb', initialdir=path, filetypes=[('PDF Files', '.pdf')])
        if file is not None:
            reader = PyPDF2.PdfFileReader(file)
            self.reader = reader
    
    def search(self):
    
        reader = self.reader
        n = reader.numPages
        self.results = n*[0]
        entry = self.builder.get_object('entry1')
        translator = Translator()
        sentence = translator.translate(entry.get()).text
        sent_list = sentence.split(" ")
        for num in range(n):
            page = reader.getPage(num)
            text = page.extractText()
            i = 0
            for word in sent_list:
                if word in text:
                    self.results[num] += 1
                i += 1
        else:
            self.get_results()
            
    def get_results(self):
    
        list_pages = []
        for n in range(5):
            i = 0
            max_score = 0
            pageindex = 0
            for result in self.results:
                in_bool = i not in list_pages
                if result > max_score and in_bool:
                    pageindex = i
                    max_score = result
                i += 1
            list_pages.append(pageindex)
        str_results = ""
        for page in list_pages:
            str_results += "Page: "+str(page+1)+"\n"
        messagebox.showinfo("Results", str(str_results))
            
    def run(self):
        self.mainwindow.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    app = ReferencingApp(root)
    app.run()

