# ══════════════════════════════════════════════════════════
#  VAPORWAVE ZSH PROMPT  (pure POSIX – paste into .zshrc)
# ══════════════════════════════════════════════════════════
# Requires: zsh, git

autoload -Uz vcs_info
zstyle ':vcs_info:*' enable git
zstyle ':vcs_info:git*' formats ' %F{#7b2fff}[%F{#ff71ce}%b%F{#7b2fff}]%f'
zstyle ':vcs_info:git*' actionformats ' %F{#ff2a6d}[%b|%a]%f'

setopt PROMPT_SUBST

precmd() { vcs_info }

# Neon pink arrow chain
PROMPT='%F{#ff2a6d}▓▒░%f%F{#7b2fff}%~%f${vcs_info_msg_0_} %F{#05d9e8}❯%F{#7b2fff}❯%F{#ff71ce}❯%f '

# Right prompt: time in cyan
RPROMPT='%F{#05d9e8}⏱ %D{%H:%M}%f'

# ── LS Colors ──────────────────────────────────────────────
export LS_COLORS="rs=0:di=01;34:ln=01;36:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:su=37;41:sg=30;43:tw=30;42:ow=34;42:st=37;44:ex=01;32"

# ── Aliases ────────────────────────────────────────────────
alias ls='ls --color=auto'
alias ll='ls -lah --color=auto'
alias la='ls -A'
alias grep='grep --color=auto'
alias diff='diff --color=auto'
alias ip='ip -color=auto'
alias cat='bat --style=plain --theme=base16'  # needs bat
alias top='btop'                               # needs btop

# ── Syntax highlighting + autosuggestions ─────────────────
# Uncomment if installed:
# source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
# source /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh

ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE='fg=#3a1560'
ZSH_HIGHLIGHT_STYLES[default]='fg=#e0d0ff'
ZSH_HIGHLIGHT_STYLES[command]='fg=#05d9e8,bold'
ZSH_HIGHLIGHT_STYLES[alias]='fg=#ff71ce,bold'
ZSH_HIGHLIGHT_STYLES[builtin]='fg=#7b2fff,bold'
ZSH_HIGHLIGHT_STYLES[path]='fg=#c0b0ff,underline'
ZSH_HIGHLIGHT_STYLES[string]='fg=#ffe66d'
ZSH_HIGHLIGHT_STYLES[comment]='fg=#3a1560'
