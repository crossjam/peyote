"""Package management for sketch modules."""

from pathlib import Path

from loguru import logger

from .app_dirs import get_sketches_dir


class PackageManager:
    """Manages the package structure for sketch modules."""

    def __init__(self, project_name: str = "untitled") -> None:
        """Initialize the package manager.

        Args:
            project_name: Name of the project/package

        """
        self.project_name = project_name
        self.project_dir = get_sketches_dir() / project_name
        self.project_dir.mkdir(parents=True, exist_ok=True)

        # Create __init__.py if it doesn't exist
        init_file = self.project_dir / "__init__.py"
        if not init_file.exists():
            init_file.write_text('"""Auto-generated package for sketch modules."""\n')

        logger.info(f"Package manager initialized for: {project_name}")
        logger.debug(f"Project directory: {self.project_dir}")

    def save_module(self, module_name: str, content: str) -> Path:
        """Save a module to the package.

        Args:
            module_name: Name of the module (without .py extension)
            content: Python code content

        Returns:
            Path to the saved module file

        """
        # Ensure module name is valid
        if not module_name.endswith(".py"):
            module_name += ".py"

        module_path = self.project_dir / module_name
        module_path.write_text(content)

        logger.debug(f"Saved module: {module_path}")
        return module_path

    def save_all_modules(self, modules: dict[str, str]) -> dict[str, Path]:
        """Save multiple modules to the package.

        Args:
            modules: Dictionary mapping module names to content

        Returns:
            Dictionary mapping module names to file paths

        """
        paths = {}
        for name, content in modules.items():
            paths[name] = self.save_module(name, content)

        logger.info(f"Saved {len(modules)} modules")
        return paths

    def get_module_path(self, module_name: str) -> Path:
        """Get the path to a module file.

        Args:
            module_name: Name of the module

        Returns:
            Path to the module file

        """
        if not module_name.endswith(".py"):
            module_name += ".py"

        return self.project_dir / module_name

    def module_exists(self, module_name: str) -> bool:
        """Check if a module exists.

        Args:
            module_name: Name of the module

        Returns:
            True if module exists

        """
        return self.get_module_path(module_name).exists()

    def get_package_dir(self) -> Path:
        """Get the package directory.

        Returns:
            Path to package directory

        """
        return self.project_dir

    def clear_package(self) -> None:
        """Clear all module files in the package (except __init__.py)."""
        for file in self.project_dir.glob("*.py"):
            if file.name != "__init__.py":
                file.unlink()
                logger.debug(f"Removed module: {file}")
