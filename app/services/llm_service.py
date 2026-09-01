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
        You are a strict document question-answering assistant.

        Your task is to answer the question ONLY from the provided context.

        IMPORTANT RULES:
        1. Use only facts explicitly stated in the context.
        2. Do not make assumptions.
        3. Do not infer information from related facts.
        4. Do not guess the answer.
        5. If the context does not explicitly answer the question,
           respond exactly:
           "I don't have enough information in the provided documents."
        6. A fact that is related to the question is NOT necessarily an answer.
        7. If the question asks about a preference, opinion, favorite,
           intention, or personal choice, do not infer it from skills,
           experience, or usage.

        Example:
        Context: "He knows Python."
        Question: "What is his favorite programming language?"
        Answer: "I don't have enough information in the provided documents."

        Context:
        {context}

        Question:
        {query}

        Answer:
        """

        response = await self.llm.ainvoke(prompt)
        return response.content