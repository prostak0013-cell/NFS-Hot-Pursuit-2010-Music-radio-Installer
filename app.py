import os
import sys
import shutil
import subprocess
import threading
import ctypes
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Уникальный ID приложения для корректной иконки на панели задач Windows
try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("prostak.nfshp.musicinstaller.2.0")
except Exception:
    pass

TRACK_SLOTS = [
    ("259196", "[SYS] Тема погони 1 (Pursuit Theme 1)"),
    ("265817", "[SYS] Тема гаража гонщика (Racer Garage)"),
    ("265818", "[SYS] Тема гаража копов (Cop Garage)"),
    ("579205", "[SYS] Тема погони 2 (Pursuit Theme 2)"),
    ("579235", "[SYS] Тема погони 3 (Pursuit Theme 3)"),
    ("579236", "[SYS] Тема погони 4 (Pursuit Theme 4)"),
    ("579437", "01. 30 Seconds to Mars - Edge of the Earth"),
    ("579438", "02. Bad Religion - The Resist Stance"),
    ("579439", "03. Benny Benassi, Garry Go - Cinema (Radio Edit)"),
    ("579440", "04. Black Rebel Motorcycle Club - Conscience Killer"),
    ("579441", "05. Chiddy Bang - Opposite of Adults"),
    ("579442", "06. Deadmau5, Sofi - Sofi Needs A Ladder"),
    ("579443", "07. Does It Offend You, Yeah? - All The Same"),
    ("579444", "08. Funeral Party - Giant Song"),
    ("579445", "09. Greenskeepers - Live Like You Wanna Live"),
    ("579446", "10. Hadouken! - Bombshock"),
    ("579447", "11. Killa Kela - Get A Rise"),
    ("579448", "12. Klaxons - Echoes"),
    ("579449", "13. Klaxons - Twin Flames"),
    ("579450", "14. Lazee ft. Dead By April - Stronger"),
    ("579451", "15. Lemonade - Big Weekend"),
    ("579452", "16. Lupe Fiasco, Matthew Santos - Shining Down"),
    ("579454", "17. Maximum Balloon, Theophilus London - Groove Me"),
    ("579455", "18. M.I.A. - Born Free"),
    ("579456", "19. New Politics - Yeah Yeah Yeah"),
    ("579457", "20. Pendulum - Watercolour"),
    ("579458", "21. Pint Shot Riot - Nothing From You (Redanka Remix)"),
    ("579459", "22. Plan B, Pendulum - Stay Too Long (Pendulum Remix)"),
    ("579460", "23. Teddybears feat. ADL - Devil's Music"),
    ("579461", "24. Travie McCoy - Superbad (11:34)"),
    ("579462", "25. We Have Band - Divisive (Tom Staar Remix)"),
    ("579463", "26. White Lies - Bigger Than Us"),
    ("579465", "27. Weezer - Ruling Me"),
    ("579470", "[SYS] Тема погони 5 (Pursuit Theme 5)"),
    ("579471", "[SYS] Тема погони 6 (Pursuit Theme 6)"),
    ("579697", "[SYS] Главная тема меню (Main Menu Theme)")
]

RADIO_IDS = [
    "579437", "579438", "579439", "579440", "579441", "579442", "579443",
    "579444", "579445", "579446", "579447", "579448", "579449", "579450",
    "579451", "579452", "579454", "579455", "579456", "579457", "579458",
    "579459", "579460", "579461", "579462", "579463", "579465"
]

