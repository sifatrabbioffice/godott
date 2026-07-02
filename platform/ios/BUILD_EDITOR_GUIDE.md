# 🎮 Godot iOS Editor - Complete Build & Deploy Guide

## সম্পূর্ণ Godot Editor iOS এ চালানোর গাইড (Single Layer - arm64)

---

## 📋 প্রয়োজনীয় জিনিসপত্র

### হার্ডওয়্যার
- **Mac**: Intel or Apple Silicon (M1/M2/M3)
- **iOS Device**: iPhone/iPad with iOS 14.0+
- **Storage**: Minimum 20GB free space

### সফটওয়্যার
```
✓ macOS 12.0 or later
✓ Xcode 14.0 or later
✓ iOS SDK 14.0+
✓ Python 3.8+
✓ SCons 4.0+
✓ Git
```

### ডেভেলপার অ্যাকাউন্ট
- Apple Developer Account (ঐচ্ছিক, Unsigned এর জন্য প্রয়োজন নেই)

---

## 🚀 দ্রুত শুরু করুন

### ধাপ 1: সেটআপ

```bash
# macOS এ প্রয়োজনীয় সরঞ্জাম ইনস্টল করুন
xcode-select --install
pip3 install scons
brew install git

# Repository ক্লোন করুন
git clone https://github.com/sifatrabbioffice/godott.git
cd godott
```

### ধাপ 2: Builder স্ক্রিপ্ট চালান

```bash
# সম্পূর্ণ automated বিল্ড করুন
bash platform/ios/build_quick_start.sh
```

এটি স্বয়ংক্রিয়ভাবে সবকিছু করবে:
- ✅ Engine বিল্ড করবে
- ✅ Xcode প্রজেক্ট তৈরি করবে  
- ✅ Unsigned IPA প্যাকেজ তৈরি করবে

---

## 🏗️ ম্যানুয়াল বিল্ড প্রক্রিয়া

### Phase 1: Engine বিল্ড (30-60 মিনিট)

```bash
# সম্পূর্ণ Editor সহ বিল্ড করুন
scons platform=ios arch=arm64 target=template_release \
    tools=yes dev_mode=no production=yes \
    use_lto=none build_directory=build_ios_editor \
    -j$(sysctl -n hw.logicalcpu)
```

**বিল্ড পরামিতি:**

| পরামিতি | মান | উদ্দেশ্য |
|---------|-----|---------|
| `platform` | ios | iOS এর জন্য |
| `arch` | arm64 | Device architecture (single layer) |
| `target` | template_release | Release template |
| `tools` | yes | Editor সহ |
| `dev_mode` | no | Production mode |
| `production` | yes | অপটিমাইজ করুন |
| `use_lto` | none | LTO অক্ষম |

### Phase 2: Xcode কনফিগারেশন

```bash
# Xcode প্রজেক্ট জেনারেট করুন
python3 platform/ios/generate_ios_editor.py

# বা manually
mkdir -p build_ios_editor/GodotEditor.xcodeproj
```

### Phase 3: Xcode Build

```bash
# Unsigned বিল্ড করুন
xcodebuild \
    -scheme GodotEditor \
    -configuration Release \
    -arch arm64 \
    CODE_SIGN_IDENTITY=- \
    CODE_SIGNING_REQUIRED=NO \
    CODE_SIGNING_ALLOWED=NO \
    -derivedDataPath build_ios_editor/DerivedData \
    build
```

### Phase 4: IPA প্যাকেজ তৈরি

```bash
#!/bin/bash

# Variables
DERIVED_DATA="build_ios_editor/DerivedData"
APP_PATH="$DERIVED_DATA/Build/Products/Release-iphoneos/GodotEditor.app"
IPA_NAME="godot_editor_ios.ipa"

# Create Payload structure
mkdir -p Payload
cp -r "$APP_PATH" Payload/GodotEditor.app

# Create IPA
zip -r "$IPA_NAME" Payload/

# Cleanup
rm -rf Payload/

echo "✅ IPA created: $IPA_NAME"
```

---

## 📦 Editor Features

iOS এ Godot Editor এ এই সব ফিচার পাওয়া যাবে:

### Scene Management
- ✅ Scene tree hierarchy
- ✅ Node creation and editing
- ✅ Drag and drop support
- ✅ Multi-selection

### Editing Tools
- ✅ Scene editor viewport
- ✅ Script editor with syntax highlighting
- ✅ Shader editor and preview
- ✅ Animation timeline editor

### Inspector & Properties
- ✅ Full property inspector
- ✅ Resource browser
- ✅ Node properties panel
- ✅ Real-time preview

### Development Tools
- ✅ Integrated console
- ✅ Debugger
- ✅ File system browser
- ✅ Asset manager

### Touch Optimizations
- ✅ Touch-friendly UI
- ✅ Split view layout
- ✅ Gesture support (pinch, swipe)
- ✅ On-screen keyboard
- ✅ Context menus

---

## 📱 Installation Methods

### Method 1: Xcode দিয়ে (সবচেয়ে সহজ)

```bash
# Device সংযুক্ত করুন এবং চালান
xcode-select --install
open build_ios_editor/GodotEditor.xcodeproj

# Xcode এ:
# 1. Development team নির্বাচন করুন
# 2. Bundle identifier পরিবর্তন করুন (ঐচ্ছিক)
# 3. Device ট্রিগার করুন
# 4. Build & Run করুন
```

