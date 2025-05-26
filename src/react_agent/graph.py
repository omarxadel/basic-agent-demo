"""Define a custom Reasoning and Action agent.

Works with a chat model with tool calling support.
"""

from datetime import UTC, datetime
from typing import Dict, List, Literal, cast

from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode

from react_agent.configuration import Configuration
from react_agent.state import InputState, State
from react_agent.tools import TOOLS
from react_agent.utils import load_chat_model

# Define the function that calls the model


async def call_model(state: State) -> Dict[str, List[AIMessage]]:
    """Call the LLM powering our "agent".

    This function prepares the prompt, initializes the model, and processes the response.

    Args:
        state (State): The current state of the conversation.
        config (RunnableConfig): Configuration for the model run.

    Returns:
        dict: A dictionary containing the model's response message.
    """
    configuration = Configuration.from_context()

    # Initialize the model with tool binding. Change the model or add more tools here.
    model = load_chat_model(configuration.model).bind_tools(TOOLS)

    # Format the system prompt. Customize this to change the agent's behavior.
    system_message = configuration.system_prompt.format(
        system_time=datetime.now(tz=UTC).isoformat()
    )

    # Get the model's response
    response = cast(
        AIMessage,
        await model.ainvoke(
            [{"role": "system", "content": system_message}, *state.messages]
        ),
    )

    # Handle the case when it's the last step and the model still wants to use a tool
    if state.is_last_step and response.tool_calls:
        return {
            "messages": [
                AIMessage(
                    id=response.id,
                    content="Sorry, I could not find an answer to your question in the specified number of steps.",
                )
            ]
        }

    # Return the model's response as a list to be added to existing messages
    return {"messages": [response]}


async def thinking(state: State) -> Dict[str, List[AIMessage]]:
    """Allow the agent to think about the current state and plan next actions.
    
    Args:
        state (State): The current state of the conversation.
        
    Returns:
        dict: A dictionary containing the thinking message.
    """
    configuration = Configuration.from_context()
    model = load_chat_model(configuration.model)
    
    thinking_prompt = "Let's think about what we know and what we need to do next. Consider:\n"
    thinking_prompt += "1. What information do we have?\n"
    thinking_prompt += "2. What are we trying to achieve?\n"
    thinking_prompt += "3. What tools might help us?\n"
    thinking_prompt += "4. What are potential challenges?\n"
    
    response = cast(
        AIMessage,
        await model.ainvoke(
            [
                {"role": "system", "content": "You are a thoughtful assistant that helps plan next steps."},
                *state.messages,
                HumanMessage(content=thinking_prompt)
            ]
        ),
    )
    
    return {"messages": [response]}


async def thought(state: State) -> Dict[str, List[AIMessage]]:
    """Process the thinking results and decide on next actions.
    
    Args:
        state (State): The current state of the conversation.
        
    Returns:
        dict: A dictionary containing the thought message.
    """
    configuration = Configuration.from_context()
    model = load_chat_model(configuration.model)
    
    thought_prompt = "Based on our thinking, let's decide what to do next:\n"
    thought_prompt += "1. What specific action should we take?\n"
    thought_prompt += "2. Why is this the best course of action?\n"
    thought_prompt += "3. What do we expect to learn?\n"
    
    response = cast(
        AIMessage,
        await model.ainvoke(
            [
                {"role": "system", "content": "You are a decisive assistant that helps choose the best next action."},
                *state.messages,
                HumanMessage(content=thought_prompt)
            ]
        ),
    )
    
    return {"messages": [response]}


async def observation(state: State) -> Dict[str, List[AIMessage]]:
    """Process and analyze the results of tool executions.
    
    Args:
        state (State): The current state of the conversation.
        
    Returns:
        dict: A dictionary containing the observation message.
    """
    configuration = Configuration.from_context()
    model = load_chat_model(configuration.model)
    
    observation_prompt = "Let's analyze what we learned from our last action:\n"
    observation_prompt += "1. What new information did we get?\n"
    observation_prompt += "2. How does this affect our understanding?\n"
    observation_prompt += "3. What should we do with this information?\n"
    
    response = cast(
        AIMessage,
        await model.ainvoke(
            [
                {"role": "system", "content": "You are an observant assistant that helps analyze results."},
                *state.messages,
                HumanMessage(content=observation_prompt)
            ]
        ),
    )
    
    return {"messages": [response]}


# Define a new graph

builder = StateGraph(State, input=InputState, config_schema=Configuration)

# Define the nodes we will cycle between
builder.add_node("call_model", call_model)
builder.add_node("thinking", thinking)
builder.add_node("thought", thought)
builder.add_node("observation", observation)
builder.add_node("tools", ToolNode(TOOLS))

# Set the entrypoint as `thinking`
builder.add_edge("__start__", "thinking")

def route_thinking(state: State) -> Literal["thought", "__end__"]:
    """Route after thinking phase."""
    if state.is_last_step:
        return "__end__"
    return "thought"

def route_thought(state: State) -> Literal["call_model", "__end__"]:
    """Route after thought phase."""
    if state.is_last_step:
        return "__end__"
    return "call_model"

def route_model_output(state: State) -> Literal["__end__", "tools"]:
    """Determine the next node based on the model's output.

    This function checks if the model's last message contains tool calls.

    Args:
        state (State): The current state of the conversation.

    Returns:
        str: The name of the next node to call ("__end__" or "tools").
    """
    last_message = state.messages[-1]
    if not isinstance(last_message, AIMessage):
        raise ValueError(
            f"Expected AIMessage in output edges, but got {type(last_message).__name__}"
        )
    # If there is no tool call, then we finish
    if not last_message.tool_calls:
        return "__end__"
    # Otherwise we execute the requested actions
    return "tools"

def route_tools(state: State) -> Literal["observation", "__end__"]:
    """Route after tools execution."""
    if state.is_last_step:
        return "__end__"
    return "observation"

def route_observation(state: State) -> Literal["thinking", "__end__"]:
    """Route after observation phase."""
    if state.is_last_step:
        return "__end__"
    return "thinking"

# Add conditional edges
builder.add_conditional_edges("thinking", route_thinking)
builder.add_conditional_edges("thought", route_thought)
builder.add_conditional_edges("call_model", route_model_output)
builder.add_conditional_edges("tools", route_tools)
builder.add_conditional_edges("observation", route_observation)

# Compile the builder into an executable graph
graph = builder.compile(name="ReAct Agent")
