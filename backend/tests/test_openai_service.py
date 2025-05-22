import pytest
import json
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to sys.path to allow importing modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.openai_service import generate_course_with_ai, extract_json_from_text

# Sample test data
SAMPLE_RESPONSE = {
    "title": "Test Course",
    "objective": "Learn how to test",
    "prerequisites": ["Basic programming knowledge"],
    "definitions": ["Testing: A process to evaluate..."],
    "roadmap": {"Week 1": ["Introduction", "Setup"]},
    "modules": [
        {
            "title": "Module 1",
            "steps": ["Step 1", "Step 2"],
            "example": "Example code"
        }
    ],
    "resources": ["Resource 1", "Resource 2"],
    "faqs": ["Q: Question? A: Answer"],
    "errors": ["Error 1: Solution"],
    "downloads": ["Download 1"],
    "summary": "This is a test course about testing"
}

@pytest.mark.asyncio
async def test_extract_json_from_text():
    """Test extracting JSON from different text formats"""
    # Test clean JSON
    clean_json = json.dumps(SAMPLE_RESPONSE)
    result = extract_json_from_text(clean_json)
    assert result is not None
    assert json.loads(result)["title"] == "Test Course"
    
    # Test JSON with markdown code block
    markdown_json = f"```json\n{json.dumps(SAMPLE_RESPONSE)}\n```"
    result = extract_json_from_text(markdown_json)
    assert result is not None
    assert json.loads(result)["title"] == "Test Course"
    
    # Test JSON with text before and after
    text_with_json = f"Here is the JSON:\n{json.dumps(SAMPLE_RESPONSE)}\nEnd of JSON"
    result = extract_json_from_text(text_with_json)
    assert result is not None
    assert json.loads(result)["title"] == "Test Course"

@pytest.mark.asyncio
@patch('services.openai_service.client')
async def test_generate_course_with_ai(mock_client):
    """Test the generate_course_with_ai function with a mocked OpenAI client"""
    # Mock the OpenAI API response
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = json.dumps(SAMPLE_RESPONSE)
    
    # Configure the mock client to return our mock response
    mock_client.chat.completions.create.return_value = mock_response
    
    # Call the function with test parameters
    result = await generate_course_with_ai(
        topic="Test Topic",
        experience_level="beginner",
        available_time="2 weeks"
    )
    
    # Assert that the client was called with expected parameters
    mock_client.chat.completions.create.assert_called_once()
    call_args = mock_client.chat.completions.create.call_args[1]
    assert call_args["model"] == "gpt-3.5-turbo"
    assert len(call_args["messages"]) == 2
    assert "Test Topic" in call_args["messages"][1]["content"]
    
    # Assert the result matches our expected test data
    assert result["title"] == SAMPLE_RESPONSE["title"]
    assert result["objective"] == SAMPLE_RESPONSE["objective"]
    assert len(result["modules"]) == len(SAMPLE_RESPONSE["modules"])

@pytest.mark.asyncio
@patch('services.openai_service.client')
async def test_generate_course_with_ai_error_handling(mock_client):
    """Test error handling in generate_course_with_ai function"""
    # Configure the mock client to raise an exception
    mock_client.chat.completions.create.side_effect = Exception("API error")
    
    # Call the function with test parameters
    result = await generate_course_with_ai(
        topic="Test Topic",
        experience_level="beginner",
        available_time="2 weeks"
    )
    
    # Assert that we get a valid fallback response
    assert "title" in result
    assert "Test Topic" in result["title"]
    assert "modules" in result
    assert "errors" in result
    assert any("error" in error.lower() for error in result["errors"]) 