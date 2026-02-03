"""
pc_taskbar_badge.py

Custom text display widget for windows taskbars
"""

import sys, os
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QFont, QColor, QGuiApplication
from PySide6.QtWidgets import QApplication, QWidget


class PCBadge(QWidget):
    def __init__(self, text, bg="#20242B", fg="#FFFFFF", border_radius=4):
        super().__init__(None, Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.text = text
        self.bg = QColor(bg); self.fg = QColor(fg)
        self.padding = (8, 6)
        self.font = QFont("Segoe UI", 14, QFont.Bold)
        self.border_radius = border_radius
        
        screen = QGuiApplication.primaryScreen()
        available = screen.availableGeometry()
        window = screen.geometry()
        taskbar_height = window.height() - available.height()
        self.resize(150, 40 * (taskbar_height / 48))

        self.placeBottomLeft(available)
        self._drag_off = 0

        # Keep the badge from falling behind taskbar/other always-on-top windows
        self._top_timer = QTimer(self)
        self._top_timer.setInterval(200)
        self._top_timer.timeout.connect(self.ensureOnTop)
        self._top_timer.start()

        # Prevent the badge from stealing focus
        self.setAttribute(Qt.WA_ShowWithoutActivating, True)
        self.setFocusPolicy(Qt.NoFocus)


    def placeBottomLeft(self, available):
        x, y = available.left() + 5, available.bottom() + 5
        self.move(x, y)


    def paintEvent(self, _):
        from PySide6.QtGui import QPainterPath
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        path = QPainterPath()
        path.addRoundedRect(self.rect(), self.border_radius, self.border_radius)
        p.fillPath(path, self.bg)
        p.setFont(self.font)
        p.setPen(self.fg)
        metrics = p.fontMetrics()
        tw = metrics.horizontalAdvance(self.text)
        th = metrics.ascent()
        x = (self.width() - tw) // 2
        y = (self.height() + th) // 2 - 2
        p.drawText(x, y, self.text)


    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            if (e.modifiers() & (Qt.ControlModifier | Qt.ShiftModifier)) == (Qt.ControlModifier | Qt.ShiftModifier):
                # Close window if also holding CTRL and SHIFT
                self.close()
                sys.exit()
                return
            
        super().mousePressEvent(e)

    
    def mouseMoveEvent(self, e):
        if self._drag_off:
            self.move(e.globalPosition().toPoint() - self._drag_off)


    def mouseReleaseEvent(self, e):
        self._drag_off = None


    def ensureOnTop(self):
        # Qt-level bump
        if self.isVisible():
            self.raise_()

        # Win32-level bump (more reliable vs taskbar)
        if sys.platform == "win32" and self.isVisible():
            import ctypes
            from ctypes import wintypes

            user32 = ctypes.WinDLL("user32", use_last_error=True)
            HWND_TOPMOST = -1
            SWP_NOMOVE = 0x0002
            SWP_NOSIZE = 0x0001
            SWP_NOACTIVATE = 0x0010
            SWP_SHOWWINDOW = 0x0040

            user32.SetWindowPos(
                wintypes.HWND(int(self.winId())),
                wintypes.HWND(HWND_TOPMOST),
                0, 0, 0, 0,
                SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE | SWP_SHOWWINDOW
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    host = os.environ.get("COMPUTERNAME") or os.environ.get("HOSTNAME") or "PC"
    w = PCBadge(text=host, bg="#FF8A00", fg="#000000", border_radius=8)
    w.show()
    sys.exit(app.exec())
