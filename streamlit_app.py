import streamlit as st
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import RetrievalQA

# Streamlit page configuration
st.set_page_config(
    page_title="ITC Sustainability Q&A",
    page_icon="🌱",
    layout="wide"
)

# Title and description
st.title("🌿 ITC Sustainability Q&A App")
st.markdown("""
Ask questions about ITC's sustainability efforts in 2024. 
This app uses a pre-loaded Chroma vector store and Google's Gemini model to provide accurate answers.
""")

# Initialize API key from Streamlit secrets
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except KeyError:
    st.error("Google API key not found in Streamlit secrets. Please add 'GOOGLE_API_KEY' in the Space's secrets settings.")
    st.stop()

# Initialize embeddings
try:
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=API_KEY
    )
except Exception as e:
    st.error(f"Failed to initialize embeddings: {str(e)}")
    st.stop()

# Load Chroma vector store
@st.cache_resource
def load_vector_store():
    try:
        return Chroma(
            persist_directory='./chroma_db',  # Path to chroma_db directory in Hugging Face Space
            embedding_function=embeddings
        )
    except Exception as e:
        st.error(f"Failed to load Chroma vector store: {str(e)}")
        st.write("Ensure the 'chroma_db' directory contains all necessary files (chroma.sqlite3, data_level0.bin, etc.).")
        st.stop()

vector_store = load_vector_store()

# Initialize retriever
retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 3, "lambda_mult": 1}
)

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    api_key=API_KEY,
    model="gemini-2.0-flash-exp"
)

# Initialize QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)

# Query input
query = st.text_input(
    "Enter your question about ITC's sustainability efforts in 2024:",
    placeholder="E.g., Summarize ITC's sustainability efforts in 2024"
)

# Process query and display results
if query:
    with st.spinner("Generating response..."):
        try:
            response = qa_chain({"query": query})
            
            # Display answer
            st.subheader("Answer")
            st.write(response["result"])
            
            # Display sources
            st.subheader("Sources")
            if response["source_documents"]:
                for doc in response["source_documents"]:
                    with st.expander("Source Document"):
                        st.write(f"**Metadata**: {doc.metadata}")
                        st.write(f"**Content Preview**: {doc.page_content[:200]}...")
            else:
                st.write("No source documents found.")
                
        except Exception as e:
            st.error(f"An error occurred while processing the query: {str(e)}")
            st.write("Please try again or check the Chroma database and API key.")

# Sidebar with additional information
with st.sidebar:
    st.header("About")
    st.markdown("""
    This app is built using:
    - **Streamlit** for the web interface
    - **LangChain** for retrieval-augmented generation
    - **Google Gemini** for language modeling
    - **Chroma** for vector storage
    
    The Chroma database is located in the `chroma_db` directory at the root of this Space.
    It includes files like `chroma.sqlite3`, `data_level0.bin`, and others required for vector storage.
    
    The Google API key is securely accessed via Streamlit secrets.
    """)
    
    st.header("Instructions")
    st.markdown("""
    1. Enter a question about ITC's sustainability efforts in 2024.
    2. Wait for the app to process and display the answer.
    3. Check the sources for document metadata and content previews.
    """)

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit | Powered by xAI")