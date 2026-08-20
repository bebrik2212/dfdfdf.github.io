import tkinter as tk
import obsws_python as obs
from PIL import Image, ImageTk
import os

class PNGTuber:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("PNG Tuber")
        self.window.geometry("300x400")
        self.window.configure(bg='#2b2b2b')
        
        # Настройки OBS
        self.obs = None
        self.connect_obs()
        
        # Загрузка картинок
        self.load_images()
        
        # UI
        self.setup_ui()
        
    def connect_obs(self):
        try:
            self.obs = obs.ReqClient(host="localhost", port=4455)
            print("Connected to OBS")
        except:
            print("OBS not connected")
            
    def load_images(self):
        self.images = {}
        for state in ["silent", "talking", "muted"]:
            path = f"images/{state}.png"
            if os.path.exists(path):
                img = Image.open(path)
                img.thumbnail((200, 200))
                self.images[state] = ImageTk.PhotoImage(img)
            else:
                self.images[state] = None
                
    def setup_ui(self):
        # Отображение картинки
        self.image_label = tk.Label(self.window, bg='#2b2b2b')
        self.image_label.pack(pady=20)
        
        # Кнопки
        btn_frame = tk.Frame(self.window, bg='#2b2b2b')
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="🔇 Молчать", 
                 command=lambda: self.set_state("silent"),
                 width=12, height=2).pack(pady=5)
        
        tk.Button(btn_frame, text="🗣️ Говорить", 
                 command=lambda: self.set_state("talking"),
                 width=12, height=2).pack(pady=5)
        
        tk.Button(btn_frame, text="🔴 Микро выкл", 
                 command=lambda: self.set_state("muted"),
                 width=12, height=2).pack(pady=5)
        
        self.set_state("silent")
        
    def set_state(self, state):
        if state in self.images and self.images[state]:
            self.image_label.config(image=self.images[state])
        
        # Отправка в OBS (если подключен)
        if self.obs:
            try:
                # Здесь будет логика обновления OBS
                print(f"OBS state: {state}")
            except:
                pass
                
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = PNGTuber()
    app.run()
