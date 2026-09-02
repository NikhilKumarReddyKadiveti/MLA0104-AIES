"""
IDRRA - Intelligent Disaster Response and Rescue Agent
Integrated Prototype
MLA01 - Artificial Intelligence and Expert Systems

Pipeline:
Disaster Data -> Knowledge Base -> Search (A*) -> Inference (Forward/Backward
Chaining) -> Agent Decision -> Rescue Recommendation
"""

import heapq
import math

# ---------------------------------------------------------------------------
# 1. ENVIRONMENT / MAP  (state-space for the search module)
# ---------------------------------------------------------------------------
# Assumed coordinates (km) used only to compute an admissible straight-line
# heuristic h(n) for A*.
COORDS = {
    "C0": (0, 0),    # Control Center / Depot
    "N1": (2, 1),    # Road junction
    "N2": (1, -2),   # Road junction
    "N3": (-1, 1),   # Road junction
    "L1": (4, 2),    # Building collapse
    "L2": (2, -4),   # Flooded residential area
    "L3": (-2, -1),  # Industrial accident
    "L4": (0, 3),    # Road accident
}

def euclid(a, b):
    (x1, y1), (x2, y2) = COORDS[a], COORDS[b]
    return round(math.hypot(x1 - x2, y1 - y2), 2)

# Road network (undirected). Edge cost = actual travel distance (km).
ROADS = {
    "C0": {"N1": euclid("C0", "N1"), "N2": euclid("C0", "N2"), "N3": euclid("C0", "N3")},
    "N1": {"C0": euclid("C0", "N1"), "L1": euclid("N1", "L1"), "L4": euclid("N1", "L4")},
    "N2": {"C0": euclid("C0", "N2"), "L2": euclid("N2", "L2"), "L3": euclid("N2", "L3")},
    "N3": {"C0": euclid("C0", "N3"), "L3": euclid("N3", "L3"), "L4": euclid("N3", "L4")},
    "L1": {"N1": euclid("N1", "L1"), "L4": euclid("L1", "L4")},
    "L2": {"N2": euclid("N2", "L2")},
    "L3": {"N2": euclid("N2", "L3"), "N3": euclid("N3", "L3")},
    "L4": {"N1": euclid("N1", "L4"), "N3": euclid("N3", "L4")},
}


def a_star(start, goal, graph=ROADS, coords=COORDS):
    """Standard A* search. f(n) = g(n) + h(n). Returns (path, cost, explored)."""
    h = lambda n: euclid(n, goal)
    open_set = [(h(start), 0, start, [start])]
    best_g = {start: 0}
    explored = []

    while open_set:
        f, g, node, path = heapq.heappop(open_set)
        explored.append(node)
        if node == goal:
            return path, g, explored
        for nbr, cost in graph.get(node, {}).items():
            new_g = g + cost
            if nbr not in best_g or new_g < best_g[nbr]:
                best_g[nbr] = new_g
                heapq.heappush(open_set, (new_g + h(nbr), new_g, nbr, path + [nbr]))
    return None, math.inf, explored


# ---------------------------------------------------------------------------
# 2. KNOWLEDGE BASE  (facts derived from the disaster-data feed)
# ---------------------------------------------------------------------------
# Raw facts per location, as reported by field sensors / callers.
FACTS = {
    "L1": {"building_collapse": True, "trapped_people": 12, "smoke_detected": True,
           "fire": False, "toxic_gas": False, "rising_water": False,
           "stranded_people": 0, "injured_people": 0, "ambulance_access": False},
    "L2": {"building_collapse": False, "trapped_people": 0, "smoke_detected": False,
           "fire": False, "toxic_gas": False, "rising_water": True,
           "stranded_people": 20, "injured_people": 0, "ambulance_access": False},
    "L3": {"building_collapse": False, "trapped_people": 0, "smoke_detected": False,
           "fire": True, "toxic_gas": True, "rising_water": False,
           "stranded_people": 0, "injured_people": 0, "ambulance_access": False},
    "L4": {"building_collapse": False, "trapped_people": 0, "smoke_detected": False,
           "fire": False, "toxic_gas": False, "rising_water": False,
           "stranded_people": 0, "injured_people": 4, "ambulance_access": True},
}


# ---------------------------------------------------------------------------
# 3. PRODUCTION RULE BASE (>= 10 rules) -> forward & backward chaining
# ---------------------------------------------------------------------------
# Each rule: (name, set_of_condition_facts, conclusion_fact)
RULES = [
    ("R1", {"building_collapse", "trapped_people"}, "rescue_priority_high"),
    ("R2", {"fire", "toxic_gas"}, "hazmat_team_required"),
    ("R3", {"rising_water", "stranded_people"}, "rescue_boat_required"),
    ("R4", {"injured_people", "ambulance_access"}, "medical_team_required"),
    ("R5", {"building_collapse", "smoke_detected"}, "fire_team_required"),
    ("R6", {"hazmat_team_required"}, "evacuate_surrounding_area"),
    ("R7", {"rescue_boat_required"}, "deploy_water_rescue_unit"),
    ("R8", {"rescue_priority_high", "fire_team_required"}, "multi_team_deployment"),
    ("R9", {"trapped_people", "smoke_detected"}, "structural_collapse_risk"),
    ("R10", {"structural_collapse_risk"}, "drone_survey_required"),
    ("R11", {"toxic_gas"}, "restrict_civilian_access"),
    ("R12", {"medical_team_required", "ambulance_access"}, "route_to_hospital_required"),
]

# Boolean facts derived from the raw counts (>0 => True); used by the engine.
def boolean_facts(loc):
    raw = FACTS[loc]
    bf = set()
    for k, v in raw.items():
        if isinstance(v, bool) and v:
            bf.add(k)
        elif isinstance(v, int) and v > 0:
            bf.add(k)
    return bf


