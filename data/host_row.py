from PySide6 import QtCore, QtWidgets, QtGui

class HostRow(QtWidgets.QFrame):
    delete_requested = QtCore.Signal(object)
    sig_set_latency = QtCore.Signal(str)
    sig_set_status = QtCore.Signal(bool)
    sig_set_lost = QtCore.Signal(int)

    def __init__(self, host_name: str, lost_per_hour: int = 0, parent=None):
        super().__init__(parent)
        self.setObjectName("hostRow")
        self.setContentsMargins(0, 0, 0, 0)

        self._host = host_name
        self._lost = int(lost_per_hour)

        h = QtWidgets.QHBoxLayout(self)
        h.setContentsMargins(12, 8, 12, 8)
        h.setSpacing(8)

        self.circle = QtWidgets.QLabel()
        self.circle.setFixedSize(14, 14)
        h.addWidget(self.circle, alignment=QtCore.Qt.AlignVCenter)

        self.host_label = QtWidgets.QLabel(self._host)
        self.host_label.setStyleSheet("font-weight: 600;")
        h.addWidget(self.host_label, stretch=1, alignment=QtCore.Qt.AlignVCenter)

        self.latency_label = QtWidgets.QLabel("0 ms")
        self.latency_label.setStyleSheet("color: #555;")
        h.addWidget(self.latency_label, alignment=QtCore.Qt.AlignVCenter)

        self.lost_text = QtWidgets.QLabel("Lost:")
        self.lost_text.setStyleSheet("color: #333; font-size: 11px;")
        h.addWidget(self.lost_text, alignment=QtCore.Qt.AlignVCenter)

        self.lost_label = QtWidgets.QLabel(str(self._lost))
        self.lost_label.setStyleSheet("color: #a33; font-weight: 600;")
        h.addWidget(self.lost_label, alignment=QtCore.Qt.AlignVCenter)

        # Delete button — только иконка
        self.del_btn = QtWidgets.QToolButton()
        self.del_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self.del_btn.setAutoRaise(True)
        self.del_btn.setFixedSize(22, 22)
        self.del_btn.setIconSize(QtCore.QSize(16, 16))
        self.del_btn.setStyleSheet("")  # нет фона

        svg_path = "data/style/trash.svg"
        icon = QtGui.QIcon()
        if QtCore.QFile.exists(svg_path):
            icon.addFile(svg_path)
        if icon.isNull():
            icon = self.style().standardIcon(QtWidgets.QStyle.SP_TrashIcon)
        self.del_btn.setIcon(icon)

        h.addWidget(self.del_btn, alignment=QtCore.Qt.AlignVCenter)

        self.setStyleSheet("QFrame#hostRow { background: #fff; border: 1px solid #888; border-radius: 8px; }")

        self.sig_set_latency.connect(self._on_set_latency)
        self.sig_set_status.connect(self._on_set_status)
        self.sig_set_lost.connect(self._on_set_lost)

        self._set_circle_color("#e74c3c")

        self.del_btn.clicked.connect(self._on_delete_clicked)

    def _on_delete_clicked(self):
        self.delete_requested.emit(self)

    def _set_circle_color(self, color: str):
        d = 14
        pix = QtGui.QPixmap(d, d)
        pix.fill(QtCore.Qt.transparent)
        p = QtGui.QPainter(pix)
        p.setRenderHint(QtGui.QPainter.Antialiasing)
        p.setBrush(QtGui.QBrush(QtGui.QColor(color)))
        p.setPen(QtCore.Qt.NoPen)
        p.drawEllipse(0, 0, d, d)
        p.end()
        self.circle.setPixmap(pix)

    def _on_set_latency(self, text: str):
        self.latency_label.setText(text)

    def _on_set_status(self, ok: bool):
        self._set_circle_color("#2ecc71" if ok else "#e74c3c")

    def _on_set_lost(self, lost: int):
        self._lost = int(lost)
        self.lost_label.setText(str(self._lost))

    def enterEvent(self, event):
        self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.unsetCursor()
        super().leaveEvent(event)

    @property
    def host(self) -> str:
        return self._host

    @property
    def lost(self) -> int:
        return self._lost
