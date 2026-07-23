from collections import deque, defaultdict

def build_tree_from_input():
    print("--- Tree Input ---")
    num_edges = int(input("Enter number of edges (parent-child links): "))
    
    tree = defaultdict(list)
    
    print("\nEnter edges as 'Parent Child' (e.g., A B):")
    for i in range(num_edges):
        line = input(f"Edge {i+1}: ").strip().split()
        if len(line) != 2:
            print("Please enter exactly two values!")
            continue
        # Convert to uppercase automatically to fix casing typos
        parent, child = line[0].upper(), line[1].upper()
        tree[parent].append(child)
        
        # Ensure leaf nodes exist in the tree dictionary
        if child not in tree:
            tree[child] = []

    return tree

def bfs(tree, start_node):
    visited = set([start_node])
    queue = deque([start_node])
    order = []

    while queue:
        curr = queue.popleft()
        order.append(curr)
        for child in tree[curr]:
            if child not in visited:
                visited.add(child)
                queue.append(child)
    return order

def dfs(tree, start_node):
    visited = set()
    order = []

    def _dfs(node):
        visited.add(node)
        order.append(node)
        for child in tree[node]:
            if child not in visited:
                _dfs(child)

    _dfs(start_node)
    return order

if __name__ == "__main__":
    user_tree = build_tree_from_input()
    start = input("\nEnter starting root node: ").strip().upper()

    print("\n--- Correct Tree Results ---")
    print(f"BFS Order: ", " -> ".join(bfs(user_tree, start)))
    print(f"DFS Order: ", " -> ".join(dfs(user_tree, start)))
