import streamlit as st
import time
import json
import random
import requests 
import os # <-- NEW: Import the os module to access environment variables

# --- Gemini API Configuration ---

# !!! SECURITY UPDATE !!!
# API_KEY is now read from the environment variable named 'GEMINI_API_KEY'.
# You MUST set this variable when running the app locally or deploying it.
API_KEY = os.environ.get("GEMINI_API_KEY") # <-- KEY READ FROM ENVIRONMENT VARIABLE

# Check if the key is available
if not API_KEY:
    # Use a placeholder URL if the key is missing to prevent crash, 
    # but the API call will fail later with a clear error message.
    API_URL = "https://generativelanguage.googleapis.com/v1beta/models/missing_key:generateContent"
    
else:
    API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={API_KEY}"

# --- Constants and Prompts (rest of the file remains the same) ---
RAG_SYSTEM_PROMPT = """
You are a highly knowledgeable and adaptive chatbot. Your primary goal is to answer the user's question ONLY using the provided context (Internal Knowledge Base).
If the provided context does not contain the answer, state clearly that the information is not available in the current knowledge base.
Do not use any external knowledge. Maintain a concise and professional tone.
"""

# --- Data Simulation Functions ---

def load_or_initialize_db():
    """Initializes the mock vector database in Streamlit's session state."""
    if 'knowledge_base' not in st.session_state:
        # Initial 'stale' knowledge base content
        st.session_state.knowledge_base = [
            {"id": "doc_1", "text": "The latest fiscal report (Q1 2024) indicates that the company's primary focus remains on legacy software, with no new AI initiatives announced."},
            {"id": "doc_2", "text": "Project Phoenix is a secret initiative aimed at upgrading our internal server infrastructure by the end of Q3 2024."},
            {"id": "doc_3", "text": "All employees are required to complete the annual security training before October 31st."},
        ]
        st.session_state.is_initialized = True
        st.session_state.last_update = "Never (Initial Load)"
    return st.session_state.knowledge_base

def get_mock_new_data():
    """Simulates crawling new documents or articles from a source."""
    st.info("Simulating new data crawl from source...")
    time.sleep(1) # Simulate network delay

    # New information that explicitly contradicts or updates the old info
    new_data_source = [
        "In a surprising mid-quarter announcement, the CEO revealed a massive pivot. A new 'Project Aether' was launched in Q2 2024, focusing entirely on large language models and generative AI research.",
        "Due to the launch of Project Aether, Project Phoenix has been indefinitely postponed. The new deadline for the server upgrade is now Q1 2025.",
        "The new mandatory training, 'AI Ethics and Compliance,' replaces the old security training and must be completed by November 15th."
    ]
    return new_data_source

def update_knowledge_base():
    """Simulates the ETL pipeline: Crawl -> Chunk -> Embed -> Store."""
    new_data = get_mock_new_data()
    if not new_data:
        st.warning("No new data found during the crawl simulation.")
        return

    # 1. Chunking/Processing (Simulated)
    new_documents = []
    for i, chunk_text in enumerate(new_data):
        # 2. Embedding (Mocked) - In a real system, you'd call an embedding model here
        new_document = {
            "id": f"new_doc_{random.randint(1000, 9999)}",
            "text": chunk_text,
        }
        new_documents.append(new_document)

    # 3. Storing (Simulated - Replacing old data with new for simplicity)
    st.session_state.knowledge_base = new_documents
    st.session_state.last_update = time.strftime("%Y-%m-%d %H:%M:%S")

    st.success(f"Knowledge Base updated successfully with {len(new_documents)} new documents!")
    st.rerun()

# --- RAG Core Functions ---