def forward_chain(known_facts, rules=RULES, verbose=True):
    """Data-driven inference: repeatedly fire rules whose conditions are met."""
    facts = set(known_facts)
    fired = []
    changed = True
    while changed:
        changed = False
        for name, conds, concl in rules:
            if conds.issubset(facts) and concl not in facts:
                facts.add(concl)
                fired.append((name, conds, concl))
                changed = True
                if verbose:
                    print(f"  Fired {name}: {conds} -> {concl}")
    return facts, fired


def backward_chain(goal, known_facts, rules=RULES, depth=0, trail=None, verbose=True):
    """Goal-driven inference: prove `goal` by recursively proving its
    sub-conditions via matching rule conclusions."""
    if trail is None:
        trail = []
    pad = "  " * depth
    if goal in known_facts:
        if verbose:
            print(f"{pad}FACT '{goal}' is already known -> TRUE")
        return True, trail
    for name, conds, concl in rules:
        if concl == goal:
            if verbose:
                print(f"{pad}Trying {name}: {goal} <- {conds}")
            all_true = True
            for c in conds:
                ok, trail = backward_chain(c, known_facts, rules, depth + 1, trail, verbose)
                if not ok:
                    all_true = False
            if all_true:
                trail.append(name)
                if verbose:
                    print(f"{pad}{name} succeeds -> '{goal}' is TRUE")
                return True, trail
    if verbose:
        print(f"{pad}No rule / fact proves '{goal}' -> FALSE")
    return False, trail


# ---------------------------------------------------------------------------
# 4. PRIORITY (SEVERITY) SCORING  -- used by the Goal/Utility-based agent
# ---------------------------------------------------------------------------
SEVERITY_WEIGHTS = {
    "trapped_people": 3.0,     # per person, life-critical & entrapped
    "stranded_people": 1.5,    # per person, exposed but mobile-rescue
    "injured_people": 2.0,     # per person, medical urgency
}
HAZARD_BONUS = {
    "fire": 15, "toxic_gas": 15, "building_collapse": 10, "rising_water": 5,
}

def severity_score(loc):
    raw = FACTS[loc]
    score = 0.0
    for k, w in SEVERITY_WEIGHTS.items():
        score += raw.get(k, 0) * w
    for k, b in HAZARD_BONUS.items():
        if raw.get(k):
            score += b
    return round(score, 2)


# ---------------------------------------------------------------------------
# 5. AGENT: perceive -> infer -> decide -> act
# ---------------------------------------------------------------------------
RESOURCE_MAP = {
    "hazmat_team_required": "Fire + Hazmat Team",
    "rescue_boat_required": "Rescue Boat + Water Rescue Team",
    "medical_team_required": "Medical / Ambulance Team",
    "rescue_priority_high": "Rescue + Medical Team",
    "fire_team_required": "Fire Team",
}

def decide_resource(derived_facts):
    for key in ["hazmat_team_required", "rescue_boat_required",
                "rescue_priority_high", "fire_team_required",
                "medical_team_required"]:
        if key in derived_facts:
            return RESOURCE_MAP[key]
    return "General Rescue Team"


def run_scenario(loc):
    print(f"\n{'='*70}\nSCENARIO: {loc}  ({FACTS[loc]})\n{'='*70}")

    # -- Search: route from Control Center to this location --
    path, cost, explored = a_star("C0", loc)
    cost = round(cost, 2)
    print(f"[SEARCH] A* explored nodes: {explored}")
    print(f"[SEARCH] Best route: {' -> '.join(path)}  | path cost g = {cost} km")

    # -- Inference: forward chaining over this location's facts --
    kb = boolean_facts(loc)
    print(f"[KB] Known facts for {loc}: {sorted(kb)}")
    print(f"[FORWARD CHAINING]")
    derived, fired = forward_chain(kb)
    new_conclusions = derived - kb
    print(f"[FORWARD CHAINING] New conclusions: {sorted(new_conclusions)}")

    # -- Inference: backward chaining, prove a key hypothesis --
    hypothesis = {
        "L1": "multi_team_deployment",
        "L2": "deploy_water_rescue_unit",
        "L3": "hazmat_team_required",
        "L4": "route_to_hospital_required",
    }[loc]
    print(f"[BACKWARD CHAINING] Goal: {hypothesis}?")
    proved, trail = backward_chain(hypothesis, kb)
    print(f"[BACKWARD CHAINING] Result: {hypothesis} = {proved} | rule trail: {trail}")

    # -- Agent decision --
    priority = severity_score(loc)
    resource = decide_resource(derived)
    print(f"[AGENT] Severity/priority score = {priority}")
    print(f"[AGENT] Recommended resource     = {resource}")
    print(f"[AGENT] Recommended route        = {' -> '.join(path)} ({cost} km)")

    return {
        "location": loc, "route": path, "route_cost": cost, "explored": explored,
        "facts": kb, "derived": derived, "priority": priority,
        "resource": resource, "backward_goal": hypothesis, "backward_result": proved,
    }


if __name__ == "__main__":
    results = [run_scenario(loc) for loc in ["L1", "L2", "L3", "L4"]]

    print(f"\n{'='*70}\nFINAL DISPATCH ORDER (by severity/priority score, descending)\n{'='*70}")
    ranked = sorted(results, key=lambda r: r["priority"], reverse=True)
    for rank, r in enumerate(ranked, 1):
        print(f"{rank}. {r['location']}  | priority={r['priority']:>5} "
              f"| resource={r['resource']:<28} | route={' -> '.join(r['route'])} "
              f"({r['route_cost']} km)")
