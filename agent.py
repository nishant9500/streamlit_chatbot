from google import genai
from google.genai.types import GenerateContentConfig

class GeminiAgent:
    def __init__(self, project_id, location="us-central1", model_id="gemini-2.0-flash-001"):
        self.project_id = project_id
        self.location = location
        self.model_id = model_id
        self.client = genai.Client(vertexai=True, project=project_id, location=location)

    def get_response(self, conversation_history):
        """
        conversation_history: list of dicts [{"role": "user"/"assistant", "content": "..."}]
        Returns: model's text reply
        """
        # Build the conversation string
        conversation_text = [
            f"{m['role'].capitalize()}: {m['content']}"
            for m in conversation_history
        ]
        prompt = "\n".join(conversation_text) + "\nAssistant:"

        # Send to Gemini
        config = GenerateContentConfig()
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config=config
        )
        return response.text
