from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from langchain_core.messages import AIMessage

from unit_tests.code_to_test import llm_node

"""
@patch("unit_tests.code_to_test.create_llm"): so now, instead of create_llm() the mock_create_llm() will be run .  

@pytest.mark.asyncio: This marks the test as asynchronous, allowing pytest to properly handle the async/await syntax.
"""

"""
The function takes two parameters:

mock_create_llm: The mocked version of the create_llm function
state: This comes from a pytest fixture defined in conftest.py, providing a standard test state
"""

"""
read the test method mockings backward to understand better, 
meaning, first the llm_model will be called, 
then, mock_create_llm will be called instead of create_llm
then it will return what? we mock it ...
like this ...
"""
@patch("unit_tests.code_to_test.create_llm")
@pytest.mark.asyncio
async def test_llm_node(mock_create_llm, state):
    """
    This creates a chain of mocks:

    mock_llm: A mock for the LLM model
    mock_response: A mock for the response from the LLM

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



    # saying mock_response will have a content property. 
    mock_response.content = "Mocked AI response"

    # saying mock_llm will have an method aiinvoke and will have a return value mock_response
    mock_llm.ainvoke.return_value = mock_response

    # saying that mock_llm will have a return value: mock_llm 
    mock_create_llm.return_value = mock_llm

    

    """ fake creating messages property, explained below. """
    mock_prompt = MagicMock()

    """
    saying mock_prompt will have a message property 
    as it will be accessed in the llm_node() .
    """
    mock_prompt.messages = state["messages"]

    """
    Updating the fixture state: 
    the llm_node method runs with the fixture state as the parameter in test.
    not the actual state. so,
    when the llm_node method calls the state['prompt'] inside the aiinvoke, 
    then it will get the mcok_prompt, as we updated the state['prompt'] here.

    so that's why now, 
    await llm.ainvoke(state["prompt"].messages) 
    in the llm_node method, it will access .messages, 
    so we are fake creating a .messages property to the mock_prompt. 

    though theres a mistake: state['prompt'] actually is a str type
    but  await llm.ainvoke(state["prompt"].messages) accesses .messages 
    which will throw and error. 
    but in the test it will pass, as we are fake creating the .messages property. 
    just above.

    """
    state["prompt"] = mock_prompt

    # calling the actual method with the fixture state. 
    updated_state = await llm_node(state)

    # now checking the response is matching with what should be the output of the actual llm_node() method.
    # with our fake data.
    assert updated_state["answer"] == "Mocked AI response"
    assert updated_state["messages"][-1] == AIMessage(content="Mocked AI response")


    # making sure these were called only once. 
    mock_llm.ainvoke.assert_called_once_with(state["messages"])
    mock_create_llm.assert_called_once()
