from __future__ import annotations

APP_NAME     = "SnapText"
TOAST_TIMEOUT = 4  


def notify(title: str, message: str, error: bool = False) -> None:
    if error:
        _show_error_popup(title, message)
    else:
        _show_toast(title, message)

def _show_toast(title: str, message: str) -> None:

    try:
        from win10toast import ToastNotifier
        toaster = ToastNotifier()
        toaster.show_toast(
            title,
            message,
            duration=TOAST_TIMEOUT,
            threaded=True,     
            icon_path=None,      
        )
        return
    except Exception:
        pass

    try:
        from plyer import notification
        notification.notify(
            app_name=APP_NAME,
            title=title,
            message=message,
            timeout=TOAST_TIMEOUT,
        )
    except Exception:
        pass

def _show_error_popup(title: str, message: str) -> None:
    import threading
    threading.Thread(
        target=_error_popup_thread,
        args=(title, message),
        daemon=True,
    ).start()


def _error_popup_thread(title: str, message: str) -> None:
    try:
        import tkinter as tk

        root = tk.Tk()
        root.withdraw()

        win = tk.Toplevel(root)
        win.title("SnapText")
        win.resizable(False, False)
        win.attributes("-topmost", True)

        root.bell = lambda: None
        win.bell  = lambda: None

        try:
            cx = root.winfo_pointerx()
            cy = root.winfo_pointery()
        except Exception:
            cx, cy = 100, 100
        win.geometry(f"+{cx + 16}+{cy + 16}")

        header = tk.Frame(win, bg="#8B0000", padx=12, pady=8)
        header.pack(fill="x")
        tk.Label(header, text=f"✗  {title}", bg="#8B0000", fg="white",
                 font=("Segoe UI", 10, "bold")).pack(anchor="w")

        body = tk.Frame(win, bg="#2B2B2B", padx=16, pady=12)
        body.pack(fill="both")
        tk.Label(body, text=message, bg="#2B2B2B", fg="#E0E0E0",
                 font=("Segoe UI", 9), wraplength=280,
                 justify="left").pack(anchor="w")

        btn_frame = tk.Frame(win, bg="#2B2B2B", pady=8)
        btn_frame.pack(fill="x")
        tk.Button(btn_frame, text="OK", bg="#8B0000", fg="white",
                  font=("Segoe UI", 9, "bold"), relief="flat",
                  padx=20, pady=4, cursor="hand2",
                  command=lambda: _close(win, root)).pack()

        win.after(6000, lambda: _close(win, root))
        win.mainloop()
    except Exception:
        pass


def _close(win, root) -> None:
    try:
        win.destroy()
        root.destroy()
    except Exception:
        pass