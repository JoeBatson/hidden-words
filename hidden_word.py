import tkinter
from tkinter import messagebox
import random
from PIL import Image
import os


class App(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("Word Pizza")
        self.configure(padx=10, pady=10, background="#FFC300")
        self.window_position()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.started = False
        self.canvas_width = 300
        self.canvas_height = 100
        self.word = ""
        self.hd = []
        self.letter_buttons = {}
        self.wrong_answers = 0
        self.reactions = ["\n  😁1","\n  😊2","\n  😐3","\n  🤨4","\n  😥5","\n  😕6","\n😭"]
        self.dialog = ["It's Okay", "Not a problem", "Hm Okay", "Hold on, Let's focus", "Only two tries left", "Oh no this is your last chance", "game over"]
        self.nextReaction = iter(self.reactions)
        self.nextDialog = iter(self.dialog)
        self.change_reaction = "\n🙂"
        self.change_dialog = "You get 7 tries to guess the word"
        self.box = None
        self.game_image()
        self.hidden_word_screen()
        self.keyboard()
        self.start_quit()
        self.mainloop()

    def window_position(self):
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        win_width = 800
        win_height = 770
        x = (screen_width - win_width) // 2
        y = (screen_height - win_height) // 2 - 40
        self.geometry(f"{win_width}x{win_height}+{x}+{y}")

    def game_image(self):
        frame_game_image = tkinter.Frame(self, background="#FFC300")
        frame_game_image.grid(row=0, column=0, sticky="news")
        frame_game_image.grid_columnconfigure(0, weight=1)
        frame_game_image.grid_rowconfigure(0, weight=0)
        self.image_box = tkinter.Canvas(frame_game_image, width=300, height=450, bg="coral")
        self.image_box.grid(row=0, column=0, sticky="news")
        self.image_box.create_text(385, 100, text=self.change_reaction, font=("Arial", 70), fill="black", tags="emoji")
        self.image_box.create_text(385, 300, text=self.change_dialog, font=("Arial", 20), fill="black", tags="emoji")

    def get_word(self): #random word choice

        file_path = os.path.join(os.path.dirname(__file__), "game_word_list.txt")
        with open(file_path, "r") as file:
        # with open(r"C:\\Users\\blues\\Documents\\python_practice\\word_pizza_game\\game_word_list.txt", "r") as file:
            return random.choice([words.strip() for words in file])
        
    def start_game(self):
        self.started = True
        self.wrong_answers = 0
        self.nextReaction = iter(self.reactions)
        self.nextDialog = iter(self.dialog)
        self.change_reaction = "\n😀"
        self.change_dialog = "Let's Go!"
        self.word = self.get_word()  
        self.hd = ["_"] * len(self.word)
        self.update_canvas()
        for button in self.letter_buttons.values():
            button.config(state="normal", bg="#FFE500")


    def hidden_word_screen(self):
        frame_hidden_word = tkinter.Frame(self, background="#FFC300")
        frame_hidden_word.grid(row=1, column=0, sticky="news")
        frame_hidden_word.grid_rowconfigure(1, weight=1)
        frame_hidden_word.grid_columnconfigure(0, weight=1)
        self.box = tkinter.Canvas(frame_hidden_word, width=self.canvas_width, height=self.canvas_height, background="coral")
        self.box.grid(row=0, column=0, sticky="news", padx=0, pady=10)

        
    def use_key(self, letter):
        if not self.started:
            return
        for idx, char in enumerate(self.word):
            if char.upper() == letter.upper():
                self.hd[idx] = char.upper()

        if "_" not in self.hd:
            self.change_reaction = "\n😁"
            self.change_dialog = "WELL DONE!"
            self.update_canvas()
            return
        
        if letter.upper() not in self.word.upper():
            self.wrong_answers += 1
            self.change_reaction = next(self.nextReaction)
            self.change_dialog = next(self.nextDialog)
            self.image_box.delete("emoji")
            self.image_box.create_text(385, 100, text=self.change_reaction, font=("Arial", 70), fill="black", tags="emoji")
            self.image_box.create_text(385, 300, text=self.change_dialog, font=("Arial", 20), fill="black", tags="emoji")

        if self.wrong_answers == 7:
            self.box.delete("word")
            self.box.create_text(self.canvas_width + 70, self.canvas_height/2,
                            text=self.word, font=("Arial", 40), fill="black",
                            anchor="center", tags="word")
            return
            
        self.update_canvas()
            
        button = self.letter_buttons.get(letter.upper())
        if button:
            button.config(state="disabled", bg="lime")

    def update_canvas(self):
        display = " ".join(self.hd)
        self.image_box.delete("emoji")
        self.box.delete("word")
        self.image_box.create_text(385, 100, text=self.change_reaction, font=("Arial", 70), fill="black", tags="emoji")
        self.image_box.create_text(385, 300, text=self.change_dialog, font=("Arial", 20), fill="black", tags="emoji")
        self.box.create_text(self.canvas_width + 70, self.canvas_height/2,
                            text=display, font=("Arial", 40), fill="black",
                            anchor="center", tags="word")

    def keyboard(self): #creates keyboard 
        keys = [["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"], 
                ["N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]]
        keyb_frame = tkinter.LabelFrame(self, text="Keyboard", padx=10, pady=10, bd=5, background="#FFC300")
        keyb_frame.grid(row=2, column=0, sticky="we")
        for j in range(len(keys[0])):
            keyb_frame.grid_columnconfigure(j, weight=1)

        for i, key_row in enumerate(keys): #keyboard clicks
            for j, key in enumerate(key_row):
                btn = tkinter.Button(keyb_frame, text=key, width=4, height=2, font="System", command=lambda key=key:self.use_key(key), background="#FFE500", activebackground="#FFE500")
                btn.grid(row=i, column=j, sticky="we")
                self.letter_buttons[key] = btn

    def confirm_quit(self):
        answer = messagebox.askyesno("Quit Game", "Are you sure you want to quit?")
        if answer:
            self.destroy()

    def start_quit(self):
        startQuitFrame = tkinter.Frame(self, padx=10, pady=10, background="#FFC300")
        startQuitFrame.grid(row=3, column=0, sticky="we")

        startQuitFrame.grid_columnconfigure(0, weight=1)
        startQuitFrame.grid_columnconfigure(1, weight=1)

        startButton = tkinter.Frame(startQuitFrame, background="#FFC300")
        startButton.grid(row=0, column=0, sticky="we")
        startButton.grid_rowconfigure(0, weight=1)
        startButton.grid_columnconfigure(0, weight=1)

        quitButton = tkinter.Frame(startQuitFrame)
        quitButton.grid(row=0, column=1)

        tkinter.Button(startButton, text="Start Game", width=10, height=0, padx=10, command=self.start_game, background="#FFE500").grid(row=0, column=0)
        tkinter.Button(quitButton, text="Quit", width=10, height=0, padx=10, command=self.confirm_quit, background="#FFE500").grid(row=0, column=0)


if __name__ == "__main__":
    app = App()
