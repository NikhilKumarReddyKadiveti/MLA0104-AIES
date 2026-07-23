import heapq
from collections import defaultdict

def build_weighted_graph():
    print("--- Uniform Cost Search (UCS) Runner ---")
    is_directed = input("Is the graph directed? (y/n): ").strip().lower() == 'y'
    num_edges = int(input("Enter number of edges: "))
    
    graph = defaultdict(list)
    print("\nEnter edges as 'Node1 Node2 Weight' (e.g., A B 5 or 0 1 10):")
    for i in range(num_edges):
        raw = input(f"Edge {i+1}: ").strip().split()
        if len(raw) != 3:
            print("  [!] Please enter 3 values: Node1 Node2 Weight")
            continue
        
        u, v = raw[0].upper(), raw[1].upper()
        weight = float(raw[2])
        
        graph[u].append((v, weight))
        if not is_directed:
            graph[v].append((u, weight))
            
        if v not in graph:
            graph[v] = []

    return graph

def uniform_cost_search(graph, start_node, goal_node):
    # Priority Queue stores tuples of: (total_cost, current_node, path)
    priority_queue = [(0, start_node, [start_node])]
    visited = set()

    while priority_queue:
        # Pop node with the MINIMUM total path cost g(n)
        cost, curr_node, path = heapq.heappop(priority_queue)

        if curr_node in visited:
            continue
        
        visited.add(curr_node)

        # Check if we reached the goal
        if curr_node == goal_node:
            return path, cost

        # Explore neighbors
        for neighbor, edge_cost in graph[curr_node]:
            if neighbor not in visited:
                total_cost = cost + edge_cost
                heapq.heappush(priority_queue, (total_cost, neighbor, path + [neighbor]))

    return None, float('inf') # Goal not reachable

if __name__ == "__main__":
    user_graph = build_weighted_graph()
    
    start = input("\nEnter starting node: ").strip().upper()
    goal = input("Enter goal node: ").strip().upper()

    path, total_cost = uniform_cost_search(user_graph, start, goal)

    print("\n--- Results ---")
    if path:
        print(f"Optimal Path :  {' -> '.join(path)}")
        print(f"Total Cost   :  {total_cost}")
    else:
        print(f"No path found from '{start}' to '{goal}'.")