# Compatibility for Experta's older frozendict dependency
import collections
import collections.abc
for name in ("Mapping", "MutableMapping", "Sequence", "Set", "Hashable", "Iterable"):
    if not hasattr(collections, name):
        setattr(collections, name, getattr(collections.abc, name))

from experta import Fact, Rule, KnowledgeEngine, OR


class SustainableAdvisor(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.result = None

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
    @Rule(Fact(item_condition="major damage", repair_feasibility="unfeasible",
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
    @Rule(Fact(item_condition="major damage", repair_feasibility="unfeasible",
               contains_hazardous_parts=False, reusable_parts=True), salience=10)
    def rule_6_parts_recovery(self):
        self.recommend(6, "Parts Recovery", "Recover functional, non-hazardous parts for reuse.")

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
    @Rule(Fact(item_condition="major damage", repair_feasibility="unfeasible",
               need_duration="long-term", secondhand_available=True,
               secondhand_cost_below_half=True), salience=40)
    def rule_10_secondhand(self):
        self.recommend(10, "Second-hand Purchase", "Choose a suitable used item costing less than half the new-item price.")

    # Rule 11
    @Rule(
        OR(
            Fact(item_condition="major damage", repair_feasibility="unfeasible",
                 need_duration="long-term", secondhand_available=False),
            Fact(item_condition="major damage", repair_feasibility="unfeasible",
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


def run_advisor(inputs):
    engine = SustainableAdvisor()
    engine.reset()
    engine.declare(Fact(**inputs))
    engine.run()
    return engine.result or {
        "rule": None,
        "recommendation": "No matching rule",
        "explanation": "The knowledge base has no rule for these inputs."
    }


if __name__ == "__main__":
    example = {
        "item_condition": "minor damage",
        "repair_feasibility": "feasible",
        "repair_cost_below_half": True,
        "warranty_valid": False
    }
    print(run_advisor(example))
