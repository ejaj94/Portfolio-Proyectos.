"""
date_picker.py — Custom Native Date Range Picker with Calendar
==============================================================
"""
from __future__ import annotations

import calendar
from datetime import datetime
from typing import Callable, Dict, Any, Optional

import customtkinter as ctk

from gui.theme import Palette, Fonts
from services.i18n import I18nService


class CalendarView(ctk.CTkFrame):
    """A single calendar view (Year, Month, Days grid)."""
    
    def __init__(self, parent: ctk.CTkFrame, i18n: I18nService, initial_date: Optional[datetime] = None) -> None:
        super().__init__(parent, fg_color="transparent")
        self._i18n = i18n
        self.selected_date = initial_date or datetime.now()
        self.view_year = self.selected_date.year
        self.view_month = self.selected_date.month
        
        self.grid_columnconfigure(0, weight=1)
        
        # Header (Month / Year selectors)
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(0, 10))
        
        self.btn_prev = ctk.CTkButton(self.header_frame, text="<", width=30, command=self._prev_month, fg_color=Palette.ENTRY_BG, text_color=Palette.TEXT)
        self.btn_prev.pack(side="left")
        
        months = self._i18n.t("months").split(",")
        self.month_var = ctk.StringVar(value=months[self.view_month - 1])
        self.month_menu = ctk.CTkOptionMenu(
            self.header_frame, values=months, variable=self.month_var, command=self._on_month_change,
            width=100, fg_color=Palette.ENTRY_BG, button_color=Palette.ENTRY_BG, button_hover_color=Palette.SURFACE2
        )
        self.month_menu.pack(side="left", padx=5)
        
        years = [str(y) for y in range(datetime.now().year, 1950, -1)]
        self.year_var = ctk.StringVar(value=str(self.view_year))
        self.year_menu = ctk.CTkOptionMenu(
            self.header_frame, values=years, variable=self.year_var, command=self._on_year_change,
            width=80, fg_color=Palette.ENTRY_BG, button_color=Palette.ENTRY_BG, button_hover_color=Palette.SURFACE2
        )
        self.year_menu.pack(side="left", padx=5)
        
        self.btn_next = ctk.CTkButton(self.header_frame, text=">", width=30, command=self._next_month, fg_color=Palette.ENTRY_BG, text_color=Palette.TEXT)
        self.btn_next.pack(side="left")
        
        # Days grid
        self.days_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.days_frame.pack(fill="both", expand=True)
        for i in range(7):
            self.days_frame.grid_columnconfigure(i, weight=1)
            
        self._build_grid()

    def _prev_month(self):
        if self.view_month == 1:
            self.view_month = 12
            self.view_year -= 1
        else:
            self.view_month -= 1
        self._update_header()
        self._build_grid()

    def _next_month(self):
        if self.view_month == 12:
            self.view_month = 1
            self.view_year += 1
        else:
            self.view_month += 1
        self._update_header()
        self._build_grid()

    def _on_month_change(self, val: str):
        months = self._i18n.t("months").split(",")
        self.view_month = months.index(val) + 1
        self._build_grid()

    def _on_year_change(self, val: str):
        self.view_year = int(val)
        self._build_grid()
        
    def _update_header(self):
        months = self._i18n.t("months").split(",")
        self.month_var.set(months[self.view_month - 1])
        self.year_var.set(str(self.view_year))

    def _build_grid(self):
        for widget in self.days_frame.winfo_children():
            widget.destroy()
            
        days_abbr = self._i18n.t("days").split(",")
        for i, d in enumerate(days_abbr):
            lbl = ctk.CTkLabel(self.days_frame, text=d, font=Fonts.label_bold(), text_color=Palette.ACCENT)
            lbl.grid(row=0, column=i, pady=(0, 5))
            
        cal = calendar.Calendar(firstweekday=0)
        month_days = cal.monthdayscalendar(self.view_year, self.view_month)
        
        now = datetime.now()
        
        for r, week in enumerate(month_days):
            for c, day in enumerate(week):
                if day != 0:
                    is_future = self.view_year > now.year or (self.view_year == now.year and self.view_month > now.month) or (self.view_year == now.year and self.view_month == now.month and day > now.day)
                    btn = ctk.CTkButton(
                        self.days_frame, text=str(day), width=20, height=30, corner_radius=8,
                        font=("Segoe UI", 12),
                        fg_color=Palette.ACCENT if self._is_selected(day) else "transparent",
                        text_color=(Palette.TEXT if self._is_selected(day) else Palette.TEXT_MUTED) if not is_future else "#4A4A5A",
                        hover_color=Palette.ACCENT_HOVER,
                        state="normal" if not is_future else "disabled",
                        command=lambda d=day: self._select_day(d)
                    )
                    btn.grid(row=r+1, column=c, padx=2, pady=2, sticky="nsew")

    def _is_selected(self, day: int) -> bool:
        if not self.selected_date:
            return False
        return (self.selected_date.year == self.view_year and 
                self.selected_date.month == self.view_month and 
                self.selected_date.day == day)

    def _select_day(self, day: int):
        self.selected_date = datetime(self.view_year, self.view_month, day)
        self._build_grid()
        
    def get_date_str(self) -> str:
        if not self.selected_date:
            return ""
        # Return DD/MM/YYYY
        return self.selected_date.strftime("%d/%m/%Y")


