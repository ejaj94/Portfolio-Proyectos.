"""
app.py — Application Entry Point
=================================
Launches the trilingual CV Generator with Graphical User Interface.
"""
import sys
import os

# Ensure the core module is in the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import MainWindow

def main() -> None:
    app = MainWindow()
    app.run()

if __name__ == "__main__":
    main()
