import asyncio
import os

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from thirdweb_ai import Insight
from thirdweb_ai.adapters.google_adk.google_adk import get_google_adk_tools

# Example app configuration
APP_NAME = "thirdweb_insight_app"
USER_ID = "test_user"
SESSION_ID = "test_session"


async def setup_agent() -> Runner:
    """Set up an agent with Thirdweb Insight tools.

    Returns:
        Runner: Google ADK runner for the agent
    """
    # Initialize Insight with secret key
    secret_key = os.getenv("THIRDWEB_SECRET_KEY")
    if not secret_key:
        raise ValueError("THIRDWEB_SECRET_KEY environment variable is required")

    # Get Insight tools
    insight = Insight(secret_key=secret_key, chain_id=1)
    insight_tools = insight.get_tools()

    # Convert to Google ADK tools
    adk_tools = get_google_adk_tools(insight_tools)

    # Print all available tools for debugging
    print(f"Available tools ({len(adk_tools)}):")
    for tool_count, tool in enumerate(adk_tools, start=1):
        print(f"- Tool #{tool_count} {tool.name}")

    # Create the agent with the tools
    agent = LlmAgent(
        model=LiteLlm(model="gpt-4o-mini"),
        name="thirdweb_insight_agent",
        tools=adk_tools,
    )

    # Set up session
    session_service = InMemorySessionService()
    # We need to create the session but don't need to store it
    await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)

    # Return runner
    return Runner(agent=agent, app_name=APP_NAME, session_service=session_service)


async def call_agent(query: str) -> None:
    """Run a query through the agent.

    Args:
        query: The query to send to the agent
    """
    runner = await setup_agent()
    content = types.Content(role="user", parts=[types.Part(text=query)])
    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

    for event in events:
        if (
            event.is_final_response()
        ):
            final_response = event.content.parts[0].text
            print("Agent Response: ", final_response)


if __name__ == "__main__":
    test_query = "Find information on transaction: 0x45027cce9d2b990349b4a1e015ec29ca7c7ef15d82487d898f24866a09e8b84c."
    asyncio.run(call_agent(test_query))
