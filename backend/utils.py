from langchain_community.llms import Ollama, HuggingFaceEndpoint
from langchain.chains import LLMChain, ConversationChain
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableLambda
from langchain import HuggingFaceHub
from langchain.memory import ConversationBufferMemory
import re
import os


#####################################################################################################


# class Chatbot:
#     def __init__(self, model_name):
#         # Initialize the Ollama model
#         self.llm = Ollama(model=model_name)  # Use the updated Ollama class
#
#         # Initialize memory (it will store the conversation history)
#         self.memory = ConversationBufferMemory(return_messages = False)
#
#         # Define the prompt without memory in the template
#         self.prompt = ChatPromptTemplate.from_messages([
#             ("system", "You are a helpful AI chatbot. Answer questions conversationally."),
#             ("human", "{query}"),
#             ("ai", "{history}")
#         ])
#
#         # Initialize the LLM chain with memory
#         self.chain = LLMChain(llm=self.llm, prompt=self.prompt, memory=self.memory)
#
#     def get_response(self, query):
#         # Retrieve the current conversation history from memory
#         memory_data = self.memory.load_memory_variables({})["history"]
#
#         # Get the response using the chain, which includes the conversation history
#         response = self.chain.invoke({"query": query})
#
#         # If response is a dict, extract the relevant text field
#         if isinstance(response, dict) and "text" in response:
#             response = response["text"]
#
#         # Clean up unwanted tags like "<think>...</think>"
#         response = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()
#
#         # Return the cleaned response
#         return response




# Chatbot when we are accessing the model from Ollama

class Chatbot:
    def __init__(self, model_name):
        # Initialize the Ollama model
        self.llm = Ollama(model=model_name)

        # Initialize memory (stores conversation history)
        self.memory = ConversationBufferMemory(return_messages=False)

        # Initialize the conversation chain with memory
        self.chain = ConversationChain(llm=self.llm, memory=self.memory)

    def get_response(self, query):
        # Retrieve response while maintaining conversation history
        response = self.chain.invoke({"input": query})

        # If response is a dict, extract the relevant text field
        if isinstance(response, dict) and "response" in response:
            response = response["response"]

        # Clean up unwanted tags like "<think>...</think>"
        responses = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()

        # Return the cleaned response
        return responses




# Chatbot when we are accessing the model from Huggingface

from huggingface_hub import login
login("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")

# Set your Hugging Face API token
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

class AIChatbot:
    def __init__(self, model_name):
        # Initialize Hugging Face LLM via Inference API
        self.llm = HuggingFaceHub(
            repo_id=model_name,
            huggingfacehub_api_token=os.environ["HUGGINGFACEHUB_API_TOKEN"],
            model_kwargs={"temperature": 0.7, "max_length": 200}
        )

        # Initialize memory to remember previous conversation (K=10 messages)
        self.memory = ConversationBufferMemory(return_messages=False)

        # Initialize conversation chain with memory
        self.chain = ConversationChain(llm=self.llm, memory=self.memory)

    def get_response(self, query):
        # Get response while maintaining conversation history
        response = self.chain.invoke({"input": query})


        if isinstance(response, dict) and "response" in response:
            response = response["response"]

        # Clean up unwanted tags like "<think>...</think>"
        response = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()

        return response

# Initialize chatbot with the desired model (for example, DeepSeek-R1)
chatbot = AIChatbot(model_name="deepseek-ai/DeepSeek-R1")

# Example usage
print(chatbot.get_response("What is the capital of America?"))



