"""Python syntax highlighter for the code editor."""

from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QColor, QFont, QSyntaxHighlighter, QTextCharFormat


class PythonSyntaxHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for Python code."""

    def __init__(self, parent=None) -> None:  # noqa: ANN001
        """Initialize the syntax highlighter.

        Args:
            parent: Parent text document

        """
        super().__init__(parent)

        # Define formatting styles for light background
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#0033B3"))  # Dark blue for keywords
        keyword_format.setFontWeight(QFont.Weight.Bold)

        builtin_format = QTextCharFormat()
        builtin_format.setForeground(QColor("#871094"))  # Purple for builtins

        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#067D17"))  # Green for strings

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#8C8C8C"))  # Gray for comments
        comment_format.setFontItalic(True)

        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#1750EB"))  # Blue for numbers

        function_format = QTextCharFormat()
        function_format.setForeground(QColor("#00627A"))  # Teal for functions

        # Define highlighting rules
        self.highlighting_rules = []

        # Keywords
        keywords = [
            "and", "as", "assert", "async", "await", "break", "class", "continue",
            "def", "del", "elif", "else", "except", "False", "finally", "for",
            "from", "global", "if", "import", "in", "is", "lambda", "None",
            "nonlocal", "not", "or", "pass", "raise", "return", "True", "try",
            "while", "with", "yield",
        ]
        for keyword in keywords:
            pattern = QRegularExpression(rf"\b{keyword}\b")
            self.highlighting_rules.append((pattern, keyword_format))

        # Built-in functions
        builtins = [
            "abs", "all", "any", "bin", "bool", "bytes", "chr", "dict", "dir",
            "divmod", "enumerate", "filter", "float", "format", "hex", "input",
            "int", "isinstance", "len", "list", "map", "max", "min", "oct",
            "open", "ord", "pow", "print", "range", "repr", "round", "set",
            "slice", "sorted", "str", "sum", "tuple", "type", "zip",
        ]
        for builtin in builtins:
            pattern = QRegularExpression(rf"\b{builtin}\b")
            self.highlighting_rules.append((pattern, builtin_format))

        # Function definitions
        self.highlighting_rules.append(
            (QRegularExpression(r"\bdef\s+(\w+)"), function_format),
        )
        self.highlighting_rules.append(
            (QRegularExpression(r"\bclass\s+(\w+)"), function_format),
        )

        # Numbers
        self.highlighting_rules.append(
            (QRegularExpression(r"\b[0-9]+\.?[0-9]*\b"), number_format),
        )

        # Strings (double quotes)
        self.highlighting_rules.append(
            (QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"'), string_format),
        )

        # Strings (single quotes)
        self.highlighting_rules.append(
            (QRegularExpression(r"'[^'\\]*(\\.[^'\\]*)*'"), string_format),
        )

        # Comments
        self.highlighting_rules.append(
            (QRegularExpression(r"#[^\n]*"), comment_format),
        )

    def highlightBlock(self, text: str) -> None:  # noqa: N802
        """Highlight a block of text.

        Args:
            text: Text to highlight

        """
        for pattern, fmt in self.highlighting_rules:
            iterator = pattern.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)
