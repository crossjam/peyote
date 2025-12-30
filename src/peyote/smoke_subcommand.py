"""Smoke test subcommand for Pyside6 integration."""

import sys

import numpy as np
import typer
from loguru import logger
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QImage, QKeyEvent, QPainter, QPaintEvent, QPen
from PySide6.QtWidgets import QApplication, QWidget


class FramebufferWidget(QWidget):
    """Widget that displays a framebuffer backed by a NumPy array."""

    def __init__(self, w: int = 640, h: int = 360) -> None:
        """Initialize the framebuffer widget.

        Args:
            w: Width of the framebuffer
            h: Height of the framebuffer

        """
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
        self.qimg._buf = self.buf  # noqa: SLF001

        self.t = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(16)  # ~60 FPS

        self.setFixedSize(w, h)
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent)

    def tick(self) -> None:
        """Update the framebuffer and trigger a repaint."""
        # ---- Clear via NumPy (fast, bulk op)
        self.buf[..., :3] = 20

        # ---- Draw vector graphics INTO THE SHARED BUFFER
        p = QPainter(self.qimg)
        p.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        pen = QPen(QColor(255, 180, 0))
        pen.setWidth(4)
        p.setPen(pen)

        x = self.t % self.w
        p.drawEllipse(x - 30, self.h // 2 - 30, 60, 60)

        p.end()

        self.t += 5
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:  # noqa: N802, ARG002
        """Handle paint events by drawing the framebuffer to the widget.

        Args:
            event: The paint event

        """
        p = QPainter(self)
        p.drawImage(0, 0, self.qimg)

    def keyPressEvent(self, event: QKeyEvent) -> None:  # noqa: N802
        """Handle key press events.

        Args:
            event: The key event

        """
        if event.key() == Qt.Key.Key_Q:
            logger.info("Q key pressed, exiting application")
            QApplication.quit()
        super().keyPressEvent(event)


cli = typer.Typer()


@cli.command()
def smoke(
    width: int = typer.Option(640, "--width", "-w", help="Window width"),
    height: int = typer.Option(360, "--height", "-h", help="Window height"),
) -> None:
    """Run a smoke test of the Pyside6 integration.

    This displays a window with a framebuffer backed by a NumPy array.
    Press 'q' to exit.
    """
    logger.info(f"Starting smoke test with {width=}, {height=}")
    app = QApplication(sys.argv)
    w = FramebufferWidget(width, height)
    w.show()
    sys.exit(app.exec())
