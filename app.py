import os
import streamlit as st
from dotenv import load_dotenv

# Load env variables from .env file if available
load_dotenv()

from recalliq.core.memory_service import MemoryService
from recalliq.core.prep_generator import PrepGenerator

# Page configuration
st.set_page_config(
    page_title="RecallIQ — AI Client Manager Powered by Hindsight",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling for polished executive look
st.markdown("""
<style>
    /* Theme overrides */
    .stApp {
        background-color: #0e1117;
        color: #e0e6ed;
    }
    
    .main-header {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 1.8rem 2rem;
        border-radius: 12px;
        border: 1px solid #334155;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        margin-bottom: 2rem;
    }
    
    .brand-title {
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(90deg, #38bdf8 0%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    
    .brand-tagline {
        font-size: 1.05rem;
        color: #94a3b8;
        margin-top: 0.3rem;
        font-weight: 400;
    }
    
    .metric-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        text-align: center;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #38bdf8;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .card-box {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 1.2rem;
        margin-bottom: 1.2rem;
    }
    
    .alert-drift {
        background: rgba(245, 158, 11, 0.1);
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 6px;
        margin-bottom: 1rem;
    }
    
    .alert-dnr {
        background: rgba(239, 68, 68, 0.1);
        border-left: 4px solid #ef4444;
        padding: 1rem;
        border-radius: 6px;
        margin-bottom: 1rem;
    }
    
    .badge-open {
        background-color: #3b82f6;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .badge-done {
        background-color: #10b981;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .badge-overdue {
        background-color: #ef4444;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .timeline-item {
        border-left: 2px solid #3b82f6;
        padding-left: 1rem;
        margin-bottom: 1rem;
        position: relative;
    }
    
    .memory-trace-box {
        background: #0f172a;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 1rem;
        font-family: monospace;
        font-size: 0.88rem;
        color: #cbd5e1;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Services
@st.cache_resource
def get_services():
    return MemoryService(), PrepGenerator()

memory_service, prep_generator = get_services()

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/isometric-folders/100/brain.png", width=60)
    st.title("RECALLIQ")
    st.caption("Client Relationship Intelligence powered by Hindsight")
    st.markdown("---")
    
    # Client Selection
    client_ids = memory_service.get_client_ids()
    client_map = {
        "novatech": "NovaTech Systems ($180k)",
        "greengrid": "GreenGrid Energy ($95k)"
    }
    
    selected_client_id = st.selectbox(
        "🏢 SELECT CLIENT",
        options=client_ids,
        format_func=lambda x: client_map.get(x, x),
        index=0
    )
    
    client_info = memory_service.get_client_info(selected_client_id)
    
    st.markdown("---")
    
    # HINDSIGHT MEMORY TOGGLE
    st.subheader("⚙️ MEMORY ENGINE")
    memory_enabled = st.toggle("HINDSIGHT MEMORY", value=True, help="Toggle Hindsight long-term memory ON or OFF to compare responses.")
    
    if memory_enabled:
        st.success("🟢 HINDSIGHT MEMORY: ON")
    else:
        st.warning("🔴 HINDSIGHT MEMORY: OFF (Generic AI Mode)")
        
    st.markdown("---")
    
    # Account Manager Profile
    st.markdown("**👤 ACCOUNT MANAGER**")
    st.write(f"**Name:** {client_info.get('account_manager', 'Maya Rao')}")
    st.write(f"**Industry:** {client_info.get('industry')}")
    st.write(f"**Contract:** {client_info.get('deal_value')}")
    
    st.markdown("---")
    
    # Pre-load/Ingest Seed Data Button
    if selected_client_id not in st.session_state.get("ingested_clients", set()):
        if st.button("⚡ Sync Hindsight Memory Bank"):
            with st.spinner(f"Ingesting relationship history for {client_info.get('name')}..."):
                count = memory_service.ingest_client_data(selected_client_id)
                st.success(f"Ingested {count} interactions into Hindsight bank `recalliq-{selected_client_id}`!")
                st.rerun()
    else:
        st.caption("✅ Hindsight Bank Synchronized")


# --- MAIN CONTENT ---

# Header Banner
st.markdown(f"""
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <div class="brand-title">RECALLIQ</div>
            <div class="brand-tagline">"Your AI client manager that gets smarter with every conversation."</div>
        </div>
        <div style="text-align: right;">
            <span style="background: #0284c7; color: white; padding: 0.4rem 0.8rem; border-radius: 20px; font-weight: 600; font-size: 0.85rem;">
                Client: {client_info.get('name')}
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Top Metrics Row
interaction_count = memory_service.get_interaction_count(selected_client_id)
commitments = memory_service.get_commitments(selected_client_id)
pref_changes = memory_service.get_preference_changes(selected_client_id)
rejections = memory_service.get_rejections(selected_client_id)

open_commitments = [c for c in commitments if c.get("status") in ["OPEN", "OVERDUE"]]

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{interaction_count}</div>
        <div class="metric-label">Memory Interactions</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color: #ef4444;">{len(open_commitments)}</div>
        <div class="metric-label">Open Commitments</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color: #f59e0b;">{len(pref_changes)}</div>
        <div class="metric-label">Preference Drifts</div>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color: #ec4899;">{len(rejections)}</div>
        <div class="metric-label">Rejected Proposals</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Memory Maturity Curve Indicator
st.subheader("📈 ACCUMULATED RELATIONSHIP CONTEXT")
maturity_pct = min(100, int((interaction_count / 20) * 100))
st.progress(maturity_pct / 100)
st.caption(f"**Memory Maturity:** Interaction {interaction_count}/20 ({maturity_pct}% relationship depth captured via Hindsight)")

st.markdown("---")

# Main Tabs
tab_brief, tab_intelligence, tab_timeline, tab_live = st.tabs([
    "🎯 MEETING PREPARATION",
    "🧠 CLIENT INTELLIGENCE",
    "📅 RELATIONSHIP TIMELINE",
    "➕ LIVE INTERACTION INGESTION"
])

# =========================================================
# TAB 1: MEETING PREPARATION DEMO
# =========================================================
with tab_brief:
    st.markdown("### 🎯 Tomorrow's Meeting Preparation")
    st.markdown("Compare generic AI output vs **RecallIQ Hindsight Memory** intelligence.")

    default_query = f"Prepare me for tomorrow's meeting with {client_info.get('name')}."
    query_input = st.text_input("Meeting Prompt / Question:", value=default_query)

    col_btn, col_toggle_info = st.columns([1, 4])
    with col_btn:
        generate_clicked = st.button("🚀 PREPARE ME", type="primary", use_container_width=True)

    if generate_clicked or st.session_state.get("last_generated_query") == query_input:
        st.session_state.last_generated_query = query_input
        
        with st.spinner("Analyzing persistent client memory via Hindsight & reasoning with Groq..."):
            # Fetch memories if Memory ON
            if memory_enabled:
                memories = memory_service.recall_memories(selected_client_id, query_input)
                prep_result = prep_generator.generate_meeting_prep(query_input, memories, client_info)
            else:
                memories = []
                prep_result = prep_generator.generate_without_memory(query_input, client_info)

        # Visual Comparison Banner
        if memory_enabled:
            st.markdown("#### ⚡ RECALLIQ MEETING BRIEF (WITH HINDSIGHT MEMORY)")
            st.markdown(prep_result)

            # MEMORY TRACE ACCORDION
            with st.expander("🔍 VIEW HINDSIGHT MEMORY TRACE (Retrieved Memories)", expanded=False):
                st.markdown("The following historical context was recalled from Hindsight memory bank:")
                st.markdown("""
                ```text
                RETAIN → PERSISTENT MEMORY → RECALL → ENRICHED PROMPT → ACTIONABLE BRIEF
                ```
                """)
                if memories:
                    for i, m in enumerate(memories, 1):
                        st.markdown(f"**{i}.** `{m}`")
                else:
                    st.info("No specific memories recalled. Using full accumulated timeline context.")
        else:
            st.markdown("#### 🔴 GENERIC AI BRIEF (WITHOUT MEMORY)")
            st.markdown(prep_result)
            st.info("💡 **Notice the difference?** Turn **HINDSIGHT MEMORY [ON]** in the sidebar to see how RecallIQ remembers rejected proposals, preference drifts, and overdue commitments!")

# =========================================================
# TAB 2: CLIENT INTELLIGENCE
# =========================================================
with tab_intelligence:
    st.markdown(f"### 🧠 Client Intelligence Model: {client_info.get('name')}")
    
    col_left, col_right = st.columns(2)

    with col_left:
        # Preference Drift Alert
        st.markdown("#### 🔄 PREFERENCE DRIFT DETECTED")
        if pref_changes:
            for pc in pref_changes:
                st.markdown(f"""
                <div class="alert-drift">
                    <strong>{pc.get('attribute')}:</strong> {pc.get('old_value')} ➔ <strong>{pc.get('new_value')}</strong><br>
                    <small style="color: #94a3b8;">Changed on {pc.get('date')} | Note: {pc.get('context')}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No preference drifts recorded yet.")

        # Do Not Repeat Warning
        st.markdown("#### 🚫 DO NOT REPEAT")
        if rejections:
            for r in rejections:
                st.markdown(f"""
                <div class="alert-dnr">
                    <strong>Rejected Proposal:</strong> {r.get('proposal')}<br>
                    <strong>Reason:</strong> {r.get('reason')}<br>
                    <small style="color: #fca5a5;">Date: {r.get('date')} | Rejected by: {r.get('rejected_by')}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No rejected proposals recorded.")

    with col_right:
        # Stakeholders
        st.markdown("#### 👥 STAKEHOLDER PRIORITIES")
        stakeholders = client_info.get("stakeholders", [])
        for s in stakeholders:
            st.markdown(f"""
            <div class="card-box">
                <div style="font-weight: 700; color: #38bdf8;">{s.get('name')} — {s.get('role')}</div>
                <div style="font-size: 0.9rem; color: #cbd5e1; margin-top: 0.4rem;">
                    <strong>Primary Concern:</strong> {s.get('primary_concern')}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Commitment Ledger
        st.markdown("#### 📑 COMMITMENT LEDGER")
        if commitments:
            for c in commitments:
                status = c.get("status")
                badge_class = "badge-open" if status == "OPEN" else ("badge-done" if status == "DONE" else "badge-overdue")
                st.markdown(f"""
                <div class="card-box" style="padding: 0.8rem 1rem; margin-bottom: 0.6rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 600;">{c.get('description')}</span>
                        <span class="{badge_class}">{status}</span>
                    </div>
                    <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 0.3rem;">
                        Owner: {c.get('owner')} | Date: {c.get('date')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No commitments logged.")

# =========================================================
# TAB 3: RELATIONSHIP TIMELINE
# =========================================================
with tab_timeline:
    st.markdown(f"### 📅 Relationship Memory Timeline ({client_info.get('name')})")
    st.caption("Chronological record of interactions captured and learned by Hindsight.")

    timeline = memory_service.get_timeline(selected_client_id)
    
    for item in timeline:
        st.markdown(f"""
        <div class="timeline-item">
            <div style="font-weight: 700; color: #38bdf8; font-size: 0.95rem;">
                Interaction #{item.get('id', '')} — {item.get('date', '')} | {item.get('type', '')}
            </div>
            <div style="font-weight: 600; color: #f8fafc; margin: 0.2rem 0;">{item.get('summary', '')}</div>
            <div style="font-size: 0.88rem; color: #94a3b8;">{item.get('content', '')}</div>
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# TAB 4: LIVE INTERACTION INGESTION
# =========================================================
with tab_live:
    st.markdown("### ➕ Live Learning: Add New Client Interaction")
    st.markdown("Demonstrate that RecallIQ **learns in real-time** when new conversations occur.")

    sample_text = (
        "NovaTech wants the first rollout phase completed by October 20. "
        "They are comfortable with the revised pricing. They still want bi-weekly executive updates "
        "and weekly technical updates. We promised to send the final rollout timeline tomorrow."
    )

    if st.button("📝 Load Demo Sample Interaction", help="Pre-fill sample meeting text for fast demoing"):
        st.session_state.new_note_input = sample_text

    new_note = st.text_area(
        "New Meeting Note / Email Content:",
        value=st.session_state.get("new_note_input", ""),
        height=140,
        placeholder="Enter meeting notes, call summary, or email thread..."
    )

    col_a, col_b = st.columns([1, 3])
    with col_a:
        remember_clicked = st.button("🧠 REMEMBER THIS", type="primary", use_container_width=True)

    if remember_clicked and new_note.strip():
        with st.spinner("Retaining memory into Hindsight client bank..."):
            res = memory_service.add_interaction(
                client_id=selected_client_id,
                content=new_note.strip(),
                interaction_type="Meeting Note",
                date="2026-09-29"
            )
            st.success("✅ **MEMORY STORED VIA HINDSIGHT RETAIN!**")
            st.info("The relationship model and timeline have been updated. Switch to the **MEETING PREPARATION** tab and click **PREPARE ME** to see the updated intelligence!")
            st.balloons()

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #64748b; font-size: 0.85rem;'>RecallIQ Hackathon Prototype • Powered by Hindsight Memory Engine & Groq Llama 3.3 70B</div>", unsafe_allow_html=True)
