import functools
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, ToolMessage
from chat.ai_tools import get_tool_status

proxima_agent_prompt = """
    You are Proxima, an advanced assistant developed by Madhu. Your primary function is to answer user queries with accuracy, utilizing any necessary tools based on the user’s request. Current chat ID is: {} (Useful for context retrieval from attached document).
    
    Assess each query to determine if external information is required, then retrieve relevant content via available tools and seamlessly integrate it into your response to provide a comprehensive and precise answer to the user.
"""


async def get_proxima_agent(llm, tools, chat_id):
    """Proxima Agent, a custom agent"""
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", proxima_agent_prompt.format(chat_id)),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    return prompt | llm.bind_tools(tools)

async def create_proxima_agent_node(state, proxima_agent):
    consumer = state['consumer']
    await consumer.send_source_status("Thinking ...")
    result = await proxima_agent.ainvoke(state)
    if isinstance(result, ToolMessage):
        pass
    else:
        result = AIMessage(**result.dict(exclude={"type", "name"}), name='Proxima')
    return {
        "messages": [result],
    }

async def get_proxima_agent_node(proxima_agent):
    return functools.partial(create_proxima_agent_node, proxima_agent=proxima_agent)

async def get_source_name_from_message(message):
    tool_slug = message.tool_calls[0]['name']
    return get_tool_status(tool_slug)