
# ========================================================================================================================
# EXPERT SYSTEM - KNOWLEDGE BASE AND INFERENCE ENGINE
# ========================================================================================================================

import streamlit as st

# Fix compatibility with older Experta dependencies
import collections
import collections.abc
for name in ("Mapping", "MutableMapping", "Sequence", "Set", "Hashable", "Iterable"):
    if not hasattr(collections, name):
        setattr(collections, name, getattr(collections.abc, name))

from experta import Fact, Rule, KnowledgeEngine, OR

# Expert system with 12 decision rules
class SustainableAdvisor(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.result = None
# Save the selected recommendation and stop the program
    def recommend(self, number, title, explanation):
        self.declare(Fact(
            recommendation=title,
            explanation=explanation,
            rule_number=number
        ))
        self.result = {
            "rule": number,
            "recommendation": title,
            "explanation": explanation
        }
        self.halt()

    # Rule 1
    @Rule(Fact(item_condition="working fine", current_need="still needed"), salience=110)
    def rule_1_reuse(self):
        self.recommend(1, "Reuse", "Continue using the working item without modification or replacement.")

    # Rule 2
    @Rule(Fact(item_condition="minor damage", repair_feasibility="feasible",
               repair_cost_below_half=True), salience=80)
    def rule_2_repair(self):
        self.recommend(2, "Repair", "Repair the minor defect instead of replacing the item.")

    # Rule 3
    @Rule(Fact(item_condition="major damage", repair_feasibility="unfeasible",current_need="still needed",
               need_duration="short-term"), salience=60)
    def rule_3_borrow(self):
        self.recommend(3, "Borrowing", "Borrow a temporary replacement instead of buying a new item.")

    # Rule 4
    @Rule(Fact(item_condition="working fine", current_need="no longer needed",
               personal_repurposing="not feasible", resale_value="low or none",
               donation_available=True), salience=90)
    def rule_4_donate(self):
        self.recommend(4, "Donation", "Donate this working item to someone who needs it.")

    # Rule 5
    @Rule(Fact(item_condition="outdated", upgrade_feasibility="feasible",
               upgrade_cost_below_half=True), salience=70)
    def rule_5_upgrade(self):
        self.recommend(5, "Upgrade", "Improve the item instead of buying a replacement.")

    # Rule 6
    @Rule(Fact(item_condition="major damage", repair_feasibility="unfeasible",current_need="no longer needed",
               contains_hazardous_parts=False, reusable_parts=True), salience=10)
    def rule_6_parts_recovery(self):
        self.recommend(
            6,
            "Parts Recovery",
            "Recover functional parts from the damaged product for reuse.")

    # Rule 7
    @Rule(Fact(usage_frequency="occasionally", borrowing_available=True), salience=50)
    def rule_7_borrow(self):
        self.recommend(7, "Borrowing", "Borrow a rarely needed product rather than buying a new one.")

    # Rule 8
    @Rule(Fact(item_condition="working fine", current_need="no longer needed",
               personal_repurposing="feasible"), salience=100)
    def rule_8_repurpose(self):
        self.recommend(8, "Reuse", "Repurpose the working item for another useful function.")

    # Rule 9
    @Rule(Fact(item_condition="outdated", upgrade_feasibility="unfeasible",
               current_need="still needed", remaining_useful_life="short",
               durable_replacement_available=True), salience=20)
    def rule_9_replace_outdated(self):
        self.recommend(9, "Replacement", "Select a durable replacement for an outdated, non-upgradable item.")

    # Rule 10
    @Rule(Fact(item_condition="major damage", repair_feasibility="unfeasible",current_need="still needed",
               need_duration="long-term", secondhand_available=True,
               secondhand_cost_below_half=True), salience=40)
    def rule_10_secondhand(self):
        self.recommend(10, "Second-hand Purchase", "Buy a suitable second-hand product instead of a new one.")

    # Rule 11
    @Rule(
        OR(
            Fact(item_condition="major damage", repair_feasibility="unfeasible",current_need="still needed",
                 need_duration="long-term", secondhand_available=False),
            Fact(item_condition="major damage", repair_feasibility="unfeasible",current_need="still needed",
                 need_duration="long-term", secondhand_available=True,
                 secondhand_cost_below_half=False)
        ),
        salience=30
    )
    def rule_11_replacement(self):
        self.recommend(11, "Replacement", "Choose a durable, repairable new item instead of an unsuitable used alternative.")

    # Rule 12
    @Rule(
        OR(
            Fact(item_condition="minor damage", warranty_valid=True, misuse_damage=False),
            Fact(item_condition="major damage", warranty_valid=True, misuse_damage=False)
        ),
        salience=120
    )
    def rule_12_warranty(self):
        self.recommend(12, "Repair under Warranty", "Check the manufacturer's warranty remedy before paying for repairs or replacement.")

# Run the expert system using the user's answers
def run_advisor(inputs):
    engine = SustainableAdvisor()
    engine.reset()
    engine.declare(Fact(**inputs))
    engine.run()
    
    return engine.result or {
        "rule": None,
        "recommendation": "Further Evaluation Needed",
        "explanation": (
            "The provided product information does not match any of the "
            "current decision rules. Consider reviewing the product's "
            "condition and available alternatives before making a decision."
        )
    }


# ========================================================================================================================
# STREAMLIT USER INTERFACE
# ========================================================================================================================

st.set_page_config(page_title="Sustainable Product Advisor", page_icon="🌿", layout="wide")

if "reset_count" not in st.session_state:
    st.session_state.reset_count = 0

st.markdown("""
<style>
.block-container {max-width: 1080px; padding-top: 2rem; padding-bottom: 4rem;}
h1, h2, h3 {color: #245c43;}
[data-testid="stButton"] button[kind="primary"] {background: #245c43; border-color: #245c43;}
</style>
""", unsafe_allow_html=True)

st.title("Sustainable Product Advisor")
st.caption("CPCS-331  |  Python + Experta  |  Forward Chaining")
st.write("Answer the relevant questions to receive a sustainable product recommendation.")


# Create a dropdown question
def choose(label, values, key):
    return st.selectbox(
        label,
        values,
        index=None,
        placeholder="Select an option",
        key=f"{key}_{st.session_state.reset_count}"
    )

# Convert Yes/No answers into Boolean values
def yes_no(label, key):
    value = choose(label, ["Yes", "No"], key)
    return None if value is None else value == "Yes"


def add(facts, name, value):
    if value is not None:
        facts[name] = value


facts = {}
required = []

# Store answers and track missing fields
def field(name, value):
    if value is None:
        required.append(name)
    else:
        facts[name] = value

# Basic product information
st.subheader("📦 Product Information")
with st.container(border=True):
    left, right = st.columns(2)
    with left:
        condition = choose("Item condition", ["working fine", "minor damage", "major damage", "outdated", "not owned"], "condition")
        field("item_condition", condition)
    with right:
        if condition == "not owned":
            needed = yes_no("Do you need to obtain this product?", "need_to_obtain")
            if needed is None:
                required.append("Do you need this product?")
            else:
                facts["current_need"] = "still needed" if needed else "no longer needed"
        elif condition:
            field("current_need", choose("Current functional need", ["still needed", "no longer needed"], "current_need"))

    left, right = st.columns(2)
    with left:
        field("usage_frequency", choose("Usage frequency", ["occasionally", "frequently"], "frequency"))
    with right:
        if condition in ("major damage", "not owned"):
            field("need_duration", choose("How long is the product needed?", ["short-term", "long-term"], "duration"))

no_purchase = condition == "not owned" and facts.get("current_need") == "no longer needed"
if no_purchase:
    st.info("You do not need this product. Avoiding an unnecessary purchase is the most sustainable option.")

if condition and not no_purchase:
    if condition in ("minor damage", "major damage"):
# Repair options and warranty details
        st.subheader("🔧 Repair & Warranty")
        with st.container(border=True):
            left, right = st.columns(2)
            with left:
                warranty = yes_no("Is the warranty valid?", "warranty")
                field("warranty_valid", warranty)
            with right:
                if warranty is True:
                    field("misuse_damage", yes_no("Was the damage caused by misuse?", "misuse"))
            left, right = st.columns(2)
            with left:
                repair = choose("Repair feasibility", ["feasible", "unfeasible"], "repair")
                field("repair_feasibility", repair)
            with right:
                if repair == "feasible":
                    field("repair_cost_below_half", yes_no("Repair cost below 50% of a new item?", "repair_cost"))
            if condition == "major damage" and repair == "unfeasible":
                left, right = st.columns(2)
                with left:
                    hazardous = yes_no("Contains batteries, electronics or hazardous materials?", "hazardous")
                    field("contains_hazardous_parts", hazardous)
                with right:
                    if hazardous is False:
                        field("reusable_parts", yes_no("Are functional reusable parts available?", "parts"))

    if condition == "outdated" or (
        condition == "working fine"
        and facts.get("current_need") == "no longer needed"
    ):
# Reuse and upgrade options
        st.subheader("♻️ Reuse & Durability")
        with st.container(border=True):
            if condition == "working fine" and facts.get("current_need") == "no longer needed":
                field("personal_repurposing", choose("Can you repurpose the product?", ["feasible", "not feasible"], "repurpose"))
                if facts.get("personal_repurposing") == "not feasible":
                    left, right = st.columns(2)
                    with left:
                        field("resale_value", choose("Resale value", ["low or none", "high"], "resale"))
                    with right:
                        field("donation_available", yes_no("Is donation available?", "donation"))
            if condition == "outdated":
                upgrade = choose("Upgrade feasibility", ["feasible", "unfeasible"], "upgrade")
                field("upgrade_feasibility", upgrade)
                if upgrade == "feasible":
                    field("upgrade_cost_below_half", yes_no("Upgrade cost below 50% of a new item?", "upgrade_cost"))
                elif upgrade == "unfeasible":
                    field("remaining_useful_life", choose("Remaining useful life", ["short", "long"], "life"))
# Borrowing and replacement alternatives
    st.subheader("🔄 Borrowing & Alternatives")
    with st.container(border=True):
        left, right = st.columns(2)
        with left:
            field("borrowing_available", yes_no("Is borrowing available?", "borrowing"))
        with right:
            if condition in ("major damage", "outdated", "not owned"):
                secondhand = yes_no("Is a second-hand option available?", "secondhand")
                field("secondhand_available", secondhand)
                if secondhand is True:
                    field("secondhand_cost_below_half", yes_no("Used price below 50% of a new item?", "used_cost"))
        if condition == "outdated":
            field("durable_replacement_available", yes_no("Is a durable new replacement available?", "durable"))

st.divider()
left, right = st.columns([1, 3])
with left:
    submitted = st.button("Get Recommendation", type="primary", use_container_width=True)
# Reset all questions to their initial state
with right:
    if st.button("Reset Answers"):
        st.session_state.reset_count += 1
        st.rerun()


# Check the answers and display the recommendation
if submitted:
    if required and not no_purchase:
        st.warning("Please answer all applicable questions before getting your recommendation.")
    elif no_purchase:
        st.success("Recommendation: No purchase needed")
        st.write("**Reason:** Avoid purchasing products you do not need.")
    else:
        try:
            result = run_advisor(facts)
            st.success(f"Recommendation: {result['recommendation']}")
            st.write(f"**Reason:** {result['explanation']}")
            st.write(f"**Rule applied:** {result['rule'] if result['rule'] is not None else 'None'}")
        except Exception as error:
            st.error(f"The expert system could not run: {error}")

