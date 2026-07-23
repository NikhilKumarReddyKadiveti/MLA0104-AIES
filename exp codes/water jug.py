from collections import deque

def get_possible_next_states(current_state, capacities, allow_fill, allow_empty):
    next_states = []
    num_jugs = len(capacities)

    # RULE 1: Fill any jug completely to its max capacity (If allowed)
    if allow_fill:
        for i in range(num_jugs):
            if current_state[i] < capacities[i]:
                new_state = list(current_state)
                new_state[i] = capacities[i]
                next_states.append(tuple(new_state))

    # RULE 2: Empty any jug completely to 0 (If allowed)
    if allow_empty:
        for i in range(num_jugs):
            if current_state[i] > 0:
                new_state = list(current_state)
                new_state[i] = 0
                next_states.append(tuple(new_state))

    # RULE 3: Pour / Swap water from jug i to jug j (Always Allowed)
    for i in range(num_jugs):
        for j in range(num_jugs):
            if i != j and current_state[i] > 0 and current_state[j] < capacities[j]:
                # Calculate how much water can be transferred
                pour_amount = min(current_state[i], capacities[j] - current_state[j])
                
                new_state = list(current_state)
                new_state[i] -= pour_amount
                new_state[j] += pour_amount
                next_states.append(tuple(new_state))

    return next_states

def solve_water_jug(capacities, initial_state, goal_input, allow_fill, allow_empty):
    # Setup BFS Queue: stores (current_state, path_history)
    queue = deque([(initial_state, [initial_state])])
    visited = set([initial_state])

    while queue:
        current_state, path = queue.popleft()

        # CHECK GOAL CONDITION
        # Case A: User gave a single target number (e.g., target = 4 in ANY jug)
        if isinstance(goal_input, int):
            if goal_input in current_state:
                return path
        # Case B: User specified exact final state for all jugs (e.g., (2, 0, 2))
        elif isinstance(goal_input, tuple):
            if current_state == goal_input:
                return path

        # Generate valid next moves
        for next_state in get_possible_next_states(current_state, capacities, allow_fill, allow_empty):
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, path + [next_state]))

    return None

if __name__ == "__main__":
    print("=== Universal Water Jug Solver ===")
    
    # 1. Jug Capacities
    capacities = tuple(map(int, input("Enter capacities of all jugs (e.g., 5 3 or 8 5 3): ").strip().split()))
    
    # 2. Initial State
    use_custom_start = input("Do jugs start with specific water levels? (y/n): ").strip().lower() == 'y'
    if use_custom_start:
        initial_state = tuple(map(int, input(f"Enter initial water in all {len(capacities)} jugs: ").strip().split()))
    else:
        initial_state = tuple([0] * len(capacities)) # All empty by default

    # 3. Rule Toggles
    allow_fill = input("Is filling from infinite source allowed? (y/n): ").strip().lower() == 'y'
    allow_empty = input("Is emptying water completely allowed? (y/n): ").strip().lower() == 'y'

    # 4. Target Definition
    target_type = input("\nGoal type: [1] Any single jug reaches target volume  [2] Exact state for all jugs (Choice 1 or 2): ").strip()
    
    if target_type == '1':
        goal_input = int(input("Enter target volume for a jug: ").strip())
    else:
        goal_input = tuple(map(int, input(f"Enter exact target values for all {len(capacities)} jugs: ").strip().split()))

    # Run Solver
    solution_path = solve_water_jug(capacities, initial_state, goal_input, allow_fill, allow_empty)

    print("\n--- SOLUTION STEPS ---")
    if solution_path:
        print(f"Total steps: {len(solution_path) - 1}\n")
        for step_idx, state in enumerate(solution_path):
            print(f"Step {step_idx}: Jug Levels = {state}")
    else:
        print("No solution exists for these parameters and rule constraints.")