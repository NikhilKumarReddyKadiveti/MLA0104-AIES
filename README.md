AI Search Algorithms Reference Guide

1. BREADTH-FIRST SEARCH (BFS)

Overview:
Breadth-First Search is an uninformed search strategy that explores a graph or tree level-by-level. It expands all neighbors of a node before moving deeper into the graph.

Pseudocode:
FUNCTION BreadthFirstSearch(Graph, StartNode, GoalNode):
CREATE Queue
CREATE VisitedSet

```
ENQUEUE StartNode INTO Queue
ADD StartNode TO VisitedSet

WHILE Queue IS NOT EMPTY:
    CurrentNode = DEQUEUE From Queue
    
    IF CurrentNode IS GoalNode:
        RETURN Success / Reconstructed Path
        
    FOR EACH Neighbor IN Graph[CurrentNode]:
        IF Neighbor NOT IN VisitedSet:
            ADD Neighbor TO VisitedSet
            ENQUEUE Neighbor INTO Queue
            
RETURN Failure (Goal not reachable)

```

Explanation:

* Data Structure: Uses a First-In, First-Out (FIFO Queue).
* Behavior: Guarantees finding the shortest path in unweighted graphs because it checks every node at depth d before moving to depth d+1.

Complexities and Properties:

* Time Complexity: O(|V| + |E|) or O(b^d) where b is the branching factor and d is depth.
* Space Complexity: O(|V|) or O(b^d) (Memory intensive due to storing all frontier nodes).
* Completeness: Complete (if branching factor b is finite).
* Optimality: Optimal for unweighted graphs (step costs are equal).

Real-World Use Cases:

* Shortest path routing in unweighted networks (e.g., social network connections like degrees of separation).
* Web crawlers discovering nearby links.
* Finding the minimum number of moves in simple puzzle games (e.g., Water Jug Problem).

2. DEPTH-FIRST SEARCH (DFS)

Overview:
Depth-First Search explores as deep as possible down each branch before backtracking. It traverses down to a leaf node before returning to explore adjacent unexplored branches.

Pseudocode:
FUNCTION DepthFirstSearch(Graph, CurrentNode, GoalNode, VisitedSet):
ADD CurrentNode TO VisitedSet

```
IF CurrentNode IS GoalNode:
    RETURN Success
    
FOR EACH Neighbor IN Graph[CurrentNode]:
    IF Neighbor NOT IN VisitedSet:
        Result = DepthFirstSearch(Graph, Neighbor, GoalNode, VisitedSet)
        IF Result IS Success:
            RETURN Success
            
RETURN Failure (Backtrack)

```

Explanation:

* Data Structure: Uses a Last-In, First-Out (LIFO Stack) or implicit system Call Stack via recursion.
* Behavior: Plunges down a single path until hitting a dead end or visited node, then backtracks up one level to try alternative paths.

Complexities and Properties:

* Time Complexity: O(|V| + |E|) or O(b^m) where m is maximum tree depth.
* Space Complexity: O(m) (Linear memory bound to maximum depth).
* Completeness: Not complete on infinite-depth graphs or cyclic graphs without visited checks.
* Optimality: Not optimal (may return a long, indirect path to goal).

Real-World Use Cases:

* Solving maze puzzles and topological sorting.
* Cycle detection in graphs.
* Game decision trees where memory is limited and deep exploration is acceptable.

3. UNIFORM COST SEARCH (UCS)

