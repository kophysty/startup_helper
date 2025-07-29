# Startup Financial OS — MVP

**Tag-line:** *OS-level reliability, game-level usability.*  
AI-агент-кофаундер задаёт 20 «золотых» вопросов, строит P&L / Runway, проверяет цифры по бенчмаркам и каждую неделю присылает совет, как продлить runway.

---

## ✨ Core Features (MVP)
| Module | What it does |
|--------|--------------|
| **Wizard 1.0** | 20 questions with smart defaults (SaaS / e-com branch) |
| **Core Engine 0.1** | Calculates MRR, churn, CAC, burn, runway |
| **Sanity-Check** | 5 benchmark rules (e.g. Runway < 6 m) |
| **Sage Agent** | Chat UI, `calculate_model` + `suggest_changes` |
| **One-Pager Export** | PDF + CSV in 1 click |
| **Gamification Lite** | Progress ring + 3 starter badges |

## 🏗️ Architecture
* Single-process Streamlit app → direct imports (`core_engine`, `agent_core`).
* SQLite file (`sage.db`) for models & chat history.
* Config-driven YAML (questions, badges, rules) ⇒ easy extensions.

## 🚀 Quick Start
```bash
git clone https://github.com/kophysty/startup_helper.git
cd startup_helper
cp env.example .env            # add OpenAI key
poetry install
poetry run streamlit run streamlit_app.py
```

## 🧩 Roadmap
| Week | Goal | Deliverables |
|------|------|--------------|
| 1 | Core Engine | formulas + unit-tests |
| 2 | Wizard + Validation | Streamlit forms, progress ring |
| 3 | One-Pager + Landing | PDF export, wait-list page |
| 4 | Gamification & Agent | badges, feedback log, integration tests |

## 📜 License
MIT — see LICENSE.

## Contact
- GitHub: [@kophysty](https://github.com/kophysty) 