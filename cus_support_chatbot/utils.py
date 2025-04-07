from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableLambda
from langgraph.prebuilt.tool_node import ToolNode

# 'state' is the LangGraph state that holds current conversation context — includes:
    # messages: a list of messages (like user input, assistant output, tool calls, etc.)
    # error: an error raised by a tool

def handle_tool_error(state) -> dict:
    """
    If the llm makes a mistake, we pass a prompt with the error back to the llm for every tool call.

    Parameters:
    state: 'state' is the LangGraph state that holds current conversation context. 
    It is a dictionary with two keys: "message" and "error"
    """
    error = state.get("error")
    tool_calls = state["messages"][-1].tool_calls
    
    return {
        "messages": [
            ToolMessage(
                content=f"Error: {repr(error)}\n please fix your mistakes.",
                tool_call_id=tc["id"],
            )
            for tc in tool_calls
        ]
    }


def create_tool_node_with_fallback(tools: list) -> dict:
    """
    If tool call fails:
        The error is added to state as "error".
        LangGraph runs handle_tool_error(state) to build a ToolMessage.
    """
    return ToolNode(tools).with_fallbacks(
        [RunnableLambda(handle_tool_error)], exception_key="error"
    )


def _print_event(event: dict, _printed: set, max_length=1500):
    """
    Used by langgraph for debugging
    """
    current_state = event.get("dialog_state")
    if current_state:
        print("Currently in: ", current_state[-1])
    message = event.get("messages")
    if message:
        if isinstance(message, list):
            message = message[-1]
        if message.id not in _printed:
            msg_repr = message.pretty_repr(html=True)
            if len(msg_repr) > max_length:
                msg_repr = msg_repr[:max_length] + " ... (truncated)"
            print(msg_repr)
            _printed.add(message.id)