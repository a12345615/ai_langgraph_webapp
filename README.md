# LangGraph AI 
Overview

langgraph_ai is a Python-based Generative AI project built using LangGraph and Groq LLMs.
The project demonstrates how to structure prompts, define graph-based AI workflows, and invoke Groq models efficiently.

This repository is intended for learning, experimentation, and building foundational GenAI workflows.

<img width="652" height="362" alt="image" src="https://github.com/user-attachments/assets/5adab12e-8a66-43e9-a7b8-a227bf22666a" />



# Features

LangGraph-based workflow orchestration
Groq LLM integration only
Modular prompt management
Simple test execution script

# Requirements

Python 3.9 or higher
Groq API Key

# Installation

1. Clone the Repository
   git clone <repository-url>
   cd langgraph_ai
2. Create Virtual Environment
   python -m venv venv
   source venv/bin/activate
3. Install Dependencies
   pip install -r requirements.txt

# Environment Setup

 GROQ_API_KEY="your_groq_api_key"

 # Running the Application
  python app.py

 # Testing the Model
   python test_invoke.py

   Sends a test prompt
   Receives and prints an AI-generated response

# File Descriptions
#app.py
Application entry point
Controls execution flow
#grapy.py
Defines LangGraph nodes and transitions
Manages AI workflow logic
#prompts.py
Stores prompt templates
Keeps prompt logic separate from execution
#test_invoke.py
Simple test harness for model invocation

<img width="1110" height="556" alt="image" src="https://github.com/user-attachments/assets/a63c8a76-9009-440b-98ec-908727bd8701" />

<img width="1064" height="506" alt="image" src="https://github.com/user-attachments/assets/ca5ba667-2be4-4f70-bdf8-fbe0a27f7f16" />
# Response 
<img width="1035" height="756" alt="image" src="https://github.com/user-attachments/assets/0f8e875c-c7a2-426a-a5b0-9b4bba437678" />

# Future Improvements
  RAG with documents
  Multi-agent LangGraph flows
  Logging and error handling
  
 







Clean and minimal codebase


