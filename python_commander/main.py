import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QMenuBar
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPalette, QColor, QAction, QIcon
from pathlib import Path

from .config import config

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
        
        # Load dark mode setting from config
        self.is_dark_mode = config.is_dark_mode()
        
        self.init_menu_bar()
        
        # Apply initial theme
        if self.is_dark_mode:
            self.set_dark_palette()
        else:
            self.set_light_palette()

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
        
        # Try to get window size from config
        width = config.get("settings.window_size.width", 800)
        height = config.get("settings.window_size.height", 600)
        
        # Set window size
        self.resize(width, height)
        
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

    def init_menu_bar(self):
        menu_bar = self.menuBar()
        
        # View menu
        view_menu = menu_bar.addMenu("View")
        self.toggle_dark_mode_action = QAction("Toggle Dark Mode", self)
        self.toggle_dark_mode_action.triggered.connect(self.toggle_dark_mode)
        view_menu.addAction(self.toggle_dark_mode_action)
        
        # File menu for monitored paths
        file_menu = menu_bar.addMenu("File")
        self.manage_paths_action = QAction("Manage Monitored Paths...", self)
        self.manage_paths_action.triggered.connect(self.show_path_manager)
        file_menu.addAction(self.manage_paths_action)

    def toggle_dark_mode(self):
        # Use config to toggle and save
        self.is_dark_mode = config.toggle_dark_mode()
        
        if self.is_dark_mode:
            self.set_dark_palette()
        else:
            self.set_light_palette()
        
        print(f"Dark mode: {'enabled' if self.is_dark_mode else 'disabled'}")

    def show_path_manager(self):
        """Show dialog to manage monitored paths"""
        from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QListWidget, 
                                       QPushButton, QFileDialog, QLabel, QSplitter)
        from PySide6.QtCore import Qt
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Manage Monitored Paths")
        dialog.setMinimumSize(500, 400)
        dialog.resize(600, 450)
        
        # Main layout
        main_layout = QVBoxLayout(dialog)
        
        # Title
        title_label = QLabel("Folders to Monitor for Python Scripts:")
        title_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-bottom: 10px;")
        main_layout.addWidget(title_label)
        
        # Content area with splitter
        content_layout = QHBoxLayout()
        
        # Left side - Path list
        left_layout = QVBoxLayout()
        
        # List of current paths
        self.path_list = QListWidget()
        self.path_list.setMinimumWidth(350)
        
        # Load current paths
        for path in config.get_monitored_paths():
            self.path_list.addItem(path)
        
        left_layout.addWidget(self.path_list)
        
        # Right side - Control buttons
        button_layout = QVBoxLayout()
        button_layout.setAlignment(Qt.AlignTop)
        
        # Add button with + icon
        add_button = QPushButton("+")
        add_button.setMinimumHeight(28)
        add_button.setMaximumHeight(28)
        add_button.setMinimumWidth(32)
        add_button.setMaximumWidth(32)
        add_button.setStyleSheet("""
            QPushButton {
                background-color: #E0E0E0;
                color: #333333;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #D0D0D0;
                border: 1px solid #BBBBBB;
            }
            QPushButton:pressed {
                background-color: #C0C0C0;
            }
        """)
        add_button.clicked.connect(lambda: self.add_monitored_path_dialog())
        button_layout.addWidget(add_button)
        
        # Remove button with - icon
        remove_button = QPushButton("-")
        remove_button.setMinimumHeight(28)
        remove_button.setMaximumHeight(28)
        remove_button.setMinimumWidth(32)
        remove_button.setMaximumWidth(32)
        remove_button.setStyleSheet("""
            QPushButton {
                background-color: #E0E0E0;
                color: #333333;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                font-weight: bold;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #D0D0D0;
                border: 1px solid #BBBBBB;
            }
            QPushButton:pressed {
                background-color: #C0C0C0;
            }
        """)
        remove_button.clicked.connect(lambda: self.remove_monitored_path_dialog())
        button_layout.addWidget(remove_button)
        
        # Spacer
        button_layout.addStretch()
        
        # Add layouts to content
        content_layout.addLayout(left_layout, 3)  # 3/4 of the width
        content_layout.addLayout(button_layout, 1)  # 1/4 of the width
        
        main_layout.addLayout(content_layout)
        
        # Bottom buttons
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        
        close_button = QPushButton("Done")
        close_button.setMinimumHeight(32)
        close_button.setMinimumWidth(80)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #F0F0F0;
                color: #333333;
                border: 1px solid #CCCCCC;
                border-radius: 6px;
                font-weight: bold;
                padding: 6px 16px;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
                border: 1px solid #BBBBBB;
            }
            QPushButton:pressed {
                background-color: #D0D0D0;
            }
        """)
        close_button.clicked.connect(dialog.accept)
        bottom_layout.addWidget(close_button)
        
        main_layout.addLayout(bottom_layout)
        
        # Store dialog reference for the helper methods
        self.path_dialog = dialog
        
        dialog.exec()
    
    def add_monitored_path_dialog(self):
        """Add a new monitored path via folder browser"""
        from PySide6.QtWidgets import QFileDialog, QMessageBox
        
        # Open folder browser
        path = QFileDialog.getExistingDirectory(
            self.path_dialog, 
            "Select Folder to Monitor",
            str(Path.home())  # Start at user's home directory
        )
        
        if path:
            # Check if path already exists
            current_paths = config.get_monitored_paths()
            if path in current_paths:
                QMessageBox.information(
                    self.path_dialog,
                    "Folder Already Monitored",
                    f"The folder '{path}' is already being monitored."
                )
                return
            
            # Add to config
            config.add_monitored_path(path)
            
            # Add to UI list
            self.path_list.addItem(path)
            
            # Select the newly added item
            self.path_list.setCurrentRow(self.path_list.count() - 1)
            
            print(f"Added monitored path: {path}")
    
    def remove_monitored_path_dialog(self):
        """Remove selected monitored path"""
        from PySide6.QtWidgets import QMessageBox
        
        current_item = self.path_list.currentItem()
        if not current_item:
            QMessageBox.information(
                self.path_dialog,
                "No Folder Selected",
                "Please select a folder from the list to remove."
            )
            return
        
        path = current_item.text()
        
        # Confirm removal
        reply = QMessageBox.question(
            self.path_dialog,
            "Remove Monitored Folder",
            f"Are you sure you want to stop monitoring:\n\n{path}",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Remove from config
            config.remove_monitored_path(path)
            
            # Remove from UI list
            self.path_list.takeItem(self.path_list.row(current_item))
            
            print(f"Removed monitored path: {path}")
    
    def add_monitored_path(self, path_list):
        """Deprecated - keeping for compatibility"""
        pass
    
    def remove_monitored_path(self, path_list):
        """Deprecated - keeping for compatibility"""
        pass

    def closeEvent(self, event):
        """Save window size when closing"""
        if config.get("settings.remember_window_position", True):
            size = self.size()
            config.set("settings.window_size.width", size.width())
            config.set("settings.window_size.height", size.height())
        
        super().closeEvent(event)

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
