# Сборка и запуск LiptonWeb Browser

## Windows

### 🚀 Способ 1: Автоматический (рекомендуется)
```cmd
# Скачайте папку liptonweb на Windows
# Дважды кликните build.bat
```

### 🛠️ Способ 2: Ручная сборка
```cmd
# 1. Установка Python (если не установлен)
# Скачайте с https://python.org (версия 3.8+)

# 2. Установка зависимостей
pip install PyQt5 PyQtWebEngine pyinstaller

# 3. Сборка .exe
pyinstaller --onefile --windowed --name "LiptonWeb" --add-data "README.md;." main.py

# 4. Результат
# dist/LiptonWeb.exe - готовый браузер
```

### 📦 Способ 3: Через Python скрипт
```cmd
python build_windows.py
```

### 🎯 Способ 4: Продвинутый (с .spec файлом)
```cmd
# Создание конфигурации
python build_windows.py

# Сборка через .spec
pyinstaller --clean LiptonWeb.spec
```

### 🏭 Создание установщика
```cmd
# 1. Установите NSIS: https://nsis.sourceforge.io/
# 2. Запустите build_windows.py (опция 2 или 3)
# 3. Скомпилируйте installer.nsi в NSIS
# Результат: LiptonWeb_Setup_1.0.0.exe
```

## Linux

### Ubuntu/Debian
```bash
# Установка зависимостей системы
sudo apt update
sudo apt install python3-pyqt5 python3-pyqt5.qtwebengine python3-pip

# Установка Python зависимостей
pip3 install PyQt5 PyQtWebEngine

# Запуск
python3 main.py
```

### Fedora/CentOS
```bash
sudo dnf install python3-qt5 python3-qt5-webengine
pip3 install PyQt5 PyQtWebEngine
python3 main.py
```

### Arch Linux
```bash
sudo pacman -S python-pyqt5 python-pyqt5-webengine
pip install PyQt5 PyQtWebEngine
python main.py
```

## macOS

### Через Homebrew
```bash
# Установка Python
brew install python

# Установка зависимостей
pip3 install PyQt5 PyQtWebEngine

# Запуск
python3 main.py
```

## Создание переносимой версии

### Windows (портативная версия)
```bash
# Создание папки для портативной версии
mkdir LiptonWeb_Portable
cd LiptonWeb_Portable

# Копирование файлов
cp ../main.py .
cp ../requirements.txt .

# Установка в локальную папку
pip install --target=./lib PyQt5 PyQtWebEngine

# Создание bat файла для запуска
echo @echo off > start.bat
echo set PYTHONPATH=./lib >> start.bat
echo python main.py >> start.bat
```

### Linux (AppImage)
```bash
# Установка python-appimage-builder
pip install python-appimage-builder

# Сборка AppImage
python-appimage-builder main.py
```

## Возможные проблемы и решения

### Windows: Ошибка с QtWebEngine
```
Проблема: "QtWebEngineWidgets not found"
Решение: pip install --upgrade PyQtWebEngine
```

### Linux: Отсутствуют библиотеки
```
Проблема: "ImportError: libQt5WebEngineCore.so.5"
Решение: sudo apt install libqt5webenginecore5
```

### macOS: Проблемы с сертификатами
```bash
# Установка сертификатов
/Applications/Python\ 3.*/Install\ Certificates.command
```

## Минимальные требования

- **Python**: 3.8+
- **ОЗУ**: 512MB (рекомендовано 1GB+)
- **Место на диске**: 100MB для установки, 50MB для работы
- **Видео**: Поддержка OpenGL 2.0+

## Совместимость

✅ **Windows**: 7/8/10/11 (x64)
✅ **Linux**: Ubuntu 18.04+, Fedora 30+, Arch
✅ **macOS**: 10.14+ (Mojave и новее)
⚠️ **Android**: Требует Termux + X11
⚠️ **iOS**: Не поддерживается (нет PyQt5)

## Проверка работы

После запуска должны увидеть:
- Окно браузера с вкладками
- Адресную строку
- Кнопки навигации
- Кнопку DevTools

Если окно не появляется, проверьте консоль на наличие ошибок импорта.
