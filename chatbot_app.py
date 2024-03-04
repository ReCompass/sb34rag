from dotenv import load_dotenv
from langchain.callbacks.base import BaseCallbackManager as CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT, QA_PROMPT
from langchain.chains.llm import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import ChatOpenAI, OpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()
vector_store = PineconeVectorStore(index_name="starter-index", embedding=OpenAIEmbeddings())
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

# the non-streaming LLM for questions
question_generator = LLMChain(llm=llm, prompt=CONDENSE_QUESTION_PROMPT)

# astreaming llm for the docs
streaming_llm = OpenAI(
    streaming=True, callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]), verbose=True, temperature=0
)
doc_chain = load_qa_chain(streaming_llm, chain_type="stuff", prompt=QA_PROMPT)

# initialize ConversationalRetrievalChain chabot
qa = ConversationalRetrievalChain(
    retriever=vector_store.as_retriever(), combine_docs_chain=doc_chain, question_generator=question_generator
)


# create an array to store the chat history.
chat_history = []
question = input(
    """Hello!
I'm a RAG agent here to answer your questions about compassionate cannabis in California. 🥦 ✨

How can I help you today?
"""
)

# create a loop to ask the chatbot questions
while True:
    result = qa.invoke({"question": question, "chat_history": chat_history})
    print("\n")
    chat_history.append((result["question"], result["answer"]))
    question = input()
