"""
Rule-Based Chatbot Module
Implementation of NLTK-based chatbot using pattern matching
"""

import re
from typing import List, Tuple, Optional
from nltk.chat.util import Chat, reflections


class RuleBasedChatbot:
    """
    Rule-based chatbot using NLTK's Chat utility
    Matches user input against regex patterns and provides responses
    """
    
    def __init__(self, pairs: List[List], use_reflections: bool = True):
        """
        Initialize the chatbot with pattern pairs
        
        Args:
            pairs: List of [pattern, responses] pairs
            use_reflections: Whether to use NLTK reflections (I -> you, etc.)
        """
        if not pairs or len(pairs) == 0:
            raise ValueError("Pairs list cannot be empty")
        
        self.pairs = pairs
        self.reflections = reflections if use_reflections else {}
        self.chat = Chat(pairs, self.reflections)
        self.conversation_history = []
        self.pattern_usage = {i: 0 for i in range(len(pairs))}
    
    def respond(self, user_input: str) -> str:
        """
        Generate a response to user input
        
        Args:
            user_input: User's message
            
        Returns:
            Chatbot's response
        """
        if not user_input or not user_input.strip():
            return "Please say something!"
        
        # Store in conversation history
        response = self.chat.respond(user_input)
        
        if response is None:
            response = "I'm not sure how to respond to that."
        
        # Track which pattern was matched
        self._track_pattern_usage(user_input)
        
        # Add to conversation history
        self.conversation_history.append({
            'user': user_input,
            'bot': response
        })
        
        return response
    
    def _track_pattern_usage(self, user_input: str):
        """
        Track which pattern was matched for analytics
        
        Args:
            user_input: User's message
        """
        for i, (pattern, _) in enumerate(self.pairs):
            if re.match(pattern, user_input, re.IGNORECASE):
                self.pattern_usage[i] += 1
                break
    
    def get_conversation_history(self) -> List[dict]:
        """
        Get the full conversation history
        
        Returns:
            List of conversation exchanges
        """
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_pattern_statistics(self) -> dict:
        """
        Get statistics about pattern usage
        
        Returns:
            Dictionary with pattern usage statistics
        """
        total_messages = sum(self.pattern_usage.values())
        
        stats = {
            'total_messages': total_messages,
            'patterns_used': sum(1 for count in self.pattern_usage.values() if count > 0),
            'total_patterns': len(self.pairs),
            'pattern_usage': []
        }
        
        for i, count in self.pattern_usage.items():
            if i < len(self.pairs):
                pattern, responses = self.pairs[i]
                stats['pattern_usage'].append({
                    'pattern': pattern,
                    'count': count,
                    'percentage': (count / total_messages * 100) if total_messages > 0 else 0
                })
        
        # Sort by usage count
        stats['pattern_usage'].sort(key=lambda x: x['count'], reverse=True)
        
        return stats
    
    def get_unused_patterns(self) -> List[str]:
        """
        Get list of patterns that haven't been matched
        
        Returns:
            List of unused pattern strings
        """
        unused = []
        for i, count in self.pattern_usage.items():
            if count == 0 and i < len(self.pairs):
                pattern, _ = self.pairs[i]
                unused.append(pattern)
        return unused
    
    def export_conversation(self, format: str = 'text') -> str:
        """
        Export conversation history in specified format
        
        Args:
            format: Export format ('text', 'json', 'markdown')
            
        Returns:
            Formatted conversation string
        """
        if format == 'text':
            lines = []
            for exchange in self.conversation_history:
                lines.append(f"User: {exchange['user']}")
                lines.append(f"Bot: {exchange['bot']}")
                lines.append("")
            return "\n".join(lines)
        
        elif format == 'json':
            import json
            return json.dumps(self.conversation_history, indent=2)
        
        elif format == 'markdown':
            lines = ["# Conversation History\n"]
            for i, exchange in enumerate(self.conversation_history, 1):
                lines.append(f"## Exchange {i}\n")
                lines.append(f"**User:** {exchange['user']}\n")
                lines.append(f"**Bot:** {exchange['bot']}\n")
            return "\n".join(lines)
        
        else:
            raise ValueError(f"Unsupported format: {format}")


class ChatbotValidator:
    """Validates chatbot patterns and responses"""
    
    @staticmethod
    def validate_pairs(pairs: List[List]) -> Tuple[bool, Optional[str]]:
        """
        Validate pattern pairs structure
        
        Args:
            pairs: List of [pattern, responses] pairs
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not isinstance(pairs, list):
            return False, "'pairs' must be a list"
        
        if len(pairs) == 0:
            return False, "'pairs' list is empty"
        
        for i, pair in enumerate(pairs):
            if not isinstance(pair, list) or len(pair) != 2:
                return False, f"Pattern {i} is not a valid [pattern, responses] pair"
            
            pattern, responses = pair
            
            if not isinstance(pattern, str):
                return False, f"Pattern {i} regex is not a string"
            
            if not isinstance(responses, list):
                return False, f"Pattern {i} responses is not a list"
            
            if len(responses) == 0:
                return False, f"Pattern {i} has no responses"
            
            # Test regex compilation
            try:
                re.compile(pattern)
            except re.error as e:
                return False, f"Pattern {i} has invalid regex: {e}"
        
        return True, None
