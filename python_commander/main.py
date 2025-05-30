import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QMenuBar
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPalette, QColor, QAction, QIcon

def set_app_icon(app):
    """Set the application icon for both PySide6 and macOS dock"""
    # For Qt application icon, prefer high-resolution PNG files
    qt_icon_paths = [
        # Try high-resolution PNG icons first for better quality
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "images", "logo-images", "IconOnly_NoBuffer_rounded.png"),
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "images", "logo-images", "IconOnly_Transparent.png"),
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "images", "icon", "iconset.iconset", "icon_512x512.png"),
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "images", "icon", "iconset.iconset", "icon_256x256.png"),
        # Fallback to ICNS
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "images", "icon", "iconset.icns"),
        "resources/images/logo-images/IconOnly_NoBuffer_rounded.png",
        "resources/images/logo-images/IconOnly_Transparent.png",
        "resources/images/icon/iconset.iconset/icon_512x512.png",
        "resources/images/icon/iconset.iconset/icon_256x256.png",
        "resources/images/icon/iconset.icns"
    ]
    
    icon_set = False
    for icon_path in qt_icon_paths:
        if os.path.exists(icon_path):
            print(f"Setting Qt application icon from: {icon_path}")
            icon = QIcon(icon_path)
            
            # If it's a PNG file, add multiple sizes to the icon for better scaling
            if icon_path.endswith('.png') and 'iconset.iconset' in icon_path:
                # Add multiple resolutions from the iconset
                iconset_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "images", "icon", "iconset.iconset")
                icon_sizes = ['icon_16x16.png', 'icon_32x32.png', 'icon_128x128.png', 'icon_256x256.png', 'icon_512x512.png']
                
                for size_file in icon_sizes:
                    size_path = os.path.join(iconset_dir, size_file)
                    if os.path.exists(size_path):
                        icon.addFile(size_path)
                        print(f"Added icon size: {size_file}")
            
            app.setWindowIcon(icon)
            icon_set = True
            break
    
    if not icon_set:
        print("Warning: Could not find icon file for Qt application")
    
    # For macOS, also set the dock icon using AppKit
    if sys.platform == "darwin":
        try:
            from AppKit import NSApplication, NSImage
            
            # Try to find a high-resolution PNG version for AppKit
            appkit_icon_paths = [
                os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "images", "logo-images", "IconOnly_NoBuffer_rounded.png"),
                os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "images", "logo-images", "IconOnly_Transparent.png"),
                os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "images", "icon", "iconset.iconset", "icon_512x512.png"),
                "resources/images/logo-images/IconOnly_NoBuffer_rounded.png",
                "resources/images/logo-images/IconOnly_Transparent.png",
                "resources/images/icon/iconset.iconset/icon_512x512.png"
            ]
            
            for icon_path in appkit_icon_paths:
                if os.path.exists(icon_path):
                    print(f"Setting macOS dock icon from: {icon_path}")
                    nsapp = NSApplication.sharedApplication()
                    image = NSImage.alloc().initByReferencingFile_(os.path.abspath(icon_path))
                    if image:
                        nsapp.setApplicationIconImage_(image)
                        print("Successfully set macOS dock icon")
                    else:
                        print(f"Failed to load image from {icon_path}")
                    break
            else:
                print("Warning: Could not find icon file for macOS dock")
                
        except ImportError:
            print("AppKit not available - dock icon will use default")
        except Exception as e:
            print(f"Could not set macOS dock icon: {e}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python Commander")
        self.setMinimumSize(800, 600)
        self.set_window_icon()
        self.set_initial_geometry()
        self.is_dark_mode = False
        self.init_menu_bar()

    def set_window_icon(self):
        """Set the window icon specifically for this window"""
        # Try to load the largest available icon for the window
        icon_paths = [
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "images", "logo-images", "IconOnly_NoBuffer_rounded.png"),
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "images", "logo-images", "IconOnly_Transparent.png"),
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "images", "icon", "iconset.iconset", "icon_512x512.png"),
            "resources/images/logo-images/IconOnly_NoBuffer_rounded.png",
            "resources/images/logo-images/IconOnly_Transparent.png",
            "resources/images/icon/iconset.iconset/icon_512x512.png"
        ]
        
        for icon_path in icon_paths:
            if os.path.exists(icon_path):
                print(f"Setting window icon from: {icon_path}")
                self.setWindowIcon(QIcon(icon_path))
                break

    def set_initial_geometry(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        width = screen_geometry.width() // 2
        height = screen_geometry.height() // 2
        # Set window to 1/4 of the screen size
        self.resize(width // 2, height // 2)
        # Center the window
        frame_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        # Removed dark mode button from UI

    def init_menu_bar(self):
        menu_bar = self.menuBar()
        view_menu = menu_bar.addMenu("View")
        self.toggle_dark_mode_action = QAction("Toggle Dark Mode", self)
        self.toggle_dark_mode_action.triggered.connect(self.toggle_dark_mode)
        view_menu.addAction(self.toggle_dark_mode_action)

    def toggle_dark_mode(self):
        if self.is_dark_mode:
            self.set_light_palette()
        else:
            self.set_dark_palette()
        self.is_dark_mode = not self.is_dark_mode

    def set_dark_palette(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(dark_palette)

    def set_light_palette(self):
        self.setPalette(QApplication.style().standardPalette())

def main():
    import sys
    from PySide6.QtCore import QCoreApplication
    QCoreApplication.setApplicationName("Python Commander")
    app = QApplication(sys.argv)
    set_app_icon(app)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
