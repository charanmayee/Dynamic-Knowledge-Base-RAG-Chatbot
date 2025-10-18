🧠 Dynamic Knowledge Base RAG Chatbot (Streamlit)
This project demonstrates a dynamic RAG (Retrieval-Augmented Generation) system built using Streamlit and the Gemini API. The key feature is the ability to simulate periodic updates to the internal knowledge base, allowing the chatbot's responses to evolve and remain current with the latest information.
✨ Features
 * Dynamic Knowledge Simulation: The application's knowledge base (simulating a Vector DB) can be updated mid-session, changing the context used for generation.
 * Secure API Handling: The Gemini API Key is loaded securely via an environment variable (GEMINI_API_KEY), ensuring your key is not committed to the repository.
 * RAG Architecture: The system retrieves the most relevant context from the current knowledge base state before generating a grounded response using Gemini.
 * Context Transparency: The context used to generate the answer is displayed to show the grounding mechanism in action.
 * Robust API Calls: Implements exponential backoff for handling potential API rate limits or transient network errors.
🛠 Repository Files
To run and deploy this application, your repository requires the following files:
 * dynamic_knowledge_chatbot.py: The main Streamlit application code.
 * requirements.txt: Python package dependencies.
 * .gitignore: Prevents sensitive files (like API keys) from being committed.
🚀 Setup and Local Run
1. Installation
Install the required Python packages:
pip install -r requirements.txt

2. API Key Configuration (Crucial)
For security, the application reads the API key from your environment. You must set the GEMINI_API_KEY environment variable before running.
How to set the variable:
| Operating System | Command |
|---|---|
| macOS / Linux | export GEMINI_API_KEY='YOUR_API_KEY_HERE' |
| Windows (CMD) | set GEMINI_API_KEY=YOUR_API_KEY_HERE |
3. Run the App
Execute the Streamlit script:
streamlit run dynamic_knowledge_chatbot.py

This will open the application in your browser.
💡 Testing the Dynamic Knowledge
The chatbot is pre-loaded with stale facts. Follow this sequence to witness the knowledge update:
Step 1: Query the Stale Knowledge
Ask a question that targets the initial, outdated facts (e.g., What is the purpose and original deadline for Project Phoenix?).
 * Expected Response: Project Phoenix is due Q3 2024 and is a server infrastructure upgrade.
Step 2: Trigger the Knowledge Update
 * Open the Knowledge Management sidebar.
 * Click the 🔄 Trigger Knowledge Update button.
 * The Last KB Update metric will change, and the Current Knowledge Base Snapshot will display the new facts (e.g., focusing on "AI Ethics," "Project Aether," and "Q1 2025").
Step 3: Query the Updated Knowledge
Ask the same question again.
 * Expected Response: Project Phoenix is indefinitely postponed with a new deadline of Q1 2025. The chatbot is now grounded on the new information.
