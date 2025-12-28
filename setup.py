"""
Setup Script for Hybrid Chatbot Generator
Downloads required NLTK data and verifies installation
"""

import os
import sys


def download_nltk_data():
    """Download required NLTK data"""
    try:
        import nltk
        print("📦 Downloading NLTK data...")
        
        # Download required packages
        packages = ['punkt', 'averaged_perceptron_tagger']
        
        for package in packages:
            print(f"  ⬇️  Downloading {package}...")
            try:
                nltk.download(package, quiet=True)
                print(f"  ✅ {package} downloaded successfully")
            except Exception as e:
                print(f"  ⚠️  Warning: Could not download {package}: {e}")
        
        print("✅ NLTK data download complete!\n")
        return True
        
    except ImportError:
        print("❌ NLTK not installed. Please run: pip install -r requirements.txt")
        return False


def verify_installation():
    """Verify all dependencies are installed"""
    print("🔍 Verifying installation...\n")
    
    required_packages = [
        ('gradio', 'Gradio'),
        ('google.generativeai', 'Google Generative AI'),
        ('dotenv', 'Python Dotenv'),
        ('nltk', 'NLTK')
    ]
    
    missing_packages = []
    
    for package, name in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {name} is installed")
        except ImportError:
            print(f"  ❌ {name} is NOT installed")
            missing_packages.append(name)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Please run: pip install -r requirements.txt")
        return False
    
    print("\n✅ All dependencies are installed!\n")
    return True


def check_env_file():
    """Check if .env file exists and has API key"""
    print("🔍 Checking environment configuration...\n")
    
    if not os.path.exists('.env'):
        print("⚠️  .env file not found")
        print("Creating .env file from template...")
        
        if os.path.exists('.env.example'):
            import shutil
            shutil.copy('.env.example', '.env')
            print("✅ .env file created")
            print("⚠️  Please edit .env and add your GEMINI_KEY\n")
        else:
            print("❌ .env.example not found")
            print("Please create a .env file with: GEMINI_KEY=your_api_key_here\n")
        return False
    
    # Check if API key is set
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('GEMINI_KEY')
    
    if not api_key or api_key == 'your_gemini_api_key_here':
        print("⚠️  GEMINI_KEY not set in .env file")
        print("Please edit .env and add your actual Gemini API key")
        print("Get your key at: https://makersuite.google.com/app/apikey\n")
        return False
    
    print("✅ Environment configuration is complete!\n")
    return True


def main():
    """Main setup function"""
    print("=" * 60)
    print("🤖 Hybrid Chatbot Generator - Setup")
    print("=" * 60)
    print()
    
    # Step 1: Verify installation
    if not verify_installation():
        print("\n❌ Setup incomplete. Please install missing dependencies.")
        sys.exit(1)
    
    # Step 2: Download NLTK data
    if not download_nltk_data():
        print("\n❌ Setup incomplete. Please install NLTK.")
        sys.exit(1)
    
    # Step 3: Check environment
    env_ready = check_env_file()
    
    # Final message
    print("=" * 60)
    if env_ready:
        print("✅ Setup complete! You're ready to run the application.")
        print("\nTo start the application, run:")
        print("  python app.py")
    else:
        print("⚠️  Setup incomplete. Please configure your .env file.")
        print("\nAfter adding your GEMINI_KEY to .env, run:")
        print("  python app.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
