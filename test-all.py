# test-all.py (static, no importlib)
import sys
import unittest
from pathlib import Path
import types

ROOT = Path(__file__).parent.resolve()

# Ensure project root is importable so tests can do: from enigma.rotor import Rotor
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Explicit, static list of test files relative to project root.
TEST_FILES = [
    ROOT / "enigma" / "test-enigma.py",
    ROOT / "bombe"  / "test-bombe.py",
]

def load_module_from_file(py_path: Path, alias: str):
    """Load a Python file into a new module object using exec(), no importlib."""
    mod = types.ModuleType(alias)
    mod.__file__ = str(py_path)
    code = py_path.read_text(encoding="utf-8")
    exec(compile(code, str(py_path), "exec"), mod.__dict__)
    return mod

def main():
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    for path in TEST_FILES:
        alias = "tests_" + "_".join(path.relative_to(ROOT).parts).replace("-", "_").replace(".", "_")
        mod = load_module_from_file(path, alias)
        suite.addTests(loader.loadTestsFromModule(mod))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)

if __name__ == "__main__":
    main()