TEXTS = {
    "ru": {
        "title": "NFS Hot Pursuit (2010 / Remastered) — Custom Soundtrack Studio",
        "subtitle": "CUSTOM RADIO & AUDIO INSTALLER",
        "info_btn": "ℹ Инфо",
        "lang_btn": "EN",
        "game_path_lbl": "ПАПКА С ИГРОЙ (КОРНЕВАЯ ИЛИ UI\\SONGS):",
        "browse_btn": "Обзор...",
        "browse_title": "Выберите корневую папку Need for Speed Hot Pursuit",
        "select_slot_lbl": "ВЫБЕРИТЕ СЛОТ ДЛЯ ЗАМЕНЫ (ДВОЙНОЙ КЛИК ПО СТРОКЕ):",
        "assigned_lbl": "Назначено треков: {count} / {total}",
        "col_id": "ID Файла",
        "col_orig": "Оригинальный трек в игре",
        "col_custom": "Ваш новый трек (MP3)",
        "not_changed": "— [Не изменено]",
        "btn_assign": "Назначить на слот",
        "btn_remove": "Убрать выбранный",
        "btn_batch": "Заполнить радио пачкой (27)",
        "btn_clear": "Очистить всё",
        "chk_backup": "Делать резервную копию оригиналов (папка BACKUP)",
        "btn_restore": "Восстановить оригиналы из BACKUP",
        "status_ready": "Готов к работе. Поддерживается оригинал 2010 и Remastered.",
        "btn_install": "УСТАНОВИТЬ В ИГРУ",
        "hint_title": "Подсказка",
        "hint_select": "Сначала кликните по нужной строке в таблице!",
        "dlg_single": "Выберите MP3 для слота {tid}",
        "dlg_batch": "Выберите до 27 MP3-файлов для радио",
        "err_title": "Ошибка",
        "err_no_songs": "Не найдена папка UI\\SONGS! Укажите правильную папку с игрой.",
        "err_no_backup": "Папка BACKUP не найдена в UI\\SONGS!",
        "warn_title": "Внимание",
        "warn_no_tracks": "Вы не назначили ни одного трека для замены!",
        "restore_title": "Восстановление завершено",
        "restore_msg": "Успешно возвращено оригинальных треков: {count}",
        "status_build": "Сборка [{cur}/{total}]: {name} -> {tid}.SPS",
        "status_done": "Готово! Успешно заменено треков: {total}.",
        "success_title": "Успех",
        "success_msg": "Установка завершена! Заменено треков: {total}.\nМожно запускать игру.",
        "info_win_title": "Справка и устройство программы",
        "tab_controls": "Управление и о проекте",
        "tab_arch": "Как это устроено внутри",
        "vibe_title": "⚡ ЧУДО ВАЙБКОДИНГА",
        "vibe_text": (
            "Эта программа — настоящее чудо вайбкодинга от prostak и ИИ.\n"
            "Мы долго ковырялись в движке EA и перебирали кодеки, пока не нашли\n"
            "единственно верную связку утилит, чтобы игра принимала кастомные\n"
            "треки без вылетов и заиканий звука."
        ),
        "controls_header": "Описание кнопок и элементов интерфейса:",
        "controls_list": [
            ("Обзор...", "Выбор корневой папки игры или сразу папки UI\\SONGS."),
            ("Двойной клик / Назначить на слот", "Выбор своего MP3-файла для конкретного слота радио, меню или погони."),
            ("Заполнить радио пачкой (27)", "Автоматически заполняет только 27 слотов радио, не трогая меню и погони."),
            ("Убрать выбранный / Очистить всё", "Сбрасывает назначенный трек с одной строки или очищает весь список."),
            ("Галочка резервной копии", "Автоматически сохраняет родные файлы в UI\\SONGS\\BACKUP перед заменой."),
            ("Восстановить оригиналы", "Возвращает заводские треки из папки BACKUP обратно в игру в один клик.")
        ],
        "arch_header": "Как работает конвертация и зачем нужны файлы:",
        "arch_blocks": [
            ("1. Зачем нужен FFmpeg (ffmpeg.exe)",
             "Движок игры вылетает от обложек альбомов, длинных ID3-тегов и нестандартной частоты. FFmpeg на лету вырезает весь мусор и переводит МР3 в чистый поток 44100 Гц, стерео, 192 кбит/с."),
            ("2. Зачем нужен Sound eXchange (sx.exe)",
             "Официальный компилятор EA. С флагами -sndplayer -fileformatversion1 -ealayer3_int -vbr100 он упаковывает звук в родной игровой контейнер .SPS (EA Layer 3 v6)."),
            ("3. Зачем нужны библиотеки (.dll)",
             "Файлы eaxmaenc.dll, libatrac9.dll и libmp3lame.dll — кодеки, без которых sx.exe не сможет кодировать аудиопоток."),
            ("4. Как работает автономный .exe (PyInstaller)",
             "При запуске утилита распаковывает вшитые инструменты во временную папку TEMP, перегоняет треки, копирует .SPS в UI\\SONGS и подчищает за собой мусор.")
        ],
        "btn_close": "Закрыть",
        "joke_title": "Базовый анекдот про обезьяну",
        "joke_btn": "Понятно, закрыть"
    },
    "en": {
        "title": "NFS Hot Pursuit (2010 / Remastered) — Custom Soundtrack Studio",
        "subtitle": "CUSTOM RADIO & AUDIO INSTALLER",
        "info_btn": "ℹ Info",
        "lang_btn": "RU",
        "game_path_lbl": "GAME DIRECTORY (ROOT FOLDER OR UI\\SONGS):",
        "browse_btn": "Browse...",
        "browse_title": "Select Need for Speed Hot Pursuit root folder",
        "select_slot_lbl": "SELECT A SLOT TO REPLACE (DOUBLE-CLICK A ROW):",
        "assigned_lbl": "Assigned tracks: {count} / {total}",
        "col_id": "File ID",
        "col_orig": "Original In-Game Track",
        "col_custom": "Your Custom Track (MP3)",
        "not_changed": "— [Not modified]",
        "btn_assign": "Assign to Slot",
        "btn_remove": "Remove Selected",
        "btn_batch": "Batch Fill Radio (27)",
        "btn_clear": "Clear All",
        "chk_backup": "Backup original tracks before replacing (BACKUP folder)",
        "btn_restore": "Restore Originals from BACKUP",
        "status_ready": "Ready. Supports both 2010 Original and Remastered.",
        "btn_install": "INSTALL TO GAME",
        "hint_title": "Hint",
        "hint_select": "Please click on a track row in the table first!",
        "dlg_single": "Select MP3 for slot {tid}",
        "dlg_batch": "Select up to 27 MP3 files for radio",
        "err_title": "Error",
        "err_no_songs": "UI\\SONGS folder not found! Please select the valid game directory.",
        "err_no_backup": "BACKUP folder not found inside UI\\SONGS!",
        "warn_title": "Warning",
        "warn_no_tracks": "You haven't assigned any tracks to replace!",
        "restore_title": "Restore Complete",
        "restore_msg": "Successfully restored original tracks: {count}",
        "status_build": "Building [{cur}/{total}]: {name} -> {tid}.SPS",
        "status_done": "Done! Successfully replaced tracks: {total}.",
        "success_title": "Success",
        "success_msg": "Installation complete! Replaced tracks: {total}.\nYou can launch the game now.",
        "info_win_title": "Help & Architecture",
        "tab_controls": "Controls & About",
        "tab_arch": "How It Works Under the Hood",
        "vibe_title": "⚡ MIRACLE OF VIBE-CODING",
        "vibe_text": (
            "This tool is a true miracle of vibe-coding by prostak and AI.\n"
            "We dug deep into EA's engine and tested codecs until we found\n"
            "the exact toolchain flags so the game plays custom tracks\n"
            "without crashes or audio stuttering."
        ),
        "controls_header": "Buttons & Interface Controls:",
        "controls_list": [
            ("Browse...", "Select the game root folder or directly the UI\\SONGS folder."),
            ("Double-click / Assign to Slot", "Pick a custom MP3 file for a specific radio, menu, or pursuit slot."),
            ("Batch Fill Radio (27)", "Automatically fills only the 27 radio slots, leaving menu/pursuit intact."),
            ("Remove Selected / Clear All", "Clears the assigned track from a single row or resets the entire list."),
            ("Backup checkbox", "Automatically saves original files to UI\\SONGS\\BACKUP before replacing."),
            ("Restore Originals", "Reverts factory tracks from the BACKUP folder back into the game in one click.")
        ],
        "arch_header": "How Conversion Works & Purpose of Files:",
        "arch_blocks": [
            ("1. Why FFmpeg (ffmpeg.exe) is needed",
             "The game engine crashes on album covers, long ID3 tags, and non-standard sample rates. FFmpeg strips metadata and converts MP3s to clean 44100 Hz, stereo, 192 kbps."),
            ("2. Why Sound eXchange (sx.exe) is needed",
             "Official EA compiler. Using -sndplayer -fileformatversion1 -ealayer3_int -vbr100 flags, it packs audio into the native .SPS container (EA Layer 3 v6)."),
            ("3. Why Libraries (.dll) are needed",
             "eaxmaenc.dll, libatrac9.dll, and libmp3lame.dll are required audio codecs used by sx.exe to encode the stream."),
            ("4. How the standalone .exe works (PyInstaller)",
             "On launch, the app unpacks bundled tools to TEMP, converts tracks, copies .SPS files to UI\\SONGS, and cleans up temporary files.")
        ],
        "btn_close": "Close",
        "joke_title": "Classic Monkey Joke",
        "joke_btn": "Got it, close"
    }
}

