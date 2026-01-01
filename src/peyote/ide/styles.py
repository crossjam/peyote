"""Qt stylesheet definitions for the IDE."""

# Dark theme inspired by Processing IDE
DARK_THEME = """
QMainWindow {
    background-color: #2b2b2b;
}

QToolBar {
    background-color: #3c3f41;
    border: none;
    spacing: 3px;
    padding: 5px;
}

QPushButton {
    background-color: #4a4a4a;
    color: #ffffff;
    border: 1px solid #5a5a5a;
    border-radius: 3px;
    padding: 5px 15px;
    min-width: 60px;
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
    border: 1px solid #3c3f41;
    background-color: #2b2b2b;
}

QTabBar::tab {
    background-color: #3c3f41;
    color: #a9b7c6;
    border: 1px solid #2b2b2b;
    padding: 5px 10px;
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
    border: 1px solid #3c3f41;
    font-family: 'Menlo', 'Monaco', 'Courier New', monospace;
    font-size: 12pt;
}

QTextEdit#console {
    background-color: #1e1e1e;
    color: #cccccc;
    font-family: 'Menlo', 'Monaco', 'Courier New', monospace;
    font-size: 11pt;
}

QTextEdit#messages {
    background-color: #3c3f41;
    color: #a9b7c6;
    font-size: 10pt;
}

QSplitter::handle {
    background-color: #3c3f41;
}

QSplitter::handle:hover {
    background-color: #5a5a5a;
}

QMenuBar {
    background-color: #3c3f41;
    color: #a9b7c6;
}

QMenuBar::item:selected {
    background-color: #4e5254;
}

QMenu {
    background-color: #3c3f41;
    color: #a9b7c6;
    border: 1px solid #2b2b2b;
}

QMenu::item:selected {
    background-color: #4e5254;
}

QStatusBar {
    background-color: #3c3f41;
    color: #a9b7c6;
}
"""


def get_stylesheet() -> str:
    """Get the default stylesheet for the IDE.

    Returns:
        Qt stylesheet string

    """
    return DARK_THEME
