"""
UI Components Module
Reusable Gradio UI components for the Hybrid Chatbot Generator
"""

import gradio as gr
from config.settings import UI_CONFIG


class UIComponents:
    """Factory class for creating Gradio UI components"""
    
    @staticmethod
    def create_header() -> gr.Markdown:
        """
        Create application header
        
        Returns:
            Gradio Markdown component
        """
        return gr.Markdown(
            """
            # 🤖 Hybrid Chatbot Generator
            ### Generate AI-powered regex patterns and test your rule-based chatbot in real-time
            
            **How it works:**
            1. Describe your chatbot's purpose
            2. Generate patterns using AI
            3. Test your chatbot instantly
            """
        )
    
    @staticmethod
    def create_purpose_input() -> gr.Textbox:
        """
        Create chatbot purpose input field
        
        Returns:
            Gradio Textbox component
        """
        return gr.Textbox(
            label="Describe Your Chatbot Purpose",
            placeholder="E.g., A customer service chatbot for a pizza delivery service that can take orders, answer questions about menu items, and provide delivery estimates...",
            lines=4,
            max_lines=8
        )
    
    @staticmethod
    def create_generate_button() -> gr.Button:
        """
        Create generate patterns button
        
        Returns:
            Gradio Button component
        """
        return gr.Button(
            "Generate Patterns",
            variant="primary",
            size="lg"
        )
    
    @staticmethod
    def create_status_output() -> gr.Textbox:
        """
        Create status message output
        
        Returns:
            Gradio Textbox component
        """
        return gr.Textbox(
            label="Status",
            interactive=False,
            show_label=True
        )
    
    @staticmethod
    def create_patterns_output() -> gr.Code:
        """
        Create patterns code output
        
        Returns:
            Gradio Code component
        """
        return gr.Code(
            label="Generated Patterns",
            language="python",
            lines=15,
            interactive=True
        )
    
    @staticmethod
    def create_examples() -> list:
        """
        Create example purposes
        
        Returns:
            List of example strings
        """
        return UI_CONFIG['default_examples']
    
    @staticmethod
    def create_chatbot_interface() -> gr.Chatbot:
        """
        Create chatbot conversation interface
        
        Returns:
            Gradio Chatbot component
        """
        return gr.Chatbot(
            label="Chat with Your Bot",
            height=400,
            show_label=True,
            avatar_images=(None, "🤖")
        )
    
    @staticmethod
    def create_chat_input() -> gr.Textbox:
        """
        Create chat message input
        
        Returns:
            Gradio Textbox component
        """
        return gr.Textbox(
            label="Your Message",
            placeholder="Type your message here and press Enter...",
            show_label=False,
            lines=1
        )
    
    @staticmethod
    def create_chat_controls() -> tuple:
        """
        Create chat control buttons
        
        Returns:
            Tuple of Gradio Button components (send, clear)
        """
        with gr.Row():
            send_btn = gr.Button("Send", variant="primary", scale=2)
            clear_btn = gr.Button("Clear Chat", variant="secondary", scale=1)
        
        return send_btn, clear_btn
    
    @staticmethod
    def create_statistics_display() -> gr.Textbox:
        """
        Create statistics display
        
        Returns:
            Gradio Textbox component
        """
        return gr.Textbox(
            label="📈 Chatbot Statistics",
            lines=8,
            interactive=False
        )
    
    @staticmethod
    def create_test_suggestions() -> gr.Textbox:
        """
        Create test suggestions display
        
        Returns:
            Gradio Textbox component
        """
        return gr.Textbox(
            label="Suggested Test Inputs",
            placeholder="Generate patterns first to see test suggestions...",
            lines=6,
            interactive=False
        )
    
    @staticmethod
    def create_export_button() -> gr.Button:
        """
        Create export conversation button
        
        Returns:
            Gradio Button component
        """
        return gr.Button(
            "Export Conversation",
            variant="secondary"
        )
    
    @staticmethod
    def create_reinitialize_button() -> gr.Button:
        """
        Create reinitialize chatbot button
        
        Returns:
            Gradio Button component
        """
        return gr.Button(
            "Reinitialize Chatbot",
            variant="secondary"
        )
    
    @staticmethod
    def create_info_accordion() -> gr.Accordion:
        """
        Create information accordion
        
        Returns:
            Gradio Accordion component
        """
        with gr.Accordion("ℹHow to Use", open=False) as accordion:
            gr.Markdown(
                """
                ### Pattern Generation
                1. **Describe Your Purpose**: Enter a detailed description of what your chatbot should do. Begin with some context as to why you need this chatbot and what domain is your industry serving.
                2. **Generate**: Click the generate button to create patterns using AI
                3. **Review**: Check the generated patterns in the code editor
                4. **Edit** (Optional): Modify patterns directly in the code editor if needed
                
                ### Testing Your Chatbot
                1. **Automatic Initialization**: Chatbot is ready once patterns are generated
                2. **Chat**: Type messages in the chat input and press Enter
                3. **Test Suggestions**: Use the suggested inputs to test different patterns
                4. **Statistics**: Monitor which patterns are being used
                5. **Export**: Save your conversation for later review
                
                ### Pattern Format
                ```python
                [r"pattern", ["response1", "response2"]]
                ```
                - Use `(.*)` to capture user input
                - Reference captures with `%1`, `%2`, etc. in responses
                - Order patterns from specific to general
                
                ### Tips
                - Be specific in your purpose description
                - Include common greetings and farewells
                - Test edge cases with the chatbot
                - Use the statistics to improve coverage
                """
            )
        
        return accordion


class UIStyles:
    """CSS styles for the UI"""
    
    @staticmethod
    def get_custom_css() -> str:
        """
        Get custom CSS styles
        
        Returns:
            CSS string
        """
        return """
        .gradio-container {
            max-width: 1400px !important;
        }
        
        .pattern-editor {
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
        }
        
        .status-success {
            color: #28a745;
        }
        
        .status-error {
            color: #dc3545;
        }
        
        .chat-message {
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
        }
        """
