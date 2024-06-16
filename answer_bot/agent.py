import os
import sys
from typing import Any, Dict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

from langchain_core.language_models.llms import LLM

from answer_bot.llama import LLAMA_LLM

PROMPT_TEMPLATE = """
You are a friendly helpful AI assistant. You are polite, respectful, and aim to provide precise responses.

The conversation transcript is as follows:
{history}

Q: {input}. A:
"""

PROMPT = PromptTemplate(input_variables=["history", "input"], template=PROMPT_TEMPLATE)


class CustomLLM(LLM):
    def _call(
        self,
        prompt: str,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        """Run the LLM on the given input.

        Override this method to implement the LLM logic.

        Args:
            prompt: The prompt to generate from.
            *args: The arguments to pass to the LLM logic.
            **kwargs: Arbitrary additional keyword arguments. These are usually passed
                to the model provider API call.

        Returns:
            The model output as a string. Actual completions SHOULD NOT include the prompt.
        """
        print(f"Inside call, prompt is: {prompt}")
        output = LLAMA_LLM(
            prompt,
            max_tokens=1024,
            stop=["Q:"],
            # stop=["Q:", "\n", "A:", ":"],
            echo=False,
        )
        return output["choices"][0]["text"].strip()

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Return a dictionary of identifying parameters."""
        return {
            "model_name": "CustomChatLLAMA",
        }

    @property
    def _llm_type(self) -> str:
        """Get the type of language model used by this chat model. Used for logging purposes only."""
        return "custom_llama"


chain = ConversationChain(
    llm=CustomLLM(),
    prompt=PROMPT,
    verbose=False,
    memory=ConversationBufferMemory(ai_prefix="A:"),
)

if __name__ == "__main__":
    ans = chain.predict(input="What is your favorite programming language?")
    print(ans)
