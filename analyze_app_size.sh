#!/bin/zsh

echo "📊 Analyzing Python Commander app size..."

# First, try to find .app in build directory (before packaging)
APP_PATH=$(find build/ -name "*.app" -type d 2>/dev/null | head -1)

if [[ -n "$APP_PATH" ]]; then
    echo "🔍 Found app bundle in build directory: $APP_PATH"
else
    # Look for DMG in dist and try to mount it
    DMG_PATH=$(find dist/ -name "*.dmg" | head -1)
    
    if [[ -n "$DMG_PATH" ]]; then
        echo "📦 Found DMG: $DMG_PATH"
        echo "🔧 Mounting DMG to analyze contents..."
        
        # Mount the DMG
        MOUNT_POINT=$(hdiutil attach "$DMG_PATH" -nobrowse -quiet | tail -1 | cut -f3)
        
        if [[ -n "$MOUNT_POINT" ]]; then
            echo "✅ Mounted at: $MOUNT_POINT"
            
            # Find .app in mounted volume
            APP_PATH=$(find "$MOUNT_POINT" -name "*.app" -type d | head -1)
            
            if [[ -z "$APP_PATH" ]]; then
                echo "❌ No .app bundle found in DMG"
                hdiutil detach "$MOUNT_POINT" -quiet
                exit 1
            fi
        else
            echo "❌ Failed to mount DMG"
            exit 1
        fi
    else
        echo "❌ No .app bundle found in build/ and no .dmg found in dist/"
        echo "Run ./build_app.sh first"
        exit 1
    fi
fi

echo "🔍 Analyzing: $APP_PATH"
echo "📏 Total app size: $(du -sh "$APP_PATH" | cut -f1)"
echo ""

# Analyze what's taking up space
echo "🗂️  Top 10 largest directories:"
du -sh "$APP_PATH"/* 2>/dev/null | sort -hr | head -10
echo ""

# Look inside Contents if it exists
if [[ -d "$APP_PATH/Contents" ]]; then
    echo "📁 Contents breakdown:"
    du -sh "$APP_PATH/Contents"/* 2>/dev/null | sort -hr | head -10
    echo ""
    
    # Check what's in Frameworks (usually the biggest)
    if [[ -d "$APP_PATH/Contents/Frameworks" ]]; then
        echo "🏗️  Frameworks breakdown:"
        du -sh "$APP_PATH/Contents/Frameworks"/* 2>/dev/null | sort -hr | head -5
        echo ""
    fi
    
    # Check Resources
    if [[ -d "$APP_PATH/Contents/Resources" ]]; then
        echo "📚 Resources breakdown:"
        du -sh "$APP_PATH/Contents/Resources"/* 2>/dev/null | sort -hr | head -10
        echo ""
        
        # Look for Python packages
        if [[ -d "$APP_PATH/Contents/Resources/app_packages" ]]; then
            echo "🐍 Python packages:"
            du -sh "$APP_PATH/Contents/Resources/app_packages"/* 2>/dev/null | sort -hr | head -10
            echo ""
        fi
        
        # Look for support directory (common in Briefcase apps)
        if [[ -d "$APP_PATH/Contents/Resources/support" ]]; then
            echo "🔧 Support directory:"
            du -sh "$APP_PATH/Contents/Resources/support"/* 2>/dev/null | sort -hr | head -10
            echo ""
        fi
    fi
fi

# If we mounted a DMG, unmount it
if [[ -n "$MOUNT_POINT" ]]; then
    echo "🏃‍♂️ Unmounting DMG..."
    hdiutil detach "$MOUNT_POINT" -quiet
fi

echo "💡 Common size reduction strategies:"
echo "   1. Exclude unused Qt modules from PySide6"
echo "   2. Use system Python instead of bundled Python"
echo "   3. Strip debug symbols"
echo "   4. Compress libraries"
echo "   5. Consider alternative frameworks (tkinter, Kivy)"
echo ""
echo "🎯 For this app, try running: ./optimize_app_size.sh" 