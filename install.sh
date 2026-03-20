#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════
#  VAPORWAVE HYPRLAND RICE – INSTALLER
#  Run: bash install.sh
# ══════════════════════════════════════════════════════════════════

set -euo pipefail

RICE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CFG="$HOME/.config"

# ── Colors ────────────────────────────────────────────────────────
PINK='\033[38;2;255;42;109m'
CYAN='\033[38;2;5;217;232m'
PURP='\033[38;2;123;47;255m'
GOLD='\033[38;2;255;230;109m'
RST='\033[0m'
BOLD='\033[1m'

banner() {
  echo -e "\n${PINK}${BOLD}░░░ VAPORWAVE HYPRLAND RICE ░░░${RST}"
  echo -e "${CYAN}▓▒░ Synthwave Edition ░▒▓${RST}\n"
}

step() { echo -e "${PURP}  ➤ ${GOLD}$*${RST}"; }
ok()   { echo -e "${CYAN}    ✔ $*${RST}"; }
warn() { echo -e "${PINK}    ⚠ $*${RST}"; }

banner

# ── Check dependencies ────────────────────────────────────────────
step "Checking dependencies…"

REQUIRED=(hyprland hyprpaper hypridle hyprlock waybar rofi dunst kitty python3 pip)
MISSING=()

for dep in "${REQUIRED[@]}"; do
  if ! command -v "$dep" &>/dev/null 2>&1; then
    MISSING+=("$dep")
  else
    ok "$dep found"
  fi
done

if [ ${#MISSING[@]} -gt 0 ]; then
  warn "Missing packages: ${MISSING[*]}"
  warn "Install with your package manager before using this rice."
  warn "Continuing anyway to install config files…"
fi

# ── Generate wallpaper ────────────────────────────────────────────
step "Generating vaporwave wallpaper (2560×1440)…"
pip3 install Pillow --break-system-packages -q || pip3 install Pillow -q || true
python3 "$RICE_DIR/wallpaper/generate_wallpaper.py"
ok "Wallpaper generated at $RICE_DIR/wallpaper/vaporwave.png"

# ── Backup helper ─────────────────────────────────────────────────
backup_if_exists() {
  local target="$1"
  if [ -e "$target" ] && [ ! -L "$target" ]; then
    mv "$target" "${target}.bak.$(date +%s)"
    warn "Backed up existing $target"
  fi
}

# ── Install configs ───────────────────────────────────────────────
step "Installing Hyprland configs…"
mkdir -p "$CFG/hypr/wallpaper"

backup_if_exists "$CFG/hypr/hyprland.conf"
cp "$RICE_DIR/hypr/hyprland.conf"  "$CFG/hypr/hyprland.conf"

backup_if_exists "$CFG/hypr/hyprpaper.conf"
cp "$RICE_DIR/hypr/hyprpaper.conf" "$CFG/hypr/hyprpaper.conf"

backup_if_exists "$CFG/hypr/hypridle.conf"
cp "$RICE_DIR/hypr/hypridle.conf"  "$CFG/hypr/hypridle.conf"

backup_if_exists "$CFG/hypr/hyprlock.conf"
cp "$RICE_DIR/hypr/hyprlock.conf"  "$CFG/hypr/hyprlock.conf"

cp "$RICE_DIR/wallpaper/vaporwave.png" "$CFG/hypr/wallpaper/vaporwave.png"
ok "Hyprland configs installed"

step "Installing Waybar…"
mkdir -p "$CFG/waybar"
backup_if_exists "$CFG/waybar/config.jsonc"
backup_if_exists "$CFG/waybar/style.css"
cp "$RICE_DIR/waybar/config.jsonc" "$CFG/waybar/config.jsonc"
cp "$RICE_DIR/waybar/style.css"    "$CFG/waybar/style.css"
ok "Waybar installed"

step "Installing Rofi theme…"
mkdir -p "$CFG/rofi"
cp "$RICE_DIR/rofi/vaporwave.rasi" "$CFG/rofi/vaporwave.rasi"
ok "Rofi theme installed"

step "Installing Dunst…"
mkdir -p "$CFG/dunst"
backup_if_exists "$CFG/dunst/dunstrc"
cp "$RICE_DIR/dunst/dunstrc" "$CFG/dunst/dunstrc"
ok "Dunst config installed"

step "Installing Kitty…"
mkdir -p "$CFG/kitty"
backup_if_exists "$CFG/kitty/kitty.conf"
cp "$RICE_DIR/kitty.conf" "$CFG/kitty/kitty.conf"
ok "Kitty config installed"

step "Installing GTK settings…"
mkdir -p "$CFG/gtk-3.0" "$CFG/gtk-4.0"
backup_if_exists "$CFG/gtk-3.0/settings.ini"
backup_if_exists "$CFG/gtk-4.0/settings.ini"
cp "$RICE_DIR/gtk-settings.ini" "$CFG/gtk-3.0/settings.ini"
cp "$RICE_DIR/gtk-settings.ini" "$CFG/gtk-4.0/settings.ini"
ok "GTK settings installed"

step "Installing ZSH prompt snippet…"
ZSHRC="$HOME/.zshrc"
MARKER="# VAPORWAVE_RICE"
if ! grep -q "$MARKER" "$ZSHRC" 2>/dev/null; then
  {
    echo ""
    echo "$MARKER"
    cat "$RICE_DIR/vaporwave.zsh"
  } >> "$ZSHRC"
  ok "ZSH prompt added to $ZSHRC"
else
  warn "ZSH prompt already in $ZSHRC – skipping"
fi

# ── Recommended packages ──────────────────────────────────────────
echo ""
echo -e "${PINK}${BOLD}══ Recommended extras ══${RST}"
echo -e "${CYAN}  fonts  ${RST}: ttf-jetbrains-mono-nerd papirus-icon-theme"
echo -e "${CYAN}  gtk    ${RST}: colloid-gtk-theme bibata-cursor-theme"
echo -e "${CYAN}  tools  ${RST}: btop bat playerctl brightnessctl wlogout"
echo -e "${CYAN}  shell  ${RST}: zsh-syntax-highlighting zsh-autosuggestions"
echo ""
echo -e "${GOLD}  Arch/Manjaro install:${RST}"
echo -e "  ${PURP}paru -S ttf-jetbrains-mono-nerd papirus-icon-theme colloid-gtk-theme-git bibata-cursor-theme-bin btop bat wlogout${RST}"
echo ""
echo -e "${PINK}${BOLD}  Rice installed! Log out and select Hyprland.${RST}"
echo -e "${CYAN}  ▓▒░ ░▒▓${RST}\n"
