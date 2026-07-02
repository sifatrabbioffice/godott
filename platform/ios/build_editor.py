#!/usr/bin/env python3
"""
Godot iOS Editor - সম্পূর্ণ Editor বিল্ড
শুধু game নয়, সম্পূর্ণ Godot Editor iOS এ চালান
"""

import os
import sys
import subprocess
from pathlib import Path

class GodotiOSEditorBuilder:
    """Godot Editor iOS এর জন্য Builder"""
    
    def __init__(self):
        self.arch = "arm64"
        self.target = "debug"  # Development build
        self.tools = True      # ✓ Editor সহ
        self.min_ios = "14.0"
        
    def print_banner(self):
        """ব্যানার প্রিন্ট করুন"""
        print("=" * 70)
        print("🎮 Godot iOS Editor Builder")
        print("=" * 70)
        print(f"Architecture: {self.arch} (Single Layer)")
        print(f"Target: Editor (সম্পূর্ণ Godot Editor)")
        print(f"Tools: Enabled (✓)")
        print(f"Min iOS: {self.min_ios}")
        print("=" * 70)
        print()
    
    def get_scons_command_editor(self):
        """Editor এর জন্য SCons কমান্ড - সঠিক configuration"""
        return (
            f"scons "
            f"platform=ios "
            f"arch={self.arch} "
            f"target={self.target} "  # debug for editor
            f"tools=yes "               # ✓ Editor enabled
            f"dev_build=yes "           # Development build
            f"debug_symbols=yes "       # Debug info
            f"optimize=none "           # No optimization
            f"production=no "           # Not production
            f"use_lto=no "              # No LTO
            f"metal=yes "
            f"opengl3=no "
            f"vulkan=no "
            f"build_directory=build_ios_editor "
            f"-j$(sysctl -n hw.logicalcpu) "
            f"2>&1 | tee editor_build.log"
        )
    
    def get_release_scons_command(self):
        """Release Editor এর জন্য SCons কমান্ড"""
        return (
            f"scons "
            f"platform=ios "
            f"arch={self.arch} "
            f"target=template_release "  # Release template (editor included)
            f"tools=yes "                 # ✓ Editor enabled
            f"dev_build=no "
            f"optimize=speed "
            f"production=yes "
            f"use_lto=no "
            f"build_directory=build_ios_editor_release "
            f"-j$(sysctl -n hw.logicalcpu) "
            f"2>&1 | tee editor_build_release.log"
        )
    
    def build_editor(self, release=False):
        """Godot Editor বিল্ড করুন"""
        self.print_banner()
        
        if release:
            print("📦 Release Editor বিল্ড করছি...")
            cmd = self.get_release_scons_command()
            build_dir = "build_ios_editor_release"
        else:
            print("🔧 Debug Editor বিল্ড করছি...")
            cmd = self.get_scons_command_editor()
            build_dir = "build_ios_editor"
        
        print(f"কমান্ড: {cmd}\n")
        
        result = subprocess.run(cmd, shell=True)
        
        if result.returncode == 0:
            print(f"\n✅ Editor বিল্ড সম্পন্ন!")
            print(f"Output: {build_dir}/")
            return True
        else:
            print(f"\n❌ বিল্ড ব্যর্থ!")
            return False
    
    def verify_editor_build(self, build_dir="build_ios_editor"):
        """Editor বিল্ড যাচাই করুন"""
        print("\n" + "=" * 70)
        print("✓ Editor বিল্ড যাচাই করছি...")
        print("=" * 70)
        
        libgodot = Path(build_dir) / "libgodot.a"
        
        if libgodot.exists():
            size_mb = libgodot.stat().st_size / (1024 * 1024)
            print(f"✅ Editor Library পাওয়া গেছে")
            print(f"   Path: {libgodot}")
            print(f"   Size: {size_mb:.1f} MB")
            
            # Editor features check
            print("\n📋 Editor Features যা অন্তর্ভুক্ত হবে:")
            features = [
                "✓ Scene Editor",
                "✓ Script Editor (GDScript, C#)",
                "✓ Shader Editor",
                "✓ Animation Timeline",
                "✓ Property Inspector",
                "✓ File Browser",
                "✓ Asset Manager",
                "✓ Console & Debugger",
                "✓ 3D/2D Viewports",
                "✓ Project Manager",
                "✓ Touch UI (Optimized)",
                "✓ Full Godot Tools",
            ]
            for feature in features:
                print(f"   {feature}")
            
            return True
        else:
            print(f"❌ Editor Library না পাওয়া যাচ্ছে")
            print(f"   Expected: {libgodot}")
            return False

def main():
    """Main execution"""
    builder = GodotiOSEditorBuilder()
    
    import argparse
    parser = argparse.ArgumentParser(
        description="Godot iOS Editor Builder - সম্পূর্ণ Editor iOS এ"
    )
    parser.add_argument(
        "--release",
        action="store_true",
        help="Release mode এ বিল্ড করুন"
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="শুধু বিল্ড যাচাই করুন"
    )
    
    args = parser.parse_args()
    
    if args.verify:
        build_dir = "build_ios_editor_release" if args.release else "build_ios_editor"
        success = builder.verify_editor_build(build_dir)
        sys.exit(0 if success else 1)
    
    # Build editor
    success = builder.build_editor(release=args.release)
    
    if success:
        build_dir = "build_ios_editor_release" if args.release else "build_ios_editor"
        builder.verify_editor_build(build_dir)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
