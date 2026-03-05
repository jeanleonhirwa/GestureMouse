# 🖐️ GestureMouse - Gesture Reference Guide

## Quick Reference

| Gesture | Hand Position | Action | How To Do It |
|---------|---------------|--------|--------------|
| ☝️ **Cursor Control** | Index finger pointing | Move mouse cursor | Extend ONLY your index finger, keep others closed in a fist. Move hand to move cursor. |
| 🤏 **Left Click** | Pinch gesture | Left mouse button | Touch your THUMB and INDEX FINGER together briefly, then release. |
| 👌 **Right Click** | Two-finger pinch | Right mouse button | Touch your THUMB and MIDDLE FINGER together briefly, then release. |
| ✌️ **Scroll** | Peace sign + movement | Scroll up/down | Extend INDEX and MIDDLE fingers (keep ring and pinky closed), then move hand UP or DOWN. |

---

## Detailed Instructions

### 1. 🖱️ Move Cursor (Cursor Control)

**Hand Position:**
```
     ☝️  ← ONLY index finger up
    ✊   ← All other fingers closed (make a fist)
```

**How to perform:**
1. Make a fist with your hand
2. Extend ONLY your index finger (like pointing)
3. Keep all other fingers closed
4. Move your hand around - the cursor follows your index finger tip
5. Small movements = precise control

**Tips:**
- Keep your palm facing the camera
- Move smoothly for best results
- Adjust "Sensitivity" slider if cursor moves too fast/slow
- Adjust "Smoothing" slider if cursor is jittery

---

### 2. 🖱️ Left Click

**Hand Position:**
```
    🤏  ← Thumb and index finger touching
```

