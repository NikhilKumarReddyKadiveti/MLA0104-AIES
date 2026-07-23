import heapq
from collections import defaultdict

def build_unweighted_heuristic_graph():
    print("--- Greedy Best-First Search (No Edge Costs) ---")
    is_directed = input("Is the graph directed? (y/n): ").strip().lower() == 'y'
    num_edges = int(input("Enter number of edges: "))
    
    graph = defaultdict(list)
    print("\nEnter edges as 'Node1 Node2' (e.g., S A or 0 1):")
    for i in range(num_edges):
        raw = input(f"Edge {i+1}: ").strip().split()
        if len(raw) != 2:
            print("  [!] Please enter 2 space-separated nodes.")
            continue
        
        u, v = raw[0].upper(), raw[1].upper()
        
        graph[u].append(v)
        if not is_directed:
            graph[v].append(u)
            
        if v not in graph:
            graph[v] = []

    # Get heuristic values h(n) for each node
    print("\nEnter heuristic values h(n) for each node:")
    heuristics = {}
    
    all_nodes = set(graph.keys())
    for u in graph:
        for v in graph[u]:
            all_nodes.add(v)
            
    for node in sorted(all_nodes):
        h_val = float(input(f"  h({node}): "))
        heuristics[node] = h_val

    return graph, heuristics

def greedy_best_first_search(graph, heuristics, start_node, goal_node):
    # Priority Queue stores: (h_score, current_node, path)
    # Decisions are made ONLY using h(n)
    start_h = heuristics.get(start_node, 0)
    priority_queue = [(start_h, start_node, [start_node])]
    visited = set()

    while priority_queue:
        # Always pick the node with the lowest h(n)
        h, curr_node, path = heapq.heappop(priority_queue)

        if curr_node in visited:
            continue
            
        visited.add(curr_node)

        # Goal check
        if curr_node == goal_node:
            return path, h

        # Explore neighbors
        for neighbor in graph[curr_node]:
            if neighbor not in visited:
                neighbor_h = heuristics.get(neighbor, 0)
                heapq.heappush(priority_queue, (neighbor_h, neighbor, path + [neighbor]))

    return None, float('inf')

if __name__ == "__main__":
    user_graph, user_heuristics = build_unweighted_heuristic_graph()
    
    start = input("\nEnter starting node: ").strip().upper()
    goal = input("Enter goal node: ").strip().upper()

    path, goal_h = greedy_best_first_search(user_graph, user_heuristics, start, goal)

    print("\n--- GBFS Results ---")
    if path:
        print(f"Path Found   :  {' -> '.join(path)}")
        print(f"Number of Steps :  {len(path) - 1}")
    else:
        print(f"No path found from '{start}' to '{goal}'.")