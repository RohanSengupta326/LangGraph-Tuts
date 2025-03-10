from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from langchain_core.messages import AIMessage

from unit_tests.code_to_test import llm_node

"""
PyTest Basics
PyTest is a popular testing framework for Python that makes it easy to write simple and scalable test cases. Here are some key PyTest concepts used in this test:

Test Discovery: PyTest automatically finds test files that start with test_ or end with _test.py.
Fixtures: These are reusable pieces of test setup/data that can be used across multiple tests. In your code, the state parameter is a fixture defined in conftest.py.
Decorators: Those @ symbols before the function modify how the test works.
Assertions: The assert statements verify that your code behaves as expected.
Mocking: Replacing real objects with fake ones for testing purposes.
"""

"""
@patch: Replaces the real create_llm function with a mock. The mock is passed as the first parameter to the test function.
@pytest.mark.asyncio: Tells pytest that this is an asynchronous test.
state: This comes from a fixture defined in conftest.py:
"""
@patch("unit_tests.code_to_test.create_llm")
@pytest.mark.asyncio
async def test_llm_node(mock_create_llm, state):
    """
    This creates a chain of mocks:

    mock_llm: A mock for the LLM model
    mock_response: A mock for the response from the LLM

    When mock_llm.ainvoke() is called, it returns mock_response
    When create_llm() is called, it returns mock_llm

    Example: If the real code calls model = create_llm() and then response = await model.ainvoke(...), it will actually get our mock objects instead.
    """

    """
    1. AsyncMock() is a "Blank Canvas"
    When you create mock_llm = AsyncMock(), you're creating an empty mock object that can pretend to be anything. It has these special properties:

    It allows access to any attribute or method, even if they don't exist
    It records all interactions with it for later verification
    It's designed to work with async/await (that's why it's AsyncMock instead of just Mock)
    """
    mock_llm = AsyncMock()
    mock_response = AsyncMock()

    mock_response.content = "Mocked AI response"

    """
    You're not calling a pre-existing method. Instead:

    Accessing mock_llm.ainvoke automatically creates an attribute called "ainvoke" on your mock
    This new attribute is itself a mock object
    Setting .return_value tells this mock what to return when it's called
    """
    mock_llm.ainvoke.return_value = mock_response
    mock_create_llm.return_value = mock_llm

    """
    The following occurs:

    llm is actually our mock_llm
    The code calls .ainvoke() on it with some parameters
    The mock:

    Records this call (parameters, times called, etc.)
    Returns the configured mock_response object


    Since we're in an async function with await, AsyncMock makes sure this works properly
    """

    mock_prompt = MagicMock()
    mock_prompt.messages = state["messages"]
    state["prompt"] = mock_prompt

    updated_state = await llm_node(state)

    assert updated_state["answer"] == "Mocked AI response"
    assert updated_state["messages"][-1] == AIMessage(content="Mocked AI response")


    #making sure these were called only once. 
    mock_llm.ainvoke.assert_called_once_with(state["messages"])
    mock_create_llm.assert_called_once()
