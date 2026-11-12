# Need for Speed: Hot Pursuit (2010 / Remastered) — Custom Soundtrack Studio

A convenient graphical installer for adding your own custom music (MP3) to the in-game radio, menu, garages, and pursuit themes in **Need for Speed: Hot Pursuit (2010)** and **Remastered**.
The utility automatically converts audio tracks into the game's native format (`.SPS` with EA Layer 3 headers) and replaces the selected slots without crashes or audio stuttering.

## Features
* **36 Audio Slots:** Replace any of the 27 radio songs, main menu theme, racer/cop garage themes, and all 6 pursuit themes individually, or batch-fill all 27 radio slots in one click.
* **Bilingual Interface:** Instant switching between Russian and English (`RU / EN`) right in the top bar.
* **Automatic Audio Preparation:** Built-in FFmpeg strips metadata and normalizes bitrate/sample rate to match the Chameleon engine's requirements.
* **Safety First:** Automatically creates backups of original tracks (`UI\SONGS\BACKUP`) and allows one-click restoration.

## How to Use (For Players)
1. Go to the **[Releases](../../releases)** section on the right and download **`NFS_HP_Music_Installer.exe`** (or **`NFS_HP_Music.exe`**).
2. Launch the program and select the folder of your installed game (`Need for Speed Hot Pursuit` or directly `UI\SONGS`).
3. Double-click the desired slots to assign your `.mp3` tracks (or click batch-fill for all 27 radio tracks).
4. Click **"УСТАНОВИТЬ В ИГРУ"** / **"INSTALL TO GAME"**.

## Building from Source (For Developers)
To run or compile from source, place `ffmpeg.exe`, `sx.exe`, and the libraries `eaxmaenc.dll`, `libatrac9.dll`, `libmp3lame.dll` in the root folder alongside `app.py`.

## Author's Note (Real Talk)
Everything above was written by AI because I couldn't be bothered to write a proper doc. I just wanted to throw some dumb custom tracks into my childhood game for fun, and ended up wrestling with this engine's quirks—either the game crashed as soon as a track started, or the audio stuttered like crazy, and there's barely any decent info on this online.

If you want to do everything manually by hand: download `sx_6.00` (and `ealayer3` if you want to convert original `.SPS` tracks back to MP3 to listen to them). Convert your track to 192kbps and 44100Hz, drop that converted track into the `sx` folder, click the address bar at the top, type `cmd` and hit Enter—a command prompt will open right in that directory. 
Then type into cmd:
`sx.exe -sndplayer -fileformatversion1 -ealayer3_int -vbr100 [YOUR_FILE_NAME.mp3] -=[GAME_SLOT_ID]`

All the game's tracks are located in `\Need for Speed Hot Pursuit\UI\SONGS` (works for the Remastered version too). Look for IDs from `579437` to `579465`—that's the entire radio, and the rest (`259196`, `265817`, `265818`, `579205`, `579235`, `579236`, `579470`, `579471`, `579697`) are menu, garage, and pursuit themes—feel free to poke around and replace them if you want.

Reading this back, it looks super simple, right? Well, it took me a couple of hours of trial and error just to find the right flags and figure out which tools were even needed—first it hated MP3s over 192kbps, then it wouldn't accept files without specific flags, and finding actual guides was a pain. So to save you the headache, I vibe-coded a quick and janky `.exe` just for fun. Honestly, I would've been stoked to find something like this last night instead of figuring out how to swap tracks from scratch. Probably missed a few details in my guide, but the basics are here—you're on your own from here, you've got AIs too, I believe in you.

**Steam ID:** `76561198274126708`

---

# Need for Speed: Hot Pursuit (2010 / Remastered) — Custom Soundtrack Studio

Удобный графический установщик своей музыки (MP3) на радио, в меню, гаражи и погони для **Need for Speed: Hot Pursuit (2010)** и **Remastered**. 
Программа автоматически конвертирует треки в родной формат игры (`.SPS` с заголовком EA Layer 3) и заменяет выбранные слоты без вылетов и искажений звука.

## Возможности
* **36 слотов аудио:** точечная замена любого из 27 треков радио, темы главного меню, тем гаражей гонщика/копов и всех 6 тем погонь, либо автоматическое заполнение всех 27 слотов радио пачкой.
* **Два языка (RU / EN):** мгновенное переключение между русским и английским языком прямо в верхней шапке программы.
* **Авто-подготовка звука:** встроенный FFmpeg сам чистит метаданные и выравнивает битрейт/частоту под требования движка Chameleon.
* **Безопасность:** автоматическое создание резервных копий оригинальных треков (`UI\SONGS\BACKUP`) и восстановление в один клик.

## Как пользоваться (для игроков)
1. Перейдите в раздел **[Releases](../../releases)** справа и скачайте готовый файл **`NFS_HP_Music_Installer.exe`** (или **`NFS_HP_Music.exe`**).
2. Запустите программу и укажите папку с установленной игрой (`Need for Speed Hot Pursuit` или сразу `UI\SONGS`).
3. Двойным кликом выберите нужные слоты и назначьте свои `.mp3` треки (либо нажмите «Заполнить радио пачкой»).
4. Нажмите **«УСТАНОВИТЬ В ИГРУ»**.

## Сборка из исходников (для разработчиков)
Для запуска или компиляции потребуются `ffmpeg.exe`, `sx.exe` и библиотеки `eaxmaenc.dll`, `libatrac9.dll`, `libmp3lame.dll` в корневой папке.

## От автора
Всё выше написал ИИ т.к. мне впадлу реально чёт писать, я просто по рофлу хотел добавить свои тупые треки в игру детства, а пришлось возиться с особенностями этого движка, то просто крашило когда трек врубаешь, то звук лаганно-дёрганный был, нормальных постов на эту тему вообще мало.

Если хотите сами ручками всё сделать - качайте `sx_6.00` (и `ealayer3`, если захотите перевести родные `.SPS` треки игры обратно в MP3, чтобы послушать их), свой трек прогоняйте до 192кбит/с и 44100hz. Этот прогнанный трек закидываете в папку `sx` и сверху тыкаете по пути и туда `cmd` вписываете, откроется сразу цмдшка на нужном месте.
Вписываете в cmd:
`sx.exe -sndplayer -fileformatversion1 -ealayer3_int -vbr100 [ИМЯ_ТВОЕГО_ФАЙЛА.mp3] -=[ID_СЛОТА_В_ИГРЕ]`

Все треки игры лежат в `\Need for Speed Hot Pursuit\UI\SONGS`, с ремастером прокнет такая же темка, id смотри от `579437` до `579465` - это всё радио, остальное (`259196`, `265817`, `265818`, `579205`, `579235`, `579236`, `579470`, `579471`, `579697`) - это все остальные треки из меню, гаражей и погонь, можешь потыкать позаменять если хочешь.
Вот я расписал и ваще всё просто так кажется, а что бы найти правильные флаги и что ещё нужны приложуньки я запаривался пару часов, то он не дружил с мп3 которые больше 192, то флаги ему какие-то пропиши, без них он не кушает, то просто ваще найди инфы на то чё делать с этим, крч чтоб вам не возиться нанейронил exe корявый косой сделанный по приколу, но я был бы рад такой увидеть вчера вечером, а не думать как треки заменить.
В своём гайде чёт явно пропустил наверное, но базовую инфу дал, дальше сами, у вас тоже есть нейронки, я в вас верю.

**Steam ID:** `76561198274126708`
