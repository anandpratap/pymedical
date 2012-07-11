from Tkinter import *
import tkFileDialog, tkMessageBox, tkSimpleDialog
import os

import tkSimpleDialog

class MyDialog(tkSimpleDialog.Dialog):

    def body(self, master):

        self.v = IntVar()
        Radiobutton(master, text="Local", variable=self.v, value=1).pack(side=LEFT)
        Radiobutton(master, text="Foreign", variable=self.v, value=2).pack(side=LEFT)
    
    def ok(self, event=None):
        val = self.v.get()
        if val == 1:
            #restore from local backup
            os.system("./.lrestore.sh")
            self.cancel()
        elif val ==2:
            #restore from foreign backup
            os.system("./.lrestore.sh")
            self.cancel()
    def cancel(self, event=None):
        self.parent.focus_set()
        self.destroy()


    def apply(self):
        pass

class App:

    def __init__(self, master):
        self.pin = '123'
        try:
            f = file(".dir.log")
            self.local_dir = f.readline().replace("\n","")
            self.foreign_dir = f.readline().replace("\n","")
        except:
            self.local_dir = "/home/maverick"
            self.foreign_dir = "/home/maverick"
        frame = Frame(master)
        frame.pack()
        
        self.select_local_backup_dir = Button(frame, text="Select Local Backup Dir", command=self.select_local_dir)
        self.select_local_backup_dir.pack(side=TOP)
        
        self.select_foreign_backup_dir = Button(frame, text="Select Foreign Backup Dir", command=self.select_foreign_dir)
        self.select_foreign_backup_dir.pack(side=TOP)
       
        self.local_backup_now = Button(frame, text="Local Backup Now", command=self.func_local_backup)
        self.local_backup_now.pack(side=TOP)
        self.foreign_backup_now = Button(frame, text="Foreign Backup Now", command=self.func_foreign_backup)
        self.foreign_backup_now.pack(side=TOP)
       
        self.restore_now = Button(frame, text="Restore Now", command=self.restore)
        self.restore_now.pack(side=TOP)
       
        
        self.make_default = Button(frame, text="Default", command=self.func_default)
        self.make_default.pack(side=TOP)
        
        self.l = StringVar()
        self.f = StringVar()
        self.l.set("LOCAL: "+self.local_dir)
        self.f.set("FOREIGN: "+self.foreign_dir)
        self.show_local_dir = Label(frame, textvariable=self.l)
        self.show_local_dir.pack(side=TOP)
        self.show_foreign_dir = Label(frame, textvariable=self.f)
        self.show_foreign_dir.pack(side=TOP)


    def select_local_dir(self):
        self.local_dir = tkFileDialog.askdirectory(parent=root,initialdir="/home/maverick",title='Please select a directory')
        if len(self.local_dir ) > 0:
            self.l.set("LOCAL: "+self.local_dir)
    def select_foreign_dir(self):
        self.foreign_dir = tkFileDialog.askdirectory(parent=root,initialdir="/home/maverick",title='Please select a directory')
        if len(self.foreign_dir ) > 0:
            self.f.set("FOREIGN: "+self.foreign_dir)
    def func_local_backup(self):
        os.system("./.backup.sh")

    def func_foreign_backup(self):
        os.system("./.fbackup.sh")
    def func_default(self):
        os.system('rm .dir.log')
        cmd = "echo '" + self.local_dir + "' >> .dir.log"
        os.system(cmd)
        cmd = "echo '" + self.foreign_dir + "' >> .dir.log"
        os.system(cmd)
    
    def restore(self):
        pin = tkSimpleDialog.askstring("Restore", "PIN")
        if pin == self.pin:
            if tkMessageBox.askyesno("Restore", "Are you sure you want to restore?\n You will loose the data after the last backup"):
                d = MyDialog(root)
                
        else:
             tkMessageBox.showwarning("Restore","Wrong pin!")

            
root = Tk()
app = App(root)
root.mainloop()
