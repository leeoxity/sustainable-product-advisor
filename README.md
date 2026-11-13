
# Sustainable Product Advisor

**A Rule-Based Expert System for Sustainable Purchasing and Product Reuse**

A university group project developed for **CPCS-331: Artificial Intelligence I** at King Abdulaziz University.

## About the Project

Sustainable Product Advisor is a rule-based expert system designed to help users make environmentally responsible purchasing decisions.

Instead of immediately replacing an existing product, the system evaluates its condition, repair feasibility, remaining useful life, and available alternatives to recommend a more sustainable option.

The system aims to reduce unnecessary consumption, extend product lifespans, and encourage responsible use of resources.

## Features

- Interactive web interface with a single-page questionnaire.
- Questions that adapt to the selected product condition.
- A knowledge base containing 12 IF–THEN rules.
- Forward chaining for rule-based reasoning.
- Automatic recommendation based on user-provided information.
- Rule priorities to resolve conflicting recommendations.
- Clear explanations and identification of the applied rule.
- Reset Answers button to restart the questionnaire.
- Accessible through a web browser without installing software.

## Recommendations

Depending on the user's answers, the system may recommend:

| Recommendation | Description |
|---|---|
| Reuse | Continue using or repurpose a functional product. |
| Repair | Fix a damaged product instead of replacing it. |
| Borrowing | Borrow a product needed temporarily or occasionally. |
| Second-Hand Purchase | Purchase a suitable used product instead of a new one. |
| Replacement | Choose a durable replacement when necessary. |
| Donation | Give an unwanted functional product to someone who needs it. |
| Upgrade | Improve an outdated product rather than replacing it. |
| Parts Recovery | Recover functional components from a damaged product. |
| Repair under Warranty | Request manufacturer service when warranty conditions are met. |

If no rule matches the provided information, the system displays a "No matching rule" message.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Experta | Rule-based expert system and inference engine |
| Streamlit | Interactive web interface |
| GitHub | Source code hosting and version control |
| Streamlit Community Cloud | Web application deployment |

## How the System Works

1. The user provides information about the product through the web interface.
2. The system collects relevant facts from the user's answers.
3. The Experta inference engine evaluates the 12 IF–THEN rules using forward chaining.
4. If multiple rules match, rule priorities (salience) determine the selected recommendation.
5. The system displays the final recommendation, explanation, and applied rule number.

## Project Structure

```text
sustainable-product-advisor/
│
├── sustainable_advisor_app.py
├── requirements.txt
└── README.md
```

**sustainable_advisor_app.py** — Contains the complete application, including the Streamlit web interface, 12 IF–THEN rules, Experta inference engine, and recommendation logic.

**requirements.txt** — Lists the required Python libraries.

**README.md** — Provides project documentation.

## Run Locally

Install the required dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the application:

```bash
python -m streamlit run sustainable_advisor_app.py
```

The application will open in your web browser.

## Live Application

Try the Sustainable Product Advisor online:

**[Open the Application](https://sustainable-appuct-advisor-g12.streamlit.app/)**

## Academic Information

**University:** King Abdulaziz University

**Course:** CPCS-331 – Artificial Intelligence I

**Semester:** Fall 2026

**Project Type:** Group Project – Rule-Based Expert System

## Disclaimer

This application is an academic decision-support prototype. Its recommendations are based on predefined rules and user-provided information and should not be considered professional product repair or safety advice.

---

*Developed as part of the CPCS-331 Artificial Intelligence I group project.*
