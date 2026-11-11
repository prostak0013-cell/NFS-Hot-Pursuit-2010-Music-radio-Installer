# Need for Speed: Hot Pursuit (2010) — Custom Soundtrack Studio
Sorry, the interface is entirely in Russian

A convenient graphical installer for adding your own custom music (MP3) to the in-game radio in the original **Need for Speed: Hot Pursuit (2010)**.
The utility automatically converts audio tracks into the game's native format (`.SPS` with EA Layer 3 headers) and replaces the selected slots without crashes or audio stuttering.

## Features
* **Targeted Replacement:** Replace any of the 27 radio slots individually or load a batch of tracks automatically.
* **Automatic Audio Preparation:** Built-in FFmpeg strips metadata and normalizes bitrate/sample rate to match the Chameleon engine's requirements.
* **Safety First:** Automatically creates backups of original tracks (`UI\SONGS\BACKUP`) and allows one-click restoration.

## How to Use (For Players)
1. Go to the **[Releases](../../releases)** section on the right and download **`NFS_HP_Musicr.exe`**.
2. Launch the program and select the root folder of your installed game (`Need for Speed Hot Pursuit`).
3. Double-click the desired slots to assign your `.mp3` tracks.
4. Click **"УСТАНОВИТЬ В ИГРУ"** (Install to Game).

## Building from Source (For Developers)
To run or compile from source, place `ffmpeg.exe`, `sx.exe`, and the libraries `eaxmaenc.dll`, `libatrac9.dll`, `libmp3lame.dll` in the root folder alongside `app.py`.

## Author's Note (Real Talk)
Everything above was written by AI because I couldn't be bothered to write a proper doc. I just wanted to throw some dumb custom tracks into my childhood game for fun, and ended up wrestling with this engine's quirks—either the game crashed as soon as a track started, or the audio stuttered like crazy, and there's barely any decent info on this online.

If you want to do everything manually by hand: download `ealayer3` and `sx_6.00` (I kept both folders inside one parent folder). Convert your track to 192kbps and 44100Hz, drop that converted track into the `sx` folder, click the address bar at the top, type `cmd` and hit Enter—a command prompt will open right in that directory.
Then type into cmd:
`sx.exe -sndplayer -fileformatversion1 -ealayer3_int -vbr100 [YOUR_FILE_NAME.mp3] -=[GAME_SLOT_ID]`

All the game's tracks are located in `\Need for Speed Hot Pursuit\UI\SONGS` (pretty sure the exact same trick works for the Remastered version too). Look for IDs from `579437` to `579465`—that's the entire radio. No idea about the rest, seems like menu and credits music, feel free to poke around and replace them if you want.

Reading this back, it looks super simple, right? Well, it took me a couple of hours of trial and error just to find the right flags and figure out which tools were even needed—first it hated MP3s over 192kbps, then it wouldn't accept files without specific flags, and finding actual guides was a pain. So to save you the headache, I vibe-coded a quick and janky `.exe` just for fun. Honestly, I would've been stoked to find something like this last night instead of figuring out how to swap tracks from scratch. Probably missed a few details in my guide, but the basics are here—you're on your own from here, you've got AIs too, I believe in you.

**Steam ID:** `76561198274126708`

# RU

Удобный графический установщик своей музыки (MP3) на радио в оригинальную **Need for Speed: Hot Pursuit (2010)**. 
Программа автоматически конвертирует треки в родной формат игры (`.SPS` с заголовком EA Layer 3) и заменяет выбранные слоты без вылетов и искажений звука.

## Возможности
* **Точечная замена:** выбор любого из 27 слотов радио или автоматическая загрузка пачкой.
* **Авто-подготовка звука:** встроенный FFmpeg сам чистит метаданные и выравнивает битрейт/частоту под требования движка Chameleon.
* **Безопасность:** автоматическое создание резервных копий оригинальных треков (`UI\SONGS\BACKUP`) и восстановление в один клик.

## Как пользоваться (для игроков)
1. Перейдите в раздел **[Releases](../../releases)** справа и скачайте готовый файл **`NFS_HP_Music.exe`**.
2. Запустите программу и укажите корневую папку с установленной игрой (`Need for Speed Hot Pursuit`).
3. Двойным кликом выберите нужные слоты и назначьте свои `.mp3` треки.
4. Нажмите **«УСТАНОВИТЬ В ИГРУ»**.

## Сборка из исходников (для разработчиков)
Для запуска или компиляции потребуются `ffmpeg.exe`, `sx.exe` и библиотеки `eaxmaenc.dll`, `libatrac9.dll`, `libmp3lame.dll` в корневой папке.


## Всё выше написал ИИ т.к. мне впадлу реально чёт писать, я просто по рофлу хотел добавить свои тупые треки в игру детства, а пришлось возиться
с особенностями этого движка, то просто крашило когда трек врубаешь, то звук лаганно-дёрганный был, нормальных постов на эту тему вообще мало

Если хотите сами ручками всё сделать - качайте ealayer3 и sx_6.00 //я эти две папки держал в одной другой, свой трек прогоняйте до 192кбит/с и 44100hz
Этот прогнанный трек закидываете в папку sx и сверху тыкаете по пути и туда cmd вписываете, откроется сразу цмдшка на нужном месте
Вписываете в cmd: "sx.exe -sndplayer -fileformatversion1 -ealayer3_int -vbr100 [ИМЯ_ТВОЕГО_ФАЙЛА.mp3] -=[ID_СЛОТА_В_ИГРЕ]"

Все треки игры лежат в "\Need for Speed Hot Pursuit\UI\SONGS", уверен что и с ремастером прокнет такая же темка, id смотри от 579437 до 579465 - это всё радио,
остальное не знаю, кажется это все остальные треки из меню и титров, можешь потыкать позаменять если хочешь
Вот я расписал и ваще всё просто так кажется, а что бы найти правильные флаги и что ещё нужны приложуньки я запаривался пару часов, то он не дружил с мп3 которые
больше 192, то флаги ему какие-то пропиши, без них он не кушает, то просто ваще найди инфы на то чё делать с этим, крч чтоб вам не возиться нанейронил exe
корявый косой сделанный по приколу, но я был бы рад такой увидеть вчера вечером, а не думать как треки заменить
в своём гайде чёт явно пропустил наверное, но базовую инфу дал, дальше сами, у вас тоже есть нейронки, я в вас верю
steam id - 76561198274126708
