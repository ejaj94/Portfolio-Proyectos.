import customtkinter as ctk
from typing import List

class CTkAutocomplete(ctk.CTkEntry):
    def __init__(self, master, suggestions: List[str], **kwargs):
        super().__init__(master, **kwargs)
        self.suggestions = suggestions
        self.bind("<KeyRelease>", self._on_key_release)
        self.bind("<FocusOut>", self._on_focus_out)
        self.bind("<FocusIn>", self._on_key_release)
        self._dropdown = None

    def _on_key_release(self, event):
        if event and event.keysym in ("Up", "Down", "Return", "Escape", "Tab"):
            return
            
        typed = self.get().lower()
        if not typed:
            self._close_dropdown()
            return
            
        matches = [s for s in self.suggestions if typed in s.lower()]
        if matches:
            self._show_dropdown(matches)
        else:
            self._close_dropdown()

    def _show_dropdown(self, matches: List[str]):
        if self._dropdown is None:
            self._dropdown = ctk.CTkToplevel(self)
            self._dropdown.overrideredirect(True)
            self._dropdown.attributes("-topmost", True)
            self._dropdown_frame = ctk.CTkScrollableFrame(self._dropdown, fg_color="#2b2b2b", corner_radius=0)
            self._dropdown_frame.pack(expand=True, fill="both")
            
        for child in self._dropdown_frame.winfo_children():
            child.destroy()
            
        for match in matches[:8]:
            btn = ctk.CTkButton(
                self._dropdown_frame, 
                text=match, 
                fg_color="transparent",
                hover_color="#3a3a3a",
                text_color="#ffffff",
                anchor="w",
                corner_radius=0,
                command=lambda m=match: self._select_suggestion(m)
            )
            btn.pack(fill="x", padx=0, pady=0)
            
        # Update geometry
        self.update_idletasks()
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height()
        width = self.winfo_width()
        height = min(len(matches) * 32 + 10, 200)
        
        self._dropdown.geometry(f"{width}x{height}+{x}+{y}")
        self._dropdown.deiconify()

    def _select_suggestion(self, match: str):
        self.delete(0, "end")
        self.insert(0, match)
        self._close_dropdown()

    def _close_dropdown(self):
        if self._dropdown is not None:
            self._dropdown.destroy()
            self._dropdown = None

    def _on_focus_out(self, event):
        self.after(200, self._close_dropdown)
