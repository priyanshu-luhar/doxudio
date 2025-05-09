import customtkinter as ctk
from PIL import Image, ImageTk
import time

class LoadingAnimation(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Doxudio Loading Screen")
        self.geometry("400x200")
        self.resizable(False, False)
        
        try:
            image_p = "img/doxaudio_dark.png"
            self.logo_image = Image.open(image_p) 
            self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        except FileNotFoundError:
            print("Error: 'doxudio_logo.png' not found. Using placeholder text.")
            self.logo_photo = None
        
        self.logo_label = ctk.CTkLabel(self, text="Doxudio", font=("Arial", 24), image=self.logo_photo)
        self.logo_label.pack(pady=50)
        
        self.fade_direction = -1  
        self.current_alpha = 1.0   
        self.animate_fade()

    def animate_fade(self):
        self.current_alpha += 0.02 * self.fade_direction
        
        if self.current_alpha <= 0.0:
            self.current_alpha = 0.0
            self.fade_direction = 1  
        elif self.current_alpha >= 1.0:
            self.current_alpha = 1.0
            self.fade_direction = -1  
        
        self.logo_label.configure(text_color=self._apply_alpha((255, 255, 255), self.current_alpha))
        
        self.after(30, self.animate_fade)

    def _apply_alpha(self, rgb_color, alpha):
        """Helper function to apply transparency to a color."""
        return f"#{int(rgb_color[0] * alpha):02x}{int(rgb_color[1] * alpha):02x}{int(rgb_color[2] * alpha):02x}"

if __name__ == "__main__":
    app = LoadingAnimation()
    app.mainloop()
