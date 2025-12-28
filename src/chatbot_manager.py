"""
Chatbot Manager Module
Manages chatbot lifecycle, state, and pattern updates
"""

from typing import Optional, List, Dict, Any
from src.chatbot import RuleBasedChatbot, ChatbotValidator
from utils.parser import PatternParser


class ChatbotManager:
    """
    Manages chatbot instances and their lifecycle
    Handles pattern updates, state management, and chatbot operations
    """
    
    def __init__(self):
        """Initialize the chatbot manager"""
        self.chatbot: Optional[RuleBasedChatbot] = None
        self.current_pairs = None
        self.current_purpose = ""
        self.is_active = False
    
    def initialize_chatbot(self, pairs_code: str, purpose: str = "") -> tuple[bool, str]:
        """
        Initialize or reinitialize the chatbot with new patterns
        
        Args:
            pairs_code: Python code string containing pairs definition
            purpose: Original purpose description (for reference)
            
        Returns:
            Tuple of (success, message)
        """
        try:
            # Parse the pairs code
            pairs = PatternParser.parse_pairs(pairs_code)
            
            # Validate pairs
            is_valid, error_msg = ChatbotValidator.validate_pairs(pairs)
            if not is_valid:
                return False, f"Validation failed: {error_msg}"
            
            # Create new chatbot instance
            self.chatbot = RuleBasedChatbot(pairs)
            self.current_pairs = pairs
            self.current_purpose = purpose
            self.is_active = True
            
            return True, f"Chatbot initialized successfully with {len(pairs)} patterns!"
            
        except Exception as e:
            self.is_active = False
            return False, f"Failed to initialize chatbot: {str(e)}"
    
    def get_response(self, user_input: str) -> str:
        """
        Get chatbot response to user input
        
        Args:
            user_input: User's message
            
        Returns:
            Chatbot's response
            
        Raises:
            RuntimeError: If chatbot is not initialized
        """
        if not self.is_active or self.chatbot is None:
            raise RuntimeError("Chatbot is not initialized. Please generate patterns first.")
        
        return self.chatbot.respond(user_input)
    
    def clear_conversation(self) -> str:
        """
        Clear conversation history
        
        Returns:
            Success message
        """
        if self.chatbot:
            self.chatbot.clear_history()
            return "🗑️ Conversation history cleared!"
        return "No active chatbot to clear."
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get chatbot statistics
        
        Returns:
            Dictionary with chatbot statistics
        """
        if not self.chatbot:
            return {
                'is_active': False,
                'message': 'No active chatbot'
            }
        
        stats = self.chatbot.get_pattern_statistics()
        stats['is_active'] = self.is_active
        stats['purpose'] = self.current_purpose
        
        return stats
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """
        Get full conversation history
        
        Returns:
            List of conversation exchanges
        """
        if not self.chatbot:
            return []
        return self.chatbot.get_conversation_history()
    
    def export_conversation(self, format: str = 'text') -> str:
        """
        Export conversation in specified format
        
        Args:
            format: Export format (text, json, markdown)
            
        Returns:
            Formatted conversation string
        """
        if not self.chatbot:
            return "No conversation to export."
        
        return self.chatbot.export_conversation(format)
    
    def get_unused_patterns(self) -> List[str]:
        """
        Get patterns that haven't been matched yet
        
        Returns:
            List of unused patterns
        """
        if not self.chatbot:
            return []
        return self.chatbot.get_unused_patterns()
    
    def get_test_suggestions(self) -> List[str]:
        """
        Generate test input suggestions based on patterns
        
        Returns:
            List of suggested test inputs
        """
        if not self.current_pairs:
            return []
        
        suggestions = []
        
        # Extract sample inputs from patterns
        for pattern, responses in self.current_pairs[:10]:  # Limit to first 10
            # Try to generate a simple test case from the pattern
            if pattern == r"(.*)":
                continue  # Skip catch-all
            
            # Simple heuristics for test generation
            test_input = self._pattern_to_test_input(pattern)
            if test_input:
                suggestions.append(test_input)
        
        return suggestions[:8]  # Return max 8 suggestions
    
    def _pattern_to_test_input(self, pattern: str) -> Optional[str]:
        """
        Convert a regex pattern to a test input
        
        Args:
            pattern: Regex pattern string
            
        Returns:
            Suggested test input or None
        """
        # Remove regex syntax
        clean = pattern.replace(r"\b", "").replace(r"\s+", " ")
        clean = clean.replace("(.*)", "something")
        clean = clean.replace(".*", "")
        clean = clean.replace(r"\?", "?")
        
        # Handle alternatives (|)
        if "|" in clean:
            options = clean.split("|")
            clean = options[0]
        
        # Clean up
        clean = clean.strip().replace("  ", " ")
        
        # If it's too short or looks like pure regex, skip
        if len(clean) < 3 or clean.startswith("^") or clean.endswith("$"):
            return None
        
        return clean
    
    def reset(self):
        """Reset the chatbot manager to initial state"""
        self.chatbot = None
        self.current_pairs = None
        self.current_purpose = ""
        self.is_active = False
    
    def is_chatbot_active(self) -> bool:
        """
        Check if chatbot is active and ready
        
        Returns:
            True if chatbot is active
        """
        return self.is_active and self.chatbot is not None
