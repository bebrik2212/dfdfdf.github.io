import tkinter as tk
from tkinter import ttk
import json
import os
import threading
import time
from PIL import Image, ImageTk
import obsws_python as obs
import pystray
from pystray import MenuItem, Menu
from PIL import Image as PILImage
import sys

class PNGTuberApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PNG Tuber Control")
        self.root.geometry("400x500")
        self.root.configure(bg='#2b2b2b')
        
        # Настройки
        self.settings_file = "settings.json"
        self.load_settings()
        
        # Состояние
        self.current_state = "silent"
        self.obs_client = None
        self.obs_connected = False
        self.running = True
        
        # Загрузка изображений
        self.load_images()
        
        # Создание интерфейса
        self.create_widgets()
        
        # Подключение к OBS
        self.connect_obs()
        
        # Запуск мониторинга OBS
        self.monitor_thread = threading.Thread(target=self.monitor_obs, daemon=True)
        self.monitor_thread.start()
        
        # Обработка закрытия
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_settings(self):
        """Загрузка настроек из файла"""
        self.settings = {
            "obs_host": "localhost",
            "obs_port": 4455,
            "obs_password": "",
            "silent_image": "silent.png",
            "talking_image": "talking.png",
            "muted_image": "muted.png",
            "obs_source_name": "PNG Tuber"
        }
        
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    saved_settings = json.load(f)
                    self.settings.update(saved_settings)
            except:
                pass

    def save_settings(self):
        """Сохранение настроек"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4)
        except:
            pass

    def load_images(self):
        """Загрузка изображений"""
        self.images = {}
        states = ["silent", "talking", "muted"]
        
        for state in states:
            image_path = self.settings.get(f"{state}_image", f"{state}.png")
            
            if os.path.exists(image_path):
                try:
                    img = Image.open(image_path)
                    img.thumbnail((300, 300))
                    self.images[state] = ImageTk.PhotoImage(img)
                except:
                    self.images[state] = None
            else:
                self.images[state] = None
                print(f"Файл не найден: {image_path}")

    def create_widgets(self):
        """Создание элементов интерфейса"""
        # Заголовок
        title_label = tk.Label(
            self.root, 
            text="PNG Tuber Control",
            font=("Arial", 16, "bold"),
            bg='#2b2b2b',
            fg='white'
        )
        title_label.pack(pady=10)
        
        # Отображение текущего состояния
        self.image_frame = tk.Frame(self.root, bg='#2b2b2b')
        self.image_frame.pack(pady=10)
        
        self.image_label = tk.Label(self.image_frame, bg='#2b2b2b')
        self.image_label.pack()
        
        self.state_label = tk.Label(
            self.root,
            text="Состояние: Молчит",
            font=("Arial", 12),
            bg='#2b2b2b',
            fg='white'
        )
        self.state_label.pack(pady=5)
        
        # Кнопки управления
        button_frame = tk.Frame(self.root, bg='#2b2b2b')
        button_frame.pack(pady=20)
        
        self.silent_button = tk.Button(
            button_frame,
            text="Молчать",
            command=lambda: self.set_state("silent"),
            width=10,
            height=2,
            bg='#4a4a4a',
            fg='white',
            font=("Arial", 10)
        )
        self.silent_button.pack(side=tk.LEFT, padx=5)
        
        self.talking_button = tk.Button(
            button_frame,
            text="Говорить",
            command=lambda: self.set_state("talking"),
            width=10,
            height=2,
            bg='#4a4a4a',
            fg='white',
            font=("Arial", 10)
        )
        self.talking_button.pack(side=tk.LEFT, padx=5)
        
        self.muted_button = tk.Button(
            button_frame,
            text="Выкл. микро",
            command=lambda: self.set_state("muted"),
            width=10,
            height=2,
            bg='#4a4a4a',
            fg='white',
            font=("Arial", 10)
        )
        self.muted_button.pack(side=tk.LEFT, padx=5)
        
        # Настройки OBS
        settings_frame = tk.Frame(self.root, bg='#2b2b2b')
        settings_frame.pack(pady=20, fill=tk.X, padx=20)
        
        tk.Label(
            settings_frame,
            text="Настройки OBS:",
            bg='#2b2b2b',
            fg='white',
            font=("Arial", 10, "bold")
        ).pack(anchor=tk.W)
        
        # Source name
        tk.Label(
            settings_frame,
            text="Имя источника в OBS:",
            bg='#2b2b2b',
            fg='white'
        ).pack(anchor=tk.W, pady=(5, 0))
        
        self.source_entry = tk.Entry(settings_frame, bg='#3a3a3a', fg='white')
        self.source_entry.insert(0, self.settings.get("obs_source_name", ""))
        self.source_entry.pack(fill=tk.X, pady=(0, 5))
        
        # Host
        tk.Label(
            settings_frame,
            text="OBS Host:",
            bg='#2b2b2b',
            fg='white'
        ).pack(anchor=tk.W)
        
        self.host_entry = tk.Entry(settings_frame, bg='#3a3a3a', fg='white')
        self.host_entry.insert(0, self.settings.get("obs_host", "localhost"))
        self.host_entry.pack(fill=tk.X, pady=(0, 5))
        
        # Port
        tk.Label(
            settings_frame,
            text="OBS Port:",
            bg='#2b2b2b',
            fg='white'
        ).pack(anchor=tk.W)
        
        self.port_entry = tk.Entry(settings_frame, bg='#3a3a3a', fg='white')
        self.port_entry.insert(0, str(self.settings.get("obs_port", 4455)))
        self.port_entry.pack(fill=tk.X, pady=(0, 5))
        
        # Password
        tk.Label(
            settings_frame,
            text="OBS Password:",
            bg='#2b2b2b',
            fg='white'
        ).pack(anchor=tk.W)
        
        self.password_entry = tk.Entry(settings_frame, bg='#3a3a3a', fg='white', show="*")
        self.password_entry.insert(0, self.settings.get("obs_password", ""))
        self.password_entry.pack(fill=tk.X, pady=(0, 5))
        
        # Кнопка сохранения настроек
        save_button = tk.Button(
            settings_frame,
            text="Сохранить настройки",
            command=self.save_current_settings,
            bg='#4a4a4a',
            fg='white'
        )
        save_button.pack(pady=10)
        
        # Статус подключения
        self.status_label = tk.Label(
            self.root,
            text="Статус: Не подключено к OBS",
            bg='#2b2b2b',
            fg='red'
        )
        self.status_label.pack(pady=10)
        
        # Обновление отображения
        self.update_display()

    def save_current_settings(self):
        """Сохранение текущих настроек"""
        self.settings["obs_host"] = self.host_entry.get()
        self.settings["obs_port"] = int(self.port_entry.get())
        self.settings["obs_password"] = self.password_entry.get()
        self.settings["obs_source_name"] = self.source_entry.get()
        self.save_settings()
        
        # Переподключение к OBS
        self.connect_obs()
        tk.messagebox.showinfo("Сохранено", "Настройки сохранены!")

    def connect_obs(self):
        """Подключение к OBS Studio"""
        try:
            if self.obs_client:
                self.obs_client.disconnect()
            
            self.obs_client = obs.ReqClient(
                host=self.settings["obs_host"],
                port=self.settings["obs_port"],
                password=self.settings["obs_password"]
            )
            self.obs_connected = True
            self.status_label.config(text="Статус: Подключено к OBS", fg='green')
        except Exception as e:
            self.obs_connected = False
            self.status_label.config(text=f"Статус: Ошибка подключения", fg='red')
            print(f"Ошибка подключения к OBS: {e}")

    def set_state(self, state):
        """Установка состояния PNG-тубера"""
        self.current_state = state
        self.update_display()
        
        # Отправка состояния в OBS
        if self.obs_connected:
            self.send_to_obs(state)

    def send_to_obs(self, state):
        """Отправка состояния в OBS Studio"""
        try:
            source_name = self.settings["obs_source_name"]
            
            # Проверяем существование источника
            try:
                response = self.obs_client.get_scene_item_list()
                # Здесь можно добавить логику поиска источника
            except:
                pass
            
            # Отправляем команду для смены изображения
            # В реальном приложении здесь должна быть логика обновления источника
            print(f"Отправлено в OBS: {state}")
            
        except Exception as e:
            print(f"Ошибка отправки в OBS: {e}")

    def update_display(self):
        """Обновление отображения текущего состояния"""
        state_names = {
            "silent": "Молчит",
            "talking": "Говорит",
            "muted": "Микрофон выключен"
        }
        
        self.state_label.config(text=f"Состояние: {state_names[self.current_state]}")
        
        # Обновление изображения
        if self.current_state in self.images and self.images[self.current_state]:
            self.image_label.config(image=self.images[self.current_state])
        else:
            self.image_label.config(image='')
            self.image_label.config(text=f"[Изображение не найдено: {self.current_state}.png]")

    def monitor_obs(self):
        """Мониторинг состояния OBS"""
        while self.running:
            if self.obs_connected:
                try:
                    # Получение информации о состоянии OBS
                    # Здесь можно добавить логику мониторинга
                    pass
                except:
                    self.obs_connected = False
                    self.root.after(0, lambda: self.status_label.config(
                        text="Статус: Соединение потеряно", 
                        fg='red'
                    ))
            
            time.sleep(2)

    def on_closing(self):
        """Обработка закрытия приложения"""
        self.running = False
        if self.obs_client:
            try:
                self.obs_client.disconnect()
            except:
                pass
        self.root.destroy()

def create_sample_images():
    """Создание примеров изображений для тестирования"""
    from PIL import ImageDraw
    
    states = {
        "silent": "red",  # Красный - молчит
        "talking": "green",  # Зеленый - говорит
        "muted": "gray"  # Серый - микрофон выключен
    }
    
    for state, color in states.items():
        img = PILImage.new('RGB', (400, 400), color)
        draw = ImageDraw.Draw(img)
        
        # Рисуем простое лицо
        draw.ellipse([100, 100, 300, 300], fill='white', outline='black', width=5)
        
        # Глаза
        draw.ellipse([150, 180, 190, 220], fill='black')
        draw.ellipse([210, 180, 250, 220], fill='black')
        
        # Рот (разный для разных состояний)
        if state == "silent":
            draw.line([170, 270, 230, 270], fill='black', width=3)
        elif state == "talking":
            draw.ellipse([160, 260, 240, 290], fill='black')
        else:  # muted
            draw.line([170, 280, 230, 280], fill='black', width=3)
            draw.line([160, 265, 240, 265], fill='red', width=5)
        
        img.save(f"{state}.png")
        print(f"Создано изображение: {state}.png")

if __name__ == "__main__":
    # Создание примеров изображений при первом запуске
    if not os.path.exists("silent.png") or not os.path.exists("talking.png") or not os.path.exists("muted.png"):
        create_sample_images()
        print("Созданы примеры изображений. Замените их на свои!")
    
    root = tk.Tk()
    app = PNGTuberApp(root)
    root.mainloop()
