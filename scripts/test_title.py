"""Verify the current animated Celebi title and both start controls."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name("test_release_title.py")),run_name="__main__")