JOKE_TEXT = (
    "Купил мужик на рынке за 500 баксов обезьяну и захотел ее научить\n"
    "разговаривать. Разговаривать не научил, а научил только одному слову\n"
    "\"конечно\". Ну подумал нафиг надо такая обезьяна понес продавать на рынок\n"
    "обратно. Ну подходит к нему мужик, спрашивает:\n"
    "- Сколько стоит обезьяна\n"
    "- 1000 баксов\n"
    "- А че так дорого\n"
    "- А она разговаривать умеет.\n"
    "- Не пи...ди\n"
    "- Подойди сам спроси\n"
    "Ну тот подходит спрашивает:\n"
    "- Ты разговаривать умеешь –??\n"
    "Та:\n"
    "- \"конечно\"\n"
    "Мужик купил, принес домой, посадил на стол, спрашивает:\n"
    "- Пить будешь?\n"
    "Та:\n"
    "- \"конечно\"\n"
    "- Курить будешь?\n"
    "- \"конечно\"\n"
    "- Жрать будешь?\n"
    "- \"конечно\"\n"
    "- Жену еб..ть будешь?\n"
    "- \"конечно\"\n"
    "Ну подумал нафиг надо такая обезьяна понес продавать на рынок. Подходит\n"
    "к нему бедный золотоискатель:\n"
    "- Сколько стоит обезьяна\n"
    "- 2000 баксов\n"
    "- А че так дорого\n"
    "- А она знает где клад лежит.\n"
    "- Не пи..ди\n"
    "- Подойди сам спроси\n"
    "Ну тот подходит спрашивает:\n"
    "- Ты знаешь где клад зарыт.\n"
    "Та:\n"
    "- \"конечно\"\n"
    "Купил, принес домой посадил на стол раскрыл карту (пальцем в карту):\n"
    "- Тут??\n"
    "Та:\n"
    "- \"конечно\"\n"
    "Забрал обезьяну поехал на север, заехал чуть ли не на северный полюс.\n"
    "Спрашивает тут копать:\n"
    "- \"конечно\"\n"
    "Разрыл сугроб\n"
    "- А может глубже?\n"
    "- \"конечно\"\n"
    "- А может шире?\n"
    "- \"конечно\"\n"
    "- А может ты наеб...еш?\n"
    "- \"конечно\"\n"
    "- А тебе пи..ды дать???\n"
    "Та:\n"
    "- НЕ НАДО..\n\n"
    "steam id - 76561198274126708"
)


