"""Display widgets for real-time and offscreen rendering."""

import numpy as np
from loguru import logger
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QPainter, QPaintEvent
from PySide6.QtWidgets import QWidget


class FramebufferWidget(QWidget):
    """Widget that displays a framebuffer backed by a NumPy array.

    This widget provides real-time display of rendered content.
    """

    def __init__(self, w: int = 640, h: int = 360, parent: QWidget | None = None) -> None:
        """Initialize the framebuffer widget.

        Args:
            w: Width of the framebuffer
            h: Height of the framebuffer
            parent: Parent widget

        """
        super().__init__(parent)
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
            QImage.Format.Format_RGBA8888,
        )

        # Keep a reference to prevent GC surprises
        self.qimg._buf = self.buf  # noqa: SLF001

        self.setFixedSize(w, h)
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent)

        # Timer for refresh (will be controlled by execution engine)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)

        logger.debug(f"FramebufferWidget initialized: {w}x{h}")

    def start_refresh(self, fps: int = 60) -> None:
        """Start the refresh timer.

        Args:
            fps: Frames per second

        """
        interval_ms = int(1000 / fps)
        self.timer.start(interval_ms)
        logger.debug(f"Refresh timer started: {fps} FPS")

    def stop_refresh(self) -> None:
        """Stop the refresh timer."""
        self.timer.stop()
        logger.debug("Refresh timer stopped")

    def clear(self, color: tuple[int, int, int] = (20, 20, 20)) -> None:
        """Clear the framebuffer to a solid color.

        Args:
            color: RGB color tuple

        """
        self.buf[..., :3] = color

    def paintEvent(self, event: QPaintEvent) -> None:  # noqa: N802, ARG002
        """Handle paint events by drawing the framebuffer to the widget.

        Args:
            event: The paint event

        """
        p = QPainter(self)
        p.drawImage(0, 0, self.qimg)

    def get_painter(self) -> QPainter:
        """Get a QPainter for drawing into the framebuffer.

        Returns:
            QPainter configured for the framebuffer

        """
        return QPainter(self.qimg)


class OffscreenWidget:
    """Offscreen rendering widget for headless operation.

    This widget provides the same NumPy buffer interface as FramebufferWidget
    but doesn't display anything. It's used for exporting images and GIFs.
    """

    def __init__(self, w: int = 640, h: int = 360) -> None:
        """Initialize the offscreen widget.

        Args:
            w: Width of the framebuffer
            h: Height of the framebuffer

        """
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
            QImage.Format.Format_RGBA8888,
        )

        # Keep a reference to prevent GC
        self.qimg._buf = self.buf  # noqa: SLF001

        logger.debug(f"OffscreenWidget initialized: {w}x{h}")

    def clear(self, color: tuple[int, int, int] = (20, 20, 20)) -> None:
        """Clear the framebuffer to a solid color.

        Args:
            color: RGB color tuple

        """
        self.buf[..., :3] = color

    def get_painter(self) -> QPainter:
        """Get a QPainter for drawing into the framebuffer.

        Returns:
            QPainter configured for the framebuffer

        """
        return QPainter(self.qimg)

    def save_png(self, path: str) -> bool:
        """Save the current framebuffer as a PNG file.

        Args:
            path: Path to save the PNG file

        Returns:
            True if successful

        """
        success = self.qimg.save(path, "PNG")
        if success:
            logger.info(f"Saved PNG: {path}")
        else:
            logger.error(f"Failed to save PNG: {path}")
        return success

    def to_pil_image(self):  # noqa: ANN201
        """Convert the current framebuffer to a PIL Image.

        Returns:
            PIL Image object

        """
        from PIL import Image

        # Convert RGBA numpy array to PIL Image
        return Image.fromarray(self.buf, mode="RGBA")

    def save_gif(self, path: str, frames: list, duration: int = 33) -> bool:
        """Save a sequence of frames as an animated GIF.

        Args:
            path: Path to save the GIF file
            frames: List of PIL Image objects
            duration: Duration per frame in milliseconds (default: 33ms ≈ 30fps)

        Returns:
            True if successful

        """
        try:
            if not frames:
                logger.error("No frames to save")
                return False

            # Save as animated GIF
            frames[0].save(
                path,
                save_all=True,
                append_images=frames[1:],
                duration=duration,
                loop=0,
                optimize=False,
            )
            logger.info(f"Saved GIF with {len(frames)} frames: {path}")
            return True
        except Exception:
            logger.exception(f"Failed to save GIF: {path}")
            return False
