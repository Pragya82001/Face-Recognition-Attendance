import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime
from tkinter import *
from playsound import playsound

images_dataset = []
names = []
i = 0

def create_data():
    path = "image_dataset"
    list_of_images = os.listdir(path)
    print(list_of_images)
    for cl in list_of_images:
        curr_image = cv2.imread(f'{path}/{cl}')
        images_dataset.append(curr_image)
        names.append(os.path.splitext(cl)[0])
    print(names)

def find_encoding(images):
    encode_list = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encode_list.append(encode)
    return encode_list

def mark_attendance(name):
    with open("attendance sheet.csv", "r+") as f:
        existing_data = f.readlines()
        existing_names = []
        for line in existing_data:
            entry = line.split(',')
            existing_names.append(entry[0])
        if name not in existing_names:
            t_date = datetime.now()
            date_string = t_date.strftime("%d/%m/%y")
            now = datetime.now()
            time_string = now.strftime("%H:%M:%S")
            f.writelines(f'\n{name},yes,{date_string},{time_string}')

def delete_data():
    with open("attendance sheet.csv", "r+") as f:
        f.seek(22)
        f.truncate()
    message.configure(text="DATA CLEARED!")

def main():
    global i
    if (i < 1):
        create_data()
        i += 1
    print("encoding of images started!")
    known_encodings_list = find_encoding(images_dataset)
    print("encoding complete")
    cap = cv2.VideoCapture(0)
    count = 0
    while True:
        if count >= 8:
            break
        count += 1
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.20, 0.20)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        currFaceLocation = face_recognition.face_locations(imgS)
        currFrameFaceEncoding = face_recognition.face_encodings(imgS, currFaceLocation)

        for encodeFace, faceLoc in zip(currFrameFaceEncoding, currFaceLocation):
            matches = face_recognition.compare_faces(known_encodings_list, encodeFace)
            faceDis = face_recognition.face_distance(known_encodings_list, encodeFace)
            print(faceDis)
            match_index = np.argmin(faceDis)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*5, x2*5, y2*5, x1*5
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)

            if matches[match_index]:
                name = names[match_index]
                cv2.putText(img, name.upper(), (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                mark_attendance(name)
                message.configure(text="WELCOME " + name.upper() +" ATTENDANCE MARKED!")
            else:
                cv2.putText(img, "UNKNOWN", (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                message.configure(text="YOU ARE NOT IN OUR RECORDS!")

        cv2.imshow('webcam', img)
        cv2.waitKey(1)

    cv2.destroyAllWindows()

def open_file():
    os.startfile("attendance sheet.csv")

#--------Tkinter Interface------------#
window = Tk()
window.title("Attendance")
window.geometry('1000x520')
window.configure(background='#fefae0')
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
window.iconbitmap('icon/icon.ico')

def btn1_hover(event):
    btn1["bg"] = "#e1f0e5"
def btn1_hover_leave(event):
    btn1["bg"] = "#ccd5ae"

def btn2_hover(event):
    btn2["bg"] = "#e1f0e5"
def btn2_hover_leave(event):
    btn2["bg"] = "#d6ccc2"

def clear_btn_hover(event):
    clear_btn["bg"] = "#e1f0e5"
def clear_btn_hover_leave(event):
    clear_btn["bg"] = "#dda15e"

def exit_btn_hover(event):
    exit_btn["bg"] = "#e1f0e5"
def exit_btn_hover_leave(event):
    exit_btn["bg"] = "#d4151c"

def start():
    main()
    playsound("sounds/sound.mp3")

heading = Label(window, text="WELCOME MARK YOUR ATTENDANCE", bg="#d4a373", fg="black", width=57, height=3, font=('Times New Roman', 18, 'bold'))
heading.place(x=95, y=20)

lbl = Label(window, text="MESSAGE:-", width=20, fg="black", bg="#faedcd", height=3, font=('Times New Roman', 15, ' bold '))
lbl.place(x=95, y=200)

message = Label(window, text="", fg="black", bg="#faedcd", activeforeground = "cyan", width=41, height=3, font=('Time New Roman', 15, ' bold '))
message.place(x=400, y=200)

btn1 = Button(window, text="MARK ATTENDANCE", command=start, fg="black", bg="#ccd5ae", width=18, height=2, activebackground="cyan", font=('Times New Roman', 15, ' bold '))
btn1.place(x=95, y=380)
btn1.bind("<Enter>", btn1_hover)
btn1.bind("<Leave>", btn1_hover_leave)

btn2 = Button(window, text="ATTENDANCE SHEET", command=open_file, fg="black", bg="#d6ccc2", width=18, height=2, activebackground="cyan", font=('Times New Roman', 15, ' bold '))
btn2.place(x=350, y=380)
btn2.bind("<Enter>", btn2_hover)
btn2.bind("<Leave>", btn2_hover_leave)

clear_btn = Button(window, text="CLEAR", command=delete_data, fg="black", bg="#dda15e", width=12, height=2, activebackground="cyan", font=('Times New Roman', 15, ' bold '))
clear_btn.place(x=602, y=380)
clear_btn.bind("<Enter>", clear_btn_hover)
clear_btn.bind("<Leave>", clear_btn_hover_leave)

exit_btn = Button(window, text="EXIT", command=window.quit, fg="black", bg="#d4151c", width=8, height=2, activebackground="cyan", font=('Times New Roman', 15, ' bold '))
exit_btn.place(x=785, y=380)
exit_btn.bind("<Enter>", exit_btn_hover)
exit_btn.bind("<Leave>", exit_btn_hover_leave)

window.mainloop()
