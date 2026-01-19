import tkinter as tk


class RegionSelector:
    def __init__(self):
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.selection = None

        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-alpha", 0.3)
        self.root.configure(background="black")
        self.root.attributes("-topmost", True)

        self.canvas = tk.Canvas(
            self.root,
            cursor="cross",
            bg="black",
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.rect = None

        self._bind_events()

    def _bind_events(self):
        self.canvas.bind("<ButtonPress-1>", self._on_mouse_down)
        self.canvas.bind("<B1-Motion>", self._on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_mouse_up)
        self.root.bind("<Escape>", self._cancel)

    def _on_mouse_down(self, event):
        self.start_x = self.canvas.winfo_pointerx()
        self.start_y = self.canvas.winfo_pointery()

        self.rect = self.canvas.create_rectangle(
            self.start_x,
            self.start_y,
            self.start_x,
            self.start_y,
            outline="red",
            width=2
        )

    def _on_mouse_drag(self, event):
        cur_x = self.canvas.winfo_pointerx()
        cur_y = self.canvas.winfo_pointery()

        self.canvas.coords(
            self.rect,
            self.start_x,
            self.start_y,
            cur_x,
            cur_y
        )

    def _on_mouse_up(self, event):
        self.end_x = self.canvas.winfo_pointerx()
        self.end_y = self.canvas.winfo_pointery()

        left = min(self.start_x, self.end_x)
        top = min(self.start_y, self.end_y)
        width = abs(self.end_x - self.start_x)
        height = abs(self.end_y - self.start_y)

        if width > 0 and height > 0:
            self.selection = (left, top, width, height)

        self.root.destroy()

    def _cancel(self, event=None):
        self.selection = None
        self.root.destroy()

    def select(self):
        self.root.mainloop()
        return self.selection
