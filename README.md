```markdown
# Omni_BankPilot 🏦🤖  
*A Context-Aware Multi-Agent Conversational Banking Assistant*

---

## 📌 Project Overview

**Omni_BankPilot** is an intelligent, voice-enabled conversational banking assistant designed to understand natural language queries, maintain conversational context, and perform banking-related tasks using a **multi-agent architecture**.  
The system supports both **voice and text interaction**, intelligently routes user requests, and provides secure, user-friendly responses.

---

## 🎯 Problem Statement

Most traditional banking chatbots are rule-based and fail to:
- Understand natural, informal user queries
- Maintain context across multiple conversation turns
- Dynamically route requests to appropriate services

This results in poor user experience and increased dependency on customer support.

---

## 💡 Proposed Solution

Omni_BankPilot solves this by using:
- **Speech-to-Text (STT)** for voice input
- **LLM-based context understanding**
- **Intent classification**
- **LangGraph-based intelligent routing**
- **Specialized agents** for banking, information, and reminders
- **Text-to-Speech (TTS)** for voice responses

---

## 🧠 System Architecture (High Level)

```

User (Voice/Text)
↓
Speech-to-Text (Whisper)
↓
Context Understanding
↓
Intent Detection
↓
LangGraph Router
↓
Bank Agent | RAG Agent | Reminder Agent
↓
Response Generator
↓
Text + Voice Output (UI)

```

---

## 🔄 Pipeline Model

1. User provides voice or text input via UI  
2. Voice input is converted to text using STT  
3. Context pipeline understands conversational meaning  
4. Intent pipeline classifies user intent and sub-intent  
5. LangGraph routes the request to the correct agent  
6. Agent fetches or processes required data  
7. Response is formatted and converted to speech  
8. Final output is shown and spoken to the user  

---

## 📂 Project Structure

```

Omni_BankPilot/
│
├── ui.py                      # User interface (voice/text input & output)
├── app.py                     # Main controller orchestrating the pipeline
│
├── pipeline/
│   ├── input_pipeline.py      # Voice → Text (STT)
│   ├── context_pipeline.py    # Conversational context understanding
│   ├── intent_pipeline.py     # Intent and sub-intent detection
│   ├── response_pipeline.py   # Final response formatting
│
├── graph/
│   ├── state.py               # Shared LangGraph state definition
│   ├── router.py              # Intent-based routing logic
│   ├── graph_builder.py       # LangGraph workflow construction
│
├── agents/
│   ├── bank_agent.py          # Banking operations (balance, transactions)
│   ├── rag_agent.py           # Informational queries using RAG
│   ├── reminder_agent.py      # Reminder CRUD operations
│
├── services/
│   ├── stt.py                 # Speech-to-Text service
│   ├── tts.py                 # Text-to-Speech service
│   ├── llm.py                 # LLM wrapper
│   ├── memory.py              # Conversation memory
│
├── db/
│   ├── mysql.py               # Bank database access
│   ├── reminder_db.py         # Reminder database access
│
├── prompts/
│   ├── context_prompt.txt     # Context understanding prompt
│   └── intent_prompt.txt      # Intent classification prompt
│
├── requirements.txt
└── README.md

````

---

## 🤖 Agents Description

- **Bank Agent**  
  Handles sensitive banking operations such as balance checks and transaction history using secure database access.

- **RAG Agent**  
  Answers informational and policy-related queries using a retrieval-augmented generation approach.

- **Reminder Agent**  
  Manages reminder creation, updates, and deletion for user tasks.

---

## 🔐 Security Considerations

- Banking actions are isolated within the **Bank Agent**
- Sensitive operations can be extended with **OTP verification**
- LLM usage is controlled via prompts and routing logic

---

## 🛠️ Tech Stack

- **Python**
- **LangGraph** (Multi-agent orchestration)
- **Large Language Models (LLMs)**
- **Whisper (STT)** – optional integration
- **Text-to-Speech (TTS)**
- **MySQL** (Banking & reminder data)
- **VS Code + GitHub**

---

## 🚀 How to Run (Basic)

```bash
pip install -r requirements.txt
python ui.py
````

---

## 📈 Future Enhancements

* OTP-based authentication for transactions
* Real-time database integration
* Gradio or Web-based UI
* User profile and session management
* Multilingual support

---

## 🧾 Conclusion

Omni_BankPilot demonstrates how modern conversational AI systems can be built using **context-aware pipelines**, **multi-agent routing**, and **LLM intelligence** to deliver secure, scalable, and user-friendly banking assistance.

---

## 👩‍💻 Author

**Paromita Karmakar**
*MSc Data Science*

```


Just tell me 👍
```
