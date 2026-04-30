#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import random
import time
from pathlib import Path
from threading import Thread, Event

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QSpinBox,
                             QFileDialog, QListWidget, QListWidgetItem,
                             QMessageBox, QGroupBox, QSlider, QStatusBar)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject
from PyQt5.QtGui import QPixmap, QIcon

# Попробуем импортировать различные менеджеры обоев
try:
    import subprocess

    def set_wallpaper_linux(image_path):
        """Установка обоев в различных DE Linux"""
        image_path = str(Path(image_path).absolute())

        # Определяем окружение рабочего стола
        desktop_env = os.environ.get('XDG_CURRENT_DESKTOP', '').lower()

        # GNOME
        if 'gnome' in desktop_env or 'unity' in desktop_env:
            cmd = f'gsettings set org.gnome.desktop.background picture-uri "file://{image_path}"'
            subprocess.run(cmd, shell=True)
            # Для GNOME 42+
            cmd = f'gsettings set org.gnome.desktop.background picture-uri-dark "file://{image_path}"'
            subprocess.run(cmd, shell=True)

        # KDE Plasma
        elif 'kde' in desktop_env or 'plasma' in desktop_env:
            cmd = f'plasma-apply-wallpaper "{image_path}"'
            subprocess.run(cmd, shell=True)

        # XFCE
        elif 'xfce' in desktop_env:
            # Для XFCE 4.14+
            cmd = f'xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/image-path -s "{image_path}"'
            subprocess.run(cmd, shell=True)

        # Cinnamon
        elif 'cinnamon' in desktop_env:
            cmd = f'gsettings set org.cinnamon.desktop.background picture-uri "file://{image_path}"'
            subprocess.run(cmd, shell=True)

        # Mate
        elif 'mate' in desktop_env:
            cmd = f'gsettings set org.mate.background picture-filename "{image_path}"'
            subprocess.run(cmd, shell=True)

        # Универсальный способ через feh (для оконных менеджеров)
        else:
            # Проверяем, установлен ли feh
            try:
                subprocess.run(['which', 'feh'], capture_output=True, check=True)
                cmd = f'feh --bg-scale "{image_path}"'
                subprocess.run(cmd, shell=True)
            except subprocess.CalledProcessError:
                print("Установите feh или настройте поддержку вашего окружения")
                return False

        return True

except ImportError:
    print("Не удалось импортировать subprocess")
    set_wallpaper_linux = lambda x: None

class WallpaperChanger(QObject):
    """Класс для управления сменой обоев в отдельном потоке"""
    changed = pyqtSignal(str)

    def __init__(self, wallpaper_list, interval_seconds=30):
        super().__init__()
        self.wallpaper_list = wallpaper_list
        self.interval_seconds = interval_seconds
        self.running = False
        self.thread = None
        self.stop_event = Event()

    def start(self):
        if not self.running:
            self.running = True
            self.stop_event.clear()
            self.thread = Thread(target=self._change_loop, daemon=True)
            self.thread.start()

    def stop(self):
        self.running = False
        self.stop_event.set()
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2)

    def update_interval(self, interval_seconds):
        self.interval_seconds = interval_seconds

    def update_wallpaper_list(self, wallpaper_list):
        self.wallpaper_list = wallpaper_list

    def _change_loop(self):
        while self.running and not self.stop_event.is_set():
            if self.wallpaper_list:
                wallpaper = random.choice(self.wallpaper_list)
                try:
                    if set_wallpaper_linux(wallpaper):
                        self.changed.emit(wallpaper)
                except Exception as e:
                    print(f"Ошибка установки обоев: {e}")

            # Ожидание с возможностью прерывания
            self.stop_event.wait(self.interval_seconds)

class WallpaperApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.wallpaper_dir = str(Path.home() / "Pictures" / "Wallpapers")
        self.wallpaper_files = []
        self.changer = None
        self.init_ui()
        self.load_wallpapers()

    def init_ui(self):
        self.setWindowTitle("Смена обоев - Wallpaper Changer")
        self.setGeometry(300, 300, 600, 500)

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Основной layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Группа выбора папки
        folder_group = QGroupBox("Папка с обоями")
        folder_layout = QHBoxLayout()

        self.folder_label = QLabel(self.wallpaper_dir)
        self.folder_label.setStyleSheet("border: 1px solid gray; padding: 5px;")
        self.folder_label.setWordWrap(True)

        select_folder_btn = QPushButton("Выбрать папку")
        select_folder_btn.clicked.connect(self.select_folder)

        folder_layout.addWidget(self.folder_label)
        folder_layout.addWidget(select_folder_btn)
        folder_group.setLayout(folder_layout)
        main_layout.addWidget(folder_group)

        # Группа списка обоев
        list_group = QGroupBox("Список обоев")
        list_layout = QVBoxLayout()

        self.wallpaper_list = QListWidget()
        self.wallpaper_list.itemDoubleClicked.connect(self.preview_wallpaper)

        list_layout.addWidget(self.wallpaper_list)
        list_group.setLayout(list_layout)
        main_layout.addWidget(list_group)

        # Группа настроек интервала
        interval_group = QGroupBox("Настройки смены")
        interval_layout = QVBoxLayout()

        # Выбор интервала
        interval_control = QHBoxLayout()
        interval_control.addWidget(QLabel("Интервал (секунды):"))

        self.interval_spinbox = QSpinBox()
        self.interval_spinbox.setRange(5, 3600)
        self.interval_spinbox.setValue(30)
        self.interval_spinbox.setSuffix(" сек")
        interval_control.addWidget(self.interval_spinbox)

        interval_control.addStretch()
        interval_layout.addLayout(interval_control)

        # Кнопки управления
        button_layout = QHBoxLayout()

        self.start_btn = QPushButton("▶ Старт")
        self.start_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        self.start_btn.clicked.connect(self.start_changing)

        self.stop_btn = QPushButton("⏹ Стоп")
        self.stop_btn.setStyleSheet("background-color: #f44336; color: white; font-weight: bold;")
        self.stop_btn.clicked.connect(self.stop_changing)
        self.stop_btn.setEnabled(False)

        self.manual_btn = QPushButton("🎨 Сменить сейчас")
        self.manual_btn.clicked.connect(self.change_wallpaper_manual)

        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.stop_btn)
        button_layout.addWidget(self.manual_btn)
        interval_layout.addLayout(button_layout)

        interval_group.setLayout(interval_layout)
        main_layout.addWidget(interval_group)

        # Статус бар
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Готов")

        # Создаем объект для смены обоев
        self.changer = WallpaperChanger([], 30)
        self.changer.changed.connect(self.on_wallpaper_changed)

        # Таймер для обновления статуса
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start(1000)

    def load_wallpapers(self):
        """Загрузка списка изображений из выбранной папки"""
        self.wallpaper_files = []
        self.wallpaper_list.clear()

        if not os.path.exists(self.wallpaper_dir):
            os.makedirs(self.wallpaper_dir, exist_ok=True)
            self.status_bar.showMessage(f"Создана папка: {self.wallpaper_dir}")

        # Поддерживаемые форматы
        extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp'}

        try:
            for file in os.listdir(self.wallpaper_dir):
                if Path(file).suffix.lower() in extensions:
                    full_path = os.path.join(self.wallpaper_dir, file)
                    self.wallpaper_files.append(full_path)

                    item = QListWidgetItem(file)
                    self.wallpaper_list.addItem(item)

            if self.wallpaper_files:
                self.status_bar.showMessage(f"Загружено {len(self.wallpaper_files)} обоев")
                if self.changer:
                    self.changer.update_wallpaper_list(self.wallpaper_files)
            else:
                self.status_bar.showMessage("В папке нет изображений! Добавьте обои.")

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить обои: {e}")

    def select_folder(self):
        """Выбор папки с обоями"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Выберите папку с обоями",
            self.wallpaper_dir
        )

        if folder:
            self.wallpaper_dir = folder
            self.folder_label.setText(folder)
            self.load_wallpapers()

            # Если смена активна, обновляем список
            if self.changer and self.changer.running:
                self.changer.update_wallpaper_list(self.wallpaper_files)

    def preview_wallpaper(self, item):
        """Предпросмотр обоев"""
        index = self.wallpaper_list.row(item)
        if 0 <= index < len(self.wallpaper_files):
            wallpaper = self.wallpaper_files[index]
            if set_wallpaper_linux(wallpaper):
                self.status_bar.showMessage(f"Предпросмотр: {item.text()}", 3000)

    def start_changing(self):
        """Запуск автоматической смены обоев"""
        if not self.wallpaper_files:
            QMessageBox.warning(self, "Предупреждение",
                              "Нет обоев для смены! Добавьте изображения в папку.")
            return

        interval = self.interval_spinbox.value()
        self.changer.update_interval(interval)
        self.changer.update_wallpaper_list(self.wallpaper_files)
        self.changer.start()

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.interval_spinbox.setEnabled(False)

        self.status_bar.showMessage(f"Автоматическая смена запущена (интервал: {interval} сек)")

    def stop_changing(self):
        """Остановка автоматической смены обоев"""
        if self.changer:
            self.changer.stop()

        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.interval_spinbox.setEnabled(True)

        self.status_bar.showMessage("Автоматическая смена остановлена", 3000)

    def change_wallpaper_manual(self):
        """Ручная смена обоев"""
        if self.wallpaper_files:
            wallpaper = random.choice(self.wallpaper_files)
            if set_wallpaper_linux(wallpaper):
                self.on_wallpaper_changed(wallpaper)

    def on_wallpaper_changed(self, wallpaper_path):
        """Слот для обработки смены обоев"""
        filename = os.path.basename(wallpaper_path)
        self.status_bar.showMessage(f"Обои изменены: {filename}")

    def update_status(self):
        """Обновление статуса в строке состояния"""
        if self.changer and self.changer.running:
            status = f"Активно | Интервал: {self.changer.interval_seconds} сек"
        else:
            status = "Остановлено"

        if hasattr(self, 'status_label'):
            self.status_label.setText(status)
        else:
            self.status_bar.showMessage(status, 1000)

    def closeEvent(self, event):
        """Обработка закрытия окна"""
        if self.changer:
            self.changer.stop()
        event.accept()

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Современный стиль

    window = WallpaperApp()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
