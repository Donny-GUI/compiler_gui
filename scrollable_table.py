from typing import Optional, Tuple, Union
import customtkinter as ctk
from customtkinter.windows.widgets.font import CTkFont


class Cell(ctk.CTkEntry):
    def __init__(self, master: any, x, y, data=None, width: int = 100, height: int = 50, corner_radius: int | None = 0, border_width: int | None = 1, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, text_color: str | None = None, scrollbar_button_color: str | Tuple[str, str] | None = None, scrollbar_button_hover_color: str | Tuple[str, str] | None = None, font: tuple | CTkFont | None = None, activate_scrollbars: bool = True, **kwargs):
        self.x = x
        self.y = y
        self.data = data 
        super().__init__(master, width=width, border_width=border_width, bg_color=bg_color, fg_color=fg_color, border_color=border_color, text_color=text_color, **kwargs)
        if data is not None:
            self.set_value(data)
        self.grid(column=x, row=y, padx=(0,1), pady=(0,1))
        
    def set_value(self, value):
        self.data = value
        self.delete(0, "end")
        self.insert(0, self.data)
    
class ScrollableTable(ctk.CTkScrollableFrame):
    def __init__(self, master, width, height, column_widths: list[int] = [100, 25, 25, 200, 200, 45, 45, 40, 40]):
        super().__init__(master, width, height)
        self.max_lines = 300
        self.rows = []
        self.map = {}
        self.data = []
        self.default_row_length = 51
        self.default_column_length = 8
        self.uuids = []
        self.column_widths = column_widths
        for i in range(0, self.default_row_length):
            j = 0
            self.uuid = str(i) + str(j)
            self.uuids.append(self.uuid)
            self.map[self.uuid] = []
            for j in range(0, self.default_column_length):
                self.map[self.uuid].append(Cell(master=self, x=j, y=i, width=column_widths[j], data="        "))
                
    
    def set_data(self, data: list[list[str]]):
        self.data = data
        # get the new column length
        column_length = len(data[0])
        # if the column length is more than the default
        if column_length > self.default_column_length:
            # get the difference
            diff = column_length - self.default_column_length
            
            for i in range(0 , diff):
                self.column_widths.append(40)
            
            # for key in uuid
            for index, uuid in enumerate(self.map.keys()):
                l = self.default_column_length + index
                # make the new cells for the extending
                adds = [
                    Cell(master=self, x=l, y=l, width=self.column_widths[l], data="        ") for o in range(0, diff)
                ]
                # append them to the correct row
                for add in adds:
                    self.map[uuid].append(add)
            # set the new defualt
            self.default_column_length = column_length
        
        row_length = len(data)
        # if the row length is greater than the row length
        if row_length > self.default_row_length:
            # get the difference in rows
            diff = row_length - self.default_row_length
            # for integer in difference
            for i in range(0, diff):
                x = 0
                # create the new row
                y = self.default_row_length + i
                uuid = str(y) + str(x)
                self.map[uuid] = []
                # for integer in column_length append the new cell to the row
                for j in range(0, self.default_column_length):
                    self.map[uuid].append(Cell(master=self, x=j, y=i, width=self.column_widths[j],  data="        "))
            # set the new default row length
            self.default_row_length = row_length
        
        # programmatically add the data to the cells
        for i in range(0, row_length):
            j = 0 
            uuid = str(i) + str(j)
            for j in range(0, self.default_column_length):
                self.map[uuid][j].set_value(data[i][j])
                