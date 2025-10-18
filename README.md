🧠 Dynamic Knowledge Base RAG Chatbot (Streamlit)
This project implements a Retrieval-Augmented Generation (RAG) chatbot using the Gemini API, featuring a crucial mechanism for dynamically updating its internal knowledge base. This setup simulates how a real-world RAG system can periodically ingest new information and automatically incorporate those facts into its responses, replacing stale data.
The application is built using Streamlit for the interactive interface and Python for the backend logic and API integration.
✨ Features
 * Dynamic Knowledge Base: Uses Streamlit's session_state to mock a vector database (KB) containing specific facts.
 * Knowledge Management Panel: A sidebar control to manually trigger a knowledge update, simulating a scheduled ETL job.
 * RAG Architecture: Retrieves relevant context from the current KB state before generating a response using the Gemini API.
 * Context Transparency: Displays the context retrieved from the KB for the current query.
 * Exponential Backoff: Implements a retry mechanism for robust API calls.
🛠 Setup and Requirements
1. Prerequisites
You need a valid Google AI API Key to run the language model. You can obtain one from [Google AI Studio].
2. Dependencies
The application relies on the following Python packages. You can install them using the provided requirements.txt file:
pip install -r requirements.txt

(If you don't have the requirements.txt file, run: pip install streamlit requests)
3. API Key Configuration
Open the dynamic_knowledge_chatbot.py file and replace the placeholder with your actual key in the API_KEY variable:
# dynamic_knowledge_chatbot.py

# !!! IMPORTANT !!!
# Replace "YOUR_GEMINI_API_KEY_HERE" with your actual Gemini API Key.
API_KEY = "YOUR_GEMINI_API_KEY_HERE" # <-- PASTE YOUR KEY HERE
# !!! IMPORTANT !!!

🚀 How to Run
 * Save the code as dynamic_knowledge_chatbot.py.
 * Ensure your virtual environment is active and dependencies are installed.
 * Run the Streamlit application from your terminal:
<!-- end list -->
streamlit run dynamic_knowledge_chatbot.py

💡 Usage: Testing the Dynamic Knowledge
The application starts with "stale" knowledge. Follow these steps to observe the dynamic update in action:
Step 1: Test the Initial (Stale) Knowledge
Ask the chatbot one of the following questions:
 * What is the purpose and original deadline for Project Phoenix?
 * When is the annual training deadline, and what subject is it about?
Expected Result: The chatbot will answer using the initial, outdated facts (e.g., Project Phoenix ends Q3 2024, Security Training).
Step 2: Trigger the Knowledge Update
 * Navigate to the Knowledge Management sidebar on the left.
 * Click the 🔄 Trigger Knowledge Update button.
 * Observe the Last KB Update metric change and the Current Knowledge Base Snapshot update.
Step 3: Test the Updated Knowledge
Ask the chatbot the same questions again:
 * What is the purpose and original deadline for Project Phoenix?
 * When is the annual training deadline, and what subject is it about?
Expected Result: The chatbot's response will now be based on the new facts (e.g., Project Phoenix is postponed to Q1 2025, new AI Ethics training deadline is November 15th). This confirms the knowledge base has been successfully updated and is influencing the RAG output.
