import tkinter as tk

class TooltipManager:
    def __init__(self, app):
        self.app = app
        self.active_tooltip = None
        self.after_id = None

    def show_tooltip(self, widget, text):
        try:
            # Always destroy any existing tooltip first
            self._destroy_tooltip()

            if not widget.winfo_exists():
                return

            x = widget.winfo_rootx() + widget.winfo_width() + 5
            y = widget.winfo_rooty() + widget.winfo_height() // 2

            tooltip = tk.Toplevel(widget)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{x}+{y}")
            
            label = tk.Label(
                tooltip,
                text=text,
                justify=tk.LEFT,
                relief=tk.SOLID,
                borderwidth=1,
                padx=5,
                pady=2,
                bg=self.app.ui_settings["listbox_bg"],
                fg=self.app.ui_settings["text_color"],
                font=(self.app.ui_settings["font_family"], 10)
            )
            label.pack()
            
            tooltip.lift()
            tooltip.attributes('-topmost', True)
            self.active_tooltip = tooltip

        except (tk.TclError, RuntimeError):
            self._destroy_tooltip()

    def hide_tooltip(self, event=None):
        self._destroy_tooltip()

    def _destroy_tooltip(self):
        if self.active_tooltip:
            try:
                self.active_tooltip.destroy()
            except tk.TclError:
                pass
            finally:
                self.active_tooltip = None