class DateRangePopup(ctk.CTkToplevel):
    """Popup window for selecting From and To dates."""
    
    def __init__(self, parent: ctk.CTkFrame, i18n, current_data: dict, on_save, current_label_key: str = "date_current"):
        super().__init__(parent)
        self._i18n = i18n
        self._on_save = on_save
        self._current_label_key = current_label_key
        
        self.title("Select Dates")
        self.geometry("650x450")
        self.resizable(False, False)
        
        # Make it modal
        self.transient(parent.winfo_toplevel())
        self.grab_set()
        
        self.configure(fg_color=Palette.BG)
        
        # Parse existing data
        d_from = None
        d_to = None
        is_current = current_data.get("current", False)
        
        # Bottom Actions FIRST to guarantee visibility
        self.bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_frame.pack(side="bottom", fill="x", padx=10, pady=(0, 15))
        
        self.current_var = ctk.BooleanVar(value=is_current)
        self.chk_current = ctk.CTkCheckBox(
            self.bottom_frame, text=self._i18n.t(self._current_label_key), variable=self.current_var,
            font=Fonts.label(), fg_color=Palette.ACCENT, hover_color=Palette.ACCENT_HOVER,
            command=self._on_current_toggle
        )
        self.chk_current.pack(side="left", padx=10)
        
        self.btn_save = ctk.CTkButton(
            self.bottom_frame, text=self._i18n.t("btn_save"), command=self._save,
            fg_color=Palette.ACCENT, hover_color=Palette.ACCENT_HOVER
        )
        self.btn_save.pack(side="right", padx=10)
        
        self.btn_cancel = ctk.CTkButton(
            self.bottom_frame, text=self._i18n.t("btn_cancel"), command=self.destroy,
            fg_color="transparent", border_width=1, border_color=Palette.BORDER, text_color=Palette.TEXT
        )
        self.btn_cancel.pack(side="right")
        
        # Layout for content
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=1)
        
        # Left: From
        self.frame_from = ctk.CTkFrame(self.content_frame, fg_color=Palette.SURFACE, corner_radius=10)
        self.frame_from.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(self.frame_from, text=self._i18n.t("date_from"), font=Fonts.label_bold()).pack(pady=10)
        
        # Parse existing data
        d_from = None
        d_to = None
        is_current = current_data.get("current", False)
        
        try:
            if current_data.get("from"):
                d_from = datetime.strptime(current_data["from"], "%d/%m/%Y")
            if current_data.get("to") and not is_current:
                d_to = datetime.strptime(current_data["to"], "%d/%m/%Y")
        except ValueError:
            pass
            
        self.cal_from = CalendarView(self.frame_from, i18n, d_from)
        self.cal_from.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Right: To
        self.frame_to = ctk.CTkFrame(self.content_frame, fg_color=Palette.SURFACE, corner_radius=10)
        self.frame_to.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(self.frame_to, text=self._i18n.t("date_to"), font=Fonts.label_bold()).pack(pady=10)
        
        self.cal_to = CalendarView(self.frame_to, i18n, d_to)
        self.cal_to.pack(fill="both", expand=True, padx=10, pady=10)
        
        self._on_current_toggle()
        
    def _on_current_toggle(self):
        if self.current_var.get():
            # Disable To calendar
            for widget in self.cal_to.winfo_children():
                try: widget.configure(state="disabled")
                except: pass
        else:
            for widget in self.cal_to.winfo_children():
                try: widget.configure(state="normal")
                except: pass
                
    def _save(self):
        data = {
            "from": self.cal_from.get_date_str(),
            "to": "" if self.current_var.get() else self.cal_to.get_date_str(),
            "current": self.current_var.get()
        }
        self._on_save(data)
        self.destroy()


class DateRangeField(ctk.CTkFrame):
    """Button that opens the DateRangePopup and displays the selected range."""
    
    def __init__(self, parent: ctk.CTkFrame, i18n: I18nService, current_label_key: str = "date_current") -> None:
        super().__init__(parent, fg_color="transparent")
        self._i18n = i18n
        self._current_label_key = current_label_key
        self._data = {"from": "", "to": "", "current": False}
        
        self.btn = ctk.CTkButton(
            self, text=self._i18n.t("exp_dates"), anchor="w", 
            fg_color=Palette.ENTRY_BG, text_color=Palette.TEXT_MUTED,
            border_color=Palette.BORDER, border_width=1, hover_color=Palette.SURFACE2,
            command=self._open_popup, height=36
        )
        self.btn.pack(fill="x", expand=True)
        
    def _open_popup(self):
        DateRangePopup(self, self._i18n, self._data, self._on_save, self._current_label_key)
        
    def _on_save(self, data: Dict[str, Any]):
        self._data = data
        self._update_display()
        
    def _update_display(self):
        if not self._data["from"] and not self._data["to"] and not self._data["current"]:
            self.btn.configure(text=self._i18n.t("exp_dates"), text_color=Palette.TEXT_MUTED)
            return
            
        t = f"{self._data['from']} - "
        if self._data["current"]:
            t += self._i18n.t(self._current_label_key)
        else:
            t += self._data["to"]
            
        self.btn.configure(text=t, text_color=Palette.TEXT)
        
    def get_data(self) -> str:
        # For simplicity, convert the dict to a string so CVContentProvider handles it easily
        if not self._data["from"] and not self._data["to"] and not self._data["current"]:
            return ""
            
        t = f"{self._data['from']} - "
        if self._data["current"]:
            t += self._i18n.t("date_current")
        else:
            t += self._data["to"]
        return t

    def update_labels(self):
        self._update_display()
