import os
import typing
from typing import Dict, Any
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.messages import ToolMessage
from langchain.tools import tool
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from sqlalchemy.ext.asyncio import result

load_dotenv()

embedding = OpenAIEmbeddings(model="text-embedding-3-small")
vector_store= PineconeVectorStore(index_name=os.getenv("PINECONE_INDEX_NAME"), embedding=embedding)

model = init_chat_model(model="gpt-4o", model_provider="openai")

@tool(response_format="content_and_artifact")
def retrieve_content(query:str):
    """Retrieve relavent documentation to help answer user queries about langchain agents"""
    retrived_documents = vector_store.as_retriever().invoke(query, k=4)

    serialized = "\n\n".join(
        (f"Source: {doc.metadata.get('source', 'Unknown')}\n\nContent:{doc.page_content}")
        for doc in retrived_documents
    )

    return serialized, retrived_documents


def run_llm(query:str)->Dict[str, Any]:
    """
    Run the RAG pipeline to answer a query using retrieved documentation
    Args:
        query: The user's question
    Returns:
        Dictionary containing:
            - answer: The generated answer
            - context: List of retrived documents
    """
    system_prompt =(
        "You are an helpful AI assistant that answers questions about Langchain documentation."
        "You have access to a tool that retrieved relevant documentation."
        "Use the tool to find relevant information before answering the questions."
        "Always cite the source you use in your answers."
        "If you cannot find the answer in the retrieved documentation, say no."
    )

    agent = create_agent(model, tools=[retrieve_content],system_prompt=system_prompt)
    messages= [{"role":"user", "content":query}]
    responses=agent.invoke({"messages":messages})
    answer = responses["messages"][-1].content

    context_docs=[]

    for message in responses["messages"]:
        if isinstance(message, ToolMessage) and hasattr(message, "artifact"):
            if isinstance(message.artifact, list):
                context_docs.extend(message.artifact)

    return {
        "answer": answer,
        "context": context_docs
    }

if __name__=="__main__":
    result=run_llm("what are deep agents")
    print(result)