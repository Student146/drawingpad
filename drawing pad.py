import tkinter
from tkinter import *
from tkinter import ttk
from PIL import ImageGrab
from io import BytesIO
import win32clipboard


class MyApplication(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        canvas_width = 700
        canvas_height = 350
        global circle
        global rectangle2
        global pen_color
        circle = 0
        rectangle2 = 0
        pen_color = "#000000"

        def send_to_clipboard(clip_type, data):
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(clip_type, data)
            win32clipboard.CloseClipboard()

        def create_entry(event):
            self.update()
            entry = tkinter.Entry(cv, borderwidth=0)
            width = entry.winfo_width()
            x1, y1 = event.x, event.y
            cv.create_window(x1 + 60, y1, window=entry)
            entry.focus_set()
            print(width)

        def button_text_clicked():
            cv.unbind('<Button-1>')
            cv.bind('<Button-1>', create_entry)


        def change_pen_color_red():
            global pen_color
            pen_color = "#FF0000"

        def change_pen_color_black():
            global pen_color
            pen_color = "#000000"

        def change_pen_color_green():
            global pen_color
            pen_color = "#00fe00"

        def change_pen_color_blue():
            global pen_color
            pen_color = "#0000fe"

        def unbind_every():
            cv.unbind('<B1-Motion>')
            cv.unbind('<Motion>')
            cv.unbind('<Button-1>')

        def paint(event):
            global pen_color
            x1, y1 = (event.x - 3), (event.y - 3)
            x2, y2 = (event.x + 3), (event.y + 3)
            cv.create_oval(x1, y1, x2, y2, fill=pen_color, outline=pen_color)

        def erase(event):
            global circle
            global rectangle2
            cv.delete(circle)
            cv.delete(rectangle2)
            python_white = "#FFFFFF"
            python_black = "#000000"
            x1, y1 = (event.x - 20), (event.y - 20)
            x2, y2 = (event.x + 20), (event.y + 20)
            cv.create_oval(x1, y1, x2, y2, fill=python_white, outline=python_white)
            rectangle2 = cv.create_rectangle(x1, y1, x2, y2, fill=python_white, outline=python_black)

        def draw():
            unbind_every()
            global circle
            cv.delete(circle)
            self.config(cursor="")
            cv.bind("<B1-Motion>", paint)
            cv.unbind("<Motion>")

        def eraser():
            unbind_every()
            self.config(cursor="circle")
            cv.bind("<B1-Motion>", erase)
            cv.bind("<Motion>", motion)

        def getter():
            global circle
            cv.delete(circle)
            self.update()
            width = cv.winfo_width()
            height = cv.winfo_height()
            x = cv.winfo_rootx()
            y = cv.winfo_rooty()

            x1 = x + width
            y1 = y + height
            print((x, y, x1, y1))
            image = ImageGrab.grab(bbox=(x * 1.5, y * 1.5, x1 * 1.5, y1 * 1.5))
            image.show()
            output = BytesIO()
            image.convert("RGB").save(output, "BMP")
            data = output.getvalue()[14:]
            output.close()
            send_to_clipboard(win32clipboard.CF_DIB, data)

        def motion(event):
            x1, y1 = event.x - 20, event.y - 20
            x2, y2 = event.x + 20, event.y + 20
            global rectangle2
            global circle

            cv.delete(circle)  # to refresh the circle each motion
            cv.delete(rectangle2)

            circle = cv.create_rectangle(x1, y1, x2, y2,fill='#FFFFFF', outline="black")

        self.geometry("+200+200")
        self.title("Drawing pad")

        cv = Canvas(self, width=canvas_width, height=canvas_height, background="#FFFFFF")
        cv.pack(expand=YES, fill=BOTH)
        cv.bind("<B1-Motion>", paint)

        button_done = ttk.Button(self, text="Done", command=lambda: getter())
        button_done.pack(side=TOP)

        button_pen = ttk.Button(self, text="Pen", command=lambda: draw())
        button_pen.pack()

        button_eraser = ttk.Button(self, text="Eraser", command=lambda: eraser())
        button_eraser.pack()

        button_text = ttk.Button(text="Text", command=button_text_clicked)
        button_text.pack()

        pen_color_label = ttk.Label(self, text="Pen color:       ")
        pen_color_label.pack(side=LEFT)

        red_color_button = tkinter.Button(self, background="#FF0000", command=change_pen_color_red, width=2)
        red_color_button.pack(side=LEFT)

        green_color_button = tkinter.Button(self, background="#00fe00", command=change_pen_color_green, width=2)
        green_color_button.pack(side=LEFT)

        blue_color_button = tkinter.Button(self, background="#0000fe", command=change_pen_color_blue, width=2)
        blue_color_button.pack(side=LEFT)

        black_color_button = tkinter.Button(self, background="#000000", command=change_pen_color_black, width=2)
        black_color_button.pack(side=LEFT)

if __name__ == "__main__":
    app = MyApplication()
    app.mainloop()

