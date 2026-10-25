"""Compatibility entry point; pass OpenJLPT and Japanese Language Data paths."""
import runpy,pathlib
runpy.run_path(str(pathlib.Path(__file__).parent/"scripts/expand_n1.py"),run_name="__main__")
