from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
LANGUAGE_FONT = ("Ariel", 40, "italic")
WORD_FONT = ("Ariel", 60, "bold")

# Data csv
try:
    data_frame = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data_frame = pandas.read_csv("data/french_words.csv")
else:
    data_dictionary = data_frame.to_dict(orient="records")
    current_card = random.choice(data_dictionary)

def next_card():
    global timer, current_card
    window.after_cancel(timer)
    current_card = random.choice(data_dictionary)
    canvas.itemconfig(canvas_bg, image=front_card)
    canvas.itemconfig(title, text="French", fill="black")
    canvas.itemconfig(word, text=current_card["French"], fill="black")
    timer = window.after(ms=3000, func=flip_card)

def flip_card():
    global current_card
    canvas.itemconfig(canvas_bg, image=back_card)
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word, text=current_card["English"], fill="white")

def learned_word():
    global current_card, data_dictionary
    data_dictionary.remove(current_card)
    new_data = pandas.DataFrame(data_dictionary)
    new_data.to_csv("data/words_to_learn.csv", index=False)
    next_card()

window = Tk()
window.title("Quizzy")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

timer = window.after(3000, flip_card)

# images
front_card = PhotoImage(file="images/card_front.png")
back_card = PhotoImage(file="images/card_back.png")
right_logo = PhotoImage(file="images/right.png")
wrong_logo = PhotoImage(file="images/wrong.png")

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas_bg = canvas.create_image(400, 265, image=front_card)
title = canvas.create_text(400, 150, text="Title", font=LANGUAGE_FONT, fill="black")
word = canvas.create_text(400, 263, text="Word", font=WORD_FONT, fill="black")
canvas.grid(row=0, column=0, columnspan=2)

wrong = Button(image=wrong_logo, highlightthickness=0, highlightbackground=BACKGROUND_COLOR, command=next_card)
wrong.grid(row=1, column=0)
correct = Button(image=right_logo, highlightthickness=0, highlightbackground=BACKGROUND_COLOR, command=learned_word)
correct.grid(row=1, column=1)

window.mainloop()