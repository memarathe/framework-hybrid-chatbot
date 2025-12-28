"""
Validation Utilities
Utilities for validating patterns, inputs, and configurations
"""

import re
from typing import Tuple, Optional, List
from config.settings import VALIDATION_CONFIG


class InputValidator:
    """Validates user inputs and configurations"""
    
    @staticmethod
    def validate_purpose(purpose: str) -> Tuple[bool, Optional[str]]:
        """
        Validate chatbot purpose input
        
        Args:
            purpose: User-provided chatbot purpose
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not purpose or not purpose.strip():
            return False, "Purpose cannot be empty"
        
        if len(purpose.strip()) < 10:
            return False, "Purpose is too short. Please provide more details (at least 10 characters)"
        
        if len(purpose) > 1000:
            return False, "Purpose is too long. Please keep it under 1000 characters"
        
        return True, None
    
    @staticmethod
    def validate_pattern(pattern: str) -> Tuple[bool, Optional[str]]:
        """
        Validate a single regex pattern
        
        Args:
            pattern: Regex pattern string
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not pattern:
            return False, "Pattern cannot be empty"
        
        if len(pattern) > VALIDATION_CONFIG['max_pattern_length']:
            return False, f"Pattern exceeds maximum length of {VALIDATION_CONFIG['max_pattern_length']}"
        
        # Try to compile the regex
        try:
            re.compile(pattern)
        except re.error as e:
            return False, f"Invalid regex pattern: {str(e)}"
        
        return True, None
    
    @staticmethod
    def validate_response(response: str) -> Tuple[bool, Optional[str]]:
        """
        Validate a chatbot response
        
        Args:
            response: Response string
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not response:
            return False, "Response cannot be empty"
        
        if len(response) > VALIDATION_CONFIG['max_response_length']:
            return False, f"Response exceeds maximum length of {VALIDATION_CONFIG['max_response_length']}"
        
        return True, None
    
    @staticmethod
    def validate_pairs_structure(pairs: List) -> Tuple[bool, Optional[str]]:
        """
        Validate the structure of pairs list
        
        Args:
            pairs: List of pattern pairs
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not isinstance(pairs, list):
            return False, "Pairs must be a list"
        
        if len(pairs) == 0:
            return False, "Pairs list is empty"
        
        # Check if catch-all pattern exists (if required)
        if VALIDATION_CONFIG['required_catch_all']:
            has_catch_all = any(pattern == r"(.*)" for pattern, _ in pairs)
            if not has_catch_all:
                return False, "Missing required catch-all pattern: [r\"(.*)\", [...]]"
        
        # Validate each pair
        for i, pair in enumerate(pairs):
            if not isinstance(pair, list) or len(pair) != 2:
                return False, f"Pair {i} must be a list with exactly 2 elements [pattern, responses]"
            
            pattern, responses = pair
            
            # Validate pattern
            is_valid, error = InputValidator.validate_pattern(pattern)
            if not is_valid:
                return False, f"Pair {i} - {error}"
            
            # Validate responses
            if not isinstance(responses, list):
                return False, f"Pair {i} - Responses must be a list"
            
            if len(responses) == 0:
                return False, f"Pair {i} - Responses list is empty"
            
            for j, response in enumerate(responses):
                is_valid, error = InputValidator.validate_response(response)
                if not is_valid:
                    return False, f"Pair {i}, Response {j} - {error}"
        
        return True, None


class CodeValidator:
    """Validates generated code"""
    
    @staticmethod
    def validate_python_code(code: str) -> Tuple[bool, Optional[str]]:
        """
        Validate Python code syntax
        
        Args:
            code: Python code string
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not code or not code.strip():
            return False, "Code is empty"
        
        try:
            compile(code, '<string>', 'exec')
            return True, None
        except SyntaxError as e:
            return False, f"Syntax error: {str(e)}"
        except Exception as e:
            return False, f"Code validation error: {str(e)}"
    
    @staticmethod
    def check_for_dangerous_code(code: str) -> Tuple[bool, Optional[str]]:
        """
        Check for potentially dangerous code patterns
        
        Args:
            code: Python code string
            
        Returns:
            Tuple of (is_safe, warning_message)
        """
        dangerous_patterns = [
            (r'\bimport\s+os\b', "imports os module"),
            (r'\bimport\s+sys\b', "imports sys module"),
            (r'\beval\s*\(', "uses eval()"),
            (r'\b__import__\s*\(', "uses __import__()"),
            (r'\bopen\s*\(', "opens files"),
            (r'\bexec\s*\(', "uses exec() with external input"),
        ]
        
        warnings = []
        for pattern, description in dangerous_patterns:
            if re.search(pattern, code):
                warnings.append(description)
        
        if warnings:
            warning_msg = "Code contains potentially dangerous operations: " + ", ".join(warnings)
            return False, warning_msg
        
        return True, None
