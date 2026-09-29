"""
Memory Service - Higher-level service for managing client memory through Hindsight.
"""
import json
import os
import time
import streamlit as st
from .hindsight_client import RecallIQHindsightClient


class MemoryService:
    def __init__(self):
        self.hindsight = RecallIQHindsightClient()
        self.seed_file_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "seed_data.json"
        )

        # Initialize session state for tracking ingested clients
        if "ingested_clients" not in st.session_state:
            st.session_state.ingested_clients = set()
        if "extra_interactions" not in st.session_state:
            st.session_state.extra_interactions = {}

    def _load_seed_data(self) -> dict:
        if not os.path.exists(self.seed_file_path):
            return {}
        try:
            with open(self.seed_file_path, "r") as f:
                data = json.load(f)
            # Navigate into "clients" if present
            return data.get("clients", data)
        except Exception:
            return {}

    def ingest_client_data(self, client_id: str, progress_callback=None) -> int:
        """Ingest all seed interactions for a client into Hindsight."""
        if client_id in st.session_state.ingested_clients:
            return 0

        seed_data = self._load_seed_data()
        client_data = seed_data.get(client_id, {})
        interactions = client_data.get("interactions", [])

        count = 0
        total = len(interactions)
        for i, interaction in enumerate(interactions):
            content = interaction.get("content", "")
            date = interaction.get("date", "")
            itype = interaction.get("type", "")
            summary = interaction.get("summary", "")
            participants = ", ".join(interaction.get("participants", []))

            enriched = (
                f"[{date}] {itype}: {summary}\n"
                f"Participants: {participants}\n"
                f"{content}"
            )

            if enriched.strip():
                res = self.hindsight.retain_interaction(client_id, enriched)
                if res.get("success"):
                    count += 1

            if progress_callback and total > 0:
                progress_callback((i + 1) / total)

        st.session_state.ingested_clients.add(client_id)
        return count

    def add_interaction(self, client_id: str, content: str, interaction_type: str = "Note", date: str = "") -> dict:
        """Add a new interaction and retain it in Hindsight."""
        if not date:
            from datetime import datetime
            date = datetime.now().strftime("%Y-%m-%d")

        enriched = f"[{date}] {interaction_type}: {content}"
        result = self.hindsight.retain_interaction(client_id, enriched)

        # Track in session state
        if client_id not in st.session_state.extra_interactions:
            st.session_state.extra_interactions[client_id] = []
        st.session_state.extra_interactions[client_id].append({
            "date": date,
            "type": interaction_type,
            "content": content,
            "summary": content[:100] + "..." if len(content) > 100 else content,
            "participants": ["Maya Rao"]
        })

        return result

    def get_client_info(self, client_id: str) -> dict:
        """Get client metadata from seed data."""
        seed_data = self._load_seed_data()
        client_data = seed_data.get(client_id, {})
        return {
            "name": client_data.get("name", "Unknown"),
            "industry": client_data.get("industry", ""),
            "deal_value": client_data.get("deal_value", ""),
            "stakeholders": client_data.get("stakeholders", []),
            "account_manager": client_data.get("account_manager", ""),
        }

    def get_interaction_count(self, client_id: str) -> int:
        """Get total interaction count (seed + added)."""
        seed_data = self._load_seed_data()
        client_data = seed_data.get(client_id, {})
        seed_count = len(client_data.get("interactions", []))
        extra_count = len(st.session_state.extra_interactions.get(client_id, []))
        return seed_count + extra_count

    def get_timeline(self, client_id: str) -> list:
        """Get chronological timeline of all interactions."""
        seed_data = self._load_seed_data()
        client_data = seed_data.get(client_id, {})
        interactions = client_data.get("interactions", [])

        # Add any extra interactions from this session
        extras = st.session_state.extra_interactions.get(client_id, [])
        all_interactions = list(interactions) + [
            {"id": len(interactions) + i + 1, **e} for i, e in enumerate(extras)
        ]

        return sorted(all_interactions, key=lambda x: x.get("date", ""))

    def get_commitments(self, client_id: str) -> list:
        """Extract commitments from seed data."""
        seed_data = self._load_seed_data()
        client_data = seed_data.get(client_id, {})
        return client_data.get("commitments", [])

    def get_preference_changes(self, client_id: str) -> list:
        """Extract preference changes from seed data."""
        seed_data = self._load_seed_data()
        client_data = seed_data.get(client_id, {})
        return client_data.get("preference_changes", [])

    def get_rejections(self, client_id: str) -> list:
        """Extract rejected proposals from seed data."""
        seed_data = self._load_seed_data()
        client_data = seed_data.get(client_id, {})
        return client_data.get("rejections", [])

    def get_client_ids(self) -> list:
        """Get list of available client IDs."""
        seed_data = self._load_seed_data()
        return list(seed_data.keys())

    def recall_memories(self, client_id: str, query: str) -> list:
        """Recall memories from Hindsight and return as list of strings."""
        if client_id not in st.session_state.ingested_clients:
            self.ingest_client_data(client_id)

        results = self.hindsight.recall_memories(client_id, query)
        memories = []
        if hasattr(results, 'results'):
            for r in results.results:
                memories.append(r.text if hasattr(r, 'text') else str(r))
        elif hasattr(results, '__iter__'):
            for r in results:
                if hasattr(r, 'text'):
                    memories.append(r.text)
                elif isinstance(r, dict):
                    memories.append(r.get("text", str(r)))
                else:
                    memories.append(str(r))
        return memories
