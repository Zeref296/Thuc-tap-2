import tkinter as tk
from tkinter import messagebox

class AVLNode:
    def __init__(self, key, data, left=None, right=None):
        self.key = key
        self.data = data
        self.left = left
        self.right = right
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    def height(self, node):
        if not node:
            return 0
        return node.height

    def balance(self, node):
        if not node:
            return 0
        return self.height(node.left) - self.height(node.right)

    def rotate_right(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        y.height = 1 + max(self.height(y.left), self.height(y.right))
        x.height = 1 + max(self.height(x.left), self.height(x.right))

        return x

    def rotate_left(self, x):
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        x.height = 1 + max(self.height(x.left), self.height(x.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))

        return y

    def insert(self, node, key, data):
        if not node:
            return AVLNode(key, data)

        if key < node.key:
            node.left = self.insert(node.left, key, data)
        elif key > node.key:
            node.right = self.insert(node.right, key, data)
        else:
            return node

        node.height = 1 + max(self.height(node.left), self.height(node.right))

        balance = self.balance(node)

        # Left Heavy
        if balance > 1:
            if key < node.left.key:
                return self.rotate_right(node)
            else:
                node.left = self.rotate_left(node.left)
                return self.rotate_right(node)

        # Right Heavy
        if balance < -1:
            if key > node.right.key:
                return self.rotate_left(node)
            else:
                node.right = self.rotate_right(node.right)
                return self.rotate_left(node)

        return node

class CinemaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Đặt vé rạp phim")

        self.num_halls = 6
        self.current_hall = 1

        # List to store the state of seats for each hall
        self.seat_states = [{} for _ in range(self.num_halls)]

        self.rows = 5
        self.cols = 10

        # Attribute to store seat buttons
        self.buttons = None

        self.create_gui()

    def create_gui(self):
        # Create the cinema screen (green area)
        self.screen_label = tk.Label(self.root, text="Màn hình", font=("Helvetica", 16), bg="green", fg="white")
        self.screen_label.grid(row=0, column=0, columnspan=self.cols, sticky="ew", padx=5, pady=5)

        # Create cinema hall buttons
        for hall_num in range(1, self.num_halls + 1):
            hall_button = tk.Button(self.root, text=f"Phòng {hall_num}", width=15, height=3,
                                    command=lambda hall_num=hall_num: self.switch_hall(hall_num), relief=tk.GROOVE)
            hall_button.grid(row=1, column=hall_num - 1, padx=5, pady=5)

        # Create the seat buttons
        self.create_seat_buttons()

    def create_seat_buttons(self):
        self.buttons = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        
        for i in range(self.rows):
            for j in range(self.cols):
                seat_number = j + 1 + (i * self.cols)
                seat_status = self.get_seat_status(seat_number)

                btn_text = f"Ghế {seat_number}\n{seat_status}"
                color = "gray" if seat_status == "Đã đặt" else "red"
                width = 15 if i == 0 or i >= self.rows - 4 else 10
                padx = 2 if i >= self.rows - 4 else 5

                self.buttons[i][j] = tk.Button(self.root, text=btn_text, width=width, height=3, bg=color,
                                               command=lambda i=i, j=j, seat_number=seat_number: self.toggle_seat(i, j, seat_number),
                                               relief=tk.GROOVE, borderwidth=3)
                
                self.buttons[i][j].grid(row=i + 2, column=j, padx=padx, pady=2)

    def switch_hall(self, hall_num):
        # Update the current hall
        self.current_hall = hall_num

        # Destroy the existing seat buttons
        for i in range(self.rows):
            for j in range(self.cols):
                self.buttons[i][j].destroy()

        # Recreate the seat buttons for the new hall
        self.create_seat_buttons()

    def toggle_seat(self, row, col, seat_number):
        seat_status = self.get_seat_status(seat_number)
        new_status = "Chưa đặt" if seat_status == "Đã đặt" else "Đã đặt"
        self.set_seat_status(seat_number, new_status)

        btn_text = f"Ghế {seat_number}\n{new_status}"
        color = "gray" if new_status == "Đã đặt" else "red"

        self.buttons[row][col].config(text=btn_text, bg=color)

    def get_seat_status(self, seat_number):
        return self.seat_states[self.current_hall - 1].get(seat_number, "Chưa đặt")

    def set_seat_status(self, seat_number, status):
        self.seat_states[self.current_hall - 1][seat_number] = status

if __name__ == "__main__":
    root = tk.Tk()
    app = CinemaApp(root)
    root.mainloop()