**How to perform:**
1. Start with index finger extended (cursor control mode)
2. Bring your THUMB and INDEX FINGER together until they touch
3. Release immediately (don't hold)
4. You'll hear/see the click happen

**Tips:**
- Quick pinch works best
- Don't hold the pinch - just tap and release
- If getting accidental clicks, move hand more slowly
- There's a 300ms delay between clicks to prevent double-clicking

---

### 3. 🖱️ Right Click

**Hand Position:**
```
    👌  ← Thumb and MIDDLE finger touching
    ☝️  ← Index finger can stay extended
```

**How to perform:**
1. Start with index finger extended
2. Bring your THUMB and MIDDLE FINGER together until they touch
3. Release immediately
4. Right-click menu appears

**Tips:**
- Similar to left click but use middle finger instead
- Useful for context menus
- Also has 300ms debounce delay

---

### 4. 📜 Scroll Up/Down

**Hand Position - Step 1: Enter Scroll Mode**
```
    ✌️  ← INDEX and MIDDLE fingers extended
    ✊   ← Ring and pinky fingers closed
```

**Hand Position - Step 2: Scroll**
```
    ✌️
    ↑   ← Move hand UP = Scroll UP (page scrolls down)
    ↓   ← Move hand DOWN = Scroll DOWN (page scrolls up)
```

**How to perform:**
1. Extend your INDEX finger AND MIDDLE finger (like a peace sign ✌️)
2. Keep your RING and PINKY fingers closed
3. Move your hand VERTICALLY:
   - **Move hand UP** → Page scrolls down (reveals content above)
   - **Move hand DOWN** → Page scrolls up (reveals content below)

**Important - Scrolling Direction:**
- When you move your hand **UP**, the page scrolls **DOWN** (like pushing page down)
- When you move your hand **DOWN**, the page scrolls **UP** (like pulling page up)
- This mimics natural touchscreen scrolling behavior

**Tips:**
- Keep fingers clearly separated
- Use smooth vertical movements
- Adjust "Scroll Sensitivity" if scrolling too fast/slow
- Only moves in vertical direction (up/down)

---

## ❌ NOT Implemented Yet (Future Features)

These gestures are planned but not yet available:

- **Double Click** - Currently not implemented
  - *Workaround:* Do two quick left clicks manually
  
- **Drag and Drop** - Currently not implemented
  - *Planned:* Pinch + hold + move + release

- **Zoom In/Out** - Currently not implemented
  - *Planned:* Two-hand pinch gesture

---

## 🎯 Pro Tips

### Best Practices

1. **Lighting:**
   - Use bright, even lighting
   - Avoid backlighting (don't sit in front of a bright window)
   - Turn on room lights for best detection

2. **Camera Position:**
   - Keep camera at eye level
   - Position yourself 1-2 feet (30-60cm) from camera
   - Keep hand visible in camera frame

3. **Hand Position:**
   - Keep palm facing the camera
   - Keep hand within the camera view
   - Avoid moving too fast - smooth motions work best

4. **Background:**
   - Simple backgrounds work best
   - Avoid busy/cluttered backgrounds
   - Solid-colored walls are ideal

### Common Issues

**"Cursor not moving smoothly"**
- ✓ Increase "Smoothing" slider value
- ✓ Keep hand movements smooth and steady
- ✓ Check lighting is adequate

**"Accidental clicks happening"**
- ✓ Make more deliberate pinch gestures
- ✓ Keep fingers separated when not clicking
- ✓ Slow down hand movements
- ✓ Uncheck click gestures in UI if not needed

**"Hand not detected"**
- ✓ Improve room lighting
- ✓ Keep hand fully in camera view
- ✓ Make sure palm faces camera
- ✓ Move closer/farther from camera

**"Gestures not recognized"**
- ✓ Make more exaggerated gestures
- ✓ Keep fingers clearly extended/closed
- ✓ Check "Status" panel shows "Hand Detected"
- ✓ Ensure good lighting

---

## ⚙️ Settings Adjustment

### Sensitivity (1-10)
- **Low (1-3):** Slow, precise cursor movement
- **Medium (4-6):** Balanced (recommended: 5)
- **High (7-10):** Fast cursor movement

### Smoothing (1-10)
- **Low (1-3):** Responsive but may be jittery
- **Medium (4-6):** Balanced (recommended: 3)
- **High (7-10):** Very smooth but slightly delayed

### Enable/Disable Gestures
Uncheck any gestures you don't want to use:
- ☑ Cursor Control
- ☑ Left Click
- ☑ Right Click
- ☑ Scrolling

---

## 🎓 Practice Exercises

### Exercise 1: Basic Cursor Control
1. Start tracking
2. Extend index finger only
3. Draw circles in the air
4. Watch cursor follow smoothly

### Exercise 2: Clicking Practice
1. Open Notepad or any text editor
2. Use index finger to move cursor
3. Practice left clicks (thumb + index pinch)
4. Try clicking different UI elements

### Exercise 3: Scroll Practice
1. Open a long webpage or document
2. Extend index + middle fingers
3. Move hand up and down smoothly
4. Observe page scrolling

### Exercise 4: Right Click Menu
1. Move cursor to desktop
2. Use right click gesture (thumb + middle)
3. Context menu should appear
4. Use left click to select menu items

---

## 📊 Gesture Success Tips

| Gesture | Success Rate Tips |
|---------|-------------------|
| Cursor Move | Keep only index extended, smooth movements |
| Left Click | Quick pinch, don't hold, deliberate motion |
| Right Click | Use middle finger clearly, not too fast |
| Scroll | Keep two fingers clearly separated, vertical motion only |

---

## 🆘 Quick Troubleshooting

**Nothing works?**
1. Check "Status" panel shows "Tracking" (green)
2. Check "Hand Detected" shows "✓ Yes"
3. Verify camera feed shows your hand with green landmarks
4. Check all gesture checkboxes are enabled

**Still having issues?**
1. Restart the application
2. Adjust lighting in your room
3. Try different camera position
4. Check system camera permissions
5. Review USER_GUIDE.md for detailed help

---

**Happy Gesturing! 🎉**

For more help, see:
- `docs/USER_GUIDE.md` - Complete user guide
- `QUICKSTART.md` - Quick start guide
- `FIXES_APPLIED.md` - Technical fixes applied
