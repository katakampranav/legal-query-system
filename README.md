<div align="center">

# ⚖️ LegalQ

### AI-Powered Legal Assistant for Indian Criminal Law

LegalQ is a full-stack AI application that helps users understand crimes, punishments, and their rights under the **Bharatiya Nyaya Sanhita (BNS) 2023** — in plain, simple language.

[![Next.js](https://img.shields.io/badge/Next.js-16-black?logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2-orange)](https://www.langgraph.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript)](https://www.typescriptlang.org/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-4-06B6D4?logo=tailwindcss)](https://tailwindcss.com/)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup — Backend (Server)](#setup--backend-server)
- [Setup — Frontend (Client)](#setup--frontend-client)
- [API Contract](#api-contract)
- [Features](#features)
- [Environment Variables](#environment-variables)

---

## Overview

LegalQ uses a **RAG (Retrieval-Augmented Generation)** pipeline to answer legal questions grounded in the BNS. The system retrieves relevant legal text from a Pinecone vector store and feeds it to an LLM (Groq / Mixtral) via a LangGraph workflow to produce accurate, context-grounded responses.

It supports two response modes:
- **Normal Mode** — Plain language explanation for everyday citizens
- **Lawyer Mode** — Structured legal analysis with sections, punishment, and reasoning

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Next.js 16, React 19, TypeScript, TailwindCSS v4 |
| **UI Components** | shadcn/ui (custom), Radix UI, Lucide React |
| **Theming** | next-themes (Light / Dark / System) |
| **Backend** | FastAPI, Python 3.12 |
| **AI Orchestration** | LangGraph, LangChain |
| **LLM** | Groq (Mixtral-8x7b-32768) |
| **Embeddings** | Cohere (`embed-english-v3.0`) |
| **Vector Store** | Pinecone |
| **Package Manager** | npm (frontend), uv (backend) |

---

## Project Structure

```
legalq/
├── client/                     # Next.js frontend
│   └── src/
│       ├── app/
│       │   ├── layout.tsx       # Root layout + ThemeProvider
│       │   ├── page.tsx         # Landing page
│       │   ├── globals.css      # Design system (light/dark CSS vars)
│       │   └── chat/
│       │       └── page.tsx     # Chat page
│       ├── components/
│       │   ├── ui/              # shadcn-style UI primitives
│       │   └── common/          # Logo, Navbar, ThemeToggle
│       ├── features/
│       │   └── chat/
│       │       ├── components/  # ChatWindow, MessageBubble, ChatInput, etc.
│       │       ├── hooks/       # useChat (all state management)
│       │       ├── services/    # legalq-api.ts (API calls)
│       │       └── types/       # chat-types.ts
│       └── lib/
│           ├── http-client.ts   # fetch wrapper (timeout + error handling)
│           ├── providers.tsx    # ThemeProvider
│           └── utils.ts         # cn() utility
│
└── server/                     # FastAPI + LangGraph backend
    ├── src/
    │   ├── app/                 # FastAPI app factory
    │   ├── endpoints/           # API route handlers
    │   ├── graph/               # LangGraph workflow definition
    │   ├── nodes/               # LangGraph nodes (retriever, generator, etc.)
    │   ├── llm/                 # LLM client (Groq)
    │   ├── services/            # Business logic
    │   ├── models/              # Pydantic request/response models
    │   └── state/               # LangGraph state schema
    ├── ingestion/               # PDF ingestion pipeline (BNS document)
    ├── settings.toml            # App configuration (dynaconf)
    ├── requirements.txt         # Python dependencies
    ├── run.sh                   # Linux/Mac startup script
    └── run.bat                  # Windows startup script
```

---

## Prerequisites

Make sure you have all of the following installed:

| Tool | Version | Download |
|---|---|---|
| Node.js | 18+ | [nodejs.org](https://nodejs.org) |
| Python | 3.12 | [python.org](https://python.org) |
| uv | latest | `pip install uv` |
| npm | 9+ | Comes with Node.js |

You will also need accounts and API keys for:
- [Groq](https://console.groq.com) — LLM inference
- [Pinecone](https://app.pinecone.io) — Vector database
- [Cohere](https://dashboard.cohere.com) — Embeddings

---

## Setup — Backend (Server)

### 1. Navigate to the server directory

```bash
cd legalq/server
```

### 2. Create a `.env` file

Copy the example and fill in your API keys:

```bash
cp .env.example .env   # if available, otherwise create manually
```

Your `.env` should contain:

```env
GROQ_API_KEY=your_groq_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
COHERE_API_KEY=your_cohere_api_key_here
PINECONE_INDEX=legal-docs
```

### 3. Install Python dependencies

Using **uv** (recommended):

```bash
uv sync
```

Or using **pip**:

```bash
pip install -r requirements.txt
```

### 4. Ingest the BNS document (first time only)

Before you can answer questions, you must ingest the Bharatiya Nyaya Sanhita PDF into Pinecone:

```bash
# Place the BNS PDF inside the data/ folder, then run:
uv run python -m ingestion.ingest
```

> ⚠️ This step only needs to be run **once**. It chunks the PDF and uploads embeddings to Pinecone.

### 5. Start the backend server

**Windows:**
```bash
run.bat
```

**Linux / Mac:**
```bash
chmod +x run.sh
./run.sh
```

**Or manually:**
```bash
uv run uvicorn src.app.main:app --host 0.0.0.0 --port 8000 --reload
```

The server will be available at: **`http://localhost:8000`**

API docs (auto-generated): **`http://localhost:8000/docs`**

---

## Setup — Frontend (Client)

### 1. Navigate to the client directory

```bash
cd legalq/client
```

### 2. Install dependencies

```bash
npm install
```

### 3. Create a `.env.local` file

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

> If you leave this blank, the frontend defaults to `http://localhost:8000`.

### 4. Start the development server

```bash
npm run dev
```

The app will be available at: **`http://localhost:3000`**

### 5. Build for production

```bash
npm run build
npm run start
```

---

## API Contract

The frontend communicates with only **one endpoint**:

### `POST /api/v1/ask`

**Request:**
```json
{
  "question": "What is the punishment for theft under BNS?",
  "mode": "normal"
}
```

| Field | Type | Values |
|---|---|---|
| `question` | `string` | Any legal question |
| `mode` | `string` | `"normal"` or `"lawyer"` |

**Response:**
```json
{
  "answer": "Under Section 303 of the Bharatiya Nyaya Sanhita...",
  "citations": ["Section 303", "Section 304"],
  "mode": "normal",
  "session_id": "abc123"
}
```

---

## Features

- 🤖 **AI-Powered Q&A** — Answers grounded in the BNS via RAG pipeline
- ⚖️ **Two Response Modes** — Normal (plain language) and Lawyer (structured legal analysis)
- 🌗 **Dark / Light / System Theme** — Toggleable with warm terracotta palette
- 📱 **Fully Responsive** — Works on mobile, tablet, and desktop
- 📝 **Markdown Rendering** — AI responses render headers, bullet points, bold text
- ⌨️ **Smart Input** — Enter to send, Shift+Enter for newline, auto-resizing textarea
- 🔒 **Safe Refusals** — Declines questions unrelated to Indian criminal law

---

## Environment Variables

### Backend (`server/.env`)

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | ✅ | Groq LLM API key |
| `PINECONE_API_KEY` | ✅ | Pinecone vector DB key |
| `COHERE_API_KEY` | ✅ | Cohere embeddings key |
| `PINECONE_INDEX` | ✅ | Name of your Pinecone index |

### Frontend (`client/.env.local`)

| Variable | Required | Description |
|---|---|---|
| `NEXT_PUBLIC_API_URL` | ⬜ | Backend base URL (default: `http://localhost:8000`) |

---

## Running Both Together

Open **two terminals** side by side:

**Terminal 1 — Backend:**
```bash
cd legalq/server
./run.sh        # or run.bat on Windows
```

**Terminal 2 — Frontend:**
```bash
cd legalq/client
npm run dev
```

Then open **`http://localhost:3000`** in your browser. 🚀

---

<div align="center">

Made with ❤️ for accessible legal literacy in India

> **Disclaimer:** LegalQ is for informational purposes only. Always consult a qualified lawyer for legal advice.

</div>
