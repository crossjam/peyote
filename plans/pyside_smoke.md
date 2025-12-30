## Objective

Implement an initial subcommand for the updated peyote that simply displays
a frame buffer backed by an ndarray

## Tasks

- Add numpy as a dependency
- Add pyside6 as a dependency
- Create a new peyote subcommand named `smoke`

The smoke subcommand should incorporate the python code below to
render a window and display. Also configure the windows to exit the
program when a q key is pressed.

```python
import sys
import numpy as np

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QPainter, QColor, QPen
from PySide6.QtWidgets import QApplication, QWidget


class FramebufferWidget(QWidget):
    def __init__(self, w=640, h=360):
        super().__init__()
        self.w = w
        self.h = h

        # Shared RGBA framebuffer
        self.buf = np.zeros((h, w, 4), dtype=np.uint8, order="C")
        self.buf[..., 3] = 255  # opaque alpha

        # Wrap NumPy memory with QImage (NO COPY)
        self.qimg = QImage(
            self.buf.data,
            w,
            h,
            self.buf.strides[0],
            QImage.Format_RGBA8888,
        )

        # Keep a reference to prevent GC surprises
        self.qimg._buf = self.buf  # noqa

        self.t = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(16)  # ~60 FPS

        self.setFixedSize(w, h)
        self.setAttribute(Qt.WA_OpaquePaintEvent)

    def tick(self):
        # ---- Clear via NumPy (fast, bulk op)
        self.buf[..., :3] = 20

        # ---- Draw vector graphics INTO THE SHARED BUFFER
        p = QPainter(self.qimg)
        p.setRenderHint(QPainter.Antialiasing, True)

        pen = QPen(QColor(255, 180, 0))
        pen.setWidth(4)
        p.setPen(pen)

        x = (self.t % self.w)
        p.drawEllipse(x - 30, self.h // 2 - 30, 60, 60)

        p.end()

        self.t += 5
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.drawImage(0, 0, self.qimg)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = FramebufferWidget()
    w.show()
    sys.exit(app.exec())
```
