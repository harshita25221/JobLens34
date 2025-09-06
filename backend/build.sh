#!/bin/bash
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Set memory optimization environment variables
export MALLOC_ARENA_MAX=2
export PYTHONHASHSEED=random
export PYTHON_GC_AGGRESSIVE=1
export PYTHONUNBUFFERED=1

# Create .profile.d directory for Render environment variables persistence
mkdir -p .profile.d
cat > .profile.d/memory_optimization.sh << 'EOL'
#!/bin/bash
export MALLOC_ARENA_MAX=2
export PYTHONHASHSEED=random
export PYTHON_GC_AGGRESSIVE=1
export PYTHONUNBUFFERED=1
EOL
chmod +x .profile.d/memory_optimization.sh