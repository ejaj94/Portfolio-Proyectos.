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
from services.i18n import I18nService
from services.cv_service import CVGenerationService

def main() -> None:
    i18n_svc = I18nService("es")
    cv_svc = CVGenerationService()
    app = MainWindow(i18n_svc, cv_svc)
    app.mainloop()

if __name__ == "__main__":
    main()
