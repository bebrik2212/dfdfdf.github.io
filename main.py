import tkinter as tk
from PIL import Image, ImageTk
import os

class PNGTuber:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("PNG Tuber - Вставь свои фото!")
        self.window.geometry("400x500")
        self.window.configure(bg='#2b2b2b')
        
        # Папка с фото
        self.images_folder = "my_photos"  # СЮДА ВСТАВЛЯЙ СВОИ ФОТО
        
        # Загрузка фото
        self.load_images()
        
        # Создание интерфейса
        self.setup_ui()
        
    def load_images(self):
        """Загрузка фото из папки my_photos"""
        self.images = {}
        
        # Проверяем папку
        if not os.path.exists(self.images_folder):
            os.makedirs(self.images_folder)
            print(f"Создана папка {self.images_folder}. Положи туда свои фото!")
        
        # Загружаем фото
        photos = {
            "silent": "silent.png",    # Фото когда молчишь
            "talking": "talking.png",  # Фото когда говоришь
            "muted": "muted.png"       # Фото когда микрофон выключен
        }
        
        for state, filename in photos.items():
            path = os.path.join(self.images_folder, filename)
            if os.path.exists(path):
                img = Image.open(path)
                img.thumbnail((300, 300))
                self.images[state] = ImageTk.PhotoImage(img)
                print(f"✅ Загружено: {filename}")
            else:
                self.images[state] = None
                print(f"❌ Не найдено: {filename}")
        
    def setup_ui(self):
        # Заголовок
        title = tk.Label(
            self.window, 
            text="ТВОЙ PNG ТУБЕР",
            font=("Arial", 20, "bold"),
            bg='#2b2b2b',
            fg='white'
        )
        title.pack(pady=20)
        
        # Отображение фото
        self.image_label = tk.Label(self.window, bg='#2b2b2b')
        self.image_label.pack(pady=10)
        
        # Статус
        self.status_label = tk.Label(
            self.window,
            text="Молчу 😊",
            font=("Arial", 14),
            bg='#2b2b2b',
            fg='white'
        )
        self.status_label.pack(pady=5)
        
        # Кнопки
        btn_frame = tk.Frame(self.window, bg='#2b2b2b')
        btn_frame.pack(pady=20)
        
        # Стиль кнопок
        button_style = {
            'width': 15,
            'height': 2,
            'font': ("Arial", 12, "bold"),
            'cursor': 'hand2'
        }
        
        # Кнопка "Молчать"
        self.btn_silent = tk.Button(
            btn_frame,
            text="😊 МОЛЧАТЬ",
            command=lambda: self.set_state("silent"),
            bg='#4CAF50',
            fg='white',
            **button_style
        )
        self.btn_silent.pack(pady=5)
        
        # Кнопка "Говорить"
        self.btn_talking = tk.Button(
            btn_frame,
            text="🗣️ ГОВОРИТЬ",
            command=lambda: self.set_state("talking"),
            bg='#2196F3',
            fg='white',
            **button_style
        )
        self.btn_talking.pack(pady=5)
        
        # Кнопка "Микрофон выключен"
        self.btn_muted = tk.Button(
            btn_frame,
            text="🔇 МИКРО ВЫКЛ",
            command=lambda: self.set_state("muted"),
            bg='#f44336',
            fg='white',
            **button_style
        )
        self.btn_muted.pack(pady=5)
        
        # Подсказка
        hint = tk.Label(
            self.window,
            text=f"📁 Положи свои фото в папку:\n{self.images_folder}/",
            font=("Arial", 10),
            bg='#2b2b2b',
            fg='#888888',
            justify=tk.CENTER
        )
        hint.pack(pady=20)
        
        # Показываем первое состояние
        self.set_state("silent")
        
    def set_state(self, state):
        """Переключение состояния"""
        states_text = {
            "silent": "Молчу 😊",
            "talking": "Говорю 🗣️",
            "muted": "Микрофон выключен 🔇"
        }
        
        # Обновляем текст
        self.status_label.config(text=states_text[state])
        
        # Обновляем фото
        if state in self.images and self.images[state]:
            self.image_label.config(image=self.images[state])
        else:
            # Если фото нет, показываем заглушку
            self.image_label.config(
                image='',
                text=f"Нет фото: {state}.png\nПоложи его в папку {self.images_folder}/",
                font=("Arial", 12),
                fg='#888888'
            )
        
        # Подсветка активной кнопки
        self.btn_silent.config(bg='#4CAF50' if state == "silent" else '#666666')
        self.btn_talking.config(bg='#2196F3' if state == "talking" else '#666666')
        self.btn_muted.config(bg='#f44336' if state == "muted" else '#666666')
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    print("=" * 50)
    print("PNG TUBER - ПРОСТАЯ ВЕРСИЯ")
    print("=" * 50)
    print("\n📁 Как использовать:")
    print("1. Создай папку 'my_photos'")
    print("2. Положи туда 3 фото:")
    print("   - silent.png (когда молчишь)")
    print("   - talking.png (когда говоришь)")
    print("   - muted.png (когда микрофон выключен)")
    print("\n3. Запусти программу и переключай состояния!")
    print("=" * 50)
    
    app = PNGTuber()
    app.run()
