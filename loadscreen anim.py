import customtkinter as ctk
import time
from threading import Thread


class LoadingScreen:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Loading...")
        self.root.geometry("400x200")
        self.root.resizable(False, False)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.loading_label = ctk.CTkLabel(
            self.frame,
            text="Loading Application",
            font=("Arial", 18, "bold")
        )
        self.loading_label.pack(pady=(30, 10))
        self.progressbar = ctk.CTkProgressBar(
            self.frame,
            orientation="horizontal",
            mode="indeterminate",
            width=300,
            height=10,
            corner_radius=5
        )
        self.progressbar.pack(pady=10)
        self.progressbar.start()
        self.percentage_label = ctk.CTkLabel(
            self.frame,
            text="0%",
            font=("Arial", 14)
        )
        self.percentage_label.pack(pady=5)
        self.message_label = ctk.CTkLabel(
            self.frame,
            text="Initializing components...",
            font=("Arial", 12),
            text_color="gray"
        )
        self.message_label.pack(pady=5)
        self.loading_thread = Thread(target=self.simulate_loading)
        self.loading_thread.daemon = True
        self.loading_thread.start()

    def simulate_loading(self):
        messages = [
            "Loading configuration...",
            "Connecting to database...",
            "Initializing UI components...",
            "Almost there...",
            "Finishing up..."
        ]

        for i in range(1, 101):
            time.sleep(0.05)
            self.percentage_label.configure(text=f"{i}%")
            if i % 20 == 0:
                msg_index = min(i // 20 - 1, len(messages) - 1
                self.message_label.configure(text=messages[msg_index])
                self.root.update()
                time.sleep(0.5)
                self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    loading_screen = LoadingScreen()
    loading_screen.run()

    print("Loading complete! Launching main application...")
