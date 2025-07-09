import pytest
import os
import sys
from unittest.mock import Mock, patch

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from chat_handler import ChatHandler
from utils import validate_environment, format_error_message

class TestChatHandler:
    """Test cases for ChatHandler class"""
    
    def test_init_with_valid_api_key(self):
        """Test ChatHandler initialization with valid API key"""
        handler = ChatHandler("test_api_key")
        assert handler.model == "gpt-3.5-turbo"  # default model
        assert handler.system_prompt is not None
    
    @patch.dict(os.environ, {"OPENAI_MODEL": "gpt-4"})
    def test_init_with_custom_model(self):
        """Test ChatHandler initialization with custom model"""
        handler = ChatHandler("test_api_key")
        assert handler.model == "gpt-4"
    
    def test_system_prompt_content(self):
        """Test that system prompt contains business-related context"""
        handler = ChatHandler("test_api_key")
        system_prompt = handler._get_system_prompt()
        
        # Check for key business terms
        business_terms = [
            "business consultant",
            "strategic analysis",
            "market analysis",
            "financial planning"
        ]
        
        for term in business_terms:
            assert term.lower() in system_prompt.lower()

class TestUtils:
    """Test cases for utility functions"""
    
    def test_validate_environment_with_api_key(self):
        """Test environment validation with API key set"""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}):
            validation = validate_environment()
            assert validation["OPENAI_API_KEY"] is True
    
    def test_validate_environment_without_api_key(self):
        """Test environment validation without API key"""
        with patch.dict(os.environ, {}, clear=True):
            validation = validate_environment()
            assert validation["OPENAI_API_KEY"] is False
    
    def test_format_error_message_api_key(self):
        """Test error message formatting for API key errors"""
        message = format_error_message("api_key")
        assert "API Key Error" in message
        assert "OpenAI API key" in message
    
    def test_format_error_message_connection(self):
        """Test error message formatting for connection errors"""
        message = format_error_message("connection")
        assert "Connection Error" in message
        assert "internet connection" in message
    
    def test_format_error_message_general(self):
        """Test error message formatting for general errors"""
        test_details = "Custom error details"
        message = format_error_message("general", test_details)
        assert test_details in message

class TestIntegration:
    """Integration tests"""
    
    @patch('openai.OpenAI')
    def test_chat_handler_response_flow(self, mock_openai):
        """Test the complete response flow of ChatHandler"""
        # Mock OpenAI response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test response"
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        handler = ChatHandler("test_api_key")
        messages = [{"role": "user", "content": "Test question"}]
        
        response = handler.get_response(messages)
        assert response == "Test response"
        
        # Verify API was called with correct parameters
        mock_client.chat.completions.create.assert_called_once()
        call_args = mock_client.chat.completions.create.call_args
        assert call_args[1]["model"] == "gpt-3.5-turbo"
        assert len(call_args[1]["messages"]) >= 1  # Should include system prompt

if __name__ == "__main__":
    pytest.main([__file__])
