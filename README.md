# 🎨 Wallpaper Changer

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)](https://riverbankcomputing.com/software/pyqt/)
[![Linux](https://img.shields.io/badge/Linux-FCC624?logo=linux&logoColor=black)](https://www.linux.org/)
[![Debian](https://img.shields.io/badge/Debian-A81D33?logo=debian&logoColor=white)](https://www.debian.org/)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?logo=ubuntu&logoColor=white)](https://ubuntu.com/)

**Автоматическая смена обоев рабочего стола для Linux с графическим интерфейсом на PyQt5**

![Wallpaper Changer Demo](screenshots/demo.gif)

## 📋 Оглавление

- [Возможности](#-возможности)
- [Скриншоты](#-скриншоты)
- [Системные требования](#-системные-требования)
- [Установка](#-установка)
  - [Deb-пакет](#deb-пакет-рекомендуется)
  - [Из исходников](#из-исходников)
  - [Docker](#docker)
  - [Автоматическая установка](#автоматическая-установка)
- [Использование](#-использование)
- [Поддерживаемые окружения](#-поддерживаемые-окружения)
- [Сборка deb-пакета](#-сборка-deb-пакета)
- [Конфигурация](#-конфигурация)
- [Устранение проблем](#-устранение-проблем)
- [Часто задаваемые вопросы](#-часто-задаваемые-вопросы)
- [Вклад в проект](#-вклад-в-проект)
- [Лицензия](#-лицензия)
- [Авторы](#-авторы)
- [Благодарности](#-благодарности)

## ✨ Возможности

### Основные функции
- 🖼️ **Автоматическая смена обоев** с настраиваемым интервалом (5-3600 секунд)
- 🎯 **Поддержка 6+ окружений рабочего стола** (GNOME, KDE, XFCE, Cinnamon, MATE, WM)
- 📁 **Выбор любой папки с изображениями**
- 👁️ **Предпросмотр обоев** двойным кликом
- 🎮 **Ручная смена** в любой момент
- ⏯️ **Удобное управление** (Старт/Стоп)
- 📦 **Готовый deb-пакет** для легкой установки
- 🔄 **Поддержка 6 форматов**: JPG, JPEG, PNG, BMP, GIF, WEBP

### Технические особенности
- 🚀 **Многопоточность** - интерфейс не зависает
- 💾 **Низкое потребление ресурсов**
- 🎨 **Современный интерфейс** на PyQt5
- 🐍 **100% Python** код
- 📝 **Подробное логирование** действий

## 📸 Скриншоты

| Главное окно | Выбор папки | Настройки |
|-------------|-------------|-----------|
| ![Главное окно](screenshots/main_window.png) | ![Выбор папки](screenshots/folder_selection.png) | ![Настройки](screenshots/settings.png) |

*Скриншоты будут добавлены после загрузки на GitHub*

## 💻 Системные требования

### Минимальные
- **ОС**: Linux (любой дистрибутив)
- **Python**: 3.6 или выше
- **RAM**: 128 MB
- **Диск**: 50 MB свободного места
- **Графика**: Любая с поддержкой X11/Wayland

### Рекомендуемые
- **ОС**: Ubuntu 20.04+, Debian 11+, Fedora 34+
- **Python**: 3.8+
- **RAM**: 256 MB
- **Диск**: 100 MB

### Зависимости
- Python 3.6+
- PyQt5 5.15+
- feh (опционально, для оконных менеджеров)

## 🚀 Установка

### Deb-пакет (рекомендуется)

#### Способ 1: Скачать с релизов
```bash
# Скачивание последней версии
wget https://github.com/Wsper-hub/wallpaper-changer/releases/latest/download/wallpaper-changer_1.0.0_all.deb

# Установка
sudo dpkg -i wallpaper-changer_1.0.0_all.deb
sudo apt-get install -f  # Установка зависимостей
