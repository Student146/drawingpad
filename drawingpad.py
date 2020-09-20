import tkinter
from tkinter import *
from tkinter import ttk
from PIL import ImageGrab
from io import BytesIO
import win32clipboard

canvas_width = 700
canvas_height = 350
rectangle1 = 0
rectangle2 = 0
pen_color = "#000000"
python_white = "#FFFFFF"
python_black = "#000000"


def send_to_clipboard(clip_type, data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()


def create_entry(event):
    root.update()
    entry = tkinter.Entry(cv, borderwidth=0)
    x1, y1 = event.x, event.y
    cv.create_window(x1 + 60, y1, window=entry)
    entry.focus_set()


def button_text_clicked():
    cv.unbind('<Button-1>')
    cv.bind('<Button-1>', create_entry)


def button_delete_clicked():
    cv.delete('all')


def change_pen_color(color):
    global pen_color
    pen_color = color


def unbind_every():
    cv.unbind('<B1-Motion>')
    cv.unbind('<Motion>')
    cv.unbind('<Button-1>')


def paint(event):
    x1, y1 = (event.x - 3), (event.y - 3)
    x2, y2 = (event.x + 3), (event.y + 3)
    cv.create_oval(x1, y1, x2, y2, fill=pen_color, outline=pen_color)


def erase(event):
    global rectangle1
    global rectangle2
    cv.delete(rectangle1)
    cv.delete(rectangle2)
    x1, y1 = (event.x - 20), (event.y - 20)
    x2, y2 = (event.x + 20), (event.y + 20)
    cv.create_oval(x1, y1, x2, y2, fill=python_white, outline=python_white)
    rectangle2 = cv.create_rectangle(x1, y1, x2, y2, fill=python_white, outline=python_black)


def draw():
    unbind_every()
    global rectangle1
    cv.delete(rectangle1)
    root.config(cursor="")
    cv.bind("<B1-Motion>", paint)
    cv.unbind("<Motion>")


def eraser():
    unbind_every()
    root.config(cursor="circle")
    cv.bind("<B1-Motion>", erase)
    cv.bind("<Motion>", motion)


def getter():
    global rectangle1
    cv.delete(rectangle1)
    root.update()
    width = cv.winfo_width()
    height = cv.winfo_height()
    x = cv.winfo_rootx()
    y = cv.winfo_rooty()

    x1 = x + width
    y1 = y + height
    print((x, y, x1, y1))
    image = ImageGrab.grab(bbox=(x * 1.25, y * 1.25, x1 * 1.25, y1 * 1.25))
    output = BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()
    send_to_clipboard(win32clipboard.CF_DIB, data)


def motion(event):
    x1, y1 = event.x - 20, event.y - 20
    x2, y2 = event.x + 20, event.y + 20
    global rectangle2
    global rectangle1

    cv.delete(rectangle1)  # to refresh the circle each motion
    cv.delete(rectangle2)

    rectangle1 = cv.create_rectangle(x1, y1, x2, y2, fill='#FFFFFF', outline="black")


root = Tk()
root.geometry("+200+200")
root.title("Drawing pad")

cv = Canvas(width=canvas_width, height=canvas_height, background="#FFFFFF")
cv.pack(expand=YES, fill=BOTH)
cv.bind("<B1-Motion>", paint)

button_done = ttk.Button(text="Done", command=lambda: getter())
button_done.pack(side=TOP)

button_pen = ttk.Button(text="Pen", command=lambda: draw())
button_pen.pack()

button_eraser = ttk.Button(text="Eraser", command=lambda: eraser())
button_eraser.pack()

button_text = ttk.Button(text="Text", command=button_text_clicked)
button_text.pack()

button_delete = ttk.Button(text='Clear all', command=button_delete_clicked)
button_delete.pack()

pen_color_label = ttk.Label(text="Pen color:       ")
pen_color_label.pack(side=LEFT)

red_color_button = tkinter.Button(background="#FF0000", command=lambda: change_pen_color("#FF0000"), width=2)
red_color_button.pack(side=LEFT)

green_color_button = tkinter.Button(background="#00fe00", command=lambda: change_pen_color("#00fe00"), width=2)
green_color_button.pack(side=LEFT)

blue_color_button = tkinter.Button(background="#0000fe", command=lambda: change_pen_color("#0000fe"), width=2)
blue_color_button.pack(side=LEFT)

black_color_button = tkinter.Button(background="#000000", command=lambda: change_pen_color("#000000"), width=2)
black_color_button.pack(side=LEFT)

root.mainloop()


