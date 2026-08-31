from langchain_mistralai import ChatMistralAI

from app.core.config import settings


class LLMService:
    def __init__(self):
        self.llm = ChatMistralAI(
            model="mistral-small-latest",
            api_key=settings.mistral_api_key
        )
    async def generate(
            self,
            query: str,
            context: str
    ) -> str:
        prompt = f"""
        Answer the question using only the provided context.

        Context:
        {context}

        Question:
        {query}
        """
        response = await self.llm.ainvoke(prompt)
        return response.content
