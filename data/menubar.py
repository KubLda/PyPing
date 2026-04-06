import os
import shutil
from pathlib import Path
from PySide6 import QtCore, QtWidgets, QtGui
import json

def default_hosts_path():
    return str(Path.home() / ".pyping_hosts.json")

def set_menubar(window):
    self = window

    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_DontUseNativeMenuBar, True)
    menubar = self.menuBar()
    file_menu = menubar.addMenu("&Файл")
    view_menu = menubar.addMenu("&Вид")
    help_menu = menubar.addMenu("&Справка")

    # Действия Файл
    load_action = QtGui.QAction("Загрузить", self)
    load_action.setShortcut("Ctrl+O")
    load_action.triggered.connect(lambda: on_load(self))

    save_action = QtGui.QAction("Сохранить", self)
    save_action.setShortcut(QtGui.QKeySequence.Save)
    save_action.triggered.connect(lambda: on_save(self))
    exit_action = QtGui.QAction("Выход", self)
    exit_action.setShortcut("Ctrl+Q")
    exit_action.triggered.connect(self.close)

    file_menu.addAction(load_action)
    file_menu.addAction(save_action)
    file_menu.addSeparator()
    file_menu.addAction(exit_action)

    # Действия Вид
    toggle_headers = QtGui.QAction("Показывать заголовки", self, checkable=True, checked=True)
    toggle_headers.triggered.connect(lambda checked: _toggle_headers(self, checked))
    view_menu.addAction(toggle_headers)

    # Действия Справка
    about_action = QtGui.QAction("О программе", self)
    about_action.triggered.connect(lambda: show_about(self))
    help_menu.addAction(about_action)

    # Добавить хост (в меню Файл, сверху)
    add_action = QtGui.QAction("Добавить хост...", self)
    add_action.setShortcut("Ctrl+N")
    add_action.triggered.connect(lambda: on_add_host(self))
    file_menu.insertAction(load_action, add_action)

    # Статусбар
    self.status = self.statusBar()
    self.status.showMessage("Готово")

def on_load(self):
    path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл для загрузки", filter="JSON Files (*.json);;All Files (*)")
    if not path:
        return
    dst = default_hosts_path()
    try:
        # попробуем просто скопировать выбранный файл в дефолтный путь
        shutil.copyfile(path, dst)
        # затем обновим список в UI: если есть метод load_hosts, используем его, иначе читаем JSON и заполняем listw
        try:
            if hasattr(self, "load_hosts"):
                self.load_hosts(dst)
            else:
                with open(dst, "r", encoding="utf-8") as f:
                    data = json.load(f)
                # ожидается, что data — список хостов; адаптируйте под вашу структуру
                self.listw.list.clear()
                for h in data:
                    self.listw.add_host(h)
        except Exception:
            pass
        self.status.showMessage(f"Загружено в {dst}", 4000)
    except Exception as e:
        QtWidgets.QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить файл: {e}")

def on_save(self):
    path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Сохранить список хостов", filter="JSON Files (*.json);;All Files (*)")
    if path:
        try:
            self.save_hosts(path)
            self.status.showMessage(f"Сохранено: {path}", 4000)
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Ошибка", f"Не удалось сохранить: {e}")

def _toggle_headers(self, checked):
    try:
        self.table.horizontalHeader().setVisible(checked)
    except Exception:
        pass

def show_about(self):
    QtWidgets.QMessageBox.information(None, "О программе", "PyPing")

def on_add_host(self):
    text, ok = QtWidgets.QInputDialog.getText(self, "Добавить хост", "Имя или IP адрес хоста:")
    if ok and text.strip():
        self.listw.add_host(text.strip())
        try:
            self.save_hosts()
            list_changed = QtCore.Signal()
            list_changed.emit()
        except Exception:
            pass
