"""
Meeting Preparation Generator - Uses Groq LLM to generate actionable meeting intelligence.
"""
import os
import logging
from groq import Groq

logger = logging.getLogger(__name__)


SYSTEM_PROMPT_WITH_MEMORY = """You are RecallIQ, an AI client relationship intelligence assistant.

You receive historical information retrieved from a persistent memory system called Hindsight.
Use this historical information as FACTUAL context — do not invent events, commitments, preferences, decisions, or stakeholder statements.

Rules:
1. When information conflicts, prefer the most recent explicit statement.
2. When a preference changes, explicitly identify the change (e.g., "Previously X, now Y as of [date]").
3. Separate facts from recommendations.
4. Generate concise, actionable meeting intelligence.
5. The purpose is to help an account manager walk into a client meeting already understanding the relationship.

Generate your response with these EXACT section headers (use markdown ## for each):

## 🏢 CLIENT SNAPSHOT
Brief overview: company, industry, deal size, key contacts.

## 🎯 CURRENT PRIORITIES
What the client cares about RIGHT NOW based on the most recent interactions.

## 📊 RELATIONSHIP HISTORY
Key milestones and decisions in the relationship journey.

## 🔄 WHAT CHANGED
Preference drifts, changed requirements, evolved positions. Use format: "OLD: X → NEW: Y (Date)"

## ✅ OPEN COMMITMENTS
Outstanding promises from both sides. Indicate owner and status.

## ⚠️ OVERDUE COMMITMENTS
Promises that are past due. Flag these prominently.

## 🚫 DO NOT REPEAT
Proposals or approaches that were rejected. Explain WHY they were rejected.

## 👤 STAKEHOLDER CONCERNS
Per-stakeholder breakdown of what each person cares about and how to address them.

## 📋 RECOMMENDED AGENDA
Suggested meeting agenda items in priority order.

## 💬 TALKING POINTS
Specific things to say or reference in the meeting.

## ⚡ RISKS / WATCHOUTS
Potential landmines, sensitive topics, or areas of concern.
"""

SYSTEM_PROMPT_WITHOUT_MEMORY = """You are a generic AI meeting assistant. You have NO historical context about this client beyond the basic information provided. Generate a general-purpose meeting preparation document.

Generate your response with these EXACT section headers (use markdown ## for each):

## 🏢 CLIENT SNAPSHOT
## 🎯 CURRENT PRIORITIES
## 📊 RELATIONSHIP HISTORY
## 🔄 WHAT CHANGED
## ✅ OPEN COMMITMENTS
## ⚠️ OVERDUE COMMITMENTS
## 🚫 DO NOT REPEAT
## 👤 STAKEHOLDER CONCERNS
## 📋 RECOMMENDED AGENDA
## 💬 TALKING POINTS
## ⚡ RISKS / WATCHOUTS

Since you have no historical context, provide generic advice for each section. Be honest that you lack specific information."""


class PrepGenerator:
    def __init__(self):
        self.api_key = os.environ.get("GROQ_API_KEY")
        self.client = None
        self.model = "llama-3.3-70b-versatile"

        if self.api_key:
            try:
                self.client = Groq(api_key=self.api_key)
            except Exception as e:
                logger.error(f"Failed to initialize Groq client: {e}")

    def _generate(self, messages: list) -> str:
        if not self.client:
            return "⚠️ **Groq client not initialized.** Please check your `GROQ_API_KEY` environment variable."

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
                max_tokens=4096,
            )
            return completion.choices[0].message.content
        except Exception as e:
            logger.error(f"Groq API Error: {e}")
            return f"⚠️ **Error communicating with Groq:** {str(e)}"

    def generate_meeting_prep(self, query: str, memories: list, client_info: dict) -> str:
        """Generate meeting prep WITH Hindsight memory context."""
        client_desc = (
            f"Client: {client_info.get('name', 'Unknown')}\n"
            f"Industry: {client_info.get('industry', 'N/A')}\n"
            f"Deal Value: {client_info.get('deal_value', 'N/A')}\n"
            f"Account Manager: {client_info.get('account_manager', 'N/A')}\n"
        )
        stakeholders = client_info.get("stakeholders", [])
        for s in stakeholders:
            client_desc += f"Stakeholder: {s.get('name', '')} ({s.get('role', '')}) - Focus: {s.get('primary_concern', '')}\n"

        memories_text = "\n".join([f"• {m}" for m in memories]) if memories else "No memories retrieved."

        user_prompt = f"""{client_desc}

User Request: {query}

=== RETRIEVED MEMORIES FROM HINDSIGHT ===
{memories_text}
=== END MEMORIES ===

Based on the above memories and client information, generate a comprehensive meeting preparation brief."""

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT_WITH_MEMORY},
            {"role": "user", "content": user_prompt},
        ]
        return self._generate(messages)

    def generate_without_memory(self, query: str, client_info: dict) -> str:
        """Generate meeting prep WITHOUT any memory context."""
        client_desc = (
            f"Client: {client_info.get('name', 'Unknown')}\n"
            f"Industry: {client_info.get('industry', 'N/A')}\n"
            f"Deal Value: {client_info.get('deal_value', 'N/A')}\n"
            f"Account Manager: {client_info.get('account_manager', 'N/A')}\n"
        )
        stakeholders = client_info.get("stakeholders", [])
        for s in stakeholders:
            client_desc += f"Stakeholder: {s.get('name', '')} ({s.get('role', '')}) - Focus: {s.get('primary_concern', '')}\n"

        user_prompt = f"""{client_desc}

User Request: {query}

You have NO historical context about interactions with this client. Generate a generic meeting prep."""

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT_WITHOUT_MEMORY},
            {"role": "user", "content": user_prompt},
        ]
        return self._generate(messages)
