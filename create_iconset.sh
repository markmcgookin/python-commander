#!/bin/zsh

echo "🎨 Creating optimized iconset for macOS..."

# Use the largest source image we have
SOURCE_IMAGE="resources/images/logo-images/IconOnly_NoBuffer_rounded.png"

if [[ ! -f "$SOURCE_IMAGE" ]]; then
    echo "❌ Source image not found: $SOURCE_IMAGE"
    exit 1
fi

echo "✅ Using source image: $SOURCE_IMAGE (should be 1024x1024)"

# Create a new optimized iconset directory
ICONSET_DIR="resources/images/icon/iconset.iconset"
rm -rf "$ICONSET_DIR"
mkdir -p "$ICONSET_DIR"

echo "📐 Generating all required icon sizes..."

# Generate all required sizes using sips (built-in macOS tool)
# Standard resolution icons
sips -z 16 16 "$SOURCE_IMAGE" --out "$ICONSET_DIR/icon_16x16.png" > /dev/null
sips -z 32 32 "$SOURCE_IMAGE" --out "$ICONSET_DIR/icon_16x16@2x.png" > /dev/null
sips -z 32 32 "$SOURCE_IMAGE" --out "$ICONSET_DIR/icon_32x32.png" > /dev/null
sips -z 64 64 "$SOURCE_IMAGE" --out "$ICONSET_DIR/icon_32x32@2x.png" > /dev/null
sips -z 128 128 "$SOURCE_IMAGE" --out "$ICONSET_DIR/icon_128x128.png" > /dev/null
sips -z 256 256 "$SOURCE_IMAGE" --out "$ICONSET_DIR/icon_128x128@2x.png" > /dev/null
sips -z 256 256 "$SOURCE_IMAGE" --out "$ICONSET_DIR/icon_256x256.png" > /dev/null
sips -z 512 512 "$SOURCE_IMAGE" --out "$ICONSET_DIR/icon_256x256@2x.png" > /dev/null
sips -z 512 512 "$SOURCE_IMAGE" --out "$ICONSET_DIR/icon_512x512.png" > /dev/null
sips -z 1024 1024 "$SOURCE_IMAGE" --out "$ICONSET_DIR/icon_512x512@2x.png" > /dev/null


echo "🔨 Converting iconset to optimized ICNS..."
iconutil -c icns "$ICONSET_DIR" -o "resources/images/icon/iconset.icns"