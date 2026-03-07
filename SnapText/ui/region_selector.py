from __future__ import annotations

MIN_SIZE = 5 


def select_region() -> tuple[int, int, int, int] | None:
    import tkinter as tk  # local import — no Tk at module level

    result: dict[str, tuple[int, int, int, int] | None] = {"region": None}

    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-alpha", 0.25)
    root.attributes("-topmost", True)
    root.configure(background="black")
    root.title("SnapText — drag to select")

    canvas = tk.Canvas(root, cursor="cross", bg="black", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    state: dict = {"start_x": 0, "start_y": 0, "rect": None}

    def on_press(event: tk.Event) -> None:
        state["start_x"] = event.x_root
        state["start_y"] = event.y_root
        # Canvas-local coords for drawing the rectangle
        state["rect"] = canvas.create_rectangle(
            event.x, event.y, event.x, event.y,
            outline="red", width=2,
        )

    def on_drag(event: tk.Event) -> None:
        if state["rect"] is None:
            return
        # Translate screen coords back to canvas-local for drawing
        ox = state["start_x"] - root.winfo_rootx()
        oy = state["start_y"] - root.winfo_rooty()
        canvas.coords(state["rect"], ox, oy, event.x, event.y)

    def on_release(event: tk.Event) -> None:
        end_x = event.x_root
        end_y = event.y_root
        root.destroy()

        left = min(state["start_x"], end_x)
        top = min(state["start_y"], end_y)
        width = abs(end_x - state["start_x"])
        height = abs(end_y - state["start_y"])

        if width >= MIN_SIZE and height >= MIN_SIZE:
            result["region"] = (left, top, width, height)
        # else result["region"] stays None

    def on_escape(event: tk.Event) -> None: 
        root.destroy()

    canvas.bind("<ButtonPress-1>", on_press)
    canvas.bind("<B1-Motion>", on_drag)
    canvas.bind("<ButtonRelease-1>", on_release)
    root.bind("<Escape>", on_escape)

    root.mainloop()
    return result["region"]