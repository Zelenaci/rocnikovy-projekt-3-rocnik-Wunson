import tkinter as tk
wd_width = 640
wd_height = 480



window = tk.Tk()

window.title("best game ever")

wd_size =(str(wd_width),"x",str(wd_height))
window.geometry("".join(wd_size))

window.mainloop()