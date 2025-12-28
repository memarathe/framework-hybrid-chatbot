"""
Pattern Generator Module
Handles LLM-based regex pattern generation for chatbots using Google Gemini
"""

import re
from typing import Optional
try:
    from google import genai
    USING_NEW_SDK = True
except ImportError:
    import google.generativeai as genai
    USING_NEW_SDK = False
from config.settings import LLM_CONFIG, PATTERN_CONFIG


class PatternGenerator:
    """Generates regex patterns for rule-based chatbots using LLM"""
    
    def __init__(self, api_key: str):
        """
        Initialize the pattern generator with Gemini API
        
        Args:
            api_key: Google Gemini API key
            
        Raises:
            ValueError: If API key is invalid
        """
        if not api_key:
            raise ValueError("API key cannot be empty")
        
        try:
            if USING_NEW_SDK:
                # New SDK (google.genai)
                self.client = genai.Client(api_key=api_key)
                self.model_name = LLM_CONFIG['model_name']
                self.model = None  # Not used with new SDK
            else:
                # Old SDK (google.generativeai) - backward compatibility
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel(
                    LLM_CONFIG['model_name'],
                    generation_config={
                        'temperature': LLM_CONFIG['temperature'],
                        'max_output_tokens': LLM_CONFIG['max_output_tokens']
                    }
                )
                self.model_name = None
                self.client = None
        except Exception as e:
            raise ValueError(f"Failed to initialize Gemini API: {str(e)}")
    
    def create_prompt(self, user_purpose: str) -> str:
        """
        Create a structured prompt for the LLM
        
        Args:
            user_purpose: Natural language description of chatbot purpose
            
        Returns:
            Formatted prompt string
        """
        min_patterns = PATTERN_CONFIG['min_patterns']
        max_patterns = PATTERN_CONFIG['max_patterns']
        
        prompt = f"""Generate a COMPLETE Python list of regex pattern pairs for a rule-based chatbot.

    **Purpose:** {user_purpose}

    **CRITICAL REQUIREMENTS:**

    1. **Format** - Return ONLY this (no markdown, no explanation):
    pairs = [
        [r"pattern1", ["response1", "response2"]],
        [r"pattern2", ["response3"]],
        ...
    ]

    2. **Pattern Count**: Generate exactly {min_patterns} to {max_patterns} patterns

    3. **Pattern Flexibility** - VERY IMPORTANT:
    - Use `(?i).*keyword.*` format to match keywords ANYWHERE in text
    - DO NOT use `(?i)(?:...)` - this is TOO STRICT
    - Example GOOD: r"(?i).*hello.*" matches "hello", "say hello", "hello there"
    - Example BAD: r"(?i)(?:hello)" only matches if text STARTS with "hello"

    4. **Case Insensitivity**: 
    - Use (?i) flag at the start: r"(?i).*pattern.*"
    - This makes pattern match regardless of case

    5. **Capture Groups**:
    - Use (.*) to capture user input
    - Reference with %1, %2, %3 in responses
    - Example: r"(?i).*from (.*) to (.*)" → "Flight from %1 to %2"

    6. **Response Length**: 
    - Keep responses SHORT (under 100 characters)
    - Be conversational and helpful

    7. **Pattern Order** - CRITICAL:
    - Most specific patterns FIRST
    - General patterns in middle  
    - Catch-all pattern LAST

    8. **Required Patterns**:
    - Greetings: r"(?i).*(hi|hello|hey).*"
    - Farewells: r"(?i).*(bye|goodbye).*"
    - Catch-all at END: [r"(.*)", ["I didn't understand. Could you rephrase?"]]

    **GOOD Pattern Examples:**
    ```python
    [r"(?i).*(hello|hi|hey).*", ["Hello! How can I help?"]]
    [r"(?i).*my name is (.*).*", ["Nice to meet you, %1!"]]
    [r"(?i).*(help|assist).*", ["I'm here to help!"]]
    [r"(?i).*from (.*) to (.*).*", ["Flight from %1 to %2. When?"]]
    ```

    **BAD Pattern Examples (DO NOT USE):**
    ```python
    [r"(?i)(?:hello)", ...]  #  Too strict - must start with hello
    [r"^hello$", ...]        #  Exact match only
    [r"hello", ...]          #  Case sensitive
    ```

    **Output Requirements:**
    - Start with: pairs = [
    - End with: ]
    - Must be COMPLETE - do not truncate
    - Each pattern must match flexibly (use .* before and after keywords)
    - Responses must be brief and contextual

    Generate the COMPLETE list now:
    """
        return prompt
    
    def generate_patterns(self, user_purpose: str) -> str:
        """
        Generate regex patterns using Gemini LLM
        
        Args:
            user_purpose: Natural language description of chatbot purpose
            
        Returns:
            Generated patterns as Python code string
            
        Raises:
            Exception: If pattern generation fails
        """
        if not user_purpose or not user_purpose.strip():
            raise ValueError("User purpose cannot be empty")
        
        try:
            prompt = self.create_prompt(user_purpose.strip())
            
            if USING_NEW_SDK:
                # New SDK - use the client
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config={
                        'temperature': LLM_CONFIG['temperature'],
                        'max_output_tokens': LLM_CONFIG['max_output_tokens']
                    }
                )
                response_text = response.text
            else:
                # Old SDK
                response = self.model.generate_content(prompt)
                response_text = response.text
            
            if not response_text:
                raise Exception("Empty response from LLM")
            
            cleaned_response = self._clean_response(response_text)
            return cleaned_response
            
        except Exception as e:
            raise Exception(f"Pattern generation failed: {str(e)}")
    
    def _clean_response(self, response_text: str) -> str:
        """
        Clean and validate LLM response
        
        Args:
            response_text: Raw LLM response
            
        Returns:
            Cleaned Python code string
            
        Raises:
            ValueError: If response format is invalid
        """
        # Remove markdown code blocks if present
        cleaned = re.sub(r'```python\n?', '', response_text)
        cleaned = re.sub(r'```\n?', '', cleaned)
        
        # Remove any leading/trailing whitespace
        cleaned = cleaned.strip()
        
        # Remove any text before 'pairs = '
        if 'pairs = ' in cleaned:
            start_idx = cleaned.find('pairs = ')
            cleaned = cleaned[start_idx:]
        elif 'pairs=[' in cleaned:
            start_idx = cleaned.find('pairs=')
            cleaned = cleaned[start_idx:]
        else:
            raise ValueError("Response doesn't contain valid pairs definition")
        
        # Remove any text after the closing bracket of the main list
        # Find the last ] that should close the pairs list
        bracket_count = 0
        found_start = False
        end_idx = len(cleaned)
        
        for i, char in enumerate(cleaned):
            if char == '[':
                bracket_count += 1
                found_start = True
            elif char == ']':
                bracket_count -= 1
                if found_start and bracket_count == 0:
                    end_idx = i + 1
                    break
        
        cleaned = cleaned[:end_idx]
        
        # Ensure it starts with 'pairs = ' or 'pairs='
        if not (cleaned.startswith('pairs = ') or cleaned.startswith('pairs=')):
            raise ValueError("Response doesn't start with 'pairs ='")
        
        return cleaned
    
    def regenerate_with_modifications(
        self, 
        original_purpose: str, 
        feedback: str
    ) -> str:
        """
        Regenerate patterns with user feedback
        
        Args:
            original_purpose: Original chatbot purpose
            feedback: User feedback for modifications
            
        Returns:
            Regenerated patterns as Python code string
        """
        modified_purpose = f"{original_purpose}\n\nAdditional requirements: {feedback}"
        return self.generate_patterns(modified_purpose)
