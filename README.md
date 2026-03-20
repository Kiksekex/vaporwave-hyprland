# ░▒▓ VAPORWAVE HYPRLAND RICE ▓▒░
### Synthwave Edition

A complete Hyprland desktop configuration in the **vaporwave / synthwave** aesthetic.

---

## 🎨 Color Palette

| Role            | Hex         | Preview            |
|-----------------|-------------|-------------------|
| Hot Pink        | `#ff2a6d`   | borders, accents  |
| Neon Cyan       | `#05d9e8`   | active, clock     |
| Electric Purple | `#7b2fff`   | secondary accents |
| Soft Pink       | `#ff71ce`   | text highlights   |
| Gold            | `#ffe66d`   | warnings, memory  |
| Background      | `#0d0221`   | near-black indigo |

---

## 📦 Components

| Component      | Config file                        | Description                           |
|----------------|------------------------------------|---------------------------------------|
| **Hyprland**   | `hypr/hyprland.conf`               | WM config, keybinds, animations       |
| **hyprpaper**  | `hypr/hyprpaper.conf`              | Wallpaper daemon                      |
| **hyprlock**   | `hypr/hyprlock.conf`               | Lock screen with neon clock           |
| **hypridle**   | `hypr/hypridle.conf`               | Idle/sleep management                 |
| **Waybar**     | `waybar/config.jsonc` + `style.css`| Status bar with glassmorphism         |
| **Rofi**       | `rofi/vaporwave.rasi`              | App launcher                          |
| **Dunst**      | `dunst/dunstrc`                    | Notification daemon                   |
| **Kitty**      | `kitty.conf`                       | Terminal with matching palette        |
| **ZSH**        | `vaporwave.zsh`                    | Prompt + syntax highlighting colours  |
| **Wallpaper**  | `wallpaper/vaporwave.png`          | Generated 2560×1440 synthwave scene   |
| **GTK**        | `gtk-settings.ini`                 | Dark pink GTK theme settings          |

---

## 🚀 Installation

```bash
git clone <repo-url> vaporwave-hyprland
cd vaporwave-hyprland
bash install.sh
```

The installer will:
1. Generate the wallpaper via Python (requires Pillow)
2. Back up any existing configs
3. Copy all files to `~/.config/`
4. Append the ZSH prompt to `~/.zshrc`

---

## 📋 Dependencies

### Required
- `hyprland` — Wayland compositor
- `hyprpaper` — Wallpaper daemon
- `hypridle` + `hyprlock` — Idle & lock
- `waybar` — Status bar
- `rofi-wayland` — App launcher
- `dunst` — Notifications
- `kitty` — Terminal
- `python3` + `python-pillow` — Wallpaper generation

### Recommended
```bash
# Arch / Manjaro (paru/yay)
paru -S \
  ttf-jetbrains-mono-nerd \
  papirus-icon-theme \
  colloid-gtk-theme-git \
  bibata-cursor-theme-bin \
  btop bat wlogout \
  zsh-syntax-highlighting \
  zsh-autosuggestions \
  playerctl brightnessctl \
  nm-applet blueman
```

---

## ⌨️ Key Bindings

| Keys                  | Action                          |
|-----------------------|---------------------------------|
| `SUPER + A`      | Kitty terminal                  |
| `SUPER + Space`       | Rofi app launcher               |
| `SUPER + B`           | Firefox                         |
| `SUPER + E`           | Thunar file manager             |
| `SUPER + Q`           | Close window                    |
| `SUPER + F`           | Fullscreen                      |
| `SUPER + T`           | Toggle float                    |
| `SUPER + H/J/K/L`     | Focus direction (vim keys)      |
| `SUPER + SHIFT + H/J/K/L` | Move window                 |
| `SUPER + CTRL + H/J/K/L`  | Resize window               |
| `SUPER + 1–0`         | Switch workspace                |
| `SUPER + SHIFT + 1–0` | Move window to workspace        |
| `SUPER + Tab`         | Next workspace                  |
| `SUPER + S`           | Toggle scratchpad               |
| `SUPER + V`           | Clipboard history (cliphist)    |
| `Print`               | Screenshot (output)             |
| `SUPER + Print`       | Screenshot (window)             |
| `SUPER + SHIFT + Print` | Screenshot (region)           |
| `SUPER + SHIFT + R`   | Reload Hyprland                 |

---

## 🎬 Animations

The config uses custom Bézier curves for a synthwave feel:

- **`neon`** — Snappy overshoot on window open/close
- **`glide`** — Smooth window movement
- **`synth`** — Bouncy workspace switching (vertical slide)
- **`fadeIn/Out`** — Ease curves for layers & fades

---

## 🔧 Customisation

### Wallpaper resolution
Edit `wallpaper/generate_wallpaper.py` line 11:
```python
W, H = 2560, 1440   # change to your resolution
```
Then `python3 wallpaper/generate_wallpaper.py`

### Monitor setup
Edit `hypr/hyprland.conf`:
```ini
monitor = eDP-1, 1920x1080@60, 0x0, 1
monitor = HDMI-A-1, 2560x1440@144, 1920x0, 1
```

### Primary accent color
The pink `#ff2a6d` is used as the primary accent.
Do a find-replace across all configs to swap it for any color.

---

## 📸 What you'll see

- **Wallpaper**: Synthwave horizon, segmented sun, perspective grid floor, mountain silhouettes, star field, scanline overlay, "VAPORWAVE" neon title
- **Bar**: Floating, rounded, glassmorphic with pink/cyan neon borders and glow effects
- **Windows**: Blurred glass, 12px corners, pink↔cyan↔purple animated gradient borders
- **Lock screen**: Blurred wallpaper, giant cyan clock with pink glow, neon input field
- **Notifications**: Rounded cards with pink frames, urgency-coloured accents
- **Rofi**: Dark translucent launcher with cyan selection glow
- **Terminal**: Semi-transparent with full vaporwave 16-color palette

---

*▓▒░ Built for Hyprland on Wayland ░▒▓*