def retrieve_context(query, knowledge_base):
    """
    Mocks the vector search/retrieval process using simple keyword matching.
    """
    relevant_chunks = []
    query_terms = query.lower().split()

    for doc in knowledge_base:
        doc_text_lower = doc['text'].lower()
        # Simple check for relevance
        if any(term in doc_text_lower for term in query_terms if len(term) > 3):
            relevant_chunks.append(doc['text'])
        # Also check for common concepts regardless of the query
        elif any(concept in doc_text_lower for concept in ["ai", "project", "training", "deadline"]):
             relevant_chunks.append(doc['text'])

    if not relevant_chunks:
        return "No relevant context found in the knowledge base."

    # Return the top 3 (or all) relevant chunks formatted for the LLM prompt
    context_text = "\n---\n".join(relevant_chunks[:3])
    return context_text

def generate_rag_response(query, context):
    """
    Calls the Gemini API with the retrieved context for grounded generation.
    """
    if not API_KEY:
        return "ERROR: Gemini API Key not found. Please set the 'GEMINI_API_KEY' environment variable."

    full_prompt = (
        f"Context from Internal Knowledge Base:\n{context}\n\n"
        f"User Question: {query}"
    )

    payload = {
        "contents": [{"parts": [{"text": full_prompt}]}],
        "systemInstruction": {"parts": [{"text": RAG_SYSTEM_PROMPT}]},
    }

    payload_json = json.dumps(payload)

    # Exponential backoff retry loop
    max_retries = 3
    delay = 1
    for attempt in range(max_retries):
        try:
            # Simulate a brief network delay
            time.sleep(0.1)

            response = requests.post(
                API_URL,
                headers={'Content-Type': 'application/json'},
                data=payload_json,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                candidate = result.get('candidates', [{}])[0]
                text = candidate.get('content', {}).get('parts', [{}])[0].get('text', 'Error: Could not extract text from API response.')
                return text

            elif response.status_code == 429:
                if attempt < max_retries - 1:
                    print(f"Rate limit hit. Retrying in {delay}s...")
                    time.sleep(delay)
                    delay *= 2
                    continue
                else:
                    return "Error: Rate limit exceeded and max retries failed."
            else:
                return f"Error: API call failed with status code {response.status_code}. Details: {response.text}"

        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                print(f"Request failed: {e}. Retrying in {delay}s...")
                time.sleep(delay)
                delay *= 2
                continue
            else:
                return f"Error: Failed to connect to API after multiple retries: {e}"

    return "An unexpected error occurred during API communication."

# --- Streamlit UI and Execution ---

def main():
    st.set_page_config(layout="wide", page_title="Dynamic RAG Chatbot")
    st.title("🧠 Dynamic Knowledge Base RAG Chatbot")
    st.markdown("Simulate automatic incorporation of new information by updating the internal knowledge base.")

    # Load/Init Knowledge Base
    kb = load_or_initialize_db()

    # --- Sidebar for Knowledge Management (The Dynamic Mechanism) ---
    with st.sidebar:
        st.header("Knowledge Management")
        st.info("This section simulates the periodic update mechanism. Click the button to fetch and integrate new information.")
        st.metric(label="Last KB Update", value=st.session_state.last_update)

        if st.button("🔄 Trigger Knowledge Update", help="Simulates a scheduled ETL job to crawl sources and update the vector database."):
            update_knowledge_base()

        st.subheader("Current Knowledge Base Snapshot (First 3 entries):")
        if kb:
            for i, doc in enumerate(kb[:3]):
                st.caption(f"Doc {i+1}: {doc['text'][:80]}...")
        else:
            st.warning("Knowledge Base is empty.")

        st.markdown("---")
        st.markdown(
            "*Scenario:* Initial KB is stale. Click the button to simulate a scheduled job replacing the old data with new, updated facts."
        )

    # --- Main Chat Interface ---

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if query := st.chat_input("Ask a question based on the knowledge base..."):
        # Display user message
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        with st.chat_message("assistant"):
            with st.spinner("Retrieving context and generating response..."):
                # 1. Retrieval Step (using internal KB)
                context = retrieve_context(query, kb)

                # Show context to user for transparency
                with st.expander("🔍 Context Retrieved for RAG"):
                    st.code(context)

                # 2. Generation Step (Gemini API Call)
                response = generate_rag_response(query, context)
                st.markdown(response)

        # Append assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

# Run the app
if __name__ == '__main__':
    main()
