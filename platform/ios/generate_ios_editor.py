#!/usr/bin/env python3
"""
Godot iOS Editor System
iOS এ সম্পূর্ণ Godot Editor চালানোর জন্য Export System
"""

import os
import sys
import json
import subprocess
from pathlib import Path

class iOSEditorSystem:
    """iOS এ Godot Editor সিস্টেম"""
    
    def __init__(self):
        self.editor_name = "Godot Editor iOS"
        self.arch = "arm64"
        self.min_ios = "14.0"
        self.build_config = {}
    
    def get_editor_features(self):
        """iOS Editor এর Features"""
        return {
            "scene_editor": True,
            "script_editor": True,
            "shader_editor": True,
            "asset_manager": True,
            "project_manager": True,
            "debugging": True,
            "console": True,
            "file_system": True,
            "inspector": True,
            "animation_editor": True,
            "shader_preview": True,
            "touch_ui": True,  # Touch optimized UI
            "split_view": True,  # Split screen support
        }
    
    def get_editor_build_flags(self):
        """Editor বিল্ড করার জন্য Flags"""
        return {
            "platform": "ios",
            "arch": self.arch,
            "target": "template_debug",  # Debug template for development
            "tools": True,  # Include editor tools
            "dev_build": True,  # Development build
            "editor_build": True,  # Full editor
            "debug_symbols": True,  # Debug symbols
            "optimize": "none",  # No optimization for debugging
            "production": False,  # Development mode
            "use_lto": False,
            "metal": True,  # Metal rendering
            "opengl3": False,
            "vulkan": False,
        }
    
    def get_scons_command(self):
        """SCons বিল্ড কমান্ড"""
        flags = self.get_editor_build_flags()
        cmd = "scons"
        
        for key, value in flags.items():
            if isinstance(value, bool):
                cmd += f" {key}={'yes' if value else 'no'}"
            else:
                cmd += f" {key}={value}"
        
        cmd += " build_directory=build_ios_editor -j8"
        return cmd
    
    def get_editor_modules(self):
        """iOS Editor এর প্রয়োজনীয় Modules"""
        return [
            "scene",  # Scene system
            "gdscript",  # GDScript interpreter
            "csharp",  # C# support
            "mono",  # Mono runtime
            "asset",  # Asset management
            "animation",  # Animation system
            "physics_3d",  # 3D Physics
            "physics_2d",  # 2D Physics
            "navigation",  # Navigation system
            "rendering",  # Rendering engine
            "audio",  # Audio system
            "networking",  # Network support
            "filesystem",  # File system
            "debugger",  # Debugging tools
            "editor",  # Editor system
            "editor_plugins",  # Editor plugins
        ]
    
    def get_editor_ui_configuration(self):
        """iOS Editor UI Configuration"""
        return {
            "ui_scale": 1.5,  # Larger UI for touch
            "theme": "dark",
            "layout": "split",  # Split view for mobile
            "panels": {
                "top": ["main_menu", "top_toolbar"],
                "left": ["scene_tree", "file_browser"],
                "center": ["editor_viewport", "script_editor"],
                "right": ["inspector", "node_properties"],
                "bottom": ["console", "debug_output"],
            },
            "touch_gestures": {
                "two_finger_zoom": True,
                "three_finger_menu": True,
                "swipe_navigation": True,
                "long_press_context": True,
            },
            "keyboard": {
                "onscreen_keyboard": True,
                "shortcuts_bar": True,
                "command_palette": True,
            }
        }
    
    def get_editor_export_config(self):
        """Editor Export Configuration"""
        return {
            "app_name": "Godot Editor",
            "bundle_identifier": "org.godotengine.editor",
            "version": "4.0.0",
            "build_number": "1",
            "supported_orientations": [
                "UIInterfaceOrientationPortrait",
                "UIInterfaceOrientationLandscapeLeft",
                "UIInterfaceOrientationLandscapeRight",
            ],
            "min_ios_version": self.min_ios,
            "capabilities": [
                "network",  # Network access
                "file_sharing",  # Document sharing
                "icloud_drive",  # iCloud support
                "handoff",  # Handoff support
            ],
            "permissions": {
                "NSLocalNetworkUsageDescription": "Godot Editor needs local network access",
                "NSBonjourServices": ["_godot._tcp"],
                "NSNetServiceTypeUsageDescription": "Godot Editor communicates with other devices",
                "NSDocumentsFolderUsageDescription": "Godot Editor needs to access documents",
                "NSCameraUsageDescription": "Camera access for game testing",
                "NSMicrophoneUsageDescription": "Microphone access for audio testing",
            }
        }
    
    def get_info_plist(self):
        """Info.plist এর জন্য Configuration"""
        config = self.get_editor_export_config()
        return {
            "CFBundleDevelopmentRegion": "en",
            "CFBundleExecutable": "$(EXECUTABLE_NAME)",
            "CFBundleIdentifier": config["bundle_identifier"],
            "CFBundleInfoDictionaryVersion": "6.0",
            "CFBundleName": config["app_name"],
            "CFBundlePackageType": "APPL",
            "CFBundleShortVersionString": config["version"],
            "CFBundleVersion": config["build_number"],
            "LSRequiresIPhoneOS": True,
            "UIMainStoryboardFile": "",
            "UIRequiredDeviceCapabilities": ["armv7"],
            "UISupportedInterfaceOrientations": config["supported_orientations"],
            "UISupportedInterfaceOrientationsIPad": config["supported_orientations"],
            "NSLocalNetworkUsageDescription": config["permissions"]["NSLocalNetworkUsageDescription"],
            "NSBonjourServices": config["permissions"]["NSBonjourServices"],
            "NSNetServiceTypeUsageDescription": config["permissions"]["NSNetServiceTypeUsageDescription"],
        }
    
    def generate_build_script(self):
        """Complete iOS Editor বিল্ড স্ক্রিপ্ট জেনারেট করুন"""
        script = f"""#!/bin/bash
# Godot iOS Editor Build Script
# সম্পূর্ণ Editor সহ iOS এর জন্য বিল্ড

set -e

echo "=========================================="
echo "🎮 Godot iOS Editor Builder"
echo "=========================================="
echo ""

# Step 1: Build Engine with Editor
echo "[1/4] Godot Editor বিল্ড করছি (arm64)..."
{self.get_scons_command()}

# Step 2: Verify build
echo ""
echo "[2/4] বিল্ড যাচাই করছি..."
if [ -f "build_ios_editor/libgodot.a" ]; then
    echo "✓ Static library তৈরি সম্পন্ন"
else
    echo "✗ বিল্ড ব্যর্থ!"
    exit 1
fi

# Step 3: Generate Xcode project
echo ""
echo "[3/4] Xcode প্রজেক্ট তৈরি করছি..."
python3 platform/ios/generate_xcode_project.py --editor

# Step 4: Create IPA package
echo ""
echo "[4/4] IPA প্যাকেজ তৈরি করছি..."
xcodebuild \\
    -scheme GodotEditor \\
    -configuration Release \\
    -arch arm64 \\
    CODE_SIGN_IDENTITY=- \\
    CODE_SIGNING_REQUIRED=NO \\
    -derivedDataPath build_ios_editor/derived_data

# Create IPA
mkdir -p Payload
cp -r build_ios_editor/derived_data/Build/Products/Release-iphoneos/GodotEditor.app Payload/
zip -r godot_editor_ios.ipa Payload/
rm -rf Payload/

echo ""
echo "=========================================="
echo "✅ Godot iOS Editor IPA তৈরি সম্পন্ন!"
echo "=========================================="
echo ""
echo "📦 Output: godot_editor_ios.ipa"
"""
        return script
    
    def generate_xcode_pbxproj(self):
        """Xcode project configuration"""
        return {
            "ArchiveVersion": "1",
            "Classes": {},
            "ObjectVersion": "55",
            "Objects": {},
            "RootObject": "root_object",
            "target": "GodotEditor",
            "product_type": "com.apple.product-type.application",
            "product_name": "Godot Editor",
            "bundle_identifier": "org.godotengine.editor",
            "code_sign_identity": "",
            "code_signing_required": False,
            "architectures": ["arm64"],
            "deployment_target": "14.0",
        }
    
    def get_editor_entitlements_plist(self):
        """Editor Entitlements Plist"""
        return {
            "com.apple.developer.networking.local-outbound": True,
            "com.apple.developer.networking.multicast": True,
            "com.apple.security.files.user-selected.read-write": True,
            "com.apple.security.files.downloads.read-write": True,
        }
    
    def generate_config_json(self):
        """সম্পূর্ণ Configuration JSON"""
        return {
            "editor_system": self.editor_name,
            "version": "4.0",
            "architecture": self.arch,
            "min_ios_version": self.min_ios,
            "features": self.get_editor_features(),
            "build_flags": self.get_editor_build_flags(),
            "modules": self.get_editor_modules(),
            "ui_config": self.get_editor_ui_configuration(),
            "export_config": self.get_editor_export_config(),
            "info_plist": self.get_info_plist(),
            "entitlements": self.get_editor_entitlements_plist(),
            "xcode_config": self.generate_xcode_pbxproj(),
        }

def main():
    """Main execution"""
    editor_system = iOSEditorSystem()
    
    print("=" * 50)
    print("iOS Editor System Configuration Generator")
    print("=" * 50)
    print("")
    
    # Generate config
    config = editor_system.generate_config_json()
    
    # Save config file
    config_path = Path("platform/ios/editor_config.json")
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"[✓] Configuration saved: {config_path}")
    print("")
    print("Features:")
    for feature, enabled in config["features"].items():
        status = "✓" if enabled else "✗"
        print(f"  {status} {feature}")
    print("")
    print("Build command:")
    print(f"  {editor_system.get_scons_command()}")
    print("")

if __name__ == "__main__":
    main()
