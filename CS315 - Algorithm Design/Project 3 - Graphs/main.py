from heapq import heapify, heappush

adj_list = {}


def create_vertices(filename):
    file = open(filename, "r")
    lines = file.readlines()

    for i in range(len(lines)):
        lines[i] = lines[i].rstrip("\n")
        adj_list[lines[i]] = ""


def add_edges(filename):
    file = open(filename, "r")
    lines = file.readlines()

    for i in range(len(lines)):
        lines[i] = lines[i].rstrip("\n")
        lines[i] = lines[i].split(",")

        temp1 = {}
        temp2 = {}
        if adj_list[lines[i][0]] == "":
            temp1[lines[i][1]] = int(lines[i][2])
            adj_list[lines[i][0]] = temp1
        else:
            temp1.update(adj_list[lines[i][0]])
            temp1[lines[i][1]] = int(lines[i][2])
            adj_list[lines[i][0]] = temp1

        #  For undirected graph
        if adj_list[lines[i][1]] == "":
            temp2[lines[i][0]] = int(lines[i][2])
            adj_list[lines[i][1]] = temp2
        else:
            temp2.update(adj_list[lines[i][1]])
            temp2[lines[i][0]] = int(lines[i][2])
            adj_list[lines[i][1]] = temp2


def print_graph():
    for vertex in adj_list:
        print(f"{vertex} - > ", end="")
        for edges in adj_list[vertex].keys():
            print(f"{edges}", end=", ")
        print()


create_vertices("RomaniaVertices.txt")
add_edges("RomaniaEdges.txt")
print("---Graph Print:---")
print_graph()


def BFS(graph, start, goal):
    visited = []

    # Queue for traversing the graph in the BFS
    queue = [[start]]

    # If the desired node is reached
    if start == goal:
        print("Same Node")
        return

    # Loop to traverse the graph with the help of the queue
    while queue:
        path = queue.pop(0)
        node = path[-1]

        # Condition to check if the current node is not visited
        if node not in visited:
            neighbours = graph[node]

            # Loop to iterate over the neighbours of the node
            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)

                # Condition to check if the neighbour node is the goal
                if neighbour == goal:
                    print(f"Shortest path from {start} to {goal} =", *new_path)
                    return
            visited.append(node)

    # Condition when the nodes are not connected
    print("So sorry, but a connecting path doesn't exist :(")
    return

print()
print("----Breadth First Search----")
BFS(adj_list, "Arad", "Sibiu")
BFS(adj_list, "Arad", "Craiova")
BFS(adj_list, "Arad", "Bucharest")


def dijsktra(graph,src,dest):
    inf = float('inf')
    vertices = 10
    node_data = {}
    for node in graph:
        node_data[node] = {'cost': inf, 'pred': []}
    node_data[src]['cost'] = 0
    node_data[src]['cost'] = 0
    visited = []
    temp = src
    for i in range(vertices):
        if temp not in visited:
            visited.append(temp)
            min_heap = []
            for j in graph[temp]:
                if j not in visited:
                    cost = node_data[temp]['cost'] + graph[temp][j]
                    if cost < node_data[j]['cost']:
                        node_data[j]['cost'] = cost
                        node_data[j]['pred'] = node_data[temp]['pred'] + temp.split(" ")
                    heappush(min_heap, (node_data[j]['cost'], j))
        heapify(min_heap)
        temp = min_heap[0][1]
    print(f"Shortest Distance from {src} to {dest} is  {node_data[dest]['cost']}")
    print(f"Shortest Path from {src} to {dest} is : {node_data[dest]['pred'] + dest.split(' ')}")

print()
print("----Dijkstra’s Algorithm!----")
dijsktra(adj_list, "Arad", "Bucharest")

print()
print("The adjacency list:")
print(adj_list)




