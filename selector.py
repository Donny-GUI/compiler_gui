from typing_extensions import Literal
from asset import Asset
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import NW as tknw
from tkinter import ALL as tkall


class Selectable(object):
    grid_attributes = (
        'row','column','rowspan','columnspan','sticky','padx','pady','ipady','ipadx',
    )
    def __init__(self, element: ctk.CTkBaseClass):
        self.element = element
        grid_info = self.element.grid_info()
        self.grid_config = {}
        for key in self.grid_attributes:
            try:
                self.grid_config[key] = grid_info[key]
            except KeyError:
                pass
    
    def Attributes(self):
        return self.grid_config
    
    def Widget(self):
        return self.element
    
    def Row(self):
        return self.grid_attributes['row']
    
    def Column(self):
        return self.grid_attributes['column']
        
    def Master(self):
        return self.element.master
        
    
    
class Selector(object):
    def __init__(self, gif_path:str, delay:int=100):
        self.current_frame = 0
        self.delay = delay
        # Open the GIF file
        gif = Image.open(gif_path, formats=['GIF'])
        self.number_of_frames = gif.n_frames
        self.frames = []
        self.width = gif.width
        self.height = gif.height
        for frame_index in range(self.number_of_frames):
            gif.seek(frame_index)
            frame = gif.convert("RGBA").resize((self.width, self.height), Image.ANTIALIAS)
            self.frames.append(frame)
        self.current = self.frames[self.current_frame]
    
    def next(self):
        frame_rgb = self.current
        self.current_frame = (self.current_frame + 1) % self.number_of_frames
        return frame_rgb
        

class WidgetSelector:
    def __init__(self, master: ctk.CTkBaseClass, gif_path: str, delay=100) -> None:
        self.selectables        = []
        self.canvasi            = []
        self.coordinates        = []
        self.masters            = []
        self.widget_index       = 0
        self.base_widget        = master
        self.base               = Selectable(master)
        self.selector           = Selector(gif_path=gif_path, delay=delay)
        self.current_selected   = self.base
        self.frame_resized      = None
        self.image_item         = None
        self.target_acquired    = False
        self.canvas = ctk.CTkCanvas(self.base_widget, bg=self._get_fg_color(master), relief=None, insertborderwidth=0, borderwidth=0,width=self.selector.width, height=self.selector.height, border=0, highlightthickness=0)
        self.selectables.append(self.current_selected)
        self.canvasi.append(self.canvas)
        self.coordinates.append(self._get_coordinates())
        # TODO: this
    def _get_fg_color(self, widget: ctk.CTkBaseClass):
        return widget.cget("fg_color")[1]
    
    def _create_canvas(self, selectable: Selectable):
        return ctk.CTkCanvas(selectable.Master(), self._get_fg_color(selectable.element), relief=None, insertborderwidth=0, borderwidth=0,width=self.selector.width, height=self.selector.height, border=0, highlightthickness=0)
    
    def _update_frame(self):
        if not self.target_acquired:
            return
        self.delete(tkall)
        # Update the canvas with the new image
        self.itemconfig(
            self.create_image(0, 0, anchor=tknw), 
            image=ImageTk.PhotoImage(self.selector.next())
            )
        # Schedule the next frame update
        self.master.after(self.selector.delay, self._update_frame)
        self.grid(column=0, row=0, padx=0, pady=0)
    
    def add_target(self, target: ctk.CTkBaseClass, position: str='right'):
        self.target_acquired = True
        # append the target to the target list
        self.current_selected = Selectable(target)
        self.selectables.append(self.current_selected)
        self.canvasi.append(self._create_canvas(self.current_selected))
        self.coordinates.append(self._get_coordinates())
        self._update_frame()
    
    def _get_coordinates(self, position='right'):
        _col = self.current_selected.Column()
        _row = self.current_selected.Row()
        if position == 'right':
            _col+=1
        elif position == 'left':
            _col = _col - 1 if _col != 0 else 0
        elif position == 'up' or position == 'above':
            _row = _row - 1 if _row != 0 else 0
        elif position == 'down' or position == 'below':
            _row+1
        return {"row": _row, "col":_col}
    
    def next(self):
        self.widget_index += 1
        try:
            self.current_selected = self.selectables[self.widget_index]
        except IndexError:
            return 
        self.grid_forget()
        
        
    
        