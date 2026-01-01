"""Qt stylesheet definitions for the IDE."""

# Dark theme inspired by Processing IDE
DARK_THEME = """
QMainWindow {
    background-color: #2b2b2b;
}

QToolBar {
    background-color: #3c3f41;
    border: none;
    spacing: 2px;
    padding: 2px;
    min-height: 32px;
    max-height: 32px;
}

QPushButton {
    background-color: #4a4a4a;
    color: #ffffff;
    border: 1px solid #5a5a5a;
    border-radius: 3px;
    padding: 3px 10px;
    min-width: 50px;
    max-height: 24px;
}

QPushButton:hover {
    background-color: #5a5a5a;
}

QPushButton:pressed {
    background-color: #3a3a3a;
}

QPushButton:disabled {
    background-color: #3a3a3a;
    color: #7a7a7a;
}

QTabWidget::pane {
    border: 2px solid #555555;
    background-color: #2b2b2b;
}

QTabBar::tab {
    background-color: #3c3f41;
    color: #a9b7c6;
    border: 1px solid #555555;
    border-bottom: none;
    padding: 4px 10px;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background-color: #4e5254;
    color: #ffffff;
}

QTabBar::tab:hover {
    background-color: #5a5a5a;
}

QPlainTextEdit, QTextEdit {
    background-color: #2b2b2b;
    color: #a9b7c6;
    border: 2px solid #555555;
    font-family: 'Menlo', 'Monaco', 'Courier New', monospace;
    font-size: 12pt;
}

QTextEdit#console {
    background-color: #1e1e1e;
    color: #cccccc;
    font-family: 'Menlo', 'Monaco', 'Courier New', monospace;
    font-size: 11pt;
    border: 2px solid #555555;
}

QTextEdit#messages {
    background-color: #3c3f41;
    color: #a9b7c6;
    font-size: 10pt;
    border: 2px solid #555555;
}

QSplitter::handle {
    background-color: #555555;
    width: 2px;
    height: 2px;
}

QSplitter::handle:hover {
    background-color: #7a7a7a;
}

QMenuBar {
    background-color: #3c3f41;
    color: #a9b7c6;
    padding: 2px;
}

QMenuBar::item {
    padding: 2px 8px;
}

QMenuBar::item:selected {
    background-color: #4e5254;
}

QMenu {
    background-color: #3c3f41;
    color: #a9b7c6;
    border: 1px solid #555555;
}

QMenu::item:selected {
    background-color: #4e5254;
}

QStatusBar {
    background-color: #3c3f41;
    color: #a9b7c6;
    border-top: 1px solid #555555;
}

/* Style for the FramebufferWidget border */
QWidget#display_widget {
    border: 2px solid #555555;
}
"""


def get_stylesheet() -> str:
    """Get the default stylesheet for the IDE.

    Returns:
        Qt stylesheet string

    """
    return DARK_THEME
