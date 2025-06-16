# VAA GenAI Technical Test — AI Travel Assistant

## Overview

This is a lightweight GenAI travel assistant built using FastAPI, OpenAI’s Assistants API, and a custom semantic search layer. It takes user queries (e.g., “Where should I go for a solo foodie trip to Asia in September?”) and returns thoughtful destination advice by blending structured JSON data (hotels, flights, experiences) with LLM-backed reasoning.

---

# What’s Done So Far

**Core Endpoint (POST /travel-assistant)**: Parses user queries, optionally auto-selects a city, and calls the LLM agent.

**LLM Agent** : Uses `AsyncOpenAI` with function-calling to:

- Search hotels, flights, and experiences via seed-data-backed retrieval

- Return structured travel advice via a return_advice function

- Implements retry and fallback logic for both API errors and test environments

**Retrieval Layer**: Simple search functions over JSON seed data (with Faiss indexing for future scalability).

**Schemas & Guardrails**: Pydantic models (TravelAdvice) ensure consistent response shapes; impossible destinations (e.g. Mars) are handled gracefully.

**Testing**: Comprehensive pytest coverage (14 passing tests) for agent logic, API routes, and evaluation harness.

---

# Getting Started

**Clone & Run Locally:**

```bash
    git clone https://github.com/debbsjohnson/vaa-genai-travel-assistant.git
    cd vaa-genai-travel-assistant`
```

**Setup**

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on windows
pip install -r requirements.txt
```

**Env Setup:**
Create a `.env` file in the root directory with:

```bash
OPENAI_API_KEY=sk-...
OPENAI_PROJECT_ID=proj_...
```

**Run App:**
I had some trouble with my OpenAI key, which was weird so i ran this before posting (just in case you have that issue too :)

```bash
source env
```

```bash
uvicorn travel_assistant.main:app --reload
```

Then `POST` to:

```bash
http://localhost:8000/travel-assistant
```

Example:

```bash
 { "query": "Where should I go for a solo foodie trip to USA in September?" }
```

Output:

```bash
{
    "destination": "Mumbai",
    "reason": "Mumbai is a vibrant city known for its diverse and rich culinary scene, making it an ideal destination for a foodie trip.",
    "budget": "Moderate to High",
    "tips": [
        "Try the local street food like Vada Pav and Pav Bhaji.",
        "Visit the famous Leopold Cafe for a mix of local and international flavors.",
        "Explore the spice markets for a true taste of Indian spices.",
        "Don't miss the seafood at the city's coastal restaurants.",
        "Book your food tours in advance to secure a spot."
    ],
    "hotel": {
        "name": "The Taj Mahal Palace & Tower",
        "city": "Mumbai",
        "price_per_night": 500.0,
        "rating": 5.0
    },
    "flight": {
        "airline": "Virgin Atlantic",
        "from_airport": "LHR",
        "to_airport": "MUM",
        "price": 800.0,
        "duration": "9H",
        "date": "2023-09-15"
    },
    "experience": {
        "name": "Local Food Tour",
        "city": "mumbai",
        "price": 50.0,
        "duration": "3 hours"
    }
}
```

---

# What Works

- Full prompt/response pipeline via Assistants API

- JSON file ingestion (hotels, flights, experiences)

- Vector search powered by FAISS + NumPy

- Dynamic response generation (reasoning + tips)

- Validated with 14/14 green tests

- Logs + graceful fallback for failed completions

---

# Mistakes i made

- I definitely overcomplicated some parts and overengineering too early: I built things like embedding support and a test harness before validating the core OpenAI pipeline. This cost time I could’ve spent refining the actual assistant.

- I underestimated how tricky containerizing a multi-layer Python project would be. Pathing issues, dependency mismatches, and unclear context loading made the containerisation phase stressful.

- I structured seed data access assuming a static file system layout, which didn’t translate cleanly into the container context. This blocked successful runs until adjusted.

- The tool_call_ids required by OpenAI’s API were tricky to handle without a proper middleware layer or abstraction, which led to repeated failed requests when the assistant didn’t auto-resolve them.

---

# Next Steps

While the current agent fulfills its basic functionality of returning travel recommendations via OpenAI's Assistants API, there are several powerful and creative directions I’m eager to explore with more time and resources:

- I’d love to restructure the assistant into a collaborative network of specialized agents—for example, one for travel logistics, another for culinary experiences, and a third for budgeting. Using LangGraph or similar agent orchestration frameworks would allow these agents to “negotiate” and converge on richer, more context-aware recommendations.

- In future iterations, I'd integrate LangChain and a Retrieval-Augmented Generation (RAG) pipeline. This would allow the assistant to query external sources (e.g., Expedia APIs, flight aggregators, or even live news APIs for weather/conflict alerts) and inject live results into the assistant’s decision-making. Not only does this keep the assistant current, it also grounds it in reality—crucial for travel planning.

- For maintainability and demonstration purposes, I'd wire up the system in LangFlow to allow stakeholders to visually experiment with prompt chains, tool usage, and decision logic. This also enables faster experimentation and onboarding of non-technical team members.

- In future development, I’d introduce a lightweight reranker (likely trained on curated destination-vs-query pairs) to prioritize or reweight results more intelligently. This model could sit behind the primary generation layer, ensuring that the top recommendation always feels tailored and compelling.

- I'd incorporate a user feedback mechanism to log and learn from rejected or highly-rated suggestions. Over time, this dataset would enable model refinement or fine-tuning, improving personalization and user satisfaction.

- Given more time, I would abstract each tool (flight, hotel, experience search) into modular OpenAI tools and improve tool routing using robust prompt engineering. I also explored how OpenAI manages tool_call chaining via the tool_choice param, which would be a great next step.

- I faced a few OpenAI tool_call errors during development. To tackle this, I consistently leaned on OpenAI’s API documentation, GitHub issues, and Azure’s model compatibility tables. If I had more time, I’d formalize a proper evaluation framework using pytest + evals and consider mocking LLM outputs using a shadow-mode setup during test runs.

- Lastly, I’d secure secrets with GitHub Actions + Vault or Doppler and set up a full CI/CD pipeline to auto-deploy the agent on each successful push—enabling safe, traceable experimentation and smoother iteration cycles.

---

# Reflections

This was easily one of the most engaging tasks I’ve worked on. The real challenge wasn’t just to “call OpenAI and respond,” but to carefully choreograph context, tools, and fallbacks in a way that feels coherent to users.

I also realised partway through that I might have overcomplicated things—maybe out of excitement to “do it all properly.” There’s beauty in starting lean and iterating fast, and I plan to carry that lesson into future builds.

Despite the frustrations (hello, docker 😅), I learned a lot—from managing environment config across dev/staging modes to the quirks of OpenAI’s new assistant framework.

I think the next leap is moving from “an app that uses AI” to “an app designed around AI.” That’s where things get fun.

Thanks for reading, and I hope this project gives a peek into how I build, think, and grow :D

**Deborah Johnson**
