import os
import sys
import ctypes
import shutil
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

TRACK_SLOTS = [
    ("579437", "01. 30 Seconds to Mars - Edge of the Earth"),
    ("579438", "02. Bad Religion - Resist Stance"),
    ("579439", "03. Benny Benassi feat. Kelis - Spaceship"),
    ("579440", "04. Black Rebel Motorcycle Club - Conscience Killer"),
    ("579441", "05. Chiddy Bang - Opposite of Adults"),
    ("579442", "06. Deadmau5 feat. Sofi - Sofi Needs a Ladder"),
    ("579443", "07. Does It Offend You, Yeah? - All the Same"),
    ("579444", "08. Funeral Party - Giant Song"),
    ("579445", "09. Greenskeepers - Live Like You Wanna Live"),
    ("579446", "10. Hadouken! - Bombshock"),
    ("579447", "11. Killa Kela - Get a Rise"),
    ("579448", "12. Klaxons - Echoes"),
    ("579449", "13. Klaxons - Twin Flames"),
    ("579450", "14. Lazee feat. Neverstore - Hold On"),
    ("579451", "15. Lemonade - Big Weekend"),
    ("579452", "16. Lupe Fiasco feat. Matthew Santos - Shining Down"),
    ("579454", "17. Maximum Balloon feat. Theophilus London - Groove Me"),
    ("579455", "18. M.I.A. - Born Free"),
    ("579456", "19. New Politics - Yeah Yeah Yeah"),
    ("579457", "20. Pendulum - Watercolour"),
    ("579458", "21. Plan B - Stay Too Long (Pendulum Remix)"),
    ("579459", "22. Teddybears - Devil's Music"),
    ("579460", "23. Travie McCoy - Superbad (11:34)"),
    ("579461", "24. We Have Band - Divisive (Tom Staar Remix)"),
    ("579462", "25. White Lies - Bigger Than Us"),
    ("579463", "26. Weezer - Ruling Me"),
    ("579465", "27. B.o.B feat. Bruno Mars - Nothing On You")
]

MONKEY_JOKE = """Купил мужик на рынке за 500 баксов обезьяну и захотел ее научить
разговаривать. Разговаривать не научил, а научил только одному слову
"конечно". Ну подумал нафиг надо такая обезьяна понес продавать на рынок
обратно. Ну подходит к нему мужик, спрашивает:
- Сколько стоит обезьяна
- 1000 баксов
- А че так дорого
- А она разговаривать умеет.
- Не пи...ди
- Подойди сам спроси
Ну тот подходит спрашивает:
- Ты разговаривать умеешь –??
Та:
- "конечно"
Мужик купил, принес домой, посадил на стол, спрашивает:
- Пить будешь?
Та:
- "конечно"
- Курить будешь?
- "конечно"
- Жрать будешь?
- "конечно"
- Жену еб..ть будешь?
- "конечно"
Ну подумал нафиг надо такая обезьяна понес продавать на рынок. Подходит
к нему бедный золотоискатель:
- Сколько стоит обезьяна
- 2000 баксов
- А че так дорого
- А она знает где клад лежит.
- Не пи..ди
- Подойди сам спроси
Ну тот подходит спрашивает:
- Ты знаешь где клад зарыт.
Та:
- "конечно"
Купил, принес домой посадил на стол раскрыл карту (пальцем в карту):
- Тут??
Та:
- "конечно"
Забрал обезьяну поехал на север, заехал чуть ли не на северный полюс.
Спрашивает тут копать:
- "конечно"
Разрыл сугроб
- А может глубже?
- "конечно"
- А может шире?
- "конечно"
- А может ты наеб...ешь?
- "конечно"
- А тебе пи..ды дать???
Та:
- НЕ НАДО..

steam id - 76561198274126708"""

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def set_dark_title_bar(window):
    try:
        window.update_idletasks()
        hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
        if hwnd == 0:
            hwnd = window.winfo_id()
        value = ctypes.c_int(1)
        # DWMWA_USE_IMMERSIVE_DARK_MODE (20 for Win11/new Win10, 19 for older Win10)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(value), ctypes.sizeof(value))
        ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 19, ctypes.byref(value), ctypes.sizeof(value))
        # Force DWM redraw so the white title bar does not flash on startup
        window.withdraw()
        window.deiconify()
        window.update()
    except Exception:
        pass

