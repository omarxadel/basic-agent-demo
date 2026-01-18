"""Define a custom Reasoning and Action agent.

Works with a chat model with tool calling support.
"""

from datetime import UTC, datetime
from typing import Dict, List, Literal, Optional, cast

from langchain_core.messages import AIMessage, BaseMessage, ToolMessage
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode

from react_agent.configuration import Configuration
from react_agent.state import InputState, State
from react_agent.tools import TOOLS
from react_agent.utils import load_chat_model

# Define the function that calls the model


def _collect_recent_tool_observations(messages: List[BaseMessage]) -> List[str]:
    observations: List[str] = []
    for message in reversed(messages):
        if isinstance(message, AIMessage):
            break
        if isinstance(message, ToolMessage):
            observations.append(str(message.content))
    observations.reverse()
    return observations


def _format_tool_calls(tool_calls: Optional[List[dict]]) -> str:
    if not tool_calls:
        return "none"
    rendered = []
    for call in tool_calls:
        name = call.get("name", "unknown")
        args = call.get("args", {})
        if isinstance(args, dict) and args:
            rendered.append(f"tool:{name} {args}")
        else:
            rendered.append(f"tool:{name}")
    return " | ".join(rendered)


def _ensure_structured_response(
    response: AIMessage, state_messages: List[BaseMessage]
) -> AIMessage:
    content = response.content if isinstance(response.content, str) else ""
    if "Thinking:" in content and "Action:" in content and "Observation:" in content and "Response:" in content:
        return response

    has_tool_calls = bool(response.tool_calls)
    observations = _collect_recent_tool_observations(state_messages)
    thinking = "Thinking:\n- Next step: " + (
        "call tool(s)" if has_tool_calls else "respond to the user"
    )
    action = "Action:\n- " + _format_tool_calls(response.tool_calls)
    if has_tool_calls:
        observation = "Observation:\n- pending"
        response_body = "Response:\n- Calling tool(s)."
    else:
        observation = "Observation:\n- " + (
            "; ".join(observations) if observations else "none"
        )
        response_body = f"Response:\n{content}" if content else "Response:\n- Done."
    response.content = "\n".join([thinking, action, observation, response_body])
    return response


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

    response = _ensure_structured_response(response, list(state.messages))

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


# Define a new graph

builder = StateGraph(State, input=InputState, config_schema=Configuration)

# Define the two nodes we will cycle between
builder.add_node(call_model)
builder.add_node("tools", ToolNode(TOOLS))

# Set the entrypoint as `call_model`
# This means that this node is the first one called
builder.add_edge("__start__", "call_model")


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


# Add a conditional edge to determine the next step after `call_model`
builder.add_conditional_edges(
    "call_model",
    # After call_model finishes running, the next node(s) are scheduled
    # based on the output from route_model_output
    route_model_output,
)

# Add a normal edge from `tools` to `call_model`
# This creates a cycle: after using tools, we always return to the model
builder.add_edge("tools", "call_model")

# Compile the builder into an executable graph
graph = builder.compile(name="ReAct Agent")
