# RUNNING THE PROGRAM

To run the program:

python3 a1.py <TEST_DATA>

where TEST_DATA is the path to the test file

For example:

python3 a1.py Asst1.data.txt


The output will print both the paths for best-first and A* search.

The 'X' symbols represent the path chosen by the algorithm.

The '=' symbols represent the cells (nodes) expanded by the algorithm.

The '-' symbols represent unexpanded nodes.


# DESCRIPTION

A node is given by a tuple T = (x, y), where x and y are the coordinates of the cell.

The goal is a tuple G. Let P be the predecessor cell of T.

The heuristic function is a function h_{G,P}(T) ie. h is parameterized by G, P.

Let D be the manhattan distance between T and P.
Let C be the cost of moving from P to T.

where h(T) = D + C

The implementation of Best-first and A* use the same tree search algorithm -
only the evaluation function is different. The search algorithm is a breadth-
first traversal using a priority queue. So the lowest cost frontier
nodes are expanded first.

After the goal is found, the path is computed by walking back through parent
nodes starting at the goal.

A closed list is maintained to prevent cycles in the search tree.
