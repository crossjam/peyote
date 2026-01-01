"""Main IDE window implementation."""

import sys

from loguru import logger
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QSplitter,
    QTabWidget,
    QTextEdit,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from .code_editor import CodeEditorWidget
from .display_widget import FramebufferWidget
from .logging_setup import setup_logging
from .styles import get_stylesheet
from .tab_manager import TabManager


class ProcessingIDEWindow(QMainWindow):
    """Main window for the Processing-like IDE."""

    def __init__(self) -> None:
        """Initialize the IDE window."""
        super().__init__()
        self.setWindowTitle("Peyote IDE")
        self.resize(1400, 900)

        # Apply dark theme stylesheet
        self.setStyleSheet(get_stylesheet())

        # Initialize tab manager (will be set after creating UI)
        self.tab_manager: TabManager | None = None

        # Create UI components
        self._create_menu_bar()
        self._create_toolbar()
        self._create_main_layout()
        self._create_status_bar()

        logger.info("IDE window initialized")

    def _create_menu_bar(self) -> None:
        """Create the menu bar."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")
        file_menu.addAction("&New Tab", self._on_new_tab, "Ctrl+T")
        file_menu.addAction("&New Project")
        file_menu.addAction("&Open Project...")
        file_menu.addAction("&Save Project")
        file_menu.addAction("Save Project &As...")
        file_menu.addSeparator()
        file_menu.addAction("&Quit")

        # Edit menu
        edit_menu = menubar.addMenu("&Edit")
        edit_menu.addAction("&Undo")
        edit_menu.addAction("&Redo")
        edit_menu.addSeparator()
        edit_menu.addAction("Cu&t")
        edit_menu.addAction("&Copy")
        edit_menu.addAction("&Paste")

        # Sketch menu
        sketch_menu = menubar.addMenu("&Sketch")
        sketch_menu.addAction("&Run")
        sketch_menu.addAction("&Stop")

        # Help menu
        help_menu = menubar.addMenu("&Help")
        help_menu.addAction("&About")
        help_menu.addAction("&Documentation")

    def _create_toolbar(self) -> None:
        """Create the toolbar with Play/Stop buttons."""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        # Play button
        self.play_button = QPushButton("▶ Play")
        self.play_button.setToolTip("Run the sketch (Ctrl+R)")
        toolbar.addWidget(self.play_button)

        # Stop button
        self.stop_button = QPushButton("⏹ Stop")
        self.stop_button.setToolTip("Stop the sketch (Ctrl+.)")
        self.stop_button.setEnabled(False)
        toolbar.addWidget(self.stop_button)

        toolbar.addSeparator()

        # Settings button (placeholder)
        settings_button = QPushButton("⚙ Settings")
        settings_button.setToolTip("Open settings")
        toolbar.addWidget(settings_button)

    def _create_main_layout(self) -> None:
        """Create the main layout with splitters."""
        # Create central widget and main splitter
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Main horizontal splitter (left pane | right pane)
        main_splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left pane with vertical splitter (editor | bottom panel)
        left_pane = QSplitter(Qt.Orientation.Vertical)

        # Editor tabs
        self.editor_tabs = QTabWidget()
        self.editor_tabs.setTabsClosable(True)
        self.editor_tabs.setMovable(True)

        # Initialize tab manager
        self.tab_manager = TabManager(self.editor_tabs)

        # Add a default tab with code editor
        self.tab_manager.add_new_tab("sketch")

        left_pane.addWidget(self.editor_tabs)

        # Bottom panel with messages and console
        bottom_panel = QSplitter(Qt.Orientation.Horizontal)

        # Messages area
        self.messages_area = QTextEdit()
        self.messages_area.setObjectName("messages")
        self.messages_area.setReadOnly(True)
        self.messages_area.setPlaceholderText("Messages will appear here...")
        self.messages_area.setMaximumHeight(150)
        bottom_panel.addWidget(self.messages_area)

        # Console area
        self.console_area = QTextEdit()
        self.console_area.setObjectName("console")
        self.console_area.setReadOnly(True)
        self.console_area.setPlaceholderText("Console output will appear here...")
        self.console_area.setMaximumHeight(150)
        bottom_panel.addWidget(self.console_area)

        left_pane.addWidget(bottom_panel)

        # Set initial sizes for left pane (editor: 70%, bottom: 30%)
        left_pane.setSizes([600, 200])

        # Right pane with display widget
        self.display_widget = FramebufferWidget(w=640, h=360)

        # Add both panes to main splitter
        main_splitter.addWidget(left_pane)
        main_splitter.addWidget(self.display_widget)

        # Set initial sizes (left: 70%, right: 30%)
        main_splitter.setSizes([900, 400])

        main_layout.addWidget(main_splitter)

    def _create_status_bar(self) -> None:
        """Create the status bar."""
        status_bar = self.statusBar()
        status_bar.showMessage("Ready")

    def show_message(self, message: str) -> None:
        """Show a message in the messages area.

        Args:
            message: Message to display

        """
        self.messages_area.append(message)
        self.statusBar().showMessage(message, 3000)

    def show_console(self, text: str) -> None:
        """Show text in the console area.

        Args:
            text: Text to display

        """
        self.console_area.append(text)

    def _on_new_tab(self) -> None:
        """Handle new tab action."""
        if self.tab_manager:
            self.tab_manager.add_new_tab()
            self.show_message("New tab created")


def launch_ide() -> int:
    """Launch the IDE application.

    Returns:
        Exit code

    """
    # Set up logging
    setup_logging()

    # Create Qt application
    app = QApplication(sys.argv)

    # Create and show the IDE window
    window = ProcessingIDEWindow()
    window.show()

    logger.info("IDE application started")

    # Run the application
    return app.exec()
