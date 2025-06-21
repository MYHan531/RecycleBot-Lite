#!/usr/bin/env python3
"""
NEA Waste Management RAG System
Uses Ollama (Llama-3-8B-Instruct), LangChain, and FAISS for question answering
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any
import logging

# LangChain imports
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.llms import Ollama

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NEARAGSystem:
    def __init__(self, knowledge_base_path: str = "data/knowledge_base/snippets"):
        self.knowledge_base_path = Path(knowledge_base_path)
        self.vector_store = None
        self.qa_chain = None
        self.embeddings = None
        
        # Initialize components
        self._setup_embeddings()
        self._load_documents()
        self._create_vector_store()
        self._setup_qa_chain()
    
    def _setup_embeddings(self):
        """Setup HuggingFace embeddings"""
        logger.info("Setting up embeddings...")
        try:
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
            logger.info("✅ Embeddings loaded successfully")
        except Exception as e:
            logger.error(f"❌ Error loading embeddings: {e}")
            raise
    
    def _load_documents(self):
        """Load documents from knowledge base"""
        logger.info("Loading documents from knowledge base...")
        
        if not self.knowledge_base_path.exists():
            raise FileNotFoundError(f"Knowledge base path not found: {self.knowledge_base_path}")
        
        try:
            # Load all markdown files
            loader = DirectoryLoader(
                str(self.knowledge_base_path),
                glob="**/*.md",
                loader_cls=TextLoader,
                loader_kwargs={'encoding': 'utf-8'}
            )
            
            documents = loader.load()
            logger.info(f"✅ Loaded {len(documents)} documents")
            
            # Split documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len,
                separators=["\n\n", "\n", " ", ""]
            )
            
            self.documents = text_splitter.split_documents(documents)
            logger.info(f"✅ Split into {len(self.documents)} chunks")
            
        except Exception as e:
            logger.error(f"❌ Error loading documents: {e}")
            raise
    
    def _create_vector_store(self):
        """Create FAISS vector store"""
        logger.info("Creating FAISS vector store...")
        
        try:
            # Create vector store
            self.vector_store = FAISS.from_documents(
                self.documents,
                self.embeddings
            )
            
            # Save vector store
            vector_store_path = "data/vector_store"
            os.makedirs(vector_store_path, exist_ok=True)
            self.vector_store.save_local(vector_store_path)
            
            logger.info(f"✅ Vector store created and saved to {vector_store_path}")
            
        except Exception as e:
            logger.error(f"❌ Error creating vector store: {e}")
            raise
    
    def _setup_qa_chain(self):
        """Setup QA chain with Ollama"""
        logger.info("Setting up QA chain with Ollama...")
        
        try:
            # Initialize Ollama LLM
            llm = Ollama(
                model="llama3",
                temperature=0.1,
                top_p=0.9,
                repeat_penalty=1.1
            )
            
            # Setup memory
            memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True,
                output_key="answer"
            )
            
            # Create QA chain
            self.qa_chain = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=self.vector_store.as_retriever(
                    search_type="similarity",
                    search_kwargs={"k": 3}
                ),
                memory=memory,
                return_source_documents=True,
                verbose=True
            )
            
            logger.info("✅ QA chain setup complete")
            
        except Exception as e:
            logger.error(f"❌ Error setting up QA chain: {e}")
            logger.error("Make sure Ollama is running and llama3 model is pulled")
            raise
    
    def ask_question(self, question: str, chat_history: List = None) -> Dict[str, Any]:
        """Ask a question and get an answer"""
        if chat_history is None:
            chat_history = []
        
        try:
            logger.info(f"Question: {question}")
            
            # Get answer from QA chain
            result = self.qa_chain({"question": question, "chat_history": chat_history})
            
            answer = result.get("answer", "No answer generated")
            source_documents = result.get("source_documents", [])
            
            # Format response
            response = {
                "question": question,
                "answer": answer,
                "sources": [doc.metadata.get("source", "Unknown") for doc in source_documents],
                "chat_history": chat_history
            }
            
            logger.info(f"Answer: {answer[:100]}...")
            return response
            
        except Exception as e:
            logger.error(f"❌ Error getting answer: {e}")
            return {
                "question": question,
                "answer": f"Sorry, I encountered an error: {str(e)}",
                "sources": [],
                "chat_history": chat_history
            }
    
    def get_similar_documents(self, query: str, k: int = 3) -> List:
        """Get similar documents for a query"""
        try:
            docs = self.vector_store.similarity_search(query, k=k)
            return docs
        except Exception as e:
            logger.error(f"❌ Error getting similar documents: {e}")
            return []
    
    def list_available_documents(self) -> List[str]:
        """List all available documents in the knowledge base"""
        try:
            docs = self.vector_store.docstore._dict
            return list(docs.keys())
        except Exception as e:
            logger.error(f"❌ Error listing documents: {e}")
            return []

def test_ollama_connection():
    """Test if Ollama is running and accessible"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = response.json().get("models", [])
            logger.info(f"✅ Ollama is running. Available models: {[m['name'] for m in models]}")
            return True
        else:
            logger.error("❌ Ollama is not responding properly")
            return False
    except Exception as e:
        logger.error(f"❌ Cannot connect to Ollama: {e}")
        return False

def main():
    """Main function for testing the RAG system"""
    print("🚀 NEA Waste Management RAG System")
    print("=" * 50)
    
    # Test Ollama connection
    if not test_ollama_connection():
        print("\n❌ Ollama is not running or accessible.")
        print("Please ensure:")
        print("1. Ollama is installed and running")
        print("2. Llama-3 model is pulled: ollama pull llama3")
        print("3. Ollama service is started")
        return
    
    try:
        # Initialize RAG system
        print("\n📚 Initializing RAG system...")
        rag_system = NEARAGSystem()
        
        # Test questions
        test_questions = [
            "What is the current recycling rate in Singapore?",
            "Can I recycle styrofoam?",
            "How much waste was generated in 2023?",
            "What is the household recycling participation rate?",
            "What are the recycling rates for different materials?"
        ]
        
        print("\n🤖 Testing RAG system with sample questions...")
        print("=" * 50)
        
        for i, question in enumerate(test_questions, 1):
            print(f"\n{i}. Question: {question}")
            response = rag_system.ask_question(question)
            print(f"Answer: {response['answer']}")
            print(f"Sources: {response['sources']}")
            print("-" * 30)
        
        # Interactive mode
        print("\n💬 Interactive Mode - Ask questions (type 'quit' to exit)")
        print("=" * 50)
        
        chat_history = []
        while True:
            question = input("\nYour question: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                break
            
            if question:
                response = rag_system.ask_question(question, chat_history)
                print(f"\nAnswer: {response['answer']}")
                print(f"Sources: {response['sources']}")
                
                # Update chat history
                chat_history.append((question, response['answer']))
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure knowledge base exists: python generate_rag_kb.py")
        print("2. Check Ollama installation and model: ollama pull llama3")
        print("3. Verify all dependencies: pip install -r requirements.txt")

if __name__ == "__main__":
    main() 