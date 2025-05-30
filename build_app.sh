#!/bin/zsh

echo "🚀 Building Python Commander with proper icon..."

# Clean any existing builds
echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/

# Verify icon exists
if [[ ! -f "resources/images/icon/iconset.icns" ]]; then
    echo "❌ Icon file not found at resources/images/icon/iconset.icns"
    exit 1
fi

echo "✅ Icon file found: resources/images/icon/iconset.icns"

# Create the app
echo "📦 Creating the app..."
briefcase create

# Build the app  
echo "🔨 Building the app..."
briefcase build

# Package the app
echo "📱 Packaging the app..."
briefcase package macOS app --adhoc-sign --clean

echo "✅ Build complete! Check the app folder."

# Optional: Open the dist folder
read -q "REPLY?Open app folder? (y/n): "
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    open build/python_commander/macos/app
fi 