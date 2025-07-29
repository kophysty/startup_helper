"""
Startup Financial OS MVP - Streamlit Application

Main entry point for the Startup Financial OS application.
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.core_engine.formulas import METRIC_FUNCS
from src.agent_core.agent_core import SageAgent
from src.infra.logging_conf import setup_logging, log_user_action

# Setup logging
logger = setup_logging()

def main():
    """Main application function."""
    
    # Page configuration
    st.set_page_config(
        page_title="Startup Financial OS",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Header
    st.title("💰 Startup Financial OS")
    st.markdown("*OS-level reliability, game-level usability*")
    
    # Sidebar
    with st.sidebar:
        st.header("🎯 Navigation")
        page = st.selectbox(
            "Choose a page:",
            ["🏠 Dashboard", "❓ Wizard", "🤖 Sage Agent", "📊 Analytics", "🏆 Badges"]
        )
        
        st.markdown("---")
        st.markdown("### Quick Stats")
        if 'metrics' in st.session_state:
            st.metric("MRR", f"${st.session_state.metrics.get('mrr', 0):,.0f}")
            st.metric("Runway", f"{st.session_state.metrics.get('runway', 0):.1f} months")
            st.metric("Churn", f"{st.session_state.metrics.get('churn', 0):.1f}%")
    
    # Main content based on selected page
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "❓ Wizard":
        show_wizard()
    elif page == "🤖 Sage Agent":
        show_sage_agent()
    elif page == "📊 Analytics":
        show_analytics()
    elif page == "🏆 Badges":
        show_badges()

def show_dashboard():
    """Show the main dashboard."""
    st.header("🏠 Dashboard")
    
    if 'metrics' not in st.session_state:
        st.info("👋 Welcome! Start by completing the Wizard to build your financial model.")
        st.button("🚀 Start Wizard", on_click=lambda: st.session_state.update({'page': 'wizard'}))
        return
    
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Monthly Recurring Revenue", f"${st.session_state.metrics.get('mrr', 0):,.0f}")
    
    with col2:
        st.metric("Runway", f"{st.session_state.metrics.get('runway', 0):.1f} months")
    
    with col3:
        st.metric("Churn Rate", f"{st.session_state.metrics.get('churn', 0):.1f}%")
    
    with col4:
        st.metric("Customer Acquisition Cost", f"${st.session_state.metrics.get('cac', 0):,.0f}")
    
    # Recent advice
    if 'sage_advice' in st.session_state:
        st.subheader("🤖 Latest Sage Advice")
        st.info(st.session_state.sage_advice)

def show_wizard():
    """Show the wizard interface."""
    st.header("❓ Financial Model Wizard")
    st.markdown("Answer 20 questions to build your startup's financial model.")
    
    # Initialize session state for wizard
    if 'wizard_answers' not in st.session_state:
        st.session_state.wizard_answers = {}
        st.session_state.current_question = 0
    
    # Load questions (simplified for MVP)
    questions = [
        {"id": "project_type", "text": "What type of project are you building?", "type": "select", "options": ["B2B SaaS", "B2C SaaS", "E-commerce", "Marketplace"]},
        {"id": "price", "text": "Average monthly subscription price (USD)?", "type": "number", "default": 50},
        {"id": "customers", "text": "How many paying customers today?", "type": "number", "default": 0},
        {"id": "churn_rate", "text": "Monthly churn rate (%)?", "type": "number", "default": 5},
        {"id": "marketing_spend", "text": "Monthly marketing spend (USD)?", "type": "number", "default": 0},
        {"id": "new_customers", "text": "New customers acquired this month?", "type": "number", "default": 0},
        {"id": "expenses_monthly", "text": "Other operating expenses per month (USD)?", "type": "number", "default": 10000},
        {"id": "cash_balance", "text": "Cash in bank today (USD)?", "type": "number", "default": 50000},
    ]
    
    # Progress bar
    progress = (st.session_state.current_question + 1) / len(questions)
    st.progress(progress)
    st.caption(f"Question {st.session_state.current_question + 1} of {len(questions)}")
    
    # Current question
    if st.session_state.current_question < len(questions):
        question = questions[st.session_state.current_question]
        
        st.subheader(question["text"])
        
        # Input based on question type
        if question["type"] == "select":
            answer = st.selectbox("Select:", question["options"], key=f"q_{question['id']}")
        elif question["type"] == "number":
            answer = st.number_input("Enter value:", value=question.get("default", 0), key=f"q_{question['id']}")
        
        # Navigation buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("⬅️ Previous") and st.session_state.current_question > 0:
                st.session_state.current_question -= 1
                st.rerun()
        
        with col2:
            if st.button("Next ➡️"):
                st.session_state.wizard_answers[question["id"]] = answer
                st.session_state.current_question += 1
                st.rerun()
    
    # Complete wizard
    else:
        st.success("✅ Wizard completed!")
        
        if st.button("🚀 Calculate Model"):
            # Calculate metrics
            agent = SageAgent()
            metrics = agent.calculate_model(st.session_state.wizard_answers)
            st.session_state.metrics = metrics
            
            # Generate advice
            advice = agent.suggest_changes(st.session_state.wizard_answers, metrics)
            st.session_state.sage_advice = advice
            
            st.success("Model calculated successfully!")
            st.rerun()

def show_sage_agent():
    """Show the Sage AI agent interface."""
    st.header("🤖 Sage AI Agent")
    st.markdown("Chat with Sage, your AI co-founder and financial advisor.")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "👋 Hi! I'm Sage, your AI co-founder. I can help you analyze your startup's financial health and suggest improvements. What would you like to know?"}
        ]
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask Sage anything..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        if 'metrics' in st.session_state:
            agent = SageAgent()
            response = agent.suggest_changes(st.session_state.wizard_answers, st.session_state.metrics)
        else:
            response = "I need to see your financial model first. Please complete the Wizard!"
        
        # Add assistant response
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

def show_analytics():
    """Show analytics and insights."""
    st.header("📊 Analytics")
    
    if 'metrics' not in st.session_state:
        st.info("Complete the Wizard to see analytics.")
        return
    
    # Metrics visualization
    st.subheader("Key Metrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("MRR", f"${st.session_state.metrics.get('mrr', 0):,.0f}")
        st.metric("LTV", f"${st.session_state.metrics.get('ltv', 0):,.0f}")
    
    with col2:
        st.metric("Burn Rate", f"${st.session_state.metrics.get('burn_rate', 0):,.0f}")
        st.metric("CAC/LTV Ratio", f"{st.session_state.metrics.get('cac', 0) / max(st.session_state.metrics.get('ltv', 1), 1):.2f}")

def show_badges():
    """Show user badges and achievements."""
    st.header("🏆 Badges & Achievements")
    
    if 'metrics' not in st.session_state:
        st.info("Complete the Wizard to earn badges!")
        return
    
    # Sample badges (simplified for MVP)
    badges = [
        {"name": "First Steps", "description": "Completed your first financial model", "icon": "🎯", "earned": True},
        {"name": "Runway Optimizer", "description": "Achieved runway of 12+ months", "icon": "⏰", "earned": st.session_state.metrics.get('runway', 0) >= 12},
        {"name": "Churn Master", "description": "Kept churn rate below 5%", "icon": "📉", "earned": st.session_state.metrics.get('churn', 0) <= 5},
    ]
    
    for badge in badges:
        col1, col2 = st.columns([1, 4])
        with col1:
            if badge["earned"]:
                st.markdown(f"✅ {badge['icon']}")
            else:
                st.markdown(f"🔒 {badge['icon']}")
        
        with col2:
            st.markdown(f"**{badge['name']}**")
            st.caption(badge['description'])

if __name__ == "__main__":
    main() 