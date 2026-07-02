#!/usr/bin/env python3
"""
Godot iOS Unsigned IPA Builder - Single Layer (arm64)
এই স্ক্রিপ্ট Godot Editor এর জন্য unsigned IPA তৈরি করে
"""
import os
import sys
import subprocess
import argparse
from pathlib import Path

class iOSBuilder:
    def __init__(self, arch="arm64", target="release", unsigned=True):
        self.arch = arch
        self.target = target
        self.unsigned = unsigned
        self.build_dir = "build_ios"
        self.root_dir = Path(__file__).parent.parent
        
    def run_command(self, cmd, description):
        """কমান্ড চালান এবং ফলাফল প্রদর্শন করুন"""
        print(f"\n[*] {description}...")
        print(f"    Command: {cmd}")
        result = subprocess.run(cmd, shell=True, cwd=str(self.root_dir))
        if result.returncode != 0:
            print(f"[ERROR] {description} ব্যর্থ হয়েছে!")
            sys.exit(1)
    
    def build_godot_engine(self):
        """Godot Engine বিল্ড করুন"""
        build_cmd = (
            f"scons platform=ios arch={self.arch} target={self.target} "
            f"build_directory={self.build_dir} "
            f"tools=yes "  # Editor সহ
            f"dev_mode=no "
            f"production=yes "
            f"use_lto=none "
            f"-j8"  # Parallel build
        )
        self.run_command(build_cmd, "Godot iOS Engine বিল্ড করছি (Single Layer - arm64)")
    
    def create_xcode_config(self):
        """Xcode কনফিগারেশন ফাইল তৈরি করুন"""
        config_content = """
# iOS Build Configuration
ARCH = arm64
MIN_VERSION = 14.0
SIGN_IDENTITY = 
CODE_SIGNING_REQUIRED = NO
CODE_SIGN_ALLOWED = NO
"""
        config_path = Path(self.build_dir) / "build_config.xcconfig"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(config_content)
        print(f"[✓] Xcode কনফিগ তৈরি: {config_path}")
    
    def build_with_xcodebuild(self):
        """xcodebuild দিয়ে বিল্ড করুন"""
        # xcodebuild configuration
        xcode_build = (
            f"xcodebuild "
            f"-scheme GodotGame "
            f"-configuration Release "
            f"-arch {self.arch} "
            f"CODE_SIGN_IDENTITY=- "
            f"CODE_SIGNING_REQUIRED=NO "
            f"CODE_SIGNING_ALLOWED=NO "
            f"PROVISIONING_PROFILE_SPECIFIER=- "
            f"-derivedDataPath {self.build_dir}/derived_data"
        )
        self.run_command(xcode_build, "Xcode থেকে বিল্ড করছি (Unsigned)")
    
    def create_unsigned_ipa(self):
        """Unsigned IPA তৈরি করুন"""
        derived_data = Path(self.build_dir) / "derived_data"
        app_path = derived_data / "Build/Products/Release-iphoneos/GodotGame.app"
        
        if not app_path.exists():
            print(f"[!] App পাওয়া যায়নি: {app_path}")
            print("[*] নতুন app path খুঁজছি...")
            # সব .app ফাইল খুঁজুন
            import glob
            apps = glob.glob(str(derived_data / "**/*.app"), recursive=True)
            if apps:
                app_path = Path(apps[0])
                print(f"[✓] App পাওয়া গেছে: {app_path}")
            else:
                print("[ERROR] কোন .app পাওয়া যায়নি!")
                sys.exit(1)
        
        # Payload ডিরেক্টরি সেটআপ
        payload_dir = Path("Payload")
        payload_dir.mkdir(exist_ok=True)
        
        # App কপি করুন
        app_dest = payload_dir / app_path.name
        if app_dest.exists():
            import shutil
            shutil.rmtree(app_dest)
        
        copy_cmd = f"cp -r '{app_path}' {payload_dir}/"
        self.run_command(copy_cmd, "App কপি করছি Payload তে")
        
        # IPA জিপ করুন
        ipa_name = f"godot_editor_{self.arch}_unsigned.ipa"
        # Using Python's zipfile for better cross-platform support
        import zipfile
        import shutil
        
        def zipdir(path, ziph):
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, path)
                    ziph.write(file_path, arcname)
        
        print(f"[*] IPA প্যাকেজ তৈরি করছি: {ipa_name}")
        with zipfile.ZipFile(ipa_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipdir(str(payload_dir), zipf)
        
        # Cleanup
        shutil.rmtree(payload_dir)
        
        print(f"✅ Unsigned IPA তৈরি সম্পন্ন: {ipa_name}")
        return ipa_name
    
    def build(self):
        """সম্পূর্ণ বিল্ড প্রক্রিয়া"""
        print("=" * 70)
        print("🎮 Godot iOS Unsigned IPA Builder")
        print("=" * 70)
        print(f"Architecture: {self.arch} (Single Layer)")
        print(f"Target: {self.target}")
        print(f"Unsigned: {self.unsigned}")
        print("=" * 70)
        
        self.build_godot_engine()
        self.create_xcode_config()
        self.create_unsigned_ipa()
        
        print("\n" + "=" * 70)
        print("✨ বিল্ড প্রক্রিয়া সম্পন্ন!")
        print("=" * 70)

def main():
    parser = argparse.ArgumentParser(
        description="Godot iOS Unsigned IPA Builder"
    )
    parser.add_argument(
        "--arch", 
        default="arm64",
        choices=["arm64", "x86_64"],
        help="Build architecture (default: arm64 - device)"
    )
    parser.add_argument(
        "--target",
        default="release",
        choices=["debug", "release"],
        help="Build target (default: release)"
    )
    parser.add_argument(
        "--simulator",
        action="store_true",
        help="Build for iOS Simulator (x86_64)"
    )
    
    args = parser.parse_args()
    
    arch = "x86_64" if args.simulator else args.arch
    
    builder = iOSBuilder(arch=arch, target=args.target, unsigned=True)
    builder.build()

if __name__ == "__main__":
    main()
