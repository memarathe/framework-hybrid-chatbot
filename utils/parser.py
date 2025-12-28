"""
Parser Utilities
Utilities for parsing and converting pattern code
"""

import re
from typing import List, Any


class PatternParser:
    """Parse and convert pattern code strings"""
    
    @staticmethod
    def parse_pairs(code_string: str) -> List[List]:
        """
        Parse Python code string containing pairs definition
        
        Args:
            code_string: Python code string with pairs = [...]
            
        Returns:
            Parsed pairs list
            
        Raises:
            ValueError: If parsing fails
        """
        if not code_string or not code_string.strip():
            raise ValueError("Code string is empty")
        
        # Clean the code string
        cleaned = code_string.strip()
        
        # Execute the code to get the pairs
        local_vars = {}
        try:
            exec(cleaned, {}, local_vars)
        except SyntaxError as e:
            raise ValueError(f"Syntax error in code: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error executing code: {str(e)}")
        
        # Extract pairs
        if 'pairs' not in local_vars:
            raise ValueError("No 'pairs' variable found in code")
        
        pairs = local_vars['pairs']
        
        if not isinstance(pairs, list):
            raise ValueError("'pairs' is not a list")
        
        return pairs
    
    @staticmethod
    def pairs_to_string(pairs: List[List]) -> str:
        """
        Convert pairs list to formatted Python code string
        
        Args:
            pairs: List of pattern pairs
            
        Returns:
            Formatted Python code string
        """
        lines = ["pairs = ["]
        
        for pattern, responses in pairs:
            # Format the pattern
            pattern_str = repr(pattern)
            
            # Format the responses
            if len(responses) == 1:
                responses_str = f"[{repr(responses[0])}]"
            else:
                responses_str = "[\n        " + ",\n        ".join(
                    repr(r) for r in responses
                ) + "\n    ]"
            
            lines.append(f"    [{pattern_str}, {responses_str}],")
        
        lines.append("]")
        
        return "\n".join(lines)
    
    @staticmethod
    def extract_patterns_summary(pairs: List[List]) -> dict:
        """
        Extract summary information from pairs
        
        Args:
            pairs: List of pattern pairs
            
        Returns:
            Dictionary with summary information
        """
        total_patterns = len(pairs)
        total_responses = sum(len(responses) for _, responses in pairs)
        
        # Find patterns with capture groups
        patterns_with_captures = sum(
            1 for pattern, _ in pairs if '(.*)' in pattern or '(' in pattern
        )
        
        # Identify pattern types
        greeting_patterns = sum(
            1 for pattern, _ in pairs 
            if any(word in pattern.lower() for word in ['hi', 'hello', 'hey'])
        )
        
        farewell_patterns = sum(
            1 for pattern, _ in pairs 
            if any(word in pattern.lower() for word in ['bye', 'goodbye', 'exit'])
        )
        
        catch_all_patterns = sum(
            1 for pattern, _ in pairs if pattern == r"(.*)"
        )
        
        return {
            'total_patterns': total_patterns,
            'total_responses': total_responses,
            'patterns_with_captures': patterns_with_captures,
            'greeting_patterns': greeting_patterns,
            'farewell_patterns': farewell_patterns,
            'catch_all_patterns': catch_all_patterns,
            'avg_responses_per_pattern': total_responses / total_patterns if total_patterns > 0 else 0
        }
