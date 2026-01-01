"""Execution engine for running sketches."""

import io
import sys
from contextlib import redirect_stderr, redirect_stdout

from loguru import logger
from PySide6.QtCore import QTimer

from .display_widget import FramebufferWidget
from .module_loader import ModuleLoader
from .package_manager import PackageManager


class SketchExecutor:
    """Executes user sketch modules with setup() and draw() functions."""

    def __init__(
        self,
        display_widget: FramebufferWidget,
        console_callback=None,  # noqa: ANN001
    ) -> None:
        """Initialize the sketch executor.

        Args:
            display_widget: Display widget for rendering
            console_callback: Function to call with console output

        """
        self.display_widget = display_widget
        self.console_callback = console_callback

        self.package_manager: PackageManager | None = None
        self.module_loader = ModuleLoader()

        self.main_module = None
        self.setup_func = None
        self.draw_func = None

        self.is_running = False
        self.frame_count = 0

        # Timer for calling draw() repeatedly
        self.draw_timer = QTimer()
        self.draw_timer.timeout.connect(self._execute_draw)

        logger.info("Sketch executor initialized")

    def load_and_run(
        self,
        modules: dict[str, str],
        main_module_name: str = "sketch",
    ) -> bool:
        """Load sketch modules and start execution.

        Args:
            modules: Dictionary mapping module names to content
            main_module_name: Name of the main module (without .py)

        Returns:
            True if successfully started

        """
        try:
            # Stop any running sketch
            self.stop()

            # Create package manager
            self.package_manager = PackageManager("current_sketch")

            # Save all modules to disk
            self.package_manager.save_all_modules(modules)

            # Load modules
            module_files = [f"{name}.py" if not name.endswith(".py") else name
                           for name in modules.keys()]

            loaded_modules = self.module_loader.load_package_modules(
                self.package_manager.get_package_dir(),
                module_files,
            )

            # Get the main module
            main_key = main_module_name.replace(".py", "")
            if main_key not in loaded_modules:
                error_msg = f"Main module '{main_key}' not found in loaded modules"
                logger.error(error_msg)
                self._output_to_console(f"Error: {error_msg}\n")
                return False

            self.main_module = loaded_modules[main_key]

            # Get setup() and draw() functions
            self.setup_func = self.module_loader.get_module_function(
                self.main_module,
                "setup",
            )
            self.draw_func = self.module_loader.get_module_function(
                self.main_module,
                "draw",
            )

            # Run setup() if it exists
            if self.setup_func:
                self._execute_with_output_capture(self.setup_func)
                logger.info("Executed setup()")
            else:
                logger.warning("No setup() function found in main module")

            # Start draw loop if draw() exists
            if self.draw_func:
                self.is_running = True
                self.frame_count = 0
                self.display_widget.start_refresh(fps=60)
                self.draw_timer.start(16)  # ~60 FPS
                logger.info("Started draw() loop")
            else:
                logger.warning("No draw() function found in main module")
                self._output_to_console("Warning: No draw() function found\n")

            return True

        except Exception:
            logger.exception("Failed to load and run sketch")
            self._output_to_console(f"Error loading sketch:\n{self._get_exception_text()}\n")
            return False

    def stop(self) -> None:
        """Stop the running sketch."""
        if not self.is_running:
            return

        self.is_running = False
        self.draw_timer.stop()
        self.display_widget.stop_refresh()

        # Clear display
        self.display_widget.clear()

        # Unload modules
        self.module_loader.unload_all()

        self.main_module = None
        self.setup_func = None
        self.draw_func = None
        self.frame_count = 0

        logger.info("Sketch stopped")

    def _execute_draw(self) -> None:
        """Execute the draw() function."""
        if not self.is_running or not self.draw_func:
            return

        try:
            self._execute_with_output_capture(self.draw_func)
            self.frame_count += 1
        except Exception:
            logger.exception("Error in draw() function")
            self._output_to_console(f"Error in draw():\n{self._get_exception_text()}\n")
            self.stop()

    def _execute_with_output_capture(self, func) -> None:  # noqa: ANN001
        """Execute a function and capture its output.

        Args:
            func: Function to execute

        """
        # Capture stdout and stderr
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()

        with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
            try:
                func()
            except Exception as e:
                # Print the exception so it's captured
                import traceback
                traceback.print_exc()
                raise e

        # Send captured output to console
        stdout_text = stdout_capture.getvalue()
        stderr_text = stderr_capture.getvalue()

        if stdout_text:
            self._output_to_console(stdout_text)

        if stderr_text:
            self._output_to_console(stderr_text)

    def _output_to_console(self, text: str) -> None:
        """Send text to the console.

        Args:
            text: Text to output

        """
        if self.console_callback:
            self.console_callback(text)

    def _get_exception_text(self) -> str:
        """Get formatted exception text.

        Returns:
            Exception text with traceback

        """
        import traceback
        return "".join(traceback.format_exception(*sys.exc_info()))
