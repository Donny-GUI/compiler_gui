import os
import dis
import marshal
import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.scrolledtext as scrolledtext


window = tk.Tk()
window.title("Hex Editor")
hex_text = scrolledtext.ScrolledText(window, width=180, height=30, bg='black', fg='green')
octal_text = scrolledtext.ScrolledText(window, width=180, height=30)
hex_text.pack()
octal_text.pack()

def hexdump(file_path, bytes_per_line=16):
    lines = []
    with open(file_path, "rb") as file:
        offset = 0
        while True:
            chunk = file.read(bytes_per_line)
            if not chunk:
                break

            hex_bytes = " ".join(f"{byte:02x}" for byte in chunk)
            ascii_chars = "".join(chr(byte) if 32 <= byte < 127 else " " for byte in chunk)

            x = f"{offset:08x}  {hex_bytes.ljust(bytes_per_line*3-1)}  {ascii_chars}\n"
            lines.append(x)
            offset += bytes_per_line
    return lines
            
def open_file():
    file_path = filedialog.askopenfilename()
    lines = hexdump(file_path=file_path)
                
    for index, line in enumerate(lines):
        hex_text.delete(f"{index}.0", tk.END)
        hex_text.insert(tk.END, line)


menubar = tk.Menu(window)
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="File", menu=file_menu)
window.config(menu=menubar)



file_path = os.path.join(os.getcwd(), "__pycache__\\gui.cpython-310.pyc")


window.mainloop()
