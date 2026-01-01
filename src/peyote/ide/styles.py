"""Qt stylesheet definitions for the IDE."""

# Processing-inspired theme
PROCESSING_THEME = """
QMainWindow {
    background-color: #7CA5C4;
}

QToolBar {
    background-color: #7CA5C4;
    border: none;
    spacing: 2px;
    padding: 2px;
    min-height: 32px;
    max-height: 32px;
}

QPushButton {
    background-color: #6A95B4;
    color: #ffffff;
    border: 1px solid #5a85a4;
    border-radius: 3px;
    padding: 3px 10px;
    min-width: 50px;
    max-height: 24px;
}

QPushButton:hover {
    background-color: #5a85a4;
}

QPushButton:pressed {
    background-color: #4a7594;
}

QPushButton:disabled {
    background-color: #8aadca;
    color: #c0c0c0;
}

QTabWidget::pane {
    border: 2px solid #5a85a4;
    background-color: #ffffff;
}

QTabBar {
    alignment: left;
}

QTabBar::tab {
    background-color: #6A95B4;
    color: #ffffff;
    border: 1px solid #5a85a4;
    border-bottom: none;
    padding: 4px 10px;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background-color: #ffffff;
    color: #000000;
}

QTabBar::tab:hover {
    background-color: #5a85a4;
}

/* Code editor - white background */
QPlainTextEdit {
    background-color: #ffffff;
    color: #000000;
    border: 2px solid #5a85a4;
    font-family: 'Menlo', 'Monaco', 'Courier New', monospace;
    font-size: 12pt;
}

/* Console - dark background */
QTextEdit#console {
    background-color: #2d3436;
    color: #dfe6e9;
    font-family: 'Menlo', 'Monaco', 'Courier New', monospace;
    font-size: 11pt;
    border: 2px solid #5a85a4;
}

/* Messages area - light blue */
QTextEdit#messages {
    background-color: #7CA5C4;
    color: #000000;
    font-size: 10pt;
    border: 2px solid #5a85a4;
}

QSplitter::handle {
    background-color: #5a85a4;
    width: 2px;
    height: 2px;
}

QSplitter::handle:hover {
    background-color: #4a7594;
}

QMenuBar {
    background-color: #7CA5C4;
    color: #000000;
    padding: 2px;
}

QMenuBar::item {
    padding: 2px 8px;
    background-color: transparent;
}

QMenuBar::item:selected {
    background-color: #6A95B4;
}

QMenu {
    background-color: #f0f0f0;
    color: #000000;
    border: 1px solid #5a85a4;
}

QMenu::item:selected {
    background-color: #7CA5C4;
}

QStatusBar {
    background-color: #7CA5C4;
    color: #000000;
    border-top: 1px solid #5a85a4;
}

/* Style for the FramebufferWidget border */
QWidget#display_widget {
    border: 2px solid #5a85a4;
}
"""


def get_stylesheet() -> str:
    """Get the default stylesheet for the IDE.

    Returns:
        Qt stylesheet string

    """
    return PROCESSING_THEME
