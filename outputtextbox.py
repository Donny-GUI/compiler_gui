import customtkinter as ctk
from tkinter import END as TEXTEND
from typing import Tuple, Optional
from customtkinter import CTkFont


class OutputTextBox(ctk.CTkTextbox):
    def  __init__(self, master: any, width: int = 200, height: int = 200, corner_radius: int | None = None, border_width: int | None = None, border_spacing: int = 3, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, text_color: str | None = None, scrollbar_button_color: str | Tuple[str, str] | None = None, scrollbar_button_hover_color: str | Tuple[str, str] | None = None, font: tuple | CTkFont | None = None, activate_scrollbars: bool = True, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, border_spacing, bg_color, fg_color, border_color, text_color, scrollbar_button_color, scrollbar_button_hover_color, font, activate_scrollbars, **kwargs)
        self.x = 0 
        self.y = 0
    
    def new_text(self , reference=None, text=""):
        msg = ""
        cc = 0
        for char in text:
            msg+=char
            cc+=1
            if cc > 198:
                msg+="\n\t"
                self.y+=1
                cc = 0
        msg+="\n"
        self.insert(f"{self.y}.{self.x}", msg)
        self.see(f"{self.y}.0")
        self.y+=1
        
