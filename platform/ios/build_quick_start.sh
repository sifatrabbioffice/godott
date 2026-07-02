#!/bin/bash
# Quick Start: iOS Unsigned IPA Builder for Godot
# Godot Game Engine কে iOS এ চালানোর জন্য দ্রুত গাইড

echo "=================================="
echo "🎮 Godot iOS Unsigned IPA Builder"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Check Prerequisites
echo -e "${BLUE}[Step 1] প্রয়োজনীয় সফটওয়্যার চেক করছি...${NC}"
echo ""

# Check Xcode
if ! command -v xcode-select &> /dev/null; then
    echo -e "${YELLOW}⚠️  Xcode Command Line Tools প্রয়োজন${NC}"
    xcode-select --install
fi
echo -e "${GREEN}✓ Xcode OK${NC}"

# Check SCons
if ! command -v scons &> /dev/null; then
    echo -e "${YELLOW}⚠️  SCons ইনস্টল করছি...${NC}"
    pip3 install scons
fi
echo -e "${GREEN}✓ SCons OK${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}⚠️  Python 3 প্রয়োজন${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python OK${NC}"

echo ""
echo -e "${BLUE}[Step 2] Godot iOS Engine বিল্ড করছি (arm64 - Single Layer)...${NC}"
echo ""

# Build Godot Engine
scons platform=ios arch=arm64 target=template_release \
    tools=yes dev_mode=no production=yes \
    use_lto=none build_directory=build_ios -j8

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Engine বিল্ড সম্পন্ন${NC}"
else
    echo -e "${YELLOW}✗ Engine বিল্ড ব্যর্থ${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}[Step 3] Xcode কনফিগারেশন...${NC}"
echo ""

# Create Xcode build config
mkdir -p build_ios/xcode_config

cat > build_ios/xcode_config/build_settings.xcconfig << 'EOF'
ARCHS = arm64
VALID_ARCHS = arm64
EXCLUDED_ARCHS = arm64e x86_64 i386
IPHONEOS_DEPLOYMENT_TARGET = 14.0
CODE_SIGN_IDENTITY = -
CODE_SIGNING_REQUIRED = NO
CODE_SIGNING_ALLOWED = NO
EOF

echo -e "${GREEN}✓ Xcode কনফিগ তৈরি${NC}"

echo ""
echo -e "${BLUE}[Step 4] Unsigned IPA বিল্ড করছি...${NC}"
echo ""

# Build unsigned IPA
xcodebuild \
    -scheme GodotGame \
    -configuration Release \
    -arch arm64 \
    CODE_SIGN_IDENTITY=- \
    CODE_SIGNING_REQUIRED=NO \
    CODE_SIGNING_ALLOWED=NO \
    -derivedDataPath build_ios/derived_data 2>&1 | tee build_ios/xcode_build.log

if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo -e "${GREEN}✓ Xcode বিল্ড সম্পন্ন${NC}"
else
    echo -e "${YELLOW}✗ Xcode বিল্ড ব্যর্থ${NC}"
    echo "Log দেখুন: build_ios/xcode_build.log"
fi

echo ""
echo -e "${BLUE}[Step 5] IPA প্যাকেজ তৈরি করছি...${NC}"
echo ""

# Create unsigned IPA package
APP_PATH="build_ios/derived_data/Build/Products/Release-iphoneos/GodotGame.app"
IPA_NAME="godot_editor_arm64_unsigned.ipa"

if [ ! -d "$APP_PATH" ]; then
    echo -e "${YELLOW}⚠️  App পাথ খুঁজে পাওয়া যাচ্ছে না: $APP_PATH${NC}"
    echo "সম্ভাব্য পাথ খুঁজছি..."
    
    FOUND_APP=$(find build_ios -name "*.app" -type d 2>/dev/null | head -1)
    if [ -n "$FOUND_APP" ]; then
        APP_PATH="$FOUND_APP"
        echo "পাওয়া গেছে: $APP_PATH"
    else
        echo -e "${YELLOW}✗ কোন .app ডিরেক্টরি পাওয়া যায়নি${NC}"
        exit 1
    fi
fi

# Create Payload directory
mkdir -p Payload
cp -r "$APP_PATH" Payload/

# Create ZIP IPA
zip -r "$IPA_NAME" Payload/ -q

# Cleanup
rm -rf Payload/

if [ -f "$IPA_NAME" ]; then
    IPA_SIZE=$(ls -lh "$IPA_NAME" | awk '{print $5}')
    echo -e "${GREEN}✓ IPA প্যাকেজ তৈরি: $IPA_NAME ($IPA_SIZE)${NC}"
else
    echo -e "${YELLOW}✗ IPA প্যাকেজ তৈরিতে ব্যর্থ${NC}"
    exit 1
fi

echo ""
echo "=================================="
echo -e "${GREEN}✅ সব কাজ সম্পন্ন!${NC}"
echo "=================================="
echo ""
echo -e "📦 Output: ${YELLOW}$IPA_NAME${NC}"
echo ""
echo "পরবর্তী পদক্ষেপ:"
echo "  1. Xcode এ খুলুন এবং signing এর জন্য configure করুন"
echo "  2. App Store তে upload করুন অথবা Test Flight এ পাঠান"
echo "  3. অথবা device এ ইনস্টল করুন (development provisioning profile দিয়ে)"
echo ""
echo "গুরুত্বপূর্ণ তথ্য:"
echo "  • এটি একটি unsigned IPA (শুধুমাত্র ডেভেলপমেন্ট/টেস্টিং এর জন্য)"
echo "  • Single layer architecture: arm64 শুধুমাত্র (device)"
echo "  • Tools included: Godot Editor সহ"
echo "  • Min iOS version: 14.0"
echo ""
