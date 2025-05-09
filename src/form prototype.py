import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("light")  
ctk.set_default_color_theme("blue")  


class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Login System")
        self.geometry("400x500")
        self.resizable(False, False)
        self.bg_color = "#F0F2F5" 
        self.frame_color = "#E1E5EE" 
        self.primary_color = "#4FC3F7"  
        self.text_color = "#333333"
        self.configure(fg_color=self.bg_color)
        self.login_frame = ctk.CTkFrame(self, fg_color=self.frame_color)
        self.login_frame.pack(pady=40, padx=20, fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        title_label = ctk.CTkLabel(
            self.login_frame,
            text="Welcome Back",
            font=("Arial", 24, "bold"),
            text_color=self.text_color
        )
        title_label.pack(pady=(30, 15))

        self.username_entry = ctk.CTkEntry(
            self.login_frame,
            placeholder_text="Username",
            width=220,
            height=40,
            corner_radius=10,
            border_color=self.primary_color,
            fg_color="white",
            text_color=self.text_color
        )
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(
            self.login_frame,
            placeholder_text="Password",
            width=220,
            height=40,
            corner_radius=10,
            border_color=self.primary_color,
            fg_color="white",
            text_color=self.text_color,
            show="•"
        )
        self.password_entry.pack(pady=10)

        self.remember_me = ctk.CTkCheckBox(
            self.login_frame,
            text="Remember me",
            text_color=self.text_color,
            checkbox_width=18,
            checkbox_height=18,
            border_width=2,
            fg_color=self.primary_color
        )
        self.remember_me.pack(pady=10)

        login_button = ctk.CTkButton(
            self.login_frame,
            text="Login",
            width=220,
            height=40,
            corner_radius=10,
            fg_color=self.primary_color,
            hover_color="#3DA8D8",  
            text_color="white",
            font=("Arial", 14, "bold"),
            command=self.login_action
        )
        login_button.pack(pady=20)

        signup_label = ctk.CTkLabel(
            self.login_frame,
            text="Don't have an account? Sign Up",
            text_color=self.text_color,
            font=("Arial", 12)
        )
        signup_label.pack(pady=5)
        signup_label.bind("<Button-1>", lambda e: messagebox.showinfo("Sign Up", "Sign up functionality would go here"))

    def login_action(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
        else:
            messagebox.showinfo("Success", f"Welcome, {username}!")

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
