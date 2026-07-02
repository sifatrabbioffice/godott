#!/usr/bin/env python3
"""
Godot iOS Unsigned Export Template
Unsigned IPA তৈরির জন্য Export Template Configuration
"""

import os
import sys
import json
from pathlib import Path

class iOSUnsignedExportTemplate:
    """iOS Unsigned Export Template Handler"""
    
    def __init__(self):
        self.template_name = "iOS Unsigned (Single Layer - arm64)"
        self.arch = "arm64"
        self.config = {}
    
    def get_export_options(self):
        """Export Options রিটার্ন করুন"""
        return {
            "export_template_name": self.template_name,
            "arch": self.arch,
            "architectures": ["arm64"],  # Single layer
            "include_simulator": False,
            "universal_binary": False,
            
            # Code Signing
            "code_signing_enabled": False,
            "code_signing_identity": "",
            "provisioning_profile": "",
            "team_id": "",
            
            # Build Settings
            "debug": False,
            "target": "template_release",
            "tools": True,  # Include editor tools
            "production": True,
            "use_lto": False,
            
            # Rendering
            "metal_support": True,
            "opengl_support": False,
            "vulkan_support": False,
            
            # Deployment
            "min_ios_version": "14.0",
            "supported_orientations": [
                "UIInterfaceOrientationPortrait",
                "UIInterfaceOrientationLandscapeLeft",
                "UIInterfaceOrientationLandscapeRight"
            ],
            
            # Capabilities
            "requires_network": True,
            "requires_camera": False,
            "requires_microphone": False,
            "requires_contacts": False,
            
            # IPA Output
            "ipa_filename": "godot_editor_arm64_unsigned.ipa",
            "ipa_path": "./build_ios/ipa",
            "keep_payload": False,
        }
    
    def get_build_command(self):
        """Build কমান্ড রিটার্ন করুন"""
        return (
            "scons platform=ios arch=arm64 target=template_release "
            "tools=yes dev_mode=no production=yes use_lto=none "
            "build_directory=build_ios -j8"
        )
    
    def get_xcodebuild_command(self):
        """Xcode Build কমান্ড রিটার্ন করুন"""
        return (
            "xcodebuild "
            "-scheme GodotGame "
            "-configuration Release "
            "-arch arm64 "
            "CODE_SIGN_IDENTITY=- "
            "CODE_SIGNING_REQUIRED=NO "
            "CODE_SIGNING_ALLOWED=NO "
            "-derivedDataPath build_ios/derived_data"
        )
    
    def get_packaging_script(self):
        """IPA Packaging স্ক্রিপ্ট রিটার্ন করুন"""
        script = """#!/bin/bash
# iOS Unsigned IPA Packaging Script

set -e

APP_PATH="$1"
OUTPUT_IPA="$2"

if [ -z "$APP_PATH" ] || [ -z "$OUTPUT_IPA" ]; then
    echo "Usage: $0 <app_path> <output_ipa>"
    exit 1
fi

echo "[*] Creating unsigned IPA package..."

# Create Payload directory
mkdir -p Payload
cp -r "$APP_PATH" Payload/

# Create IPA (ZIP with .ipa extension)
zip -r "$OUTPUT_IPA" Payload/

# Cleanup
rm -rf Payload/

echo "[✓] Unsigned IPA created: $OUTPUT_IPA"
"""
        return script
    
    def get_info_plist_template(self):
        """Info.plist Template রিটার্ন করুন"""
        return {
            "CFBundleDevelopmentRegion": "en",
            "CFBundleExecutable": "$(EXECUTABLE_NAME)",
            "CFBundleIdentifier": "$(PRODUCT_BUNDLE_IDENTIFIER)",
            "CFBundleInfoDictionaryVersion": "6.0",
            "CFBundleName": "$(PRODUCT_NAME)",
            "CFBundlePackageType": "APPL",
            "CFBundleShortVersionString": "1.0",
            "CFBundleVersion": "1",
            "LSRequiresIPhoneOS": True,
            "UIMainStoryboardFile": "",
            "UIRequiredDeviceCapabilities": ["armv7"],
            "UISupportedInterfaceOrientations": [
                "UIInterfaceOrientationPortrait",
                "UIInterfaceOrientationLandscapeLeft",
                "UIInterfaceOrientationLandscapeRight"
            ],
            "UISupportedInterfaceOrientationsIPad": [
                "UIInterfaceOrientationPortrait",
                "UIInterfaceOrientationPortraitUpsideDown",
                "UIInterfaceOrientationLandscapeLeft",
                "UIInterfaceOrientationLandscapeRight"
            ],
            "NSLocalNetworkUsageDescription": "Godot Editor needs local network access",
            "NSBonjourServices": ["_godot._tcp"],
            "NSLocalNetworkUsageDescription": "Allow Godot Editor to communicate with other devices",
        }
    
    def generate_export_config_json(self):
        """Export Configuration JSON Generate করুন"""
        config = {
            "version": "4.0",
            "template": self.template_name,
            "export_options": self.get_export_options(),
            "build_commands": {
                "scons": self.get_build_command(),
                "xcodebuild": self.get_xcodebuild_command(),
            },
            "info_plist": self.get_info_plist_template(),
        }
        return json.dumps(config, indent=2)
    
    def save_export_config(self, output_path):
        """Export Configuration সেভ করুন"""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        config_json = self.generate_export_config_json()
        Path(output_path).write_text(config_json)
        print(f"[✓] Export config saved: {output_path}")
        return output_path

def main():
    """Main execution"""
    exporter = iOSUnsignedExportTemplate()
    
    print("=" * 70)
    print("iOS Unsigned Export Template Configuration")
    print("=" * 70)
    
    # Print export options
    print("\n[Export Options]")
    for key, value in exporter.get_export_options().items():
        print(f"  {key}: {value}")
    
    # Print build command
    print("\n[Build Command]")
    print(f"  {exporter.get_build_command()}")
    
    # Generate and save config
    config_path = "ios_unsigned_export_config.json"
    exporter.save_export_config(config_path)
    
    print("\n" + "=" * 70)
    print("✓ Configuration ready for iOS unsigned IPA export")
    print("=" * 70)

if __name__ == "__main__":
    main()