Overview:
Uniform Cost Search (Dijkstra's Algorithm adaptation) is an uninformed search strategy that expands the node with the lowest path cost g(n) from the start node.

Pseudocode:
FUNCTION UniformCostSearch(Graph, StartNode, GoalNode):
CREATE PriorityQueue (Min-Heap sorted by g(n))
CREATE VisitedSet

```
INSERT (Cost = 0, Node = StartNode, Path = [StartNode]) INTO PriorityQueue

WHILE PriorityQueue IS NOT EMPTY:
    (CurrentCost, CurrentNode, CurrentPath) = POP MIN FROM PriorityQueue
    
    IF CurrentNode IN VisitedSet:
        CONTINUE
        
    ADD CurrentNode TO VisitedSet
    
    IF CurrentNode IS GoalNode:
        RETURN CurrentPath, CurrentCost
        
    FOR EACH (Neighbor, StepCost) IN Graph[CurrentNode]:
        IF Neighbor NOT IN VisitedSet:
            NewCost = CurrentCost + StepCost
            INSERT (NewCost, Neighbor, CurrentPath + [Neighbor]) INTO PriorityQueue
            
RETURN Failure

```

Explanation:

* Formula: Evaluates nodes purely on accumulated path cost: f(n) = g(n).
* Behavior: Expands outward in concentric contours of equal path cost, ensuring the first time a goal node is expanded, the cheapest path has been found.

Complexities and Properties:

* Time Complexity: O(b^(1 + floor(C* / epsilon))) where C* is the optimal solution cost and epsilon is minimum step cost.
* Space Complexity: O(b^(1 + floor(C* / epsilon))).
* Completeness: Complete if every edge cost >= epsilon > 0.
* Optimality: Optimal for weighted graphs with non-negative edge weights.

Real-World Use Cases:

* GPS navigation systems finding cheapest fuel/toll routes.
* Network routing protocols (e.g., OSPF finding shortest transmission paths).

4. GREEDY BEST-FIRST SEARCH (GBFS)

Overview:
Greedy Best-First Search is an informed (heuristic) search strategy that always expands the node that appears closest to the goal based solely on a heuristic function h(n).

Pseudocode:
FUNCTION GreedyBestFirstSearch(Graph, Heuristics, StartNode, GoalNode):
CREATE PriorityQueue (Min-Heap sorted by h(n))
CREATE VisitedSet

```
INSERT (h(StartNode), StartNode, Path = [StartNode]) INTO PriorityQueue

WHILE PriorityQueue IS NOT EMPTY:
    (CurrentH, CurrentNode, CurrentPath) = POP MIN FROM PriorityQueue
    
    IF CurrentNode IN VisitedSet:
        CONTINUE
        
    ADD CurrentNode TO VisitedSet
    
    IF CurrentNode IS GoalNode:
        RETURN CurrentPath
        
    FOR EACH Neighbor IN Graph[CurrentNode]:
        IF Neighbor NOT IN VisitedSet:
            INSERT (Heuristics[Neighbor], Neighbor, CurrentPath + [Neighbor]) INTO PriorityQueue
            
RETURN Failure

```

Explanation:

* Formula: Evaluates nodes purely on estimated distance to goal: f(n) = h(n).
* Behavior: Rapidly pushes toward the goal by prioritizing nodes with low h(n) values, ignoring path costs incurred so far.

Complexities and Properties:

* Time Complexity: O(b^m) in worst cases with inaccurate heuristics, but can approach O(d) with good heuristics.
* Space Complexity: O(b^m) (stores all generated nodes in memory).
* Completeness: Incomplete (can get trapped in loops if visited nodes aren't tracked).
* Optimality: Not optimal (can choose a high-cost path because individual steps looked promising).

Real-World Use Cases:

* Fast pathfinding when speed matters more than finding the absolute shortest route.
* Initial heuristic exploration in complex decision landscapes.

5. A* SEARCH ALGORITHM

Overview:
A* Search combines the path cost g(n) from UCS and the heuristic estimate h(n) from GBFS to achieve optimal, complete, and efficient pathfinding.

Pseudocode:
FUNCTION AStarSearch(Graph, Heuristics, StartNode, GoalNode):
CREATE PriorityQueue (Min-Heap sorted by f(n) = g(n) + h(n))
CREATE Map gScores WITH DEFAULT infinity
CREATE VisitedSet

```
gScores[StartNode] = 0
fStart = 0 + Heuristics[StartNode]

INSERT (fStart, g = 0, Node = StartNode, Path = [StartNode]) INTO PriorityQueue

WHILE PriorityQueue IS NOT EMPTY:
    (CurrentF, CurrentG, CurrentNode, CurrentPath) = POP MIN FROM PriorityQueue
    
    IF CurrentNode IN VisitedSet:
        CONTINUE
        
    ADD CurrentNode TO VisitedSet
    
    IF CurrentNode IS GoalNode:
        RETURN CurrentPath, CurrentG
        
    FOR EACH (Neighbor, StepCost) IN Graph[CurrentNode]:
        TentativeG = CurrentG + StepCost
        
        IF TentativeG < gScores[Neighbor]:
            gScores[Neighbor] = TentativeG
            NewF = TentativeG + Heuristics[Neighbor]
            INSERT (NewF, TentativeG, Neighbor, CurrentPath + [Neighbor]) INTO PriorityQueue
            
RETURN Failure

```

Explanation:

* Formula: Evaluates total estimated path cost: f(n) = g(n) + h(n).
* g(n): Exact path cost from start to node n.
* h(n): Estimated cost from node n to goal.


* Behavior: Balances accumulated cost and distance remaining, avoiding expensive paths while making steady progress toward the goal.

Complexities and Properties:

* Time Complexity: Exponential O(b^d) worst-case; sub-exponential with an accurate heuristic.
* Space Complexity: O(b^d) (Keeps all expanded nodes in memory).
* Completeness: Complete.
* Optimality: Optimal if h(n) is admissible (never overestimates real cost) and consistent (satisfies triangle inequality).

Real-World Use Cases:

* Video game pathfinding and NPC movement (e.g., RTS and RPG games).
* Robotics movement planning and autonomous vehicle navigation.

6. MINIMAX ALGORITHM

Overview:
Minimax is a decision-making algorithm for two-player, zero-sum, turn-based competitive games. It maximizes the utility score for MAX while assuming MIN plays optimally to minimize it.

Pseudocode:
FUNCTION Minimax(Node, Depth, IsMaxTurn):
IF Depth == 0 OR Node IS LeafNode:
RETURN Node.UtilityValue

```
IF IsMaxTurn:
    MaxEval = -Infinity
    FOR EACH Child IN Node.Children:
        Eval = Minimax(Child, Depth - 1, FALSE)
        MaxEval = MAX(MaxEval, Eval)
    RETURN MaxEval
ELSE:
    MinEval = +Infinity
    FOR EACH Child IN Node.Children:
        Eval = Minimax(Child, Depth - 1, TRUE)
        MinEval = MIN(MinEval, Eval)
    RETURN MinEval

```

Explanation:

* Concept: Explores the full game tree down to a specified depth or terminal state.
* Evaluation:
* MAX level takes the maximum among child values.
* MIN level takes the minimum among child values.



Complexities and Properties:

* Time Complexity: O(b^m) where b is game branching factor and m is maximum search depth.
* Space Complexity: O(b * m) for depth-first recursive call stack.

Real-World Use Cases:

* Turn-based board games (e.g., Tic-Tac-Toe, Connect Four, Checkers).

7. ALPHA-BETA PRUNING

Overview:
Alpha-Beta Pruning is an optimization technique for Minimax that eliminates (prunes) branches that cannot influence the final decision, dramatically reducing evaluation time without altering the optimal outcome.

Pseudocode:
FUNCTION AlphaBeta(Node, Depth, Alpha, Beta, IsMaxTurn):
IF Depth == 0 OR Node IS LeafNode:
RETURN Node.UtilityValue

```
IF IsMaxTurn:
    MaxEval = -Infinity
    FOR EACH Child IN Node.Children:
        Eval = AlphaBeta(Child, Depth - 1, Alpha, Beta, FALSE)
        MaxEval = MAX(MaxEval, Eval)
        Alpha = MAX(Alpha, MaxEval)
        
        IF Beta <= Alpha:
            BREAK  // Beta Cutoff (Prune remaining children)
            
    RETURN MaxEval
ELSE:
    MinEval = +Infinity
    FOR EACH Child IN Node.Children:
        Eval = AlphaBeta(Child, Depth - 1, Alpha, Beta, TRUE)
        MinEval = MIN(MinEval, Eval)
        Beta = MIN(Beta, MinEval)
        
        IF Beta <= Alpha:
            BREAK  // Alpha Cutoff (Prune remaining children)
            
    RETURN MinEval

```

Explanation:

* Alpha: The best value MAX is guaranteed so far along the path (starts at -Infinity).
* Beta: The best value MIN is guaranteed so far along the path (starts at +Infinity).
* Pruning Rule: If Beta <= Alpha, MIN or MAX can discard remaining subtrees because the parent node will never select a path leading to this branch.

Complexities and Properties:

* Time Complexity:
* Worst Case: O(b^m) (Same as Minimax if move ordering is poor).
* Best Case: O(b^(m/2)) with optimal move ordering (Effectively doubles the search depth!).


* Space Complexity: O(b * m).

Real-World Use Cases:

* Advanced game engines (e.g., Chess, Go, Othello AI engines).
