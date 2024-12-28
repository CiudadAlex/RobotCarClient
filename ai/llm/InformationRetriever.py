
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import LlamaCpp


class InformationRetriever:

    def __init__(self, model_llama_ccp_path):

        # Callbacks support token-wise streaming
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

        # Make sure the model path is correct for your system!
        self.llm = LlamaCpp(
            model_path=model_llama_ccp_path,
            temperature=0.75,
            max_tokens=2000,
            top_p=1,
            callback_manager=callback_manager,
            verbose=True,  # Verbose is required to pass to the callback manager
            n_ctx=2048
        )

    def get_answer(self, question):
        return self.llm(question)

