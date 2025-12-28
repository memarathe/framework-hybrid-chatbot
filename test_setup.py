"""
Test Script for Hybrid Chatbot Generator
Runs basic tests to verify all components work correctly
"""

import os
import sys


def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import gradio
        print("  ✅ Gradio")
    except ImportError as e:
        print(f"  ❌ Gradio: {e}")
        return False
    
    try:
        import google.generativeai
        print("  ✅ Google Generative AI")
    except ImportError as e:
        print(f"  ❌ Google Generative AI: {e}")
        return False
    
    try:
        import nltk
        print("  ✅ NLTK")
    except ImportError as e:
        print(f"  ❌ NLTK: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("  ✅ Python Dotenv")
    except ImportError as e:
        print(f"  ❌ Python Dotenv: {e}")
        return False
    
    print("✅ All imports successful!\n")
    return True


def test_project_structure():
    """Test if all required files and directories exist"""
    print("🧪 Testing project structure...")
    
    required_paths = [
        'src/',
        'src/__init__.py',
        'src/pattern_generator.py',
        'src/chatbot.py',
        'src/chatbot_manager.py',
        'src/ui/',
        'src/ui/__init__.py',
        'src/ui/components.py',
        'src/ui/interface.py',
        'utils/',
        'utils/__init__.py',
        'utils/validators.py',
        'utils/parser.py',
        'config/',
        'config/__init__.py',
        'config/settings.py',
        'app.py',
        'requirements.txt',
        'README.md',
    ]
    
    all_exist = True
    for path in required_paths:
        if os.path.exists(path):
            print(f"  ✅ {path}")
        else:
            print(f"  ❌ {path} (missing)")
            all_exist = False
    
    if all_exist:
        print("✅ Project structure is complete!\n")
    else:
        print("⚠️  Some files are missing!\n")
    
    return all_exist


def test_module_imports():
    """Test if custom modules can be imported"""
    print("🧪 Testing custom module imports...")
    
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        
        from src.pattern_generator import PatternGenerator
        print("  ✅ PatternGenerator")
        
        from src.chatbot import RuleBasedChatbot, ChatbotValidator
        print("  ✅ RuleBasedChatbot")
        print("  ✅ ChatbotValidator")
        
        from src.chatbot_manager import ChatbotManager
        print("  ✅ ChatbotManager")
        
        from utils.parser import PatternParser
        print("  ✅ PatternParser")
        
        from utils.validators import InputValidator, CodeValidator
        print("  ✅ InputValidator")
        print("  ✅ CodeValidator")
        
        from config.settings import APP_CONFIG, LLM_CONFIG
        print("  ✅ APP_CONFIG")
        print("  ✅ LLM_CONFIG")
        
        print("✅ All custom modules imported successfully!\n")
        return True
        
    except Exception as e:
        print(f"❌ Module import failed: {e}\n")
        return False


def test_chatbot_functionality():
    """Test basic chatbot functionality"""
    print("🧪 Testing chatbot functionality...")
    
    try:
        from src.chatbot import RuleBasedChatbot
        
        # Test pairs
        test_pairs = [
            [r"hi|hello", ["Hello!", "Hi there!"]],
            [r"my name is (.*)", ["Nice to meet you, %1!"]],
            [r"(.*)", ["I'm not sure I understand."]]
        ]
        
        chatbot = RuleBasedChatbot(test_pairs)
        print("  ✅ Chatbot initialized")
        
        # Test response
        response = chatbot.respond("Hello")
        if response:
            print(f"  ✅ Response generated: '{response}'")
        else:
            print("  ⚠️  Empty response")
        
        # Test with capture group
        response = chatbot.respond("my name is Alice")
        if "Alice" in response:
            print(f"  ✅ Capture group working: '{response}'")
        else:
            print(f"  ⚠️  Capture group issue: '{response}'")
        
        # Test statistics
        stats = chatbot.get_pattern_statistics()
        if stats['total_messages'] == 2:
            print(f"  ✅ Statistics tracking working")
        else:
            print(f"  ⚠️  Statistics issue")
        
        print("✅ Chatbot functionality works!\n")
        return True
        
    except Exception as e:
        print(f"❌ Chatbot test failed: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_pattern_parser():
    """Test pattern parsing functionality"""
    print("🧪 Testing pattern parser...")
    
    try:
        from utils.parser import PatternParser
        
        # Test code string
        test_code = '''pairs = [
    [r"hi|hello", ["Hello!"]],
    [r"bye", ["Goodbye!"]]
]'''
        
        parsed = PatternParser.parse_pairs(test_code)
        
        if len(parsed) == 2:
            print(f"  ✅ Parsed {len(parsed)} patterns")
        else:
            print(f"  ⚠️  Expected 2 patterns, got {len(parsed)}")
        
        # Test summary
        summary = PatternParser.extract_patterns_summary(parsed)
        if summary['total_patterns'] == 2:
            print(f"  ✅ Pattern summary working")
        else:
            print(f"  ⚠️  Summary issue")
        
        print("✅ Pattern parser works!\n")
        return True
        
    except Exception as e:
        print(f"❌ Parser test failed: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_validators():
    """Test validation functionality"""
    print("🧪 Testing validators...")
    
    try:
        from utils.validators import InputValidator
        
        # Test purpose validation
        is_valid, error = InputValidator.validate_purpose("This is a valid purpose for testing")
        if is_valid:
            print("  ✅ Purpose validation working")
        else:
            print(f"  ⚠️  Purpose validation issue: {error}")
        
        # Test pattern validation
        is_valid, error = InputValidator.validate_pattern(r"hello|hi")
        if is_valid:
            print("  ✅ Pattern validation working")
        else:
            print(f"  ⚠️  Pattern validation issue: {error}")
        
        # Test invalid pattern
        is_valid, error = InputValidator.validate_pattern(r"[invalid(")
        if not is_valid:
            print("  ✅ Invalid pattern detection working")
        else:
            print("  ⚠️  Should have detected invalid pattern")
        
        print("✅ Validators work!\n")
        return True
        
    except Exception as e:
        print(f"❌ Validator test failed: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 Running Tests for Hybrid Chatbot Generator")
    print("=" * 60)
    print()
    
    tests = [
        ("Imports", test_imports),
        ("Project Structure", test_project_structure),
        ("Custom Module Imports", test_module_imports),
        ("Chatbot Functionality", test_chatbot_functionality),
        ("Pattern Parser", test_pattern_parser),
        ("Validators", test_validators),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}\n")
            results.append((test_name, False))
    
    # Summary
    print("=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
        print("\nYou can now run the application:")
        print("  python app.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    print("=" * 60)
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
