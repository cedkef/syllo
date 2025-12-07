import tkinter as tk
from tkinter import ttk, messagebox
import random


class SylloGame:
    def __init__(self, root):
        self.root = root
        self.root.title("SYLLO - Word Puzzle Game")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')

        self.word = ['' for _ in range(1000)]
        self.def_ = ['' for _ in range(1000)]
        self.fwords = ['', '', '']
        self.fdefs = ['', '', '']
        self.entireblocks = []
        self.num_of_blocks = [0, 0, 0]

        self.load_words()
        self.setup_ui()
        self.new_game()

    def load_words(self):
        with open('words.txt', 'r') as fd:
            buf = fd.read()
            lines = buf.split('\n')
            a = 0
            for line in lines:
                if ':' in line and a < 1000:
                    colon = line.find(':')
                    self.word[a] = line[:colon].strip()[:19]
                    self.def_[a] = line[colon + 1:].strip()[:999]
                    a += 1

    def setup_ui(self):
        title_label = tk.Label(
            self.root,
            text="--- SYLLO ---",
            font=('Arial', 24, 'bold'),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        title_label.pack(pady=20)

        self.questions_frame = tk.Frame(self.root, bg='#34495e')
        self.questions_frame.pack(pady=10, padx=20, fill='both', expand=True)

        self.question_labels = []
        self.answer_entries = []

        for i in range(3):
            q_container = tk.Frame(self.questions_frame, bg='#34495e')
            q_container.pack(pady=10, fill='x')

            q_label = tk.Label(
                q_container,
                text=f"{i + 1}. Definition here",
                font=('Arial', 12),
                bg='#34495e',
                fg='#ecf0f1',
                wraplength=600,
                justify='left'
            )
            q_label.pack(anchor='w', padx=10)
            self.question_labels.append(q_label)

            entry = tk.Entry(
                q_container,
                font=('Arial', 12),
                bg='#ecf0f1',
                fg='#2c3e50',
                width=40
            )
            entry.pack(anchor='w', padx=10, pady=5)
            self.answer_entries.append(entry)

        blocks_frame = tk.Frame(self.root, bg='#2c3e50')
        blocks_frame.pack(pady=10)

        tk.Label(
            blocks_frame,
            text="Blocks:",
            font=('Arial', 14, 'bold'),
            bg='#2c3e50',
            fg='#ecf0f1'
        ).pack()

        self.blocks_label = tk.Label(
            blocks_frame,
            text="",
            font=('Arial', 16),
            bg='#34495e',
            fg='#3498db',
            padx=20,
            pady=10
        )
        self.blocks_label.pack(pady=5)

        button_frame = tk.Frame(self.root, bg='#2c3e50')
        button_frame.pack(pady=20)

        tk.Button(
            button_frame,
            text="Submit",
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            padx=20,
            pady=10,
            command=self.check_answers
        ).pack(side='left', padx=5)

        tk.Button(
            button_frame,
            text="show answers",
            font=('Arial', 12, 'bold'),
            bg='#e67e22',
            fg='white',
            padx=20,
            pady=10,
            command=self.show_answers
        ).pack(side='left', padx=5)

        tk.Button(
            button_frame,
            text="New Game",
            font=('Arial', 12, 'bold'),
            bg='#3498db',
            fg='white',
            padx=20,
            pady=10,
            command=self.new_game
        ).pack(side='left', padx=5)

    def split(self, fwords):
        blocks = []
        length = len(fwords)
        a = 0

        while a < length:
            block = 2 + random.randint(0, 1)
            if a + block > length:
                block = length - a
            blocks.append(fwords[a:a + block])
            a += block

        return blocks

    def new_game(self):
        for entry in self.answer_entries:
            entry.delete(0, tk.END)
            entry.config(bg='#ecf0f1')

        for i in range(3):
            randomnum = random.randint(0, 999)
            self.fwords[i] = self.word[randomnum]
            self.fdefs[i] = self.def_[randomnum]

        self.entireblocks = []
        blockcounter = 0

        for i in range(3):
            blocks = self.split(self.fwords[i])
            self.num_of_blocks[i] = len(blocks)

            for j in range(len(blocks)):
                self.entireblocks.append(blocks[j])
                blockcounter += 1

        for i in range(blockcounter):
            j = random.randint(0, blockcounter - 1)
            temp = self.entireblocks[i]
            self.entireblocks[i] = self.entireblocks[j]
            self.entireblocks[j] = temp

        for i in range(3):
            blanks = ""
            for j in range(self.num_of_blocks[i]):
                blanks += "_/"
            self.question_labels[i].config(
                text=f"{i + 1}. {self.fdefs[i]} : {blanks}"
            )

        blocks_text = ""
        for i in range(len(self.entireblocks)):
            blocks_text += self.entireblocks[i] + "/"
        self.blocks_label.config(text=blocks_text)

    def check_answers(self):
        a = self.answer_entries[0].get().strip()
        b = self.answer_entries[1].get().strip()
        c = self.answer_entries[2].get().strip()

        num_of_ans = 0

        if a == self.fwords[0]:
            self.answer_entries[0].config(bg='#2ecc71')
            num_of_ans += 1
        else:
            self.answer_entries[0].config(bg='#e74c3c')

        if b == self.fwords[1]:
            self.answer_entries[1].config(bg='#2ecc71')
            num_of_ans += 1
        else:
            self.answer_entries[1].config(bg='#e74c3c')

        if c == self.fwords[2]:
            self.answer_entries[2].config(bg='#2ecc71')
            num_of_ans += 1
        else:
            self.answer_entries[2].config(bg='#e74c3c')

        if num_of_ans == 3:
            messagebox.showinfo("Result", "All correct!")
        else:
            messagebox.showinfo("Result", f"{num_of_ans} correct")

    def show_answers(self):
        messagebox.showinfo("answers", f"{self.fwords[0]}, {self.fwords[1]}, {self.fwords[2]}")


def main():
    root = tk.Tk()
    app = SylloGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()