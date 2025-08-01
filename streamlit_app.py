"""
Startup Financial OS MVP - Streamlit Application

Main entry point for the Startup Financial OS application.
"""

import streamlit as st
import sys
import os
import yaml
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.core_engine.formulas import METRIC_FUNCS
from src.agent_core.agent_core import SageAgent
from src.infra.logging_conf import setup_logging, log_user_action
from src.wizard.quality_score import calculate_quality_score, get_quality_feedback, calculate_score_delta

# Setup logging
logger = setup_logging()

# Load questions and tips
def load_questions():
    """Load questions from YAML file."""
    questions_path = Path(__file__).parent / "src" / "wizard" / "questions.yml"
    with open(questions_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def load_tips():
    """Load tips from YAML file."""
    tips_path = Path(__file__).parent / "src" / "wizard" / "tips.yml"
    with open(tips_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def create_progress_ring(progress_percent):
    """Create a simple progress ring using HTML/CSS."""
    html = f"""
    <div style="display: flex; justify-content: center; align-items: center;">
        <div style="
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: conic-gradient(#00ff88 {progress_percent}%, #e0e0e0 {progress_percent}%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 14px;
            color: #333;
        ">
            {progress_percent}%
        </div>
    </div>
    """
    return html

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
        
        # Quality Score in sidebar
        if 'quality_score' in st.session_state:
            st.markdown("### 🎯 Quality Score")
            st.metric("Score", f"{st.session_state.quality_score}/100")
            if 'quality_delta' in st.session_state and st.session_state.quality_delta != "0 pts":
                st.caption(f"Δ {st.session_state.quality_delta}")
    
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
    
    # Quality Score
    if 'quality_score' in st.session_state:
        st.subheader("🎯 Startup Quality Score")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.metric("Score", f"{st.session_state.quality_score}/100")
        with col2:
            st.info(get_quality_feedback(st.session_state.quality_score))
    
    # Recent advice
    if 'sage_advice' in st.session_state:
        st.subheader("🤖 Latest Sage Advice")
        st.info(st.session_state.sage_advice)

def show_wizard():
    """Show the wizard interface with enhanced UI."""
    st.header("❓ Financial Model Wizard")
    st.markdown("Answer questions to build your startup's financial model.")
    
    # Initialize session state for wizard
    if 'wizard_answers' not in st.session_state:
        st.session_state.wizard_answers = {}
        st.session_state.current_question = 0
        st.session_state.quality_score = 0
        st.session_state.quality_delta = "0 pts"
    
    # Load questions and tips
    questions = load_questions()
    tips = load_tips()
    
    # Filter questions based on project type
    project_type = st.session_state.wizard_answers.get("project_type", "B2B SaaS")
    filtered_questions = []
    for q in questions:
        if not q.get("branch") or project_type in q.get("branch", []):
            filtered_questions.append(q)
    
    # Progress calculation
    progress_percent = int((st.session_state.current_question + 1) / len(filtered_questions) * 100)
    
    # Header with progress ring
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        st.subheader(f"Step {st.session_state.current_question + 1} of {len(filtered_questions)}")
    
    with col2:
        st.markdown(create_progress_ring(progress_percent), unsafe_allow_html=True)
    
    with col3:
        if 'quality_score' in st.session_state:
            st.metric("Quality", f"{st.session_state.quality_score}/100")
    
    # Main content area
    if st.session_state.current_question < len(filtered_questions):
        question = filtered_questions[st.session_state.current_question]
        
        # Two-column layout
        colQ, colTip = st.columns([3, 1])
        
        with colQ:
            st.subheader(question["text"])
            
            # Input based on question type
            if question["type"] == "select":
                answer = st.selectbox("Select:", question["options"], key=f"q_{question['id']}")
            elif question["type"] == "number":
                answer = st.number_input("Enter value:", value=question.get("default", 0), key=f"q_{question['id']}")
            elif question["type"] == "currency":
                answer = st.number_input("Enter value (USD):", value=float(question.get("default", 0)), key=f"q_{question['id']}")
            elif question["type"] == "percent":
                answer = st.number_input("Enter percentage:", value=float(question.get("default", 0)), min_value=0.0, max_value=100.0, key=f"q_{question['id']}")
            elif question["type"] == "integer":
                answer = st.number_input("Enter number:", value=question.get("default", 0), step=1, key=f"q_{question['id']}")
            
            # Inline benchmark
            if "benchmark" in question:
                st.success(question["benchmark"])
            
            # Navigation buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("⬅️ Previous") and st.session_state.current_question > 0:
                    st.session_state.current_question -= 1
                    st.rerun()
            
            with col2:
                if st.button("⏭️ Skip"):
                    st.session_state.current_question += 1
                    st.rerun()
            
            with col3:
                if st.button("Next ➡️"):
                    # Save answer
                    st.session_state.wizard_answers[question["id"]] = answer
                    
                    # Calculate quality score
                    old_score = st.session_state.quality_score
                    new_score = calculate_quality_score(st.session_state.wizard_answers)
                    st.session_state.quality_score = new_score
                    st.session_state.quality_delta = calculate_score_delta(old_score, new_score)
                    
                    st.session_state.current_question += 1
                    st.rerun()
        
        with colTip:
            # TIP section
            if question.get("tip_id") and question["tip_id"] in tips:
                tip = tips[question["tip_id"]]
                st.markdown("#### 💡 TIP")
                st.markdown(f"**{tip['title']}**")
                st.caption(tip['text'])
                
                # Related questions
                if "related" in tip:
                    st.markdown("**Related:**")
                    for related_id in tip["related"][:3]:  # Show max 3 related
                        for q in questions:
                            if q["id"] == related_id:
                                st.caption(f"🔗 {q['short']}")
                                break
                
                # Score delta
                if 'quality_delta' in st.session_state and st.session_state.quality_delta != "0 pts":
                    delta_color = "green" if "+" in st.session_state.quality_delta else "red"
                    st.markdown(f"<span style='color: {delta_color}; font-weight: bold;'>{st.session_state.quality_delta}</span>", unsafe_allow_html=True)
            
            # Questions progress
            with st.expander("📋 Questions"):
                for i, q in enumerate(filtered_questions):
                    if i < st.session_state.current_question:
                        status = "✅"
                    elif i == st.session_state.current_question:
                        status = "🔄"
                    else:
                        status = "⬜️"
                    st.markdown(f"{status} {q['short']}")
    
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
    
    # Load badges
    badges_path = Path(__file__).parent / "src" / "gamification" / "badges.yml"
    with open(badges_path, 'r', encoding='utf-8') as f:
        badges = yaml.safe_load(f)
    
    # Calculate which badges are earned
    earned_badges = []
    total_points = 0
    
    for badge in badges:
        earned = False
        
        # Check conditions based on badge type
        if badge["id"] == "first_complete":
            earned = True  # Always earned if we're here
        
        elif badge["id"] == "quality_master":
            earned = st.session_state.get('quality_score', 0) >= 80
        
        elif badge["id"] == "quality_expert":
            earned = st.session_state.get('quality_score', 0) >= 60
        
        elif badge["id"] == "quality_improver":
            earned = st.session_state.get('quality_score', 0) >= 40
        
        elif badge["id"] == "runway_optimizer":
            earned = st.session_state.metrics.get('runway', 0) >= 12
        
        elif badge["id"] == "churn_master":
            earned = st.session_state.metrics.get('churn', 0) <= 5
        
        elif badge["id"] == "lean_startup":
            earned = st.session_state.wizard_answers.get('team_size', 1) <= 10
        
        elif badge["id"] == "price_optimizer":
            earned = st.session_state.wizard_answers.get('price', 0) >= 50
        
        elif badge["id"] == "sustainability_expert":
            revenue = st.session_state.metrics.get('mrr', 0)
            burn_rate = st.session_state.metrics.get('burn_rate', 0)
            earned = burn_rate < revenue if revenue > 0 else False
        
        # Add more badge conditions as needed
        
        if earned:
            earned_badges.append(badge)
            total_points += badge.get("points", 0)
    
    # Display total points
    st.metric("Total Points", total_points)
    
    # Display earned badges
    if earned_badges:
        st.subheader("✅ Earned Badges")
        for badge in earned_badges:
            col1, col2 = st.columns([1, 4])
            with col1:
                st.markdown(f"{badge['icon']}")
            with col2:
                st.markdown(f"**{badge['name']}**")
                st.caption(badge['description'])
                st.caption(f"+{badge.get('points', 0)} points")
    
    # Display available badges
    st.subheader("🔒 Available Badges")
    for badge in badges:
        if badge not in earned_badges:
            col1, col2 = st.columns([1, 4])
            with col1:
                st.markdown(f"🔒 {badge['icon']}")
            with col2:
                st.markdown(f"**{badge['name']}**")
                st.caption(badge['description'])
                st.caption(f"+{badge.get('points', 0)} points")

if __name__ == "__main__":
    main() 