### Method 2: TestFlight (Development Testing)

```bash
# আপনার Development Team এর সাথে শেয়ার করুন
# Xcode → Product → Archive
# তারপর Organizer এ TestFlight তে আপলোড করুন
```

### Method 3: Manual Installation

```bash
# Drag-and-drop Xcode এ
# অথবা third-party tool ব্যবহার করুন:
# - Apple Configurator 2
# - iOS App Installer
# - imobiledevice-net
```

---

## 🔧 Troubleshooting

### সমস্যা 1: "Code signing failed"

```bash
# সমাধান: নিশ্চিত করুন CODE_SIGN_IDENTITY খালি
xcodebuild ... CODE_SIGN_IDENTITY=- CODE_SIGNING_REQUIRED=NO ...
```

### সমস্যা 2: "arm64 architecture not found"

```bash
# সমাধান: শুধুমাত্র arm64 নির্বাচন করুন
xcodebuild -arch arm64 ...
```

### সমস্যা 3: "App not found"

```bash
# সমাধান: সঠিক পাথ খুঁজুন
find build_ios_editor -name "*.app" -type d
```

### সমস্যা 4: "Build too slow"

```bash
# সমাধান: আরও থ্রেড ব্যবহার করুন
scons ... -j16  # 16 threads for M1/M2/M3 Macs
```

### সমস্যা 5: "IPA too large"

```bash
# সমাধান: Bitcode enabled করুন
# Xcode Build Settings → Enable Bitcode: Yes

# অথবা irrelevant architectures হটান
scons ... arch=arm64 ...
```

---

## 📊 Build Time এস্টিমেট

| পর্যায় | সময় | নোট |
|--------|------|------|
| Clean Build | 30-60 মিনিট | প্রথমবার |
| Incremental | 5-15 মিনিট | ছোট পরিবর্তন |
| Xcode Build | 10-20 মিনিট | - |
| IPA Creation | 2-5 মিনিট | - |
| **মোট** | **50-100 মিনিট** | **প্রথম বার** |

---

## 📁 ফাইল সংগঠন

```
godott/
├── platform/ios/
│   ├── build_config/
│   │   └── ios_unsigned_build.conf
│   ├── export/
│   │   └── unsigned_export_template.py
│   ├── generate_ios_editor.py
│   ├── build_quick_start.sh
│   └── BUILD_EDITOR_GUIDE.md (এই ফাইল)
├── scripts/
│   └── build_ios_unsigned.py
├── build_ios_editor/
│   ├── libgodot.a (Static library)
│   ├── GodotEditor.xcodeproj
│   └── DerivedData/
└── godot_editor_ios.ipa (Final output)
```

---

## 🔒 Code Signing

### Unsigned IPA (Development)

```bash
CODE_SIGN_IDENTITY=
CODE_SIGNING_REQUIRED=NO
CODE_SIGNING_ALLOWED=NO
```

### Signed IPA (Production)

```bash
# Apple Developer Account প্রয়োজন
CODE_SIGN_IDENTITY="iPhone Developer: Your Name (XXXXXXXXXX)"
CODE_SIGNING_REQUIRED=YES
PROVISIONING_PROFILE_SPECIFIER="Your Provisioning Profile"
```

---

## 💾 Output Files

বিল্ড সম্পন্ন হলে পাবেন:

```
godot_editor_ios.ipa          (~600-900 MB)
build_ios_editor/
├── libgodot.a                (Static library)
├── build.log                 (Build log)
├── GodotEditor.xcodeproj/   (Xcode project)
└── DerivedData/              (Build outputs)
```

---

## ⚙️ Advanced Configuration

### Custom Build Flags

```python
# platform/ios/build_config/ios_unsigned_build.conf এ সম্পাদনা করুন

[build_settings]
arch=arm64
min_ios_version=14.0
use_lto=none
optimization=none
```

### UI Customization

```python
# platform/ios/generate_ios_editor.py এ customize করুন

ui_scale = 1.5      # Larger UI
theme = "dark"      # Dark theme
layout = "split"    # Split view
```

---

## 🎯 Performance Tips

1. **Parallel Build**: `scons ... -j$(sysctl -n hw.logicalcpu)`
2. **Incremental Build**: পুনর্নির্মাণ করবেন না, পরিবর্তন করুন
3. **Cache**: Build cache ব্যবহার করুন
4. **RAM**: অন্তত 8GB RAM সুপারিশ করা হয়

---

## 📞 Support & Community

- **GitHub Issues**: https://github.com/sifatrabbioffice/godott/issues
- **Godot Docs**: https://docs.godotengine.org
- **iOS Development**: https://developer.apple.com

---

## ✅ Verification Checklist

বিল্ড সম্পন্ন হলে যাচাই করুন:

- [ ] IPA file তৈরি হয়েছে
- [ ] IPA size reasonable (~600-900 MB)
- [ ] সব ফিচার অন্তর্ভুক্ত
- [ ] কোন signing errors নেই
- [ ] Device এ install হয়েছে
- [ ] Editor চালু হয়েছে
- [ ] সব tools কাজ করছে

---

**Version**: 1.0  
**Last Updated**: 2026-07-02  
**Godot Version**: 4.0+  
**iOS Min Version**: 14.0  
**Architecture**: arm64 (Single Layer)
