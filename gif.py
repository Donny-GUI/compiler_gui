import tkinter as tk
from PIL import Image, ImageTk



class AnimatedGif(tk.Canvas):
    def __init__(self, master, gif_path, width, height, delay=100):
        c = master.cget("fg_color")[1]

        super().__init__(master, bg=c, relief=None, insertborderwidth=0, borderwidth=0,width=width, height=height, border=0, highlightthickness=0)
        self.gif_path = gif_path
        self.delay = delay

        # Open the GIF file
        self.gif = Image.open(gif_path, formats=['GIF'])
        self.frames = []
        # Initialize the current frame
        self.current_frame = 0

        # Set up the canvas
        self.config(width=width, height=height)
        self.image_item = self.create_image(0, 0, anchor=tk.NW)

    def start_animation(self):
        self.update_frame()

    def update_frame(self):
        # Extract the current frame
        self.delete(tk.ALL)
        self.image_item = self.create_image(0, 0, anchor=tk.NW)
        self.current = self.frames[self.current_frame]

        # Convert the frame to RGB format
        frame_rgb = self.current.convert("RGBA")

        # Resize the frame to fit the canvas
        self.frame_resized = frame_rgb.resize((self.winfo_width(), self.winfo_height()), Image.ANTIALIAS)

        # Create an image from the frame
        self.image = ImageTk.PhotoImage(self.frame_resized)
        # Update the canvas with the new image
        self.itemconfig(self.image_item, image=self.image)
        
        # Schedule the next frame update
        self.current_frame = (self.current_frame + 1) % self.gif.n_frames
        self.master.after(self.delay, self.update_frame)

    def extract_frames(self):
        self.frames = []
        # Extract and save each frame from the GIF
        for frame_index in range(self.gif.n_frames):
            self.gif.seek(frame_index)
            frame = self.gif.convert("RGBA")
            self.frames.append(frame)