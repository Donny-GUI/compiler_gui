from typing import Optional, Tuple, Union
import customtkinter as ctk
from customtkinter.windows.widgets.font import CTkFont


class Cell(ctk.CTkEntry):
    def __init__(self, master: any, x, y, data, width, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, text_color: str | None = None, **kwargs):
        self.x = x
        self.y = y
        self.data = data 
        super().__init__(master, width=width, bg_color=bg_color, fg_color=fg_color, border_color=border_color, border_width=0, corner_radius=0, text_color=text_color, **kwargs)
        if data is not None:
            self.set_value(data)
        self.grid(column=x, row=y, padx=(0,1), pady=(0,0), ipadx=0, ipady=0)
        
    def set_value(self, value):
        self.data = value
        self.delete(0, "end")
        self.insert(0, self.data)
    
    def assign_command(self, type, command:any):
        self.bind(type, command)
    
class ScrollableTable(ctk.CTkScrollableFrame):
    def __init__(self, master, width, height, column_widths: list[int] = [150, 40, 40, 200, 200, 50, 50, 50, 50]):
        super().__init__(master, width, height)
        self.max_lines = 300
        self.rows = []
        self.map: dict[str: list[Cell]] = {}
        self.data = []
        self.default_row_length = 51
        self.default_column_length = 8
        self.uuids = []
        self.column_widths = column_widths
        
        for i in range(0, self.default_row_length):
            j = 0
            self.uuid = str(i)
            self.uuids.append(self.uuid)
            self.map[self.uuid] = []
            for j in range(0, self.default_column_length):
                self.map[self.uuid].append(Cell(master=self, x=j, y=i, width=column_widths[j], data="        "))
    
    def assign_command_to_row(self, uuid: str, command: any):
        for value in self.map[uuid]:
            value: Cell
            value.assign_command(command)
    
    def assign_command_to_all(self, command):
        for uuid in self.uuids:
            self.assign_command_to_row(uuid, command)
    
    def assign_command_to_column(self, column_index, command, type='<Button-1>'):
        for key in self.map.keys():
            
            self.map[key][column_index].assign_command(type, command(self.map[key][column_index].data))
            
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
                uuid = str(y)
                self.map[uuid] = []
                self.uuids.append(uuid)
                # for integer in column_length append the new cell to the row
                for j in range(0, self.default_column_length):
                    self.map[uuid].append(Cell(master=self, x=j, y=i, width=self.column_widths[j],  data="        "))
            # set the new default row length
            self.default_row_length = row_length
        
        # programmatically add the data to the cells
        for i in range(0, row_length):
            j = 0 
            uuid = str(i)
            for j in range(0, self.default_column_length):
                self.map[uuid][j].set_value(self.data[i][j])
                