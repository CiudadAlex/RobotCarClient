from utils.PropertiesReader import PropertiesReader
from ai.llm.InformationRetriever import InformationRetriever
from ai.llm.LLMContexts import LLMContexts


class ChatLLM:

    instance = None

    @staticmethod
    def get_instance():

        if ChatLLM.instance is None:
            ChatLLM.instance = ChatLLM()

        return ChatLLM.instance

    def __init__(self):
        self.properties_reader = PropertiesReader.get_instance()
        self.information_retriever = InformationRetriever(self.properties_reader.model_llama_ccp_path)

    def start(self):

        while True:
            question = input("Ask a question: ")
            answer = self.information_retriever.get_answer(question, context=LLMContexts.RUDE)
            print(f"\n{answer}\n")


ChatLLM.get_instance().start()

