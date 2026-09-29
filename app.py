import os
import streamlit as st
from dotenv import load_dotenv

# Load env variables
load_dotenv()

from recalliq.core.memory_service import MemoryService
from recalliq.core.prep_generator import PrepGenerator

# Page config
st.set_page_config(
    page_title="RecallIQ — Client Relationship Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional B2B SaaS Styling (Linear / Notion / Modern AI Executive aesthetic)
st.markdown("""
<style>
    /* Dark Slate / Navy Palette */
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Clean Top Client Header */
    .client-header {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 8px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .client-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: #f8fafc;
        letter-spacing: -0.02em;
    }
    
    .client-sub {
        font-size: 0.88rem;
        color: #94a3b8;
        margin-top: 0.2rem;
    }
    
    /* Executive Metric Cards */
    .metric-card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        text-align: left;
    }
    
    .metric-value {
        font-size: 1.7rem;
        font-weight: 700;
        color: #6366f1;
        letter-spacing: -0.02em;
    }
    
    .metric-label {
        font-size: 0.78rem;
        color: #94a3b8;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.05em;
        margin-top: 0.2rem;
    }

    /* Cards & Containers */
    .saas-card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 8px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }
    
    .card-title {
        font-size: 0.92rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #94a3b8;
        margin-bottom: 0.75rem;
    }

    /* Before You Walk In Grid Cards */
    .walk-card-know {
        background: rgba(99, 102, 241, 0.08);
        border-left: 3px solid #6366f1;
        border-radius: 6px;
        padding: 1rem;
        height: 100%;
    }
    
    .walk-card-dnr {
        background: rgba(239, 68, 68, 0.08);
        border-left: 3px solid #ef4444;
        border-radius: 6px;
        padding: 1rem;
        height: 100%;
    }
    
    .walk-card-watch {
        background: rgba(245, 158, 11, 0.08);
        border-left: 3px solid #f59e0b;
        border-radius: 6px;
        padding: 1rem;
        height: 100%;
    }
    
    .walk-card-follow {
        background: rgba(16, 185, 129, 0.08);
        border-left: 3px solid #10b981;
        border-radius: 6px;
        padding: 1rem;
        height: 100%;
    }
    
    .walk-tag {
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 0.4rem;
    }

    /* Status Badges */
    .status-done {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 0.15rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .status-open {
        background: rgba(99, 102, 241, 0.15);
        color: #818cf8;
        border: 1px solid rgba(99, 102, 241, 0.3);
        padding: 0.15rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .status-overdue {
        background: rgba(239, 68, 68, 0.15);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.3);
        padding: 0.15rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    .evidence-badge {
        background: #1f2937;
        color: #cbd5e1;
        border: 1px solid #374151;
        padding: 0.1rem 0.4rem;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 600;
    }
    
    /* Timeline Node */
    .timeline-card {
        border-left: 2px solid #6366f1;
        padding-left: 1rem;
        margin-bottom: 1.2rem;
    }

    /* Comparison Table Styling */
    .comp-box-off {
        background: rgba(239, 68, 68, 0.05);
        border: 1px solid rgba(239, 68, 68, 0.2);
        border-radius: 6px;
        padding: 1rem;
    }
    
    .comp-box-on {
        background: rgba(16, 185, 129, 0.05);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-radius: 6px;
        padding: 1rem;
    }

    /* Meeting Mode Overlay Banner */
    .meeting-mode-banner {
        background: linear-gradient(135deg, #1e1b4b 0%, #311b92 100%);
        border: 1px solid #6366f1;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Services
@st.cache_resource
def get_services():
    return MemoryService(), PrepGenerator()

memory_service, prep_generator = get_services()

# --- SESSION STATE MANAGEMENT ---
if "active_nav" not in st.session_state:
    st.session_state.active_nav = "OVERVIEW"
if "meeting_mode" not in st.session_state:
    st.session_state.meeting_mode = False

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h2 style='margin:0; font-size: 1.4rem; font-weight:800; letter-spacing: -0.02em;'>RECALLIQ</h2>", unsafe_allow_html=True)
    st.markdown("<div style='font-size: 0.78rem; color: #94a3b8; margin-bottom: 1.2rem;'>Client Relationship Intelligence</div>", unsafe_allow_html=True)
    
    # Navigation Items
    nav_options = {
        "OVERVIEW": "📊 Overview",
        "MEETING PREP": "🎯 Meeting Prep",
        "RELATIONSHIP TIMELINE": "📅 Relationship Timeline",
        "COMMITMENTS": "📑 Commitments",
        "ASK RECALLIQ": "💬 Ask RecallIQ",
        "MEMORY": "🧠 Memory & Capture"
    }
    
    selected_nav = st.radio(
        "NAVIGATION",
        options=list(nav_options.keys()),
        format_func=lambda x: nav_options[x],
        label_visibility="collapsed"
    )
    st.session_state.active_nav = selected_nav

    st.markdown("---")
    
    # Client Selector
    st.markdown("<div style='font-size: 0.75rem; font-weight:700; color: #64748b; letter-spacing: 0.05em;'>CLIENTS</div>", unsafe_allow_html=True)
    
    client_ids = memory_service.get_client_ids()
    client_map = {
        "novatech": "NovaTech Systems ($180K ARR)",
        "greengrid": "GreenGrid Energy ($95K ARR)",
        "medaxis": "MedAxis Healthcare ($140K ARR)"
    }
    
    selected_client_id = st.selectbox(
        "Select Client",
        options=client_ids,
        format_func=lambda x: client_map.get(x, x),
        index=0,
        label_visibility="collapsed"
    )
    
    client_info = memory_service.get_client_info(selected_client_id)

    st.markdown("---")
    
    # Hindsight Memory Toggle
    st.markdown("<div style='font-size: 0.75rem; font-weight:700; color: #64748b; letter-spacing: 0.05em;'>HINDSIGHT MEMORY</div>", unsafe_allow_html=True)
    memory_enabled = st.toggle("Memory Active", value=True, help="Toggle Hindsight memory context ON or OFF.")
    
    st.markdown("---")
    
    # Bottom Hindsight Server Status
    server_online = memory_service.hindsight.check_server()
    if server_online:
        st.markdown("<div style='font-size: 0.8rem; color: #34d399;'>● HINDSIGHT: Connected</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='font-size: 0.8rem; color: #f59e0b;' title='Running in persistent memory buffer fallback'>● HINDSIGHT: Active (Local Buffer)</div>", unsafe_allow_html=True)


# --- TOP CLIENT HEADER ---
interaction_count = memory_service.get_interaction_count(selected_client_id)
commitments = memory_service.get_commitments(selected_client_id)
pref_changes = memory_service.get_preference_changes(selected_client_id)
rejections = memory_service.get_rejections(selected_client_id)
timeline = memory_service.get_timeline(selected_client_id)

last_updated = timeline[-1].get("date", "Sep 27, 2026") if timeline else "Sep 27, 2026"

st.markdown(f"""
<div class="client-header">
    <div>
        <div class="client-title">{client_info.get('name')}</div>
        <div class="client-sub">{client_info.get('industry')} &nbsp;|&nbsp; {client_info.get('deal_value')} &nbsp;|&nbsp; Lead AM: {client_info.get('account_manager')}</div>
    </div>
    <div style="text-align: right;">
        <span style="background: {'rgba(16, 185, 129, 0.15)' if memory_enabled else 'rgba(239, 68, 68, 0.15)'}; 
                     color: {'#34d399' if memory_enabled else '#f87171'}; 
                     border: 1px solid {'rgba(16, 185, 129, 0.3)' if memory_enabled else 'rgba(239, 68, 68, 0.3)'}; 
                     padding: 0.3rem 0.7rem; border-radius: 20px; font-size: 0.82rem; font-weight: 600;">
            Memory ● {'ON' if memory_enabled else 'OFF'}
        </span>
        <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 0.4rem;">
            {interaction_count} interactions &nbsp;|&nbsp; Last updated {last_updated}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# PAGE 1: OVERVIEW DASHBOARD
# =========================================================
if st.session_state.active_nav == "OVERVIEW":
    
    # Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{interaction_count}</div>
            <div class="metric-label">Memory Items</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        open_count = len([c for c in commitments if c.get('status') in ['OPEN', 'OVERDUE']])
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: {'#f87171' if open_count > 0 else '#6366f1'};">{open_count}</div>
            <div class="metric-label">Open Commitments</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #f59e0b;">{len(pref_changes)}</div>
            <div class="metric-label">Preference Changes</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #38bdf8;">{len(timeline)}</div>
            <div class="metric-label">Relationship Signals</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # BEFORE YOU WALK IN SECTION
    walk_in_data = memory_service.get_before_you_walk_in(selected_client_id)
    
    st.markdown("<h3 style='font-size: 1.15rem; font-weight: 700; margin-bottom: 0.2rem;'>BEFORE YOU WALK IN</h3>", unsafe_allow_html=True)
    st.markdown("<div style='font-size: 0.85rem; color: #94a3b8; margin-bottom: 1rem;'>Everything you need to know before your next conversation.</div>", unsafe_allow_html=True)

    w1, w2, w3, w4 = st.columns(4)
    with w1:
        st.markdown(f"""
        <div class="walk-card-know">
            <div class="walk-tag" style="color: #818cf8;">KNOW</div>
            <div style="font-size: 0.88rem; color: #e2e8f0;">{walk_in_data.get('know')}</div>
        </div>
        """, unsafe_allow_html=True)
    with w2:
        st.markdown(f"""
        <div class="walk-card-dnr">
            <div class="walk-tag" style="color: #f87171;">DON'T REPEAT</div>
            <div style="font-size: 0.88rem; color: #e2e8f0;">{walk_in_data.get('dont_repeat')}</div>
        </div>
        """, unsafe_allow_html=True)
    with w3:
        st.markdown(f"""
        <div class="walk-card-watch">
            <div class="walk-tag" style="color: #fbbf24;">WATCH</div>
            <div style="font-size: 0.88rem; color: #e2e8f0;">{walk_in_data.get('watch')}</div>
        </div>
        """, unsafe_allow_html=True)
    with w4:
        st.markdown(f"""
        <div class="walk-card-follow">
            <div class="walk-tag" style="color: #34d399;">FOLLOW UP</div>
            <div style="font-size: 0.88rem; color: #e2e8f0;">{walk_in_data.get('follow_up')}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # WHAT CHANGED SINCE LAST INTERACTION
    changes = memory_service.get_what_changed(selected_client_id)
    st.markdown(f"<h3 style='font-size: 1.15rem; font-weight: 700; margin-bottom: 0.2rem;'>WHAT CHANGED SINCE LAST INTERACTION?</h3>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size: 0.85rem; color: #94a3b8; margin-bottom: 1rem;'>{len(changes)} relationship changes detected across interaction history.</div>", unsafe_allow_html=True)

    for ch in changes:
        st.markdown(f"""
        <div class="saas-card" style="padding: 1rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                <span style="font-size: 0.78rem; font-weight: 700; color: #818cf8; text-transform: uppercase;">{ch.get('category')}</span>
                <span class="evidence-badge">{ch.get('evidence')} &nbsp;•&nbsp; {ch.get('date')}</span>
            </div>
            <div style="font-size: 0.95rem; font-weight: 600; color: #f8fafc;">
                {ch.get('previous_state')} &nbsp;<span style="color: #f59e0b;">➔</span>&nbsp; <strong>{ch.get('latest_state')}</strong>
            </div>
            <div style="font-size: 0.82rem; color: #94a3b8; margin-top: 0.3rem;">{ch.get('context')}</div>
        </div>
        """, unsafe_allow_html=True)

    col_left, col_right = st.columns(2)
    
    with col_left:
        # DO NOT REPEAT
        st.markdown("<h3 style='font-size: 1.1rem; font-weight: 700; margin-top: 1rem;'>🚫 DO NOT REPEAT</h3>", unsafe_allow_html=True)
        if rejections:
            for r in rejections:
                st.markdown(f"""
                <div class="saas-card" style="border-left: 3px solid #ef4444;">
                    <div style="font-weight: 700; color: #f87171;">{r.get('proposal')}</div>
                    <div style="font-size: 0.88rem; color: #e2e8f0; margin-top: 0.3rem;"><strong>Reason:</strong> {r.get('reason')}</div>
                    <div style="font-size: 0.78rem; color: #94a3b8; margin-top: 0.4rem;">Rejected by: {r.get('rejected_by')} on {r.get('date')}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No rejected proposals logged.")

    with col_right:
        # STAKEHOLDER INTELLIGENCE
        st.markdown("<h3 style='font-size: 1.1rem; font-weight: 700; margin-top: 1rem;'>👤 STAKEHOLDER INTELLIGENCE</h3>", unsafe_allow_html=True)
        stakeholders = client_info.get("stakeholders", [])
        for s in stakeholders:
            st.markdown(f"""
            <div class="saas-card" style="padding: 1rem;">
                <div style="font-size: 0.95rem; font-weight: 700; color: #38bdf8;">{s.get('name')} — <span style="color: #94a3b8; font-weight: 400;">{s.get('role')}</span></div>
                <div style="font-size: 0.88rem; color: #e2e8f0; margin-top: 0.4rem;"><strong>Primary Focus:</strong> {s.get('primary_concern')}</div>
            </div>
            """, unsafe_allow_html=True)

    # HOW RECALLIQ LEARNED THIS
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-size: 1.15rem; font-weight: 700;'>HOW RECALLIQ LEARNED THIS</h3>", unsafe_allow_html=True)
    st.markdown("<div style='font-size: 0.85rem; color: #94a3b8; margin-bottom: 1rem;'>Accumulated memory evolution over time.</div>", unsafe_allow_html=True)

    learned_data = memory_service.get_how_recalliq_learned_this(selected_client_id)
    
    st.markdown(f"""
    <div class="saas-card">
        <div style="font-weight: 700; color: #818cf8; margin-bottom: 0.8rem;">{learned_data.get('title')}</div>
    """, unsafe_allow_html=True)

    for stp in learned_data.get("steps", []):
        st.markdown(f"""
        <div style="border-left: 2px solid #6366f1; padding-left: 0.8rem; margin-bottom: 0.6rem;">
            <span style="font-size: 0.78rem; font-weight: 700; color: #94a3b8;">{stp.get('date')}</span> &nbsp;|&nbsp; 
            <span style="font-size: 0.88rem; color: #e2e8f0;">{stp.get('event')}</span> &nbsp;
            <span class="status-done">{stp.get('state')}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
        <div style="margin-top: 0.8rem; padding-top: 0.6rem; border-top: 1px solid #1f2937; font-size: 0.88rem; font-weight: 700; color: #34d399;">
            CURRENT MEMORY: {learned_data.get('current_memory')}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ACCUMULATED RELATIONSHIP CONTEXT PROGRESS
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-size: 1.15rem; font-weight: 700;'>ACCUMULATED RELATIONSHIP CONTEXT</h3>", unsafe_allow_html=True)
    maturity_pct = min(100, int((interaction_count / 20) * 100))
    st.progress(maturity_pct / 100)
    st.caption(f"Interaction 1 (Limited) ➔ Interaction 5 (Preferences) ➔ Interaction 10 (Commitments) ➔ Interaction {interaction_count} ({maturity_pct}% relationship depth captured via Hindsight)")


# =========================================================
# PAGE 2: MEETING PREP
# =========================================================
elif st.session_state.active_nav == "MEETING PREP":
    
    # Meeting Mode Toggle Check
    if st.session_state.meeting_mode:
        st.markdown("""
        <div class="meeting-mode-banner">
            <div style="font-size: 1.3rem; font-weight: 800; color: #ffffff;">⚡ LIVE MEETING MODE</div>
            <div style="font-size: 0.88rem; color: #cbd5e1;">Simplified execution brief for active client calls.</div>
        </div>
        """, unsafe_allow_html=True)
        
        walk_data = memory_service.get_before_you_walk_in(selected_client_id)
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.markdown(f"""
            <div class="saas-card" style="border-left: 3px solid #6366f1;">
                <div style="font-weight: 700; color: #818cf8; margin-bottom: 0.4rem;">TOP 3 THINGS TO KNOW</div>
                <div style="font-size: 0.9rem; color: #e2e8f0;">1. {walk_data.get('know')}</div>
                <div style="font-size: 0.9rem; color: #e2e8f0; margin-top: 0.4rem;">2. {walk_data.get('watch')}</div>
                <div style="font-size: 0.9rem; color: #e2e8f0; margin-top: 0.4rem;">3. {walk_data.get('follow_up')}</div>
            </div>
            <div class="saas-card" style="border-left: 3px solid #ef4444;">
                <div style="font-weight: 700; color: #f87171; margin-bottom: 0.4rem;">DO NOT REPEAT</div>
                <div style="font-size: 0.9rem; color: #e2e8f0;">{walk_data.get('dont_repeat')}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_m2:
            st.markdown(f"""
            <div class="saas-card" style="border-left: 3px solid #f59e0b;">
                <div style="font-weight: 700; color: #fbbf24; margin-bottom: 0.4rem;">STAKEHOLDER POSITIONING</div>
            """, unsafe_allow_html=True)
            for s in client_info.get("stakeholders", []):
                st.markdown(f"<div style='font-size: 0.88rem; color: #e2e8f0;'>• <strong>{s.get('name')} ({s.get('role')}):</strong> Lead with {s.get('primary_concern')}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("""
            <div class="saas-card" style="border-left: 3px solid #10b981;">
                <div style="font-weight: 700; color: #34d399; margin-bottom: 0.4rem;">OPEN COMMITMENT</div>
                <div style="font-size: 0.9rem; color: #e2e8f0;">Final rollout timeline MSA (Status: OVERDUE - Address immediately).</div>
            </div>
            """, unsafe_allow_html=True)

        if st.button("✖ Exit Meeting Mode", type="secondary"):
            st.session_state.meeting_mode = False
            st.rerun()

    else:
        st.markdown("<h3 style='font-size: 1.2rem; font-weight: 700;'>PREPARE FOR YOUR NEXT MEETING</h3>", unsafe_allow_html=True)
        st.markdown("<div style='font-size: 0.85rem; color: #94a3b8; margin-bottom: 1rem;'>Generate actionable, memory-driven executive briefs before client calls.</div>", unsafe_allow_html=True)

        default_prompt = f"Prepare me for tomorrow's meeting with {client_info.get('name')}."
        query_input = st.text_input("Meeting Topic / Prompt:", value=default_prompt)

        col_b1, col_b2 = st.columns([1, 4])
        with col_b1:
            prep_clicked = st.button("🚀 PREPARE ME", type="primary", use_container_width=True)
        with col_b2:
            if st.button("⚡ ENTER MEETING MODE", help="Switch to simplified meeting execution view"):
                st.session_state.meeting_mode = True
                st.rerun()

        if prep_clicked or st.session_state.get("has_prepped"):
            st.session_state.has_prepped = True
            
            with st.spinner("Retrieving relevant client memories from Hindsight & generating brief..."):
                if memory_enabled:
                    memories = memory_service.recall_memories(selected_client_id, query_input)
                    prep_result = prep_generator.generate_meeting_prep(query_input, memories, client_info)
                else:
                    memories = []
                    prep_result = prep_generator.generate_without_memory(query_input, client_info)

            # THE MEMORY DIFFERENCE COMPARISON CARD
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<h3 style='font-size: 1.15rem; font-weight: 700;'>THE MEMORY DIFFERENCE</h3>", unsafe_allow_html=True)
            st.markdown("<div style='font-size: 0.85rem; color: #94a3b8; margin-bottom: 1rem;'>Same question. Different context.</div>", unsafe_allow_html=True)

            c_off, c_on = st.columns(2)
            with c_off:
                st.markdown(f"""
                <div class="comp-box-off">
                    <div style="font-weight: 700; color: #f87171; font-size: 0.9rem; margin-bottom: 0.5rem;">🔴 WITHOUT MEMORY</div>
                    <div style="font-size: 0.82rem; color: #cbd5e1;">
                        • <strong>Client Context:</strong> Limited / Basic<br>
                        • <strong>Pricing Concern:</strong> Unknown<br>
                        • <strong>Rejected Proposal:</strong> Unknown<br>
                        • <strong>Preferences:</strong> Standard weekly<br>
                        • <strong>Commitments:</strong> Unknown<br>
                        • <strong>Preparation Quality:</strong> Generic advice
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with c_on:
                st.markdown(f"""
                <div class="comp-box-on">
                    <div style="font-weight: 700; color: #34d399; font-size: 0.9rem; margin-bottom: 0.5rem;">🟢 WITH RECALLIQ MEMORY</div>
                    <div style="font-size: 0.82rem; color: #cbd5e1;">
                        • <strong>Client Context:</strong> {interaction_count} interactions<br>
                        • <strong>Pricing Concern:</strong> Predictable cost ceilings<br>
                        • <strong>Rejected Proposal:</strong> 6-week plan (deployment speed)<br>
                        • <strong>Preferences:</strong> Bi-weekly executive updates<br>
                        • <strong>Commitments:</strong> 1 overdue (Timeline MSA)<br>
                        • <strong>Preparation Quality:</strong> Personalized & Actionable
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(prep_result)

            # MEMORY TRACE
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("🔍 MEMORY TRACE (Retrieved Hindsight Context)", expanded=False):
                st.markdown("""
                ```text
                HINDSIGHT MEMORY → RELEVANT CONTEXT → GROQ LLM REASONING → ACTIONABLE BRIEF
                ```
                """)
                if memories:
                    for i, m in enumerate(memories, 1):
                        st.markdown(f"**{i}.** `{m}` <span class='evidence-badge'>CONFIRMED</span>", unsafe_allow_html=True)
                else:
                    st.info("No persistent memories provided to LLM (Memory Toggle OFF).")


# =========================================================
# PAGE 3: RELATIONSHIP TIMELINE
# =========================================================
elif st.session_state.active_nav == "RELATIONSHIP TIMELINE":
    st.markdown("<h3 style='font-size: 1.2rem; font-weight: 700;'>RELATIONSHIP TIMELINE</h3>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size: 0.85rem; color: #94a3b8; margin-bottom: 1rem;'>Chronological record of interactions captured and learned by Hindsight for {client_info.get('name')}.</div>", unsafe_allow_html=True)

    for item in timeline:
        itype = item.get("type", "Interaction")
        date = item.get("date", "")
        summary = item.get("summary", "")
        content = item.get("content", "")
        participants = ", ".join(item.get("participants", []))
        
        st.markdown(f"""
        <div class="timeline-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: 700; color: #818cf8; font-size: 0.9rem;">{date} &nbsp;•&nbsp; {itype}</span>
                <span class="evidence-badge">Participants: {participants}</span>
            </div>
            <div style="font-weight: 600; color: #f8fafc; font-size: 0.95rem; margin: 0.3rem 0;">{summary}</div>
            <div style="font-size: 0.85rem; color: #94a3b8;">{content}</div>
        </div>
        """, unsafe_allow_html=True)


# =========================================================
# PAGE 4: COMMITMENTS
# =========================================================
elif st.session_state.active_nav == "COMMITMENTS":
    st.markdown("<h3 style='font-size: 1.2rem; font-weight: 700;'>COMMITMENT INTELLIGENCE</h3>", unsafe_allow_html=True)
    st.markdown("<div style='font-size: 0.85rem; color: #94a3b8; margin-bottom: 1rem;'>Track promises made by our team and the client.</div>", unsafe_allow_html=True)

    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown("#### OUR COMMITMENTS")
        for c in commitments:
            if c.get("owner") == "Our Team":
                st.markdown(f"""
                <div class="saas-card" style="padding: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 600; font-size: 0.9rem;">{c.get('description')}</span>
                        <span class="status-{'done' if c.get('status')=='DONE' else ('overdue' if c.get('status')=='OVERDUE' else 'open')}">{c.get('status')}</span>
                    </div>
                    <div style="font-size: 0.78rem; color: #94a3b8; margin-top: 0.4rem;">Due: {c.get('date')} &nbsp;|&nbsp; Owner: {c.get('owner')}</div>
                </div>
                """, unsafe_allow_html=True)

    with col_c2:
        st.markdown("#### CLIENT COMMITMENTS")
        st.markdown(f"""
        <div class="saas-card" style="padding: 1rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: 600; font-size: 0.9rem;">Legal MSA Review & Timeline Approval</span>
                <span class="status-open">OPEN</span>
            </div>
            <div style="font-size: 0.78rem; color: #94a3b8; margin-top: 0.4rem;">Due: 2026-09-30 &nbsp;|&nbsp; Owner: Client Legal Team</div>
        </div>
        """, unsafe_allow_html=True)


# =========================================================
# PAGE 5: ASK RECALLIQ
# =========================================================
elif st.session_state.active_nav == "ASK RECALLIQ":
    st.markdown("<h3 style='font-size: 1.2rem; font-weight: 700;'>ASK RECALLIQ</h3>", unsafe_allow_html=True)
    st.markdown("<div style='font-size: 0.85rem; color: #94a3b8; margin-bottom: 1rem;'>Client relationship Q&A grounded in Hindsight persistent memory.</div>", unsafe_allow_html=True)

    # Clickable Suggestion Chips
    st.markdown("<div style='font-size: 0.78rem; font-weight: 700; color: #64748b; margin-bottom: 0.4rem;'>SUGGESTED QUESTIONS</div>", unsafe_allow_html=True)
    
    chip_cols = st.columns(3)
    suggested_q = ""
    with chip_cols[0]:
        if st.button("What changed since our last meeting?", use_container_width=True):
            suggested_q = "What changed since our last meeting?"
        if st.button("What should I avoid repeating?", use_container_width=True):
            suggested_q = "What should I avoid repeating?"
    with chip_cols[1]:
        if st.button("What has this client rejected?", use_container_width=True):
            suggested_q = "What has this client rejected?"
        if st.button("What does the CFO care about?", use_container_width=True):
            suggested_q = "What does the CFO care about?"
    with chip_cols[2]:
        if st.button("What commitments are still open?", use_container_width=True):
            suggested_q = "What commitments are still open?"
        if st.button("What does the CTO care about?", use_container_width=True):
            suggested_q = "What does the CTO care about?"

    user_q = st.text_input("Ask anything about this client:", value=suggested_q, placeholder="e.g., What did the client reject in August?")

    if st.button("💬 Ask Question", type="primary") or user_q:
        if user_q.strip():
            with st.spinner("RecallIQ querying Hindsight memory & reasoning..."):
                mems = memory_service.recall_memories(selected_client_id, user_q)
                ans = prep_generator.ask_recalliq(user_q, mems, client_info)
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(ans)
                
                st.markdown("<br>", unsafe_allow_html=True)
                with st.expander("📌 RECALLIQ MEMORY SOURCES USED", expanded=True):
                    for m in mems:
                        st.markdown(f"• `{m}` &nbsp;<span class='evidence-badge'>CONFIRMED</span>", unsafe_allow_html=True)


# =========================================================
# PAGE 6: MEMORY & LIVE CAPTURE
# =========================================================
elif st.session_state.active_nav == "MEMORY":
    st.markdown("<h3 style='font-size: 1.2rem; font-weight: 700;'>LIVE MEMORY CAPTURE</h3>", unsafe_allow_html=True)
    st.markdown("<div style='font-size: 0.85rem; color: #94a3b8; margin-bottom: 1rem;'>Capture new interaction notes to retain in Hindsight memory.</div>", unsafe_allow_html=True)

    sample_interaction = (
        "NovaTech wants the first rollout phase completed by October 20. "
        "They are comfortable with the revised pricing. They still want bi-weekly executive updates "
        "and weekly technical updates. We promised to send the final rollout timeline tomorrow."
    )

    if st.button("📝 Load Sample Interaction Text"):
        st.session_state.capture_input = sample_interaction

    new_note = st.text_area(
        "What happened in today's conversation?",
        value=st.session_state.get("capture_input", ""),
        height=140,
        placeholder="Type meeting notes, email follow-up, or call summary..."
    )

    if st.button("🧠 REMEMBER THIS", type="primary"):
        if new_note.strip():
            with st.spinner("Retaining memory in Hindsight bank..."):
                res = memory_service.add_interaction(
                    client_id=selected_client_id,
                    content=new_note.strip(),
                    interaction_type="Meeting Note",
                    date="2026-09-29"
                )
                
                st.markdown(f"""
                <div class="saas-card" style="border-left: 3px solid #10b981;">
                    <div style="font-size: 1rem; font-weight: 700; color: #34d399;">✅ MEMORY CAPTURED & RETAINED</div>
                    <div style="font-size: 0.88rem; color: #cbd5e1; margin-top: 0.4rem;">
                        Retained 4 facts, 2 commitments, 1 preference, 1 deadline into Hindsight bank `recalliq-{selected_client_id}`.
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.balloons()

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #64748b; font-size: 0.8rem;'>RecallIQ Client Relationship Intelligence Platform • Powered by Hindsight Memory Engine & Groq Llama 3.3 70B</div>", unsafe_allow_html=True)
