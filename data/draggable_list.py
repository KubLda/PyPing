from PySide6 import QtCore, QtWidgets
from data.host_row import HostRow

class DraggableList(QtWidgets.QWidget):
    list_changed = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.list = QtWidgets.QListWidget()
        self.list.setSpacing(8)
        self.list.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.list.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.list.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.list.setStyleSheet("QListWidget::item:selected { background: transparent; } QListWidget::item { border: none; }")
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.list)

        # пересоздаём виджеты после завершения перетаскивания
        self.list.model().rowsMoved.connect(self._on_rows_moved)

    def add_host(self, name: str, lost: int = 0):
        item = QtWidgets.QListWidgetItem()
        item.setData(QtCore.Qt.UserRole, {"name": name, "lost": lost})
        widget = HostRow(name, lost)
        item.setSizeHint(widget.sizeHint())
        self.list.addItem(item)
        self.list.setItemWidget(item, widget)

        widget.delete_requested.connect(self._on_delete_requested)
        self.list_changed.emit()
        return widget

    def iterate_rows(self):
        for i in range(self.list.count()):
            it = self.list.item(i)
            w = self.list.itemWidget(it)
            if w:
                yield w

    def _on_delete_requested(self, hostrow):
        for i in range(self.list.count()):
            it = self.list.item(i)
            w = self.list.itemWidget(it)
            if w is hostrow:
                try:
                    w.delete_requested.disconnect(self._on_delete_requested)
                except Exception:
                    pass
                self.list.takeItem(i)
                w.deleteLater()
                self.list_changed.emit()
                return

    def _on_rows_moved(self, parent, start, end, destination, row):
        data_list = []
        for i in range(self.list.count()):
            it = self.list.item(i)
            data_list.append(it.data(QtCore.Qt.UserRole))

        self.list.blockSignals(True)
        widgets = []
        for i in reversed(range(self.list.count())):
            it = self.list.takeItem(i)

        for data in data_list:
            it = QtWidgets.QListWidgetItem()
            it.setData(QtCore.Qt.UserRole, data)
            widget = HostRow(data["name"], data.get("lost", 0))
            it.setSizeHint(widget.sizeHint())
            self.list.addItem(it)
            self.list.setItemWidget(it, widget)
            widget.delete_requested.connect(self._on_delete_requested)

        self.list.blockSignals(False)
        self.list_changed.emit()
