"""Module loading utilities for sketch execution."""

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

from loguru import logger


class ModuleLoader:
    """Loads and manages Python modules for sketch execution."""

    def __init__(self) -> None:
        """Initialize the module loader."""
        self.loaded_modules: dict[str, ModuleType] = {}
        self.package_path: Path | None = None

    def load_module(self, module_name: str, module_path: Path) -> ModuleType:
        """Load a Python module from a file.

        Args:
            module_name: Name for the module
            module_path: Path to the .py file

        Returns:
            Loaded module object

        """
        # Create module spec
        spec = importlib.util.spec_from_file_location(module_name, module_path)

        if spec is None or spec.loader is None:
            msg = f"Could not create module spec for {module_path}"
            raise ImportError(msg)

        # Create module from spec
        module = importlib.util.module_from_spec(spec)

        # Add to sys.modules for imports to work
        sys.modules[module_name] = module

        # Execute the module
        spec.loader.exec_module(module)

        # Store reference
        self.loaded_modules[module_name] = module

        logger.debug(f"Loaded module: {module_name} from {module_path}")
        return module

    def load_package_modules(
        self,
        package_dir: Path,
        module_files: list[str],
    ) -> dict[str, ModuleType]:
        """Load all modules in a package.

        Args:
            package_dir: Directory containing the package
            module_files: List of module file names (e.g., ['main.py', 'helpers.py'])

        Returns:
            Dictionary of loaded modules

        """
        # Add package directory to sys.path if not already there
        package_dir_str = str(package_dir.parent)
        if package_dir_str not in sys.path:
            sys.path.insert(0, package_dir_str)
            logger.debug(f"Added to sys.path: {package_dir_str}")

        self.package_path = package_dir
        package_name = package_dir.name

        # Load each module
        modules = {}
        for module_file in module_files:
            module_path = package_dir / module_file
            if not module_path.exists():
                logger.warning(f"Module file not found: {module_path}")
                continue

            # Module name without .py extension
            module_base_name = module_file.replace(".py", "")

            # Full module name within package
            full_module_name = f"{package_name}.{module_base_name}"

            try:
                module = self.load_module(full_module_name, module_path)
                modules[module_base_name] = module
            except Exception:
                logger.exception(f"Failed to load module: {module_file}")

        logger.info(f"Loaded {len(modules)} modules from package: {package_name}")
        return modules

    def reload_module(self, module: ModuleType) -> ModuleType:
        """Reload a module.

        Args:
            module: Module to reload

        Returns:
            Reloaded module

        """
        reloaded = importlib.reload(module)
        logger.debug(f"Reloaded module: {module.__name__}")
        return reloaded

    def unload_all(self) -> None:
        """Unload all loaded modules."""
        for module_name in list(self.loaded_modules.keys()):
            if module_name in sys.modules:
                del sys.modules[module_name]
                logger.debug(f"Unloaded module: {module_name}")

        self.loaded_modules.clear()

        # Remove package path from sys.path
        if self.package_path:
            package_dir_str = str(self.package_path.parent)
            if package_dir_str in sys.path:
                sys.path.remove(package_dir_str)
                logger.debug(f"Removed from sys.path: {package_dir_str}")

        logger.info("All modules unloaded")

    def get_module_function(self, module: ModuleType, function_name: str):  # noqa: ANN201
        """Get a function from a module if it exists.

        Args:
            module: Module to search
            function_name: Name of the function

        Returns:
            Function object or None

        """
        return getattr(module, function_name, None)
