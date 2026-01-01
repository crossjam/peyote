"""Code editor widget with syntax highlighting and line numbers."""

from PySide6.QtCore import QRect, QSize, Qt
from PySide6.QtGui import QColor, QFont, QPainter, QTextFormat
from PySide6.QtWidgets import QPlainTextEdit, QTextEdit, QWidget

from .syntax_highlighter import PythonSyntaxHighlighter


class LineNumberArea(QWidget):
    """Widget for displaying line numbers in the code editor."""

    def __init__(self, editor: "CodeEditorWidget") -> None:
        """Initialize the line number area.

        Args:
            editor: Parent code editor

        """
        super().__init__(editor)
        self.code_editor = editor

    def sizeHint(self) -> QSize:  # noqa: N802
        """Return the size hint for the line number area.

        Returns:
            Size hint

        """
        return QSize(self.code_editor.line_number_area_width(), 0)

    def paintEvent(self, event) -> None:  # noqa: ANN001, N802
        """Paint the line numbers.

        Args:
            event: Paint event

        """
        self.code_editor.line_number_area_paint_event(event)


class CodeEditorWidget(QPlainTextEdit):
    """Code editor with Python syntax highlighting and line numbers."""

    def __init__(self, parent=None) -> None:  # noqa: ANN001
        """Initialize the code editor.

        Args:
            parent: Parent widget

        """
        super().__init__(parent)

        # Set up font
        font = QFont("Menlo, Monaco, Courier New, monospace")
        font.setPointSize(12)
        font.setStyleHint(QFont.StyleHint.Monospace)
        font.setFixedPitch(True)
        self.setFont(font)

        # Set tab width to 4 spaces
        self.setTabStopDistance(4 * self.fontMetrics().horizontalAdvance(' '))

        # Create line number area
        self.line_number_area = LineNumberArea(self)

        # Connect signals
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)

        # Initialize
        self.update_line_number_area_width(0)
        self.highlight_current_line()

        # Set up syntax highlighter
        self.highlighter = PythonSyntaxHighlighter(self.document())

        # Set placeholder text
        self.setPlaceholderText("# Write your Python code here...")

    def line_number_area_width(self) -> int:
        """Calculate the width needed for the line number area.

        Returns:
            Width in pixels

        """
        digits = 1
        max_num = max(1, self.blockCount())
        while max_num >= 10:
            max_num //= 10
            digits += 1

        space = 10 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def update_line_number_area_width(self, _: int) -> None:
        """Update the width of the line number area.

        Args:
            _: New block count (unused)

        """
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect: QRect, dy: int) -> None:
        """Update the line number area when the editor scrolls.

        Args:
            rect: Update rectangle
            dy: Vertical scroll delta

        """
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(
                0,
                rect.y(),
                self.line_number_area.width(),
                rect.height(),
            )

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event) -> None:  # noqa: ANN001, N802
        """Handle resize events.

        Args:
            event: Resize event

        """
        super().resizeEvent(event)

        cr = self.contentsRect()
        self.line_number_area.setGeometry(
            QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()),
        )

    def highlight_current_line(self) -> None:
        """Highlight the line containing the cursor."""
        extra_selections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor("#E8F2FF")  # Light blue highlight for current line
            selection.format.setBackground(line_color)
            selection.format.setProperty(
                QTextFormat.Property.FullWidthSelection,
                True,
            )
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)

    def line_number_area_paint_event(self, event) -> None:  # noqa: ANN001
        """Paint the line numbers.

        Args:
            event: Paint event

        """
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor("#E8E8E8"))  # Light gray for line number area

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QColor("#606060"))  # Dark gray for line numbers
                painter.drawText(
                    0,
                    int(top),
                    self.line_number_area.width() - 5,
                    self.fontMetrics().height(),
                    Qt.AlignmentFlag.AlignRight,
                    number,
                )

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1

    def keyPressEvent(self, event) -> None:  # noqa: ANN001, N802
        """Handle key press events.

        Args:
            event: Key event

        """
        # Handle Tab key to insert spaces
        if event.key() == Qt.Key.Key_Tab:
            cursor = self.textCursor()
            cursor.insertText("    ")  # Insert 4 spaces
            return

        # Handle Shift+Tab for dedent
        if event.key() == Qt.Key.Key_Backtab:
            cursor = self.textCursor()
            cursor.movePosition(cursor.MoveOperation.StartOfLine)
            line_text = cursor.block().text()
            if line_text.startswith("    "):
                cursor.movePosition(
                    cursor.MoveOperation.Right,
                    cursor.MoveMode.KeepAnchor,
                    4,
                )
                cursor.removeSelectedText()
            return

        # Auto-indent on Enter
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            cursor = self.textCursor()
            block_text = cursor.block().text()
            indent = len(block_text) - len(block_text.lstrip())

            # Add extra indent after colon
            if block_text.rstrip().endswith(":"):
                indent += 4

            super().keyPressEvent(event)
            cursor = self.textCursor()
            cursor.insertText(" " * indent)
            return

        super().keyPressEvent(event)
