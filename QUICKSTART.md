# GestureMouse - Quick Start Guide

## ⚡ Get Started in 3 Steps

### Step 1️⃣: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** Requires Python 3.10 or higher. Check with `python --version`

---

### Step 2️⃣: Run the Application

```bash
python run.py
```

---

### Step 3️⃣: Start Using Gestures

1. Click **"Start Tracking"** button
2. Position your hand in front of the webcam
3. Try these gestures:

| Gesture | How To | What It Does |
|---------|--------|--------------|
| ☝️ **Point** | Extend index finger | Move cursor |
| 🤏 **Pinch** | Thumb + index touch | Left click |
| 👌 **Two-finger pinch** | Thumb + middle touch | Right click |
| ✌️ **Peace + Move** | Two fingers + vertical motion | Scroll |

---

## 🎯 Tips for Best Results

### ✅ Good Setup
- 💡 **Lighting:** Bright, even lighting from front
- 📷 **Camera:** Eye level, 1-2 feet away
- 🖐️ **Hand:** Palm facing camera, within frame
- 🎨 **Background:** Simple, not too busy

### ❌ Avoid
- ⚫ Dim lighting or backlighting
- 📐 Extreme camera angles
- 🏃 Fast, jerky movements
- 🎪 Complex/moving background

---

## ⚙️ Adjust Settings

**Cursor too fast/slow?**
→ Adjust **Sensitivity** slider (1-10)

**Cursor jittery?**
→ Increase **Smoothing** slider (1-10)

**Accidental clicks?**
→ Uncheck unwanted gestures in **Gestures** panel

---

## 🆘 Troubleshooting

### "Hand Not Detected"
1. Check lighting - add more light
2. Keep hand in camera view
3. Position hand 1-2 feet from camera

### "Camera Not Working"
1. Grant camera permissions in OS settings
2. Close other apps using camera
3. Try different camera in settings dropdown

### "Installation Errors"
```bash
# Update pip and reinstall
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

---

## 📚 More Help

- **Full User Guide:** `docs/USER_GUIDE.md`
- **Installation Help:** `INSTALLATION.md`
- **Project Details:** `PROJECT_SUMMARY.md`
- **PRD:** `prd.md`

---

## 🎉 That's It!

You're ready to control your mouse with hand gestures!

**Minimize to Tray:** Click "Minimize to Tray" to run in background

**System Tray:** Double-click tray icon to show window again

---

**Enjoy GestureMouse! 🚀**