def apply_app_icon(window):
    try:
        icon_img = tk.PhotoImage(width=32, height=32)
        icon_img.put("#181b20", to=(0, 0, 32, 32))
        # Orange border
        icon_img.put("#ff6b00", to=(0, 0, 32, 2))
        icon_img.put("#ff6b00", to=(0, 30, 32, 32))
        icon_img.put("#ff6b00", to=(0, 0, 2, 32))
        icon_img.put("#ff6b00", to=(30, 0, 32, 32))
        # Equalizer bars
        icon_img.put("#ff6b00", to=(6, 16, 10, 26))
        icon_img.put("#ff6b00", to=(12, 9, 16, 26))
        icon_img.put("#ff6b00", to=(18, 13, 22, 26))
        icon_img.put("#ff6b00", to=(24, 6, 28, 26))
        window.iconphoto(True, icon_img)
        window._custom_icon = icon_img
    except Exception:
        pass

def draw_prostak_logo(parent, bg_color, click_callback=None):
    canvas = tk.Canvas(parent, width=84, height=58, bg=bg_color, highlightthickness=0,
                       cursor="hand2" if click_callback else "")
    color = "#969cf2"
    # Left raised eyebrow (chevron)
    canvas.create_line(10, 24, 24, 10, 37, 24, fill=color, width=3.2, capstyle="round", joinstyle="round")
    # Left eye
    canvas.create_oval(21, 22, 27, 32, fill=color, outline=color)
    # Right flat eyebrow
    canvas.create_line(51, 25, 66, 24, 75, 27, fill=color, width=3.2, capstyle="round", joinstyle="round")
    # Right eye
    canvas.create_oval(60, 29, 66, 39, fill=color, outline=color)
    # Mouth
    canvas.create_line(31, 48, 57, 48, fill=color, width=3.2, capstyle="round")

    if click_callback:
        canvas.bind("<Button-1>", lambda e: click_callback())
    return canvas

class ModernNFSMusicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NFS Hot Pursuit (2010) — Custom Soundtrack Studio")
        self.root.geometry("760x640")
        self.root.configure(bg="#121417")
        self.root.resizable(False, False)
        self.assigned_tracks = {}

        apply_app_icon(self.root)
        self.setup_styles()
        self.build_ui()
        set_dark_title_bar(self.root)

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Treeview",
                        background="#1c2026",
                        foreground="#e1e4e8",
                        fieldbackground="#1c2026",
                        rowheight=25,
                        borderwidth=0,
                        font=("Segoe UI", 9))
        style.configure("Treeview.Heading",
                        background="#252a32",
                        foreground="#ff6b00",
                        font=("Segoe UI", 9, "bold"),
                        borderwidth=0)
        style.map("Treeview", background=[("selected", "#2d3540")], foreground=[("selected", "#ffffff")])

        style.configure("Orange.Horizontal.TProgressbar",
                        troughcolor="#1c2026",
                        background="#ff6b00",
                        borderwidth=0,
                        thickness=8)

        style.configure("TNotebook", background="#121417", borderwidth=0)
        style.configure("TNotebook.Tab", background="#1c2026", foreground="#8b949e",
                        padding=[14, 6], font=("Segoe UI", 9, "bold"), borderwidth=0)
        style.map("TNotebook.Tab",
                  background=[("selected", "#252a32")],
                  foreground=[("selected", "#ff6b00")])

    def build_ui(self):
        header = tk.Frame(self.root, bg="#181b20", height=64)
        header.pack(fill="x")
        header.pack_propagate(False)

        title_block = tk.Frame(header, bg="#181b20")
        title_block.pack(side="left", padx=20, pady=8)

        top_title = tk.Frame(title_block, bg="#181b20")
        top_title.pack(anchor="w")
        tk.Label(top_title, text="NEED FOR SPEED: HOT PURSUIT", bg="#181b20", fg="#ff6b00",
                 font=("Segoe UI", 13, "bold")).pack(side="left")
        tk.Label(top_title, text="  • vibe coded edition", bg="#181b20", fg="#8b949e",
                 font=("Segoe UI", 9, "italic")).pack(side="left", pady=(3, 0))

        tk.Label(title_block, text="by prostak", bg="#181b20", fg="#969cf2",
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")

        tk.Button(header, text="ℹ Инфо", bg="#252a32", fg="#e1e4e8", activebackground="#323842",
                  activeforeground="#ffffff", relief="flat", font=("Segoe UI", 9, "bold"),
                  cursor="hand2", command=self.open_info_window, padx=14, pady=5).pack(side="right", padx=20)

        path_frame = tk.Frame(self.root, bg="#121417")
        path_frame.pack(fill="x", padx=20, pady=(14, 8))
        tk.Label(path_frame, text="ПАПКА С ИГРОЙ (КОРНЕВАЯ ДИРЕКТОРИЯ):", bg="#121417", fg="#8b949e",
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", pady=(0, 4))

        input_row = tk.Frame(path_frame, bg="#121417")
        input_row.pack(fill="x")
        self.game_path_var = tk.StringVar()
        entry = tk.Entry(input_row, textvariable=self.game_path_var, bg="#1c2026", fg="#ffffff",
                         insertbackground="white", relief="flat", font=("Segoe UI", 10))
        entry.pack(side="left", fill="x", expand=True, ipady=5, padx=(0, 8))

        tk.Button(input_row, text="Обзор...", bg="#252a32", fg="#ffffff", activebackground="#323842",
                  activeforeground="#ffffff", relief="flat", font=("Segoe UI", 9, "bold"),
                  cursor="hand2", command=self.browse_game, padx=15, pady=4).pack(side="right")

        list_header = tk.Frame(self.root, bg="#121417")
        list_header.pack(fill="x", padx=20, pady=(4, 4))
        tk.Label(list_header, text="ВЫБЕРИТЕ СЛОТ ДЛЯ ЗАМЕНЫ (ДВОЙНОЙ КЛИК ПО СТРОКЕ):",
                 bg="#121417", fg="#8b949e", font=("Segoe UI", 8, "bold")).pack(side="left")
        self.count_label = tk.Label(list_header, text="Назначено треков: 0 / 27", bg="#121417", fg="#ff6b00",
                                    font=("Segoe UI", 8, "bold"))
        self.count_label.pack(side="right")

        tree_frame = tk.Frame(self.root, bg="#1c2026", height=310)
        tree_frame.pack(fill="x", padx=20)
        tree_frame.pack_propagate(False)

        columns = ("id", "original", "custom")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse", height=11)
        self.tree.heading("id", text="ID Файла")
        self.tree.heading("original", text="Оригинальный трек в игре")
        self.tree.heading("custom", text="Ваш новый трек (MP3)")

        self.tree.column("id", width=80, anchor="center")
        self.tree.column("original", width=310, anchor="w")
        self.tree.column("custom", width=305, anchor="w")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<Double-1>", self.on_double_click)
        self.populate_tree()

        ctrl_frame = tk.Frame(self.root, bg="#121417")
        ctrl_frame.pack(fill="x", padx=20, pady=(10, 4))

        btn_style = {"bg": "#252a32", "fg": "#e1e4e8", "activebackground": "#323842",
                     "activeforeground": "#ffffff", "relief": "flat", "font": ("Segoe UI", 9),
                     "cursor": "hand2", "padx": 10, "pady": 4}

        tk.Button(ctrl_frame, text="Назначить трек на выбранный слот", command=self.assign_single, **btn_style).pack(side="left", padx=(0, 6))
        tk.Button(ctrl_frame, text="Убрать выбранный", command=self.remove_single, **btn_style).pack(side="left", padx=(0, 6))
        tk.Button(ctrl_frame, text="Заполнить пачкой (авто)", command=self.assign_batch, **btn_style).pack(side="left", padx=(0, 6))
        tk.Button(ctrl_frame, text="Очистить всё", command=self.clear_all, **btn_style).pack(side="right")

        bottom_frame = tk.Frame(self.root, bg="#181b20", pady=12, padx=20)
        bottom_frame.pack(fill="x", side="bottom")

        top_bottom = tk.Frame(bottom_frame, bg="#181b20")
        top_bottom.pack(fill="x", pady=(0, 8))

        self.backup_var = tk.BooleanVar(value=True)
        chk = tk.Checkbutton(top_bottom, text="Делать резервную копию оригиналов (папка BACKUP)",
                             variable=self.backup_var, bg="#181b20", fg="#c9d1d9",
                             selectcolor="#121417", activebackground="#181b20",
                             activeforeground="#ffffff", font=("Segoe UI", 9))
        chk.pack(side="left")

        tk.Button(top_bottom, text="Восстановить оригиналы из BACKUP", bg="#252a32", fg="#8b949e",
                  activebackground="#323842", activeforeground="#ffffff", relief="flat",
                  font=("Segoe UI", 8), cursor="hand2", command=self.restore_backup, padx=8, pady=2).pack(side="right")

        self.progress = ttk.Progressbar(bottom_frame, orient="horizontal", mode="determinate",
                                        style="Orange.Horizontal.TProgressbar")
        self.progress.pack(fill="x", pady=(0, 8))

        action_row = tk.Frame(bottom_frame, bg="#181b20")
        action_row.pack(fill="x")

        self.status_label = tk.Label(action_row, text="Готов к работе. Выберите папку игры и нужные слоты.",
                                     bg="#181b20", fg="#8b949e", font=("Segoe UI", 9))
        self.status_label.pack(side="left")

        self.start_btn = tk.Button(action_row, text="УСТАНОВИТЬ В ИГРУ", bg="#ff6b00", fg="#ffffff",
                                   activebackground="#e05e00", activeforeground="#ffffff",
                                   relief="flat", font=("Segoe UI", 10, "bold"), cursor="hand2",
                                   padx=20, pady=6, command=self.start_thread)
        self.start_btn.pack(side="right")

    def open_info_window(self):
        info_win = tk.Toplevel(self.root)
        info_win.title("О программе и инструкция")
        info_win.geometry("680x590")
        info_win.configure(bg="#121417")
        info_win.resizable(False, False)
        info_win.transient(self.root)
        info_win.grab_set()

        notebook = ttk.Notebook(info_win)
        notebook.pack(fill="both", expand=True, padx=16, pady=(14, 6))

        # --- Вкладка 1: Управление и кнопки ---
        page1 = tk.Frame(notebook, bg="#181b20", padx=16, pady=14)
        notebook.add(page1, text="  Управление и кнопки  ")

        warn_box = tk.Frame(page1, bg="#261c15", highlightbackground="#ff6b00", highlightthickness=1, padx=12, pady=8)
        warn_box.pack(fill="x", pady=(0, 12))
        tk.Label(warn_box, text="⚠ ВНИМАНИЕ ПО ТРЕКЛИСТУ:", bg="#261c15", fg="#ff6b00",
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        tk.Label(warn_box,
                 text="Оригинальные названия треков в таблице не тестировались по каждому отдельному файлу. Реальная песня на конкретном ID может отличаться от названия в таблице (но все 27 ID-номеров 100% рабочие).",
                 bg="#261c15", fg="#e1e4e8", font=("Segoe UI", 8), justify="left", wraplength=585).pack(anchor="w", pady=(2, 0))

        buttons_desc = [
            ("Обзор...:", "Выбор корневой папки Need for Speed Hot Pursuit (внутри должна быть папка UI\\SONGS)."),
            ("Двойной клик / Назначить трек:", "Привязывает выбранный MP3-файл к конкретному игровому слоту (от 1 до 27)."),
            ("Убрать выбранный:", "Снимает назначенный трек с выделенной строки в таблице."),
            ("Заполнить пачкой (авто):", "Позволяет выделить сразу до 27 MP3-файлов и раскидать их по порядку."),
            ("Очистить всё:", "Сбрасывает все выбранные треки в таблице."),
            ("Галочка резервной копии:", "Автоматически сохраняет родные файлы игры в UI\\SONGS\\BACKUP перед заменой."),
            ("Восстановить оригиналы:", "Возвращает стандартные треки игры обратно из папки BACKUP в один клик."),
            ("УСТАНОВИТЬ В ИГРУ:", "Запускает конвертацию в формат .SPS и копирует файлы в папку игры.")
        ]

        for b_name, b_text in buttons_desc:
            row = tk.Frame(page1, bg="#181b20")
            row.pack(fill="x", pady=3)
            tk.Label(row, text=f"• {b_name}", bg="#181b20", fg="#ff6b00", width=28, anchor="w",
                     font=("Segoe UI", 8, "bold")).pack(side="left", anchor="n")
            tk.Label(row, text=b_text, bg="#181b20", fg="#c9d1d9", anchor="w", justify="left",
                     wraplength=410, font=("Segoe UI", 8)).pack(side="left", fill="x", expand=True)

        # --- Вкладка 2: Как это работает и файлы проекта ---
        page2 = tk.Frame(notebook, bg="#181b20", padx=16, pady=14)
        notebook.add(page2, text="  Как это работает и файлы проекта  ")

        vibe_box = tk.Frame(page2, bg="#181d2b", highlightbackground="#969cf2", highlightthickness=1, padx=12, pady=8)
        vibe_box.pack(fill="x", pady=(0, 12))
        tk.Label(vibe_box, text="⚡ ЧУДО ВАЙБКОДИНГА", bg="#181d2b", fg="#969cf2",
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        tk.Label(vibe_box,
                 text="Эта утилита — настоящее чудо вайбкодинга от prostak и ИИ. Мы долго запаривались, копались в старых форматах и перебирали ключи официальных утилит EA, чтобы всё работало без вылетов и кривого звука.",
                 bg="#181d2b", fg="#e1e4e8", font=("Segoe UI", 8), justify="left", wraplength=585).pack(anchor="w", pady=(2, 0))

        tech_items = [
            ("Как происходит магия:", "Скрипт чистит ваши MP3 от обложек и тегов, выравнивает частоту до 44100 Гц и пересобирает в родной контейнер движка Chameleon (.SPS) с правильным заголовком."),
            ("app.py / EXE-оболочка:", "Графический интерфейс на Python, который управляет очередью файлов, бэкапами и запускает конвертеры в фоне."),
            ("ffmpeg.exe:", "Универсальный аудиоконвертер — вырезает лишние метаданные и подгоняет битрейт, чтобы движок игры не крашился."),
            ("sx.exe (Sound eXchange):", "Официальный компилятор звука Electronic Arts — упаковывает чистый MP3 в игровой формат .SPS (кодек ealayer3_int)."),
            ("eaxmaenc / libatrac9 / libmp3lame.dll:", "Обязательные системные библиотеки, без которых утилита sx.exe не сможет кодировать звук.")
        ]

        for t_name, t_text in tech_items:
            row = tk.Frame(page2, bg="#181b20")
            row.pack(fill="x", pady=4)
            tk.Label(row, text=f"▪ {t_name}", bg="#181b20", fg="#ff6b00", width=28, anchor="w",
                     font=("Segoe UI", 8, "bold")).pack(side="left", anchor="n")
            tk.Label(row, text=t_text, bg="#181b20", fg="#c9d1d9", anchor="w", justify="left",
                     wraplength=410, font=("Segoe UI", 8)).pack(side="left", fill="x", expand=True)

        # Нижняя часть с логотипом prostak и кнопкой закрытия
        footer_frame = tk.Frame(info_win, bg="#121417")
        footer_frame.pack(fill="x", pady=(4, 12))

        logo_canvas = draw_prostak_logo(footer_frame, "#121417", click_callback=lambda: self.open_joke_window(info_win))
        logo_canvas.pack()

        nick_lbl = tk.Label(footer_frame, text="prostak", bg="#121417", fg="#969cf2",
                            font=("Segoe UI", 9, "bold"), cursor="hand2")
        nick_lbl.pack(pady=(0, 8))
        nick_lbl.bind("<Button-1>", lambda e: self.open_joke_window(info_win))

        tk.Button(footer_frame, text="Понятно, закрыть", bg="#252a32", fg="#ffffff",
                  activebackground="#323842", activeforeground="#ffffff", relief="flat",
                  font=("Segoe UI", 9, "bold"), cursor="hand2", padx=24, pady=5,
                  command=info_win.destroy).pack()

        set_dark_title_bar(info_win)

    def open_joke_window(self, parent_win):
        joke_win = tk.Toplevel(parent_win)
        joke_win.title("Базовый анекдот про обезьяну")
        joke_win.geometry("500x540")
        joke_win.configure(bg="#121417")
        joke_win.resizable(False, False)
        joke_win.transient(parent_win)
        joke_win.grab_set()

        tk.Label(joke_win, text="Базовый анекдот про обезьяну", bg="#121417", fg="#969cf2",
                 font=("Segoe UI", 11, "bold")).pack(pady=(12, 6))

        text_frame = tk.Frame(joke_win, bg="#181b20", padx=12, pady=10)
        text_frame.pack(fill="both", expand=True, padx=16, pady=(0, 10))

        txt = tk.Text(text_frame, bg="#181b20", fg="#e1e4e8", font=("Segoe UI", 9),
                      relief="flat", wrap="word", highlightthickness=0)
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=txt.yview)
        txt.configure(yscrollcommand=scrollbar.set)

        txt.insert("1.0", MONKEY_JOKE)
        txt.config(state="disabled")

        txt.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        tk.Button(joke_win, text="Понятно, закрыть", bg="#252a32", fg="#ffffff",
                  activebackground="#323842", activeforeground="#ffffff", relief="flat",
                  font=("Segoe UI", 9, "bold"), cursor="hand2", padx=24, pady=5,
                  command=joke_win.destroy).pack(pady=(0, 12))

        set_dark_title_bar(joke_win)

    def populate_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for tid, orig_name in TRACK_SLOTS:
            custom_name = "- [Не изменено]"
            if tid in self.assigned_tracks:
                custom_name = "> " + os.path.basename(self.assigned_tracks[tid])
            self.tree.insert("", tk.END, iid=tid, values=(tid, orig_name, custom_name))
        self.count_label.config(text=f"Назначено треков: {len(self.assigned_tracks)} / 27")

    def browse_game(self):
        folder = filedialog.askdirectory(title="Выберите корневую папку Need for Speed Hot Pursuit")
        if folder:
            self.game_path_var.set(folder)

    def on_double_click(self, event):
        self.assign_single()

    def assign_single(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Подсказка", "Сначала кликните по нужной строке трека в таблице!")
            return
        tid = selected[0]
        file_path = filedialog.askopenfilename(title=f"Выберите MP3 для слота {tid}")
        if file_path and file_path.lower().endswith(".mp3"):
            self.assigned_tracks[tid] = file_path
            self.populate_tree()
            self.tree.selection_set(tid)

    def remove_single(self):
        selected = self.tree.selection()
        if selected and selected[0] in self.assigned_tracks:
            del self.assigned_tracks[selected[0]]
            self.populate_tree()

    def assign_batch(self):
        files = filedialog.askopenfilenames(title="Выберите до 27 MP3 файлов")
        if not files:
            return
        mp3_list = [f for f in files if f.lower().endswith(".mp3")]
        self.assigned_tracks.clear()
        for idx, f in enumerate(mp3_list[:27]):
            tid = TRACK_SLOTS[idx][0]
            self.assigned_tracks[tid] = f
        self.populate_tree()

    def clear_all(self):
        self.assigned_tracks.clear()
        self.populate_tree()

    def restore_backup(self):
        game_dir = self.game_path_var.get().strip()
        songs_dir = os.path.join(game_dir, "UI", "SONGS")
        backup_dir = os.path.join(songs_dir, "BACKUP")
        if not os.path.exists(backup_dir):
            messagebox.showerror("Ошибка", "Папка BACKUP не найдена в UI\\SONGS!")
            return
        restored = 0
        for tid, _ in TRACK_SLOTS:
            bkp = os.path.join(backup_dir, f"{tid}.SPS")
            orig = os.path.join(songs_dir, f"{tid}.SPS")
            if os.path.exists(bkp):
                shutil.copy2(bkp, orig)
                restored += 1
        messagebox.showinfo("Готово", f"Успешно возвращено оригинальных треков: {restored}")

    def start_thread(self):
        game_dir = self.game_path_var.get().strip()
        songs_dir = os.path.join(game_dir, "UI", "SONGS")
        if not os.path.exists(songs_dir):
            messagebox.showerror("Ошибка", "Не найдена папка UI\\SONGS! Укажите правильную папку с игрой.")
            return
        if not self.assigned_tracks:
            messagebox.showwarning("Внимание", "Вы не назначили ни одного трека для замены!")
            return
        self.start_btn.config(state="disabled")
        threading.Thread(target=self.convert_and_install, args=(songs_dir,), daemon=True).start()

    def convert_and_install(self, songs_dir):
        temp_dir = os.path.join(os.environ["TEMP"], "nfs_hp_music_temp")
        os.makedirs(temp_dir, exist_ok=True)
        ffmpeg_exe = get_resource_path("ffmpeg.exe")
        sx_exe = get_resource_path("sx.exe")

        if self.backup_var.get():
            backup_dir = os.path.join(songs_dir, "BACKUP")
            os.makedirs(backup_dir, exist_ok=True)
            for tid in self.assigned_tracks.keys():
                orig = os.path.join(songs_dir, f"{tid}.SPS")
                bkp = os.path.join(backup_dir, f"{tid}.SPS")
                if os.path.exists(orig) and not os.path.exists(bkp):
                    shutil.copy2(orig, bkp)

        items = list(self.assigned_tracks.items())
        total = len(items)
        self.progress["maximum"] = total
        self.progress["value"] = 0

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        for idx, (tid, mp3_path) in enumerate(items):
            self.status_label.config(text=f"Сборка [{idx+1}/{total}]: {os.path.basename(mp3_path)} -> {tid}.SPS", fg="#ff6b00")
            clean_mp3 = os.path.join(temp_dir, f"{tid}.mp3")
            out_sps = os.path.join(temp_dir, f"{tid}.sps")

            subprocess.run([ffmpeg_exe, "-y", "-loglevel", "error", "-i", mp3_path, "-map_metadata", "-1", "-vn", "-ar", "44100", "-ac", "2", "-b:a", "192k", clean_mp3], startupinfo=startupinfo)
            subprocess.run([sx_exe, "-sndplayer", "-fileformatversion1", "-ealayer3_int", "-vbr100", f"{tid}.mp3", f"-={tid}"], cwd=temp_dir, startupinfo=startupinfo)

            if os.path.exists(out_sps):
                shutil.copy2(out_sps, os.path.join(songs_dir, f"{tid}.SPS"))
            self.progress["value"] = idx + 1

        shutil.rmtree(temp_dir, ignore_errors=True)
        self.status_label.config(text=f"Готово! Успешно заменено треков: {total}.", fg="#2ea043")
        self.start_btn.config(state="normal")
        messagebox.showinfo("Успех", f"Установка завершена! Заменено треков: {total}.\nМожно запускать игру.")

if __name__ == "__main__":
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("prostak.nfshp2010.musicinstaller.1.0")
    except Exception:
        pass
    root = tk.Tk()
    app = ModernNFSMusicApp(root)
    root.mainloop()
