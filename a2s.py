import speech_recognition as sr
import pyttsx3 as tr
import tkinter
from PIL import Image, ImageTk

r = sr.Recognizer()
engine = tr.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', 125)
images = []


def load_images():
    letter_list = []
    for i in range(65, 91):
        letter_list.append(chr(i))

    for letters in letter_list:
        name = "letters/{}.jpg".format(letters)
        image = ImageTk.PhotoImage(Image.open(name))
        images.append((letters, image,))
    sp_img = ImageTk.PhotoImage(Image.open("letters/sp.jpg"))
    images.append((" ", sp_img))


with sr.Microphone() as src:
    while True:
        r.adjust_for_ambient_noise(src)
        print("say something")
        audio = r.listen(src)
        try:
            text = r.recognize_google(audio)
            # text = "hello everyone i am a good student"
            if text == "shutdown":
                engine.say("Goodbye.")
                engine.runAndWait()
                break
            else:
                win = tkinter.Tk()
                win.title("Sign")
                win.geometry("720x1280")
                load_images()

                def create(event):
                    sign_canvas.config(scrollregion=sign_canvas.bbox('all'), width=1300, height=650,
                                       yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)


                print("said this  :  " + text)

                frame = tkinter.Frame(win, height=650, width=1300, relief="raised", borderwidth=2)
                frame.grid(row=1, column=1)

                sign_canvas = tkinter.Canvas(frame, relief="sunken", height=650, width=1300)
                sign_canvas.grid(row=0, column=0)
                window = tkinter.Frame(sign_canvas)
                window.bind('<Configure>', create)
                sign_canvas.create_window((0, 0), window=window, anchor="nw")

                # Scrollbars
                y_scroll = tkinter.Scrollbar(win, orient=tkinter.VERTICAL, command=sign_canvas.yview)
                y_scroll.grid(row=1, column=0, sticky="ns")
                x_scroll = tkinter.Scrollbar(win, orient=tkinter.HORIZONTAL, command=sign_canvas.xview)
                x_scroll.grid(row=0, column=1, sticky="ew")

                text = text.upper()
                x = [word for j in text.split() for word in (j, " ")][:-1]

                row = 0
                ct = 0
                col = 0
                for i in range(0,len(x)):

                    if len(x[i])+ct <= 16:
                        ct = len(x[i])+ct
                        if i+1 < len(x) and x[i] == ' ' and len(x[i+1])+ct >16:
                            continue

                        for letter in x[i]:
                            for char, img in images:
                                if char == letter:
                                    tkinter.Label(window, image=img, relief="raised").grid(row=row, column=col, padx=2,
                                                                                           pady=2)
                                    col += 1
                                    continue
                    else:
                        ct = 0
                        col = 0
                        row += 1
                        if x[i] == " ":
                            continue
                        ct += len(x[i])
                        for letter in x[i]:
                            for char, img in images:
                                if char == letter:
                                    tkinter.Label(window, image=img, relief="raised").grid(row=row, column=col, padx=2,
                                                                                           pady=2)
                                    col += 1
                                    continue
                win.mainloop()
                images.clear()
        except sr.UnknownValueError:
            engine.say("I'm sorry. I couldn't catch that.")
            engine.runAndWait()
        except sr.RequestError as e:
            print("Could not request result from google: {}".format(e))
