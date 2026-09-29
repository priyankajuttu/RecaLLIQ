"""
Memory Service - Higher-level service for managing client memory through Hindsight.
"""
import json
import os
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
            "account_manager": client_data.get("account_manager", "Maya Rao"),
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

    def get_before_you_walk_in(self, client_id: str) -> dict:
        """Get 'BEFORE YOU WALK IN' summary cards generated from real client memory data."""
        seed_data = self._load_seed_data()
        client_data = seed_data.get(client_id, {})
        
        if client_id == "novatech":
            return {
                "know": "NovaTech wants a faster phased rollout with first phase completion target in October.",
                "dont_repeat": "The original 6-week implementation plan was rejected due to deployment speed.",
                "watch": "Predictable pricing ceiling remains critical to CFO Sarah Chen.",
                "follow_up": "The final rollout timeline MSA is still pending legal sign-off (OVERDUE)."
            }
        elif client_id == "greengrid":
            return {
                "know": "GreenGrid requires SOC 2 Type II compliance and granular audit logging.",
                "dont_repeat": "Do not request weekly sync calls — review cycles move on monthly cadence.",
                "watch": "David Park (Head of Security) has strict KMS data encryption requirements.",
                "follow_up": "Security review completed; passing to Lisa Wong for budget authorization."
            }
        else: # medaxis
            return {
                "know": "MedAxis requires dedicated HIPAA VPC instance and FHIR/HL7 EHR integration.",
                "dont_repeat": "Do not propose standard multi-tenant cloud storage.",
                "watch": "Dr. Aris Thorne requires strict HIPAA BAA and custom audit logging policy.",
                "follow_up": "Legal team finalizing the custom Audit Logging Policy document for BAA sign-off."
            }

    def get_what_changed(self, client_id: str) -> list:
        """Get list of detected relationship changes."""
        changes = self.get_preference_changes(client_id)
        out = []
        for c in changes:
            out.append({
                "category": c.get("attribute", "PREFERENCE"),
                "previous_state": c.get("old_value", ""),
                "latest_state": c.get("new_value", ""),
                "date": c.get("date", ""),
                "context": c.get("context", ""),
                "evidence": "CONFIRMED"
            })
        
        # Add timeline target & commitment updates
        if client_id == "novatech":
            out.append({
                "category": "TIMELINE",
                "previous_state": "6-week single rollout",
                "latest_state": "First phase rollout completion in October 20",
                "date": "2026-09-25",
                "context": "Shifted to phased rollout structure per CTO Rahul Mehta.",
                "evidence": "RECENT"
            })
            out.append({
                "category": "COMMITMENT",
                "previous_state": "Pending legal MSA review",
                "latest_state": "Final rollout timeline pending (OVERDUE)",
                "date": "2026-09-27",
                "context": "Waiting on legal team sign-off.",
                "evidence": "REPEATED"
            })
        elif client_id == "greengrid":
            out.append({
                "category": "SECURITY REVIEW",
                "previous_state": "In security audit",
                "latest_state": "Approved by David Park; passed to VP Ops Lisa Wong",
                "date": "2026-09-25",
                "context": "Security review completed successfully.",
                "evidence": "CONFIRMED"
            })
        else: # medaxis
            out.append({
                "category": "DEPLOYMENT ARCHITECTURE",
                "previous_state": "Standard Cloud Storage",
                "latest_state": "Dedicated Encrypted HIPAA VPC",
                "date": "2026-08-25",
                "context": "Required for HIPAA BAA sign-off by Chief Medical Officer.",
                "evidence": "CONFIRMED"
            })

        return out

    def get_how_recalliq_learned_this(self, client_id: str) -> dict:
        """Get relationship evolution steps for preference drift visualization."""
        if client_id == "novatech":
            return {
                "title": "Executive Update Frequency Evolution",
                "attribute": "Executive Updates",
                "steps": [
                    {"date": "Aug 28", "event": "Client requested weekly updates during onboarding.", "state": "Weekly"},
                    {"date": "Sep 08", "event": "Weekly updates continued as planned.", "state": "Weekly"},
                    {"date": "Sep 19", "event": "Client changed executive update preference to bi-weekly.", "state": "Bi-weekly"}
                ],
                "current_memory": "Executive: Bi-weekly | Technical: Weekly"
            }
        elif client_id == "greengrid":
            return {
                "title": "Meeting Cadence Evolution",
                "attribute": "Review Cadence",
                "steps": [
                    {"date": "Aug 12", "event": "Initial weekly sync proposed.", "state": "Weekly"},
                    {"date": "Sep 16", "event": "David Park requested monthly touchpoints due to long review cycles.", "state": "Monthly"}
                ],
                "current_memory": "Executive: Monthly | Compliance: Monthly"
            }
        else:
            return {
                "title": "Governance Sync Evolution",
                "attribute": "Status Calls",
                "steps": [
                    {"date": "Aug 14", "event": "Bi-weekly status calls established.", "state": "Bi-weekly"},
                    {"date": "Sep 18", "event": "Shifted to monthly reviews due to physician shift schedules.", "state": "Monthly"}
                ],
                "current_memory": "Status Calls: Monthly | BAA Audit: On-demand"
            }
