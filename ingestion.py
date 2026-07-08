import asyncio
import os

from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from langchain_docling.loader import DoclingLoader
from sympy import false
from tavily import TavilyClient
from langchain_tavily import TavilyMap, TavilyCrawl, tavily_extract
from typing import List, Dict, Any
import certifi



load_dotenv()

embeddig = OpenAIEmbeddings(model="text-embedding-3-small", chunk_size=50, retry_min_seconds=10)

vector_store = PineconeVectorStore(index_name=os.getenv("PINECONE_INDEX_NAME"), embedding=embeddig)
tavily_map= TavilyMap(max_depth=5, max_breadth=20, max_pages=1000)
tavily_crawl= TavilyCrawl()


async def index_documents_async(documents: List[Document], batch_size:int =50):
    batches = [
        documents[i: i+batch_size] for i in range(0, len(documents), batch_size)
    ]

    async def add_batch(batch:List[Document], batch_num:int):
        try:
            await vector_store.aadd_documents(batch)

        except Exception as e:
            return False
        return True

    tasks = [add_batch(batch, i+1) for i, batch in enumerate(batches)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    successful = sum(1 for result in results if result is True)

    if(successful==len(batches)):
        print("All the batches are sucessfully inserted to VectorDB")
    else:
        print(f"Failed to insert {len(batches)-successful} batches to VectorDB ")






async def main():

    # Crawl documentation site
    res=tavily_crawl.invoke({
        "url":"https://python.langchain.com/",
        "max_depth":5,
        "extract_depth":"advanced",
        "instructions":"content on ai agents"
    })

    all_docs = [Document(page_content=result["raw_content"] , metadata={"source": result['url']}) for result in res["results"]]

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(all_docs)

    await index_documents_async(chunks, batch_size=500)

    



if __name__=="__main__":
    asyncio.run(main())