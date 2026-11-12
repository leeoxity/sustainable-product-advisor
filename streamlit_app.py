import streamlit as st
from sustainable_advisor_engine import run_advisor

st.set_page_config(page_title="Sustainable Product Advisor", page_icon="🌿", layout="wide")

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


def choose(label, values, key):
    return st.selectbox(label, values, index=None, placeholder="Select an option", key=key)


def yes_no(label, key):
    value = choose(label, ["Yes", "No"], key)
    return None if value is None else value == "Yes"


def add(facts, name, value):
    if value is not None:
        facts[name] = value


facts = {}
required = []


def field(name, value):
    if value is None:
        required.append(name)
    else:
        facts[name] = value


st.subheader("1. Product Information")
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
        st.subheader("2. Repair & Warranty")
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

    if condition in ("working fine", "outdated"):
        st.subheader("3. Reuse & Durability")
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

    st.subheader("4. Borrowing & Alternatives")
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
with right:
    if st.button("Reset Answers"):
        st.session_state.clear()
        st.rerun()

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

st.caption("Academic decision-support prototype. Recommendations depend on the twelve approved IF–THEN rules.")
