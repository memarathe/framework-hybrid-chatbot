"""
Main Interface Module
Main Gradio interface orchestrating all components
"""

import gradio as gr
from typing import List, Tuple, Dict, Any
from src.pattern_generator import PatternGenerator
from src.chatbot_manager import ChatbotManager
from src.ui.components import UIComponents, UIStyles
from utils.validators import InputValidator
from utils.parser import PatternParser
from config.settings import UI_CONFIG


class HybridChatbotInterface:
    """Main Gradio interface for the Hybrid Chatbot Generator"""
    
    def __init__(self, api_key: str):
        """
        Initialize the interface
        
        Args:
            api_key: Google Gemini API key
        """
        self.pattern_generator = PatternGenerator(api_key)
        self.chatbot_manager = ChatbotManager()
        self.current_purpose = ""
    
    def generate_patterns(self, purpose: str) -> Tuple[str, str, str, str]:
        """
        Generate patterns from user purpose
        
        Args:
            purpose: User's chatbot purpose description
            
        Returns:
            Tuple of (status, patterns_code, suggestions, chatbot_status)
        """
        # Validate input
        is_valid, error_msg = InputValidator.validate_purpose(purpose)
        if not is_valid:
            return f"⚠️ {error_msg}", "", "", "⚠️ Chatbot not initialized"
        
        try:
            # Generate patterns
            patterns_code = self.pattern_generator.generate_patterns(purpose)
            
            # Initialize chatbot with generated patterns
            success, init_msg = self.chatbot_manager.initialize_chatbot(
                patterns_code, 
                purpose
            )
            
            if not success:
                return f"⚠️ Patterns generated but chatbot initialization failed: {init_msg}", patterns_code, "", init_msg
            
            # Get test suggestions
            suggestions = self._format_suggestions(
                self.chatbot_manager.get_test_suggestions()
            )
            
            # Store current purpose
            self.current_purpose = purpose
            
            status = "✅ Patterns generated successfully!"
            return status, patterns_code, suggestions, init_msg
            
        except Exception as e:
            error_status = f"❌ Error: {str(e)}"
            return error_status, "", "", "❌ Chatbot initialization failed"
    
    def reinitialize_chatbot(self, patterns_code: str) -> str:
        """
        Reinitialize chatbot with edited patterns
        
        Args:
            patterns_code: Modified patterns code
            
        Returns:
            Status message
        """
        if not patterns_code or not patterns_code.strip():
            return "⚠️ No patterns code provided"
        
        success, msg = self.chatbot_manager.initialize_chatbot(
            patterns_code,
            self.current_purpose
        )
        
        return msg
    
    def chat_respond(
        self, 
        message: str, 
        history: List
    ) -> Tuple[List, str]:
        """
        Handle chat interaction
        
        Args:
            message: User's message
            history: Chat history in Gradio format
            
        Returns:
            Tuple of (updated_history, empty_string)
        """
        if not message or not message.strip():
            return history, ""
        
        if not self.chatbot_manager.is_chatbot_active():
            if history is None:
                history = []
            history.append({
                "role": "user",
                "content": message
            })
            history.append({
                "role": "assistant", 
                "content": "⚠️ Please generate patterns first before chatting!"
            })
            return history, ""
        
        try:
            response = self.chatbot_manager.get_response(message)
            
            if history is None:
                history = []
            
            history.append({
                "role": "user",
                "content": message
            })
            history.append({
                "role": "assistant",
                "content": response
            })
            
            return history, ""
        except Exception as e:
            if history is None:
                history = []
            history.append({
                "role": "user",
                "content": message
            })
            history.append({
                "role": "assistant",
                "content": f"❌ Error: {str(e)}"
            })
            return history, ""
    
    def clear_chat(self) -> Tuple[List, str]:
        """
        Clear chat history
        
        Returns:
            Tuple of (empty_history, status_message)
        """
        msg = self.chatbot_manager.clear_conversation()
        return [], msg
    
    def get_statistics(self) -> str:
        """
        Get chatbot statistics
        
        Returns:
            Formatted statistics string
        """
        stats = self.chatbot_manager.get_statistics()
        
        if not stats.get('is_active'):
            return "📊 No active chatbot. Generate patterns to see statistics."
        
        lines = [
            "📊 Chatbot Statistics",
            "=" * 50,
            f"Purpose: {stats.get('purpose', 'N/A')}",
            "",
            f"Total Messages: {stats['total_messages']}",
            f"Total Patterns: {stats['total_patterns']}",
            f"Patterns Used: {stats['patterns_used']}",
            "",
            "Top 5 Most Used Patterns:",
        ]
        
        for i, pattern_stat in enumerate(stats['pattern_usage'][:5], 1):
            lines.append(
                f"{i}. {pattern_stat['pattern'][:50]}... "
                f"({pattern_stat['count']} times, {pattern_stat['percentage']:.1f}%)"
            )
        
        # Show unused patterns
        unused = self.chatbot_manager.get_unused_patterns()
        if unused:
            lines.append("")
            lines.append(f"⚠️ Unused Patterns: {len(unused)}")
            for pattern in unused[:3]:
                lines.append(f"  - {pattern[:60]}...")
        
        return "\n".join(lines)
    
    def export_conversation(self) -> str:
        """
        Export conversation history
        
        Returns:
            Exported conversation text
        """
        if not self.chatbot_manager.is_chatbot_active():
            return "No conversation to export."
        
        exported = self.chatbot_manager.export_conversation('markdown')
        
        if not exported or exported == "No conversation to export.":
            return "💬 No messages in conversation yet."
        
        return exported
    
    def _format_suggestions(self, suggestions: List[str]) -> str:
        """
        Format test suggestions for display
        
        Args:
            suggestions: List of suggested inputs
            
        Returns:
            Formatted string
        """
        if not suggestions:
            return "💡 No suggestions available. Try chatting to see patterns in action!"
        
        lines = ["💡 Try these test inputs:"]
        for i, suggestion in enumerate(suggestions, 1):
            lines.append(f"{i}. {suggestion}")
        
        return "\n".join(lines)
    
    def create_interface(self) -> gr.Blocks:
        """
        Create the main Gradio interface
        
        Returns:
            Configured Gradio Blocks interface
        """
        with gr.Blocks(title="Hybrid Chatbot Generator") as interface:

            
            # Header
            UIComponents.create_header()
            
            # Info accordion
            UIComponents.create_info_accordion()
            
            # Main layout - Two columns
            with gr.Row():
                # Left Column - Pattern Generation
                with gr.Column(scale=1):
                    gr.Markdown("## 🎯 Step 1: Generate Patterns")
                    
                    purpose_input = UIComponents.create_purpose_input()
                    
                    with gr.Row():
                        generate_btn = UIComponents.create_generate_button()
                    
                    status_output = UIComponents.create_status_output()
                    patterns_output = UIComponents.create_patterns_output()
                    
                    with gr.Row():
                        reinit_btn = UIComponents.create_reinitialize_button()
                    
                    reinit_status = gr.Textbox(
                        label="Reinitialize Status",
                        interactive=False,
                        visible=True
                    )
                    
                    # Examples
                    gr.Examples(
                        examples=[[ex] for ex in UIComponents.create_examples()],
                        inputs=[purpose_input],
                        label="💡 Example Purposes"
                    )
                
                # Right Column - Chatbot Testing
                with gr.Column(scale=1):
                    gr.Markdown("## 💬 Step 2: Test Your Chatbot")
                    
                    chatbot_status = gr.Textbox(
                        label="Chatbot Status",
                        value="⏳ Generate patterns to activate chatbot",
                        interactive=False
                    )
                    
                    chatbot_interface = UIComponents.create_chatbot_interface()
                    chat_input = UIComponents.create_chat_input()
                    
                    with gr.Row():
                        clear_btn = gr.Button("🗑️ Clear Chat", variant="secondary")
                    
                    # Suggestions
                    suggestions_output = UIComponents.create_test_suggestions()
                    
                    # Statistics and Export
                    with gr.Accordion("📊 Advanced Features", open=False):
                        stats_output = UIComponents.create_statistics_display()
                        
                        with gr.Row():
                            stats_btn = gr.Button("📈 Update Statistics")
                            export_btn = UIComponents.create_export_button()
                        
                        export_output = gr.Textbox(
                            label="Exported Conversation",
                            lines=10,
                            interactive=False
                        )
            
            # Event Handlers
            
            # Generate patterns
            generate_btn.click(
                fn=self.generate_patterns,
                inputs=[purpose_input],
                outputs=[status_output, patterns_output, suggestions_output, chatbot_status]
            )
            
            # Also trigger on Enter in purpose input
            purpose_input.submit(
                fn=self.generate_patterns,
                inputs=[purpose_input],
                outputs=[status_output, patterns_output, suggestions_output, chatbot_status]
            )
            
            # Reinitialize chatbot with edited patterns
            reinit_btn.click(
                fn=self.reinitialize_chatbot,
                inputs=[patterns_output],
                outputs=[reinit_status]
            )
            
            # Chat interactions
            chat_input.submit(
                fn=self.chat_respond,
                inputs=[chat_input, chatbot_interface],
                outputs=[chatbot_interface, chat_input]
            )
            
            # Clear chat
            clear_btn.click(
                fn=self.clear_chat,
                inputs=[],
                outputs=[chatbot_interface, chatbot_status]
            )
            
            # Update statistics
            stats_btn.click(
                fn=self.get_statistics,
                inputs=[],
                outputs=[stats_output]
            )
            
            # Export conversation
            export_btn.click(
                fn=self.export_conversation,
                inputs=[],
                outputs=[export_output]
            )
        
        return interface
    
    def launch(self, **kwargs):
        """
        Launch the Gradio interface
        
        Args:
            **kwargs: Additional arguments for gr.Blocks.launch()
        """
        interface = self.create_interface()
        
        # Set default theme and css if not provided
        if 'theme' not in kwargs:
            kwargs['theme'] = gr.themes.Soft()
        if 'css' not in kwargs:
            kwargs['css'] = UIStyles.get_custom_css()
        
        interface.launch(**kwargs)
