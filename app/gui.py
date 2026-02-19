import tkinter as tk
from PIL import ImageTk
import threading
import queue
import sys


class MatrixStream:
    """File-like object that redirects writes to the MatrixWindow."""

    def __init__(self, write_callback):
        self._write = write_callback

    def write(self, text):
        self._write(text)

    def flush(self):
        pass


class MatrixWindow:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GREAT MEN INDEX")
        self.root.configure(bg="black")
        self.root.geometry("900x650")

        self._queue = queue.Queue()
        self._images = []  # keep references to prevent garbage collection
        self._target_func = None

        title = tk.Label(
            self.root,
            text="[ GREAT MEN INDEX ]",
            bg="black",
            fg="#00FF00",
            font=("Courier", 16, "bold"),
        )
        title.pack(pady=(15, 2))

        sep = tk.Label(
            self.root,
            text="=" * 70,
            bg="black",
            fg="#005500",
            font=("Courier", 10),
        )
        sep.pack()

        frame = tk.Frame(self.root, bg="black")
        frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=(10, 0))

        scrollbar = tk.Scrollbar(
            frame,
            bg="#003300",
            troughcolor="black",
            activebackground="#00FF00",
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._text = tk.Text(
            frame,
            bg="black",
            fg="#00FF00",
            font=("Courier", 11),
            wrap=tk.WORD,
            state=tk.DISABLED,
            insertbackground="#00FF00",
            selectbackground="#003300",
            selectforeground="#00FF00",
            yscrollcommand=scrollbar.set,
            borderwidth=0,
            highlightthickness=0,
        )
        self._text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self._text.yview)

        # Input bar
        input_frame = tk.Frame(self.root, bg="#001100")
        input_frame.pack(fill=tk.X, padx=12, pady=10)

        prompt = tk.Label(
            input_frame,
            text="> ",
            bg="#001100",
            fg="#00FF00",
            font=("Courier", 11, "bold"),
        )
        prompt.pack(side=tk.LEFT)

        self._entry = tk.Entry(
            input_frame,
            bg="#001100",
            fg="#00FF00",
            font=("Courier", 11),
            insertbackground="#00FF00",
            relief=tk.FLAT,
            highlightthickness=1,
            highlightcolor="#00FF00",
            highlightbackground="#003300",
        )
        self._entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
        self._entry.bind("<Return>", self._handle_command)
        self._entry.focus()

    def _handle_command(self, _event=None):
        cmd = self._entry.get().strip().lower()
        self._entry.delete(0, tk.END)

        if cmd == "exit":
            self.root.destroy()
        elif cmd == "next":
            self._queue.put(("write", "\n" + "=" * 70 + "\n\n"))
            thread = threading.Thread(
                target=lambda: self._target_func(self), daemon=True
            )
            thread.start()
        else:
            self._queue.put(("write", f"Command not recognized: '{cmd}'\n"))

    def write(self, text):
        self._queue.put(("write", text))

    def set_mark(self, name):
        self._queue.put(("set_mark", name))

    def delete_from_mark(self, name):
        self._queue.put(("delete_from_mark", name))

    def show_image(self, pil_image):
        self._queue.put(("show_image", pil_image))

    def _process_queue(self):
        try:
            while True:
                item = self._queue.get_nowait()
                cmd, value = item
                self._text.configure(state=tk.NORMAL)
                if cmd == "write":
                    self._text.insert(tk.END, value)
                    self._text.see(tk.END)
                elif cmd == "set_mark":
                    self._text.mark_set(value, tk.END)
                    self._text.mark_gravity(value, tk.LEFT)
                elif cmd == "delete_from_mark":
                    self._text.delete(value, tk.END)
                elif cmd == "show_image":
                    photo = ImageTk.PhotoImage(value)
                    self._images.append(photo)
                    self._text.image_create(tk.END, image=photo)
                    self._text.insert(tk.END, "\n\n")
                    self._text.see(tk.END)
                self._text.configure(state=tk.DISABLED)
        except queue.Empty:
            pass
        self.root.after(50, self._process_queue)

    def run(self, target_func):
        self._target_func = target_func
        sys.stdout = MatrixStream(self.write)
        thread = threading.Thread(target=lambda: target_func(self), daemon=True)
        thread.start()
        self._process_queue()
        self.root.mainloop()
