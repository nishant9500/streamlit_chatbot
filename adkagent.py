import requests
import json

class ADKAgent:
    """
    Wraps a deployed ADK agent so it can be called like a GeminiAgent.
    """
    def __init__(self, agent_endpoint_url, api_key=None):
        """
        agent_endpoint_url: URL of your deployed ADK agent
        api_key: optional, if your ADK agent requires authentication
        """
        self.agent_url = agent_endpoint_url
        self.api_key = api_key

    def get_response(self, conversation_history, memory_on=True):
        """
        conversation_history: list of dicts [{"role": "user"/"assistant", "content": "..."}]
        memory_on: if True, send full history; else, only last user message
        """
        if memory_on:
            payload = {
                "messages": conversation_history
            }
        else:
            # Only last user message
            last_user_msg = next((m['content'] for m in reversed(conversation_history) if m["role"]=="user"), "")
            payload = {"messages": [{"role": "user", "content": last_user_msg}]}

        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        response = requests.post(self.agent_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        data = response.json()
        # Assume the ADK agent returns {"reply": "..."}
        return data.get("reply", "Error: No reply received")
