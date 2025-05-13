import customtkinter as ctk
from PIL import Image, ImageTk
from server_utils import login_user, add_user_to_server, hash_password
from main import PDFReaderApp
import globals

class AuthWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("doxudio")
        self.geometry("+0+0")
        self.geometry("1200x800")
        self.resizable(False, False)

        self.current_mode = "login"
        self.current_theme = "System"

        # Fonts
        self.font_title = ctk.CTkFont(family="Silom", size=40, weight="bold")
        self.font_entry = ctk.CTkFont(family="Silom", size=24)
        self.font_button = ctk.CTkFont(family="Silom", size=22)

        # Layout
        self.columnconfigure(0, weight=0, minsize=700)
        self.columnconfigure(1, weight=1)

        # Left side image frame
        self.image_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.image_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0, ipadx=0, ipady=0)

        # Load and place image with crop
        try:
            raw_img = Image.open("../str/meshHD.JPG")
            cropped_img = raw_img.crop((0, 200, 700, 800)).resize((700, 800))
            self.image = ctk.CTkImage(light_image=cropped_img, size=(700, 800))
            self.image_label = ctk.CTkLabel(self.image_frame, image=self.image, text="")
            self.image_label.pack(expand=True, fill="both", padx=0, pady=0)
            self.image_label.pack(expand=True, fill="both")
        except Exception as e:
            print("Error loading image:", e)

        # Right side content frame
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.columnconfigure(0, weight=1)

        # Theme toggle button
        self.theme_toggle = ctk.CTkButton(self.content_frame, text="♞", width=60, font=self.font_button, command=self.toggle_theme)
        self.theme_toggle.grid(row=0, column=0, sticky="ne", padx=20, pady=20)

        # Title
        self.title_label = ctk.CTkLabel(self.content_frame, text="Welcome to Doxudio", font=self.font_title)
        self.title_label.grid(row=1, column=0, pady=(20, 10))

        # Form frame
        self.form_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.form_frame.grid(row=2, column=0, pady=10)

        # Username and password
        self.uname_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Username", font=self.font_entry, height=60, width=400)
        self.uname_entry.grid(row=0, column=0, pady=10, padx=10, columnspan=2)

        self.pw_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Password", show="*", font=self.font_entry, height=60, width=400)
        self.pw_entry.grid(row=1, column=0, pady=10, padx=10, columnspan=2)

        self.fname_entry = ctk.CTkEntry(self.form_frame, placeholder_text="First Name", font=self.font_entry, height=60, width=195)
        self.lname_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Last Name", font=self.font_entry, height=60, width=195)

        # Status label
        self.status_label = ctk.CTkLabel(self.content_frame, text="", text_color="red", font=self.font_entry)
        self.status_label.grid(row=3, column=0, pady=10)

        # Action buttons
        self.action_button = ctk.CTkButton(self.content_frame, text="Sign IN", font=self.font_button, height=60, width=300, command=self.handle_action)
        self.action_button.grid(row=4, column=0, pady=10)

        self.switch_button = ctk.CTkButton(self.content_frame, text="Sign UP", font=self.font_button, height=60, width=300, command=self.switch_mode)
        self.switch_button.grid(row=5, column=0, pady=10)

    def toggle_theme(self):
        if self.current_theme == "Dark":
            ctk.set_appearance_mode("Light")
            self.current_theme = "Light"
            self.theme_toggle.configure(text="♘")
        else:
            ctk.set_appearance_mode("Dark")
            self.current_theme = "Dark"
            self.theme_toggle.configure(text="♞")

    def switch_mode(self):
        if self.current_mode == "login":
            self.current_mode = "signup"
            self.action_button.configure(text="Sign Up")
            self.switch_button.configure(text="Already have an account? Login")
            self.fname_entry.grid(row=2, column=0, pady=10, padx=(0, 5), sticky="e")
            self.lname_entry.grid(row=2, column=1, pady=10, padx=(5, 0), sticky="w")
            self.status_label.configure(text="")
        else:
            self.current_mode = "login"
            self.action_button.configure(text="Login")
            self.switch_button.configure(text="Don't have an account? Sign up")
            self.fname_entry.grid_forget()
            self.lname_entry.grid_forget()
            self.status_label.configure(text="")

    def handle_action(self):
        uname = self.uname_entry.get().strip()
        pw = self.pw_entry.get().strip()

        if not uname or not pw:
            self.status_label.configure(text="Username and password are required.")
            return

        hashed = hash_password(pw)

        '''
        if self.current_mode == "login":
            result = login_user(uname, hashed)
            if result["status"] == "success":
                self.status_label.configure(text="Login successful!", text_color="green")
                print("User:", result["user"])  # TODO: integrate with main app
            else:
                self.status_label.configure(text=result["message"], text_color="red")
        '''

        if self.current_mode == "login":
            result = login_user(uname, hashed)
            if result["status"] == "success":
                self.status_label.configure(text="Login successful!", text_color="green")
                globals.me = result["user"]  # Save user globally

                self.destroy()  # Close the login window
                reader_app = PDFReaderApp()
                reader_app.mainloop()
            else:
                self.status_label.configure(text=result["message"], text_color="red")
        elif self.current_mode == "signup":
            fname = self.fname_entry.get().strip()
            lname = self.lname_entry.get().strip()
            if not fname or not lname:
                self.status_label.configure(text="First and last name required.")
                return
            result = add_user_to_server(uname, fname, lname, hashed)
            if "success" in result:
                self.status_label.configure(text="Signup successful! Please login.", text_color="green")
                self.switch_mode()
            else:
                self.status_label.configure(text="Signup failed: " + result.get("error", "unknown error"), text_color="red")

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    #ctk.set_default_color_theme("green")
    app = AuthWindow()
    app.mainloop()
