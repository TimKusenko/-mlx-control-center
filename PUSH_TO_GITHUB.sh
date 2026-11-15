#!/bin/bash
# Einfach ausführen: bash PUSH_TO_GITHUB.sh

echo "🚀 Uploading to GitHub..."

# 1. GitHub URL setzen
git remote add origin https://github.com/tarnyx/mlx-control-center.git 2>/dev/null

# 2. Branch umbenennen
git branch -M main

# 3. Konfigurieren
git config user.email "timkusenko.tk@gmail.com"
git config user.name "Tim Kusenko"

# 4. Pushen (GitHub fragt nach Passwort)
git push -u origin main

echo "✅ Done! Check: https://github.com/tarnyx/mlx-control-center"
