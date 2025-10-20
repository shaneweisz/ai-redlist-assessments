#!/bin/bash
# Setup script for IUCN Red List Assessment Pipeline

set -e

echo "🔧 Setting up IUCN Red List Assessment Pipeline..."

# Check Python version
echo "📋 Checking Python version..."
python3 --version || { echo "❌ Python 3 not found. Please install Python 3.10+"; exit 1; }

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "🐍 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "✨ Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directory structure..."
mkdir -p data/panthera_leo data/templates src/utils src/config tests

# Create .env file template if it doesn't exist
if [ ! -f "src/config/api_keys.env" ]; then
    echo "🔑 Creating API keys template..."
    cat > src/config/api_keys.env << 'EOF'
# API Keys for IUCN Red List Assessment Pipeline
# Copy this file and add your actual API keys

# IUCN Red List API (required for taxonomy and historical assessments)
# Get your key at: https://api.iucnredlist.org/users/sign_up
IUCN_API_KEY=your_key_here

# Optional: Other API keys
# CROSSREF_API_KEY=your_key_here
# GBIF_API_KEY=not_required_for_basic_use
EOF
    echo "⚠️  Please add your API keys to src/config/api_keys.env"
fi

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x scripts/*.py
chmod +x scripts/*.sh

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Add your IUCN API key to src/config/api_keys.env"
echo "2. Run the assessment pipeline: /assess Panthera leo"
echo ""
echo "To activate the virtual environment in the future:"
echo "  source venv/bin/activate"
echo ""
