from ctypes import resize
from struct import pack
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as tk_file
import PIL
from PIL import ImageTk
from PIL import Image
import pydicom as dicom

import os
#sudo apt-get install python3-pil python3-pil.imagetk
root = tk.Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
# root.geometry('500x550' )
root.title('Image Viewer')

def popup_menu(e):
    menu_bar.tk_popup(x=e.x_root,y=e.y_root)
images_list = []
images_vars = []
def display_images(index):
    image_display_lb.config(image=images_list[index][1])
def load_images():
    dir_path = tk_file.askdirectory()


    images_files = os.listdir(dir_path)
  
    for r in range(0, len(images_files)):
        try:            
            image_path = f"{dir_path}/{images_files[r]}"
            ds = dicom.dcmread(image_path)
            images_list.append([
                ImageTk.PhotoImage(
                    Image.fromarray(ds.pixel_array).resize((50, 50),Image.ANTIALIAS)),
                ImageTk.PhotoImage(
                    Image.fromarray(ds.pixel_array).resize((720,480),Image.ANTIALIAS ))
            ])
            images_vars.append(f'img_{r}')
        except IsADirectoryError:
            continue
        except PIL.UnidentifiedImageError:
            continue
    for n in range(len(images_vars)):
        globals()[images_vars[n]] = tk.Button(slider, image=images_list[n][0], bd=0,
                                                command= lambda n=n:display_images(n))
        globals()[images_vars[n]].pack(side=tk.LEFT)


    pass

menu_btn = tk.Button(root,text='☰',bd=0,font=('Bold',15))
menu_btn.pack(side=tk.TOP, anchor=tk.W,pady=20,padx=20)
menu_btn.bind('<Button-1>', popup_menu)


menu_bar = tk.Menu(root,tearoff=False)
menu_bar.add_command(label='Open Folder',command=load_images)
menu_bar.add_command(label='Exit')


image_display_lb = tk.Label(root)
image_display_lb.pack(anchor=tk.CENTER)

canvas = tk.Canvas(root, height=60,width=500)
canvas.pack(side=tk.BOTTOM,fill=tk.X)

x_scroll_bar = ttk.Scrollbar(root,orient=tk.HORIZONTAL)
x_scroll_bar.pack(side=tk.BOTTOM,fill=tk.X)
x_scroll_bar.config(command=canvas.xview)

canvas.config(xscrollcommand=x_scroll_bar.set)
canvas.bind('<Configure>',lambda e:canvas.bbox('all'))


slider = tk.Frame(canvas)
canvas.create_window((0, 0), window=slider, anchor=tk.NW)
root.mainloop()