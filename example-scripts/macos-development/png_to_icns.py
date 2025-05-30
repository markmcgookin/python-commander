title = "PNG to ICNS Converter"
description = """
Converts a PNG file to a macOS .icns icon file by generating all required icon sizes and using sips and iconutil.
Requires macOS with sips and iconutil available in PATH.
"""

arguments = [
    {"name": "input_png", "type": "str", "default": "resources/logos/IconOnly_Transparent.png", "description": "Path to the source PNG file."},
    {"name": "output_folder", "type": "str", "default": "macos-app-icon", "description": "Folder to store the iconset and ICNS file."},
    {"name": "output_icns", "type": "str", "default": "IconOnly_Transparent.icns", "description": "Name of the output ICNS file (will be placed in output_folder)."}
]

def main(args):
    import os
    import subprocess
    input_png = args["input_png"]
    output_folder = args["output_folder"]
    output_icns = args["output_icns"]
    iconset_dir = os.path.join(output_folder, "iconset.iconset")
    icns_path = os.path.join(output_folder, output_icns)

    print(f"Input PNG: {input_png}")
    print(f"Output folder: {output_folder}")
    print(f"Iconset directory: {iconset_dir}")
    print(f"ICNS output path: {icns_path}")

    os.makedirs(iconset_dir, exist_ok=True)
    sizes = [
        (16, 16, "icon_16x16.png"),
        (32, 32, "icon_16x16@2x.png"),
        (32, 32, "icon_32x32.png"),
        (64, 64, "icon_32x32@2x.png"),
        (128, 128, "icon_128x128.png"),
        (256, 256, "icon_128x128@2x.png"),
        (256, 256, "icon_256x256.png"),
        (512, 512, "icon_256x256@2x.png"),
        (512, 512, "icon_512x512.png"),
        (1024, 1024, "icon_512x512@2x.png"),
    ]
    for width, height, filename in sizes:
        out_path = os.path.join(iconset_dir, filename)
        print(f"Creating {out_path} ({width}x{height})")
        try:
            subprocess.run(["sips", "-z", str(height), str(width), input_png, "--out", out_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error creating {out_path}: {e}")
            return
    try:
        print(f"Running iconutil to create {icns_path}")
        subprocess.run(["iconutil", "-c", "icns", iconset_dir, "-o", icns_path], check=True)
        print(f"ICNS icon created at {icns_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error running iconutil: {e}")
        return
    # Optionally clean up
    # import shutil; shutil.rmtree(iconset_dir) 

if __name__ == "__main__":
    import sys
    # Parse arguments from command line in the format key=value
    args = {}
    for arg in sys.argv[1:]:
        if '=' in arg:
            k, v = arg.split('=', 1)
            args[k] = v
    # Fill in defaults for missing arguments
    for argdef in arguments:
        if argdef["name"] not in args:
            args[argdef["name"]] = argdef["default"]
    main(args) 