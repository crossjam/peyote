"""Tab management for the IDE."""

from pathlib import Path

from loguru import logger
from PySide6.QtWidgets import QTabWidget

from .code_editor import CodeEditorWidget


class TabManager:
    """Manager for editor tabs in the IDE."""

    def __init__(self, tab_widget: QTabWidget) -> None:
        """Initialize the tab manager.

        Args:
            tab_widget: QTabWidget to manage

        """
        self.tab_widget = tab_widget
        self.tab_counter = 1
        self.modified_tabs: set[int] = set()

        # Connect signals
        self.tab_widget.tabCloseRequested.connect(self.close_tab)

    def add_new_tab(self, name: str | None = None) -> CodeEditorWidget:
        """Add a new editor tab.

        Args:
            name: Optional name for the tab

        Returns:
            The new code editor widget

        """
        if name is None:
            name = f"module_{self.tab_counter}"
            self.tab_counter += 1

        editor = CodeEditorWidget()
        editor.textChanged.connect(lambda: self._mark_modified(editor))

        tab_index = self.tab_widget.addTab(editor, name)
        self.tab_widget.setCurrentIndex(tab_index)

        logger.info(f"Added new tab: {name}")
        return editor

    def close_tab(self, index: int) -> None:
        """Close a tab at the given index.

        Args:
            index: Tab index to close

        """
        if self.tab_widget.count() <= 1:
            logger.warning("Cannot close the last tab")
            return

        # TODO: Check if modified and prompt to save
        if index in self.modified_tabs:
            self.modified_tabs.remove(index)

        widget = self.tab_widget.widget(index)
        self.tab_widget.removeTab(index)

        if widget:
            widget.deleteLater()

        logger.info(f"Closed tab at index {index}")

    def get_current_editor(self) -> CodeEditorWidget | None:
        """Get the currently active editor.

        Returns:
            Current CodeEditorWidget or None

        """
        widget = self.tab_widget.currentWidget()
        return widget if isinstance(widget, CodeEditorWidget) else None

    def get_all_editors(self) -> list[CodeEditorWidget]:
        """Get all editor widgets.

        Returns:
            List of CodeEditorWidget instances

        """
        editors = []
        for i in range(self.tab_widget.count()):
            widget = self.tab_widget.widget(i)
            if isinstance(widget, CodeEditorWidget):
                editors.append(widget)
        return editors

    def get_tab_name(self, index: int) -> str:
        """Get the name of a tab.

        Args:
            index: Tab index

        Returns:
            Tab name

        """
        return self.tab_widget.tabText(index)

    def set_tab_name(self, index: int, name: str) -> None:
        """Set the name of a tab.

        Args:
            index: Tab index
            name: New name

        """
        self.tab_widget.setTabText(index, name)
        logger.info(f"Renamed tab {index} to: {name}")

    def _mark_modified(self, editor: CodeEditorWidget) -> None:
        """Mark a tab as modified.

        Args:
            editor: Editor that was modified

        """
        index = self.tab_widget.indexOf(editor)
        if index >= 0 and index not in self.modified_tabs:
            self.modified_tabs.add(index)
            current_text = self.tab_widget.tabText(index)
            if not current_text.endswith("*"):
                self.tab_widget.setTabText(index, current_text + "*")
