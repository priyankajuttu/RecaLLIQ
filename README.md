# RECALLIQ

> **"Your AI client manager that gets smarter with every conversation."**

RecallIQ is an AI-powered client relationship intelligence assistant powered by **Hindsight**. It transforms generic AI responses into highly contextualized, evolving meeting preparation and account intelligence by maintaining persistent long-term memory across all interactions.

---

## 🎯 The Problem

Sales reps and senior account managers interact with clients across dozens of meetings, calls, emails, and proposals. Critical nuances get buried:
- What the client requested or rejected (and *why* they rejected it)
- Stakeholder-specific priorities (CFO vs CTO)
- Drift in communication preferences (e.g., weekly → bi-weekly updates)
- Open & overdue commitments
- Sensitive topics that should **never** be repeated

Traditional LLM assistants treat every conversation as a fresh prompt. Standard RAG only performs naive vector search over document snippets. **Without memory, AI gives generic advice.**

---

## 💡 The Idea

RecallIQ uses **Hindsight** as a persistent long-term memory layer. 

```
Interaction 1  → Generic understanding
Interaction 5  → Recognizes client preferences & history
Interaction 10 → Understands patterns, changes & commitments
Interaction 20 → Feels like an experienced account manager following the account from day one
```

---

## 🏗️ Technical Architecture

```
                               ┌─────────────────────────┐
                               │  Client Interaction     │
                               │  (Meeting / Email / Note)│
                               └────────────┬────────────┘
                                            │
                                            ▼
                               ┌─────────────────────────┐
                               │    Hindsight RETAIN     │
                               │  (Memory Bank Ingestion)│
                               └────────────┬────────────┘
                                            │
                                            ▼
                               ┌─────────────────────────┐
                               │ Persistent Client Memory│
                               │  (Hindsight Engine)     │
                               └────────────┬────────────┘
                                            │
                                            ▼
                               ┌─────────────────────────┐
                               │    Hindsight RECALL     │
                               │  (Contextual Memory)    │
                               └────────────┬────────────┘
                                            │
                                            ▼
                               ┌─────────────────────────┐
                               │  Groq (Llama 3.3 70B)   │
                               │  Reasoning & Prep Brief │
                               └────────────┬────────────┘
                                            │
                                            ▼
                               ┌─────────────────────────┐
                               │  RECALLIQ DASHBOARD     │
                               │ Actionable Intelligence │
                               └─────────────────────────┘
```

---

## 🔑 How Hindsight Is Used

RecallIQ leverages Hindsight's 3-tier memory operation:

1. **RETAIN (`client.retain`)**: Every meeting transcript, email follow-up, or note is retained into client-isolated memory banks (`recalliq-{client_id}`).
2. **RECALL (`client.recall`)**: When the user requests meeting prep, RecallIQ queries Hindsight to retrieve relevant facts, past objections, preference changes, and commitments.
3. **MEMORY TRACE**: The dashboard explicitly displays the recalled memory trace so judges can trace how Hindsight context shapes the LLM's reasoning and output.

---

## ✨ Key Features

- **Memory ON / OFF Toggle**: Controlled comparison showing generic AI responses vs RecallIQ Hindsight-powered briefs for the exact same prompt.
- **Preference Drift Detection**: Automatically tracks evolved client preferences (e.g. `Weekly updates → Bi-weekly executive updates`).
- **Do-Not-Repeat Warnings**: Highlights rejected proposals and negative memory (e.g. *NovaTech rejected 6-week implementation proposal due to deployment speed*).
- **Commitment Ledger**: Tracks promises with statuses (`OPEN`, `DONE`, `OVERDUE`).
- **Live Memory Ingestion**: Add new interactions in real-time and witness meeting prep update dynamically.
- **Client Memory Isolation**: Isolated memory banks ensure NovaTech memory never bleeds into GreenGrid Energy.

---

## 🛠️ Tech Stack

- **Frontend / Dashboard**: Streamlit 1.38+
- **Memory Engine**: Hindsight (Python SDK `hindsight-client` + REST API)
- **Reasoning LLM**: Groq (`llama-3.3-70b-versatile`)
- **Backend Language**: Python 3.10+ / Python 3.14

---

## 🚀 Quick Setup & Installation

### 1. Clone & Set Up Directory
```bash
cd recalliq
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env` and fill in your API keys:
```env
HINDSIGHT_API_KEY=your-hindsight-api-key-here
HINDSIGHT_BASE_URL=https://api.hindsight.vectorize.io
GROQ_API_KEY=your-groq-api-key-here
```

### 4. Run the RecallIQ Streamlit Dashboard
```bash
streamlit run app.py
```

---

## 🎬 Demo Script (90-Second Walkthrough)

1. **Open RecallIQ**: Select **NovaTech Systems** ($180k deal).
2. **Turn Memory OFF**: Click `[ PREPARE ME ]`. Observe generic advice (review status, review budget).
3. **Turn Hindsight Memory ON**: Click `[ PREPARE ME ]` again. Observe specific intelligence (CFO Sarah Chen cost focus, CTO Rahul Mehta milestone focus, rejected 6-week proposal warning, overdue final rollout timeline).
4. **Expand Memory Trace**: Show exact recalled memories from Hindsight.
5. **Show Preference Drift**: Highlight `Weekly → Bi-weekly executive updates`.
6. **Show Do-Not-Repeat**: Highlight rejected 6-week implementation proposal.
7. **Live Learning**: Go to **LIVE INTERACTION INGESTION**, enter new note, click `[ 🧠 REMEMBER THIS ]`. Re-run prep to show live adaptation.
8. **Client Isolation**: Switch to **GreenGrid Energy**. Confirm 0 NovaTech data spillover.

---

## 🔮 Future Scope

- **Multi-channel Sync**: Auto-ingest Zoom transcripts, Slack threads, and Salesforce notes via webhooks.
- **Predictive Risk Scoring**: Pre-meeting alert system when client satisfaction signals decline.
- **Automated Follow-up Drafting**: Auto-draft post-meeting emails based on promised commitments.