def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def set_dark_title_bar(window, instant_refresh=False):
    try:
        window.update_idletasks()
        hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
        if hwnd == 0:
            hwnd = window.winfo_id()
        value = ctypes.c_int(2)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(value), ctypes.sizeof(value))
        ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 19, ctypes.byref(value), ctypes.sizeof(value))
        if instant_refresh:
            window.withdraw()
            window.deiconify()
    except Exception:
        pass


def create_app_icon():
    img = tk.PhotoImage(width=32, height=32)
    img.put("#121417", to=(0, 0, 32, 32))
    img.put("#ff6b00", to=(2, 2, 30, 4))
    img.put("#ff6b00", to=(2, 28, 30, 30))
    img.put("#ff6b00", to=(2, 2, 4, 30))
    img.put("#ff6b00", to=(28, 2, 30, 30))
    img.put("#ff6b00", to=(7, 16, 11, 25))
    img.put("#ffffff", to=(14, 8, 18, 25))
    img.put("#969cf2", to=(21, 12, 25, 25))
    return img


class ModernNFSMusicApp:
    def __init__(self, root):
        self.root = root
        self.lang = "ru"
        self.root.geometry("780x640")
        self.root.configure(bg="#121417")
        self.root.resizable(False, False)

        self.app_icon = create_app_icon()
        self.root.iconphoto(True, self.app_icon)

        self.assigned_tracks = {}
        self.is_running = False

        self.setup_styles()
        self.build_ui()
        self.apply_language()
        set_dark_title_bar(self.root, instant_refresh=True)

    def t(self, key):
        return TEXTS[self.lang][key]

    def resolve_songs_dir(self):
        raw_path = os.path.normpath(self.game_path_var.get().strip())
        if not raw_path or raw_path == ".":
            return None
        # Если пользователь указал сразу папку UI\SONGS
        if os.path.basename(raw_path).upper() == "SONGS" and os.path.exists(raw_path):
            return raw_path
        # Если пользователь указал папку UI
        if os.path.basename(raw_path).upper() == "UI":
            candidate = os.path.join(raw_path, "SONGS")
            if os.path.exists(candidate):
                return candidate
        # Стандартный случай: корневая папка игры
        candidate = os.path.join(raw_path, "UI", "SONGS")
        if os.path.exists(candidate):
            return candidate
        return None

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#1c2026", foreground="#e1e4e8",
                        fieldbackground="#1c2026", rowheight=25, borderwidth=0, font=("Segoe UI", 9))
        style.configure("Treeview.Heading", background="#252a32", foreground="#ff6b00",
                        font=("Segoe UI", 9, "bold"), borderwidth=0)
        style.map("Treeview", background=[("selected", "#2d3540")], foreground=[("selected", "#ffffff")])
        style.configure("Orange.Horizontal.TProgressbar", troughcolor="#1c2026",
                        background="#ff6b00", borderwidth=0, thickness=8)
        style.configure("TNotebook", background="#181b20", borderwidth=0)
        style.configure("TNotebook.Tab", background="#252a32", foreground="#c9d1d9",
                        padding=[14, 6], font=("Segoe UI", 9, "bold"))
        style.map("TNotebook.Tab", background=[("selected", "#ff6b00")], foreground=[("selected", "#ffffff")])

    def build_ui(self):
        header = tk.Frame(self.root, bg="#181b20", height=64)
        header.pack(fill="x")
        header.pack_propagate(False)

        title_box = tk.Frame(header, bg="#181b20")
        title_box.pack(side="left", padx=20, pady=8)

        top_title_row = tk.Frame(title_box, bg="#181b20")
        top_title_row.pack(anchor="w")
        tk.Label(top_title_row, text="NEED FOR SPEED: HOT PURSUIT", bg="#181b20", fg="#ff6b00",
                 font=("Segoe UI", 13, "bold")).pack(side="left")
        self.subtitle_lbl = tk.Label(top_title_row, text="", bg="#181b20", fg="#8b949e",
                                     font=("Segoe UI", 9, "bold"))
        self.subtitle_lbl.pack(side="left", padx=(8, 0), pady=(3, 0))

        sub_row = tk.Frame(title_box, bg="#181b20")
        sub_row.pack(anchor="w")
        tk.Label(sub_row, text="vibe coded edition", bg="#181b20", fg="#6e7681",
                 font=("Segoe UI", 8, "italic")).pack(side="left")
        tk.Label(sub_row, text="by prostak", bg="#181b20", fg="#969cf2",
                 font=("Segoe UI", 8, "bold")).pack(side="left", padx=(5, 0))

        header_btns = tk.Frame(header, bg="#181b20")
        header_btns.pack(side="right", padx=20)

        self.info_btn = tk.Button(header_btns, text="", bg="#252a32", fg="#e1e4e8",
                                  activebackground="#323842", activeforeground="#ffffff",
                                  relief="flat", font=("Segoe UI", 9, "bold"), cursor="hand2",
                                  padx=12, pady=5, command=self.open_info_window)
        self.info_btn.pack(side="right")

        self.lang_btn = tk.Button(header_btns, text="", bg="#252a32", fg="#ff6b00",
                                  activebackground="#323842", activeforeground="#ffffff",
                                  relief="flat", font=("Segoe UI", 9, "bold"), cursor="hand2",
                                  padx=10, pady=5, command=self.toggle_language)
        self.lang_btn.pack(side="right", padx=(0, 8))

        path_frame = tk.Frame(self.root, bg="#121417")
        path_frame.pack(fill="x", padx=20, pady=(12, 8))
        self.game_path_lbl = tk.Label(path_frame, text="", bg="#121417", fg="#8b949e",
                                      font=("Segoe UI", 8, "bold"))
        self.game_path_lbl.pack(anchor="w", pady=(0, 4))

        input_row = tk.Frame(path_frame, bg="#121417")
        input_row.pack(fill="x")
        self.game_path_var = tk.StringVar()
        entry = tk.Entry(input_row, textvariable=self.game_path_var, bg="#1c2026", fg="#ffffff",
                         insertbackground="white", relief="flat", font=("Segoe UI", 10))
        entry.pack(side="left", fill="x", expand=True, ipady=5, padx=(0, 8))

        self.browse_btn = tk.Button(input_row, text="", bg="#252a32", fg="#ffffff",
                                    activebackground="#323842", activeforeground="#ffffff",
                                    relief="flat", font=("Segoe UI", 9, "bold"),
                                    cursor="hand2", command=self.browse_game, padx=15, pady=4)
        self.browse_btn.pack(side="right")

        list_header = tk.Frame(self.root, bg="#121417")
        list_header.pack(fill="x", padx=20, pady=(4, 4))
        self.select_slot_lbl = tk.Label(list_header, text="", bg="#121417", fg="#8b949e",
                                        font=("Segoe UI", 8, "bold"))
        self.select_slot_lbl.pack(side="left")
        self.count_label = tk.Label(list_header, text="", bg="#121417", fg="#ff6b00",
                                    font=("Segoe UI", 8, "bold"))
        self.count_label.pack(side="right")

        tree_frame = tk.Frame(self.root, bg="#1c2026", height=295)
        tree_frame.pack(fill="x", padx=20)
        tree_frame.pack_propagate(False)

        columns = ("id", "original", "custom")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")
        self.tree.column("id", width=75, anchor="center")
        self.tree.column("original", width=335, anchor="w")
        self.tree.column("custom", width=310, anchor="w")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<Double-1>", self.on_double_click)

        ctrl_frame = tk.Frame(self.root, bg="#121417")
        ctrl_frame.pack(fill="x", padx=20, pady=(10, 4))

        btn_style = {"bg": "#252a32", "fg": "#e1e4e8", "activebackground": "#323842",
                     "activeforeground": "#ffffff", "relief": "flat", "font": ("Segoe UI", 9),
                     "cursor": "hand2", "padx": 10, "pady": 5}

        self.btn_assign = tk.Button(ctrl_frame, text="", command=self.assign_single, **btn_style)
        self.btn_assign.pack(side="left", padx=(0, 6))

        self.btn_remove = tk.Button(ctrl_frame, text="", command=self.remove_single, **btn_style)
        self.btn_remove.pack(side="left", padx=(0, 6))

        self.btn_batch = tk.Button(ctrl_frame, text="", command=self.assign_batch, **btn_style)
        self.btn_batch.pack(side="left", padx=(0, 6))

        self.btn_clear = tk.Button(ctrl_frame, text="", command=self.clear_all, **btn_style)
        self.btn_clear.pack(side="right")

        bottom_frame = tk.Frame(self.root, bg="#181b20", pady=12, padx=20)
        bottom_frame.pack(fill="x", side="bottom")

        top_bottom = tk.Frame(bottom_frame, bg="#181b20")
        top_bottom.pack(fill="x", pady=(0, 8))

        self.backup_var = tk.BooleanVar(value=True)
        self.chk_backup = tk.Checkbutton(top_bottom, text="", variable=self.backup_var,
                                         bg="#181b20", fg="#c9d1d9", selectcolor="#121417",
                                         activebackground="#181b20", activeforeground="#ffffff",
                                         font=("Segoe UI", 9))
        self.chk_backup.pack(side="left")

        self.btn_restore = tk.Button(top_bottom, text="", bg="#252a32", fg="#8b949e",
                                     activebackground="#323842", activeforeground="#ffffff",
                                     relief="flat", font=("Segoe UI", 8), cursor="hand2",
                                     command=self.restore_backup, padx=8, pady=2)
        self.btn_restore.pack(side="right")

        self.progress = ttk.Progressbar(bottom_frame, orient="horizontal", mode="determinate",
                                        style="Orange.Horizontal.TProgressbar")
        self.progress.pack(fill="x", pady=(0, 8))

        action_row = tk.Frame(bottom_frame, bg="#181b20")
        action_row.pack(fill="x")

        self.status_label = tk.Label(action_row, text="", bg="#181b20", fg="#8b949e",
                                     font=("Segoe UI", 9))
        self.status_label.pack(side="left")

        self.start_btn = tk.Button(action_row, text="", bg="#ff6b00", fg="#ffffff",
                                   activebackground="#e05e00", activeforeground="#ffffff",
                                   relief="flat", font=("Segoe UI", 10, "bold"), cursor="hand2",
                                   padx=22, pady=6, command=self.start_thread)
        self.start_btn.pack(side="right")

    def apply_language(self):
        self.root.title(self.t("title"))
        self.subtitle_lbl.config(text=self.t("subtitle"))
        self.info_btn.config(text=self.t("info_btn"))
        self.lang_btn.config(text=self.t("lang_btn"))
        self.game_path_lbl.config(text=self.t("game_path_lbl"))
        self.browse_btn.config(text=self.t("browse_btn"))
        self.select_slot_lbl.config(text=self.t("select_slot_lbl"))
        self.tree.heading("id", text=self.t("col_id"))
        self.tree.heading("original", text=self.t("col_orig"))
        self.tree.heading("custom", text=self.t("col_custom"))
        self.btn_assign.config(text=self.t("btn_assign"))
        self.btn_remove.config(text=self.t("btn_remove"))
        self.btn_batch.config(text=self.t("btn_batch"))
        self.btn_clear.config(text=self.t("btn_clear"))
        self.chk_backup.config(text=self.t("chk_backup"))
        self.btn_restore.config(text=self.t("btn_restore"))
        self.start_btn.config(text=self.t("btn_install"))
        if not self.is_running:
            self.status_label.config(text=self.t("status_ready"), fg="#8b949e")
        self.populate_tree()

    def toggle_language(self):
        self.lang = "en" if self.lang == "ru" else "ru"
        self.apply_language()

    def populate_tree(self):
        selected = self.tree.selection()
        sel_id = selected[0] if selected else None
        for item in self.tree.get_children():
            self.tree.delete(item)
        for tid, orig_name in TRACK_SLOTS:
            custom_name = self.t("not_changed")
            if tid in self.assigned_tracks:
                custom_name = "▶ " + os.path.basename(self.assigned_tracks[tid])
            self.tree.insert("", tk.END, iid=tid, values=(tid, orig_name, custom_name))
        if sel_id and self.tree.exists(sel_id):
            self.tree.selection_set(sel_id)
        self.count_label.config(text=self.t("assigned_lbl").format(count=len(self.assigned_tracks), total=len(TRACK_SLOTS)))

    def browse_game(self):
        folder = filedialog.askdirectory(title=self.t("browse_title"))
        if folder:
            self.game_path_var.set(folder)

    def on_double_click(self, event):
        self.assign_single()

    def assign_single(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo(self.t("hint_title"), self.t("hint_select"))
            return
        tid = selected[0]
        file_path = filedialog.askopenfilename(title=self.t("dlg_single").format(tid=tid))
        if file_path and file_path.lower().endswith(".mp3"):
            self.assigned_tracks[tid] = file_path
            self.populate_tree()
            self.tree.selection_set(tid)

    def remove_single(self):
        selected = self.tree.selection()
        if selected:
            tid = selected[0]
            if tid in self.assigned_tracks:
                del self.assigned_tracks[tid]
                self.populate_tree()

    def assign_batch(self):
        files = filedialog.askopenfilenames(title=self.t("dlg_batch"))
        if not files:
            return
        mp3_list = [f for f in files if f.lower().endswith(".mp3")]
        for rid in RADIO_IDS:
            self.assigned_tracks.pop(rid, None)
        for idx, f in enumerate(mp3_list[:len(RADIO_IDS)]):
            tid = RADIO_IDS[idx]
            self.assigned_tracks[tid] = f
        self.populate_tree()

    def clear_all(self):
        self.assigned_tracks.clear()
        self.populate_tree()

    def restore_backup(self):
        songs_dir = self.resolve_songs_dir()
        if not songs_dir:
            messagebox.showerror(self.t("err_title"), self.t("err_no_songs"))
            return
        backup_dir = os.path.join(songs_dir, "BACKUP")
        if not os.path.exists(backup_dir):
            messagebox.showerror(self.t("err_title"), self.t("err_no_backup"))
            return
        restored = 0
        for tid, _ in TRACK_SLOTS:
            bkp = os.path.join(backup_dir, f"{tid}.SPS")
            orig = os.path.join(songs_dir, f"{tid}.SPS")
            if os.path.exists(bkp):
                shutil.copy2(bkp, orig)
                restored += 1
        messagebox.showinfo(self.t("restore_title"), self.t("restore_msg").format(count=restored))

    def start_thread(self):
        songs_dir = self.resolve_songs_dir()
        if not songs_dir:
            messagebox.showerror(self.t("err_title"), self.t("err_no_songs"))
            return
        if not self.assigned_tracks:
            messagebox.showwarning(self.t("warn_title"), self.t("warn_no_tracks"))
            return
        self.is_running = True
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
            self.status_label.config(
                text=self.t("status_build").format(cur=idx+1, total=total, name=os.path.basename(mp3_path), tid=tid),
                fg="#ff6b00"
            )
            clean_mp3 = os.path.join(temp_dir, f"{tid}.mp3")
            out_sps = os.path.join(temp_dir, f"{tid}.sps")

            subprocess.run([ffmpeg_exe, "-y", "-loglevel", "error", "-i", mp3_path, "-map_metadata", "-1", "-vn", "-ar", "44100", "-ac", "2", "-b:a", "192k", clean_mp3], startupinfo=startupinfo)
            subprocess.run([sx_exe, "-sndplayer", "-fileformatversion1", "-ealayer3_int", "-vbr100", f"{tid}.mp3", f"-={tid}"], cwd=temp_dir, startupinfo=startupinfo)

            if os.path.exists(out_sps):
                shutil.copy2(out_sps, os.path.join(songs_dir, f"{tid}.SPS"))
            self.progress["value"] = idx + 1

        shutil.rmtree(temp_dir, ignore_errors=True)
        self.is_running = False
        self.status_label.config(text=self.t("status_done").format(total=total), fg="#2ea043")
        self.start_btn.config(state="normal")
        messagebox.showinfo(self.t("success_title"), self.t("success_msg").format(total=total))

    def open_joke_window(self, event=None):
        joke_win = tk.Toplevel(self.root)
        joke_win.title(self.t("joke_title"))
        joke_win.geometry("560x660")
        joke_win.configure(bg="#181b20")
        joke_win.resizable(False, False)
        joke_win.transient(self.root)
        joke_win.grab_set()
        set_dark_title_bar(joke_win, instant_refresh=True)

        tk.Label(joke_win, text=self.t("joke_title"), bg="#181b20", fg="#ff6b00",
                 font=("Segoe UI", 12, "bold")).pack(pady=(12, 6))

        box = tk.Frame(joke_win, bg="#1c2026", padx=15, pady=12)
        box.pack(fill="both", expand=True, padx=16, pady=(0, 8))

        txt = tk.Text(box, bg="#1c2026", fg="#e1e4e8", font=("Segoe UI", 9),
                      relief="flat", wrap="word", borderwidth=0, highlightthickness=0)
        txt.insert("1.0", JOKE_TEXT)
        txt.config(state="disabled")
        txt.pack(fill="both", expand=True)

        tk.Button(joke_win, text=self.t("joke_btn"), bg="#ff6b00", fg="#ffffff",
                  activebackground="#e05e00", activeforeground="#ffffff",
                  relief="flat", font=("Segoe UI", 9, "bold"), cursor="hand2",
                  padx=20, pady=6, command=joke_win.destroy).pack(pady=(0, 12))

    def open_info_window(self):
        info_win = tk.Toplevel(self.root)
        info_win.title(self.t("info_win_title"))
        info_win.geometry("630x665")
        info_win.configure(bg="#181b20")
        info_win.resizable(False, False)
        info_win.transient(self.root)
        info_win.grab_set()
        set_dark_title_bar(info_win, instant_refresh=True)

        notebook = ttk.Notebook(info_win)
        notebook.pack(fill="both", expand=True, padx=15, pady=(12, 6))

        # --- ВКЛАДКА 1: Управление и о проекте ---
        page1 = tk.Frame(notebook, bg="#181b20")
        notebook.add(page1, text=self.t("tab_controls"))

        vibe_box = tk.Frame(page1, bg="#1b202c", highlightbackground="#969cf2", highlightthickness=1, padx=14, pady=10)
        vibe_box.pack(fill="x", padx=10, pady=(12, 8))
        tk.Label(vibe_box, text=self.t("vibe_title"), bg="#1b202c", fg="#969cf2",
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        tk.Label(vibe_box, text=self.t("vibe_text"), bg="#1b202c", fg="#c9d1d9",
                 font=("Segoe UI", 8), justify="left").pack(anchor="w", pady=(3, 0))

        tk.Label(page1, text=self.t("controls_header"), bg="#181b20", fg="#ff6b00",
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=10, pady=(4, 4))

        for btn_name, desc in self.t("controls_list"):
            row = tk.Frame(page1, bg="#1c2026", padx=10, pady=5)
            row.pack(fill="x", padx=10, pady=2)
            tk.Label(row, text=btn_name, bg="#1c2026", fg="#ffffff",
                     font=("Segoe UI", 8, "bold"), width=25, anchor="w").pack(side="left")
            tk.Label(row, text=desc, bg="#1c2026", fg="#8b949e",
                     font=("Segoe UI", 8), anchor="w", justify="left", wraplength=360).pack(side="left", fill="x", expand=True)

        # --- ВКЛАДКА 2: Как это устроено ---
        page2 = tk.Frame(notebook, bg="#181b20")
        notebook.add(page2, text=self.t("tab_arch"))

        tk.Label(page2, text=self.t("arch_header"), bg="#181b20", fg="#ff6b00",
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=12, pady=(12, 8))

        for title, body in self.t("arch_blocks"):
            card = tk.Frame(page2, bg="#1c2026", padx=12, pady=8)
            card.pack(fill="x", padx=12, pady=4)
            tk.Label(card, text=title, bg="#1c2026", fg="#969cf2",
                     font=("Segoe UI", 9, "bold")).pack(anchor="w")
            tk.Label(card, text=body, bg="#1c2026", fg="#c9d1d9",
                     font=("Segoe UI", 8), justify="left", wraplength=540).pack(anchor="w", pady=(3, 0))

        # --- ЛОГОТИП PROSTAK (КЛИКАБЕЛЬНЫЙ) ---
        logo_frame = tk.Frame(info_win, bg="#181b20", cursor="hand2")
        logo_frame.pack(pady=(2, 4))

        logo_canvas = tk.Canvas(logo_frame, width=84, height=58, bg="#181b20", highlightthickness=0, cursor="hand2")
        logo_canvas.pack()
        color = "#969cf2"
        # Левая бровь домиком
        logo_canvas.create_line(10, 22, 26, 8, 40, 22, fill=color, width=3.5, capstyle=tk.ROUND, joinstyle=tk.ROUND)
        # Левый глаз
        logo_canvas.create_oval(22, 22, 29, 34, fill=color, outline="")
        # Правая прищуренная бровь
        logo_canvas.create_line(50, 24, 65, 22, 76, 25, fill=color, width=3.5, capstyle=tk.ROUND, joinstyle=tk.ROUND)
        # Правый глаз
        logo_canvas.create_oval(60, 28, 67, 38, fill=color, outline="")
        # Рот
        logo_canvas.create_line(30, 48, 56, 48, fill=color, width=3.5, capstyle=tk.ROUND)

        logo_lbl = tk.Label(logo_frame, text="prostak", bg="#181b20", fg="#969cf2",
                            font=("Segoe UI", 9, "bold"), cursor="hand2")
        logo_lbl.pack()

        logo_frame.bind("<Button-1>", self.open_joke_window)
        logo_canvas.bind("<Button-1>", self.open_joke_window)
        logo_lbl.bind("<Button-1>", self.open_joke_window)

        tk.Button(info_win, text=self.t("btn_close"), bg="#ff6b00", fg="#ffffff",
                  activebackground="#e05e00", activeforeground="#ffffff",
                  relief="flat", font=("Segoe UI", 9, "bold"), cursor="hand2",
                  padx=25, pady=5, command=info_win.destroy).pack(pady=(2, 10))


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernNFSMusicApp(root)
    root.mainloop()
