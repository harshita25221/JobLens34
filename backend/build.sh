#!/bin/bash
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Set memory optimization environment variables
export MALLOC_ARENA_MAX=2
export PYTHONHASHSEED=random

# Create .profile.d directory for Render environment variables persistence
mkdir -p .profile.d
echo 'export MALLOC_ARENA_MAX=2' > .profile.d/memory_optimization.sh
echo 'export PYTHONHASHSEED=random' >> .profile.d/memory_optimization.sh
chmod +x .profile.d/memory_optimization.sh