# Changelog

## [0.2.0] - 2025-07-31

### ✨ Added
- **Enhanced Wizard UI** with two-column layout
- **Contextual Tips** - inline benchmarks and right sidebar tips
- **Progress Ring** - visual progress indicator instead of linear bar
- **Startup Quality Score** - real-time scoring system (0-100)
- **Score Delta** - shows points gained/lost with each answer
- **Related Questions** - shows connections between metrics
- **Questions Progress Map** - expandable list of all questions
- **Enhanced Badges** - new quality-based achievements
- **Skip Button** - allows users to skip questions
- **Better Navigation** - Previous/Skip/Next buttons

### 🎯 New Features
- **Quality Score Calculation** based on:
  - Churn rate (< 5% = +20 points)
  - CAC/LTV ratio (< 0.3 = +15 points)
  - Runway (12+ months = +15 points)
  - Burn rate (below revenue = +15 points)
  - Growth rate (20%+ = +15 points)
  - Team size (lean = +10 points)
  - Price point ($100+ = +10 points)

### 🏆 New Badges
- **Quality Master** (80+ score)
- **Quality Expert** (60+ score)
- **Quality Improver** (40+ score)
- **Lean Startup** (team < 10)
- **Price Optimizer** (price > $50)
- **Growth Hacker** (20%+ growth)

### 📊 UI Improvements
- **Inline Benchmarks** - industry standards shown under each field
- **TIP Column** - contextual help and related metrics
- **Progress Ring** - circular progress indicator
- **Score Feedback** - real-time quality assessment
- **Enhanced Navigation** - better button layout

### 🔧 Technical
- **YAML Configuration** - questions and tips in separate files
- **Modular Design** - quality score calculator as separate module
- **Session State** - improved state management
- **Responsive Layout** - better mobile experience

## [0.1.0] - 2025-07-30

### 🚀 Initial Release
- Basic Streamlit application
- Wizard with 8 questions
- Core financial calculations
- Sage AI Agent
- Basic badges system
- Dashboard with metrics 