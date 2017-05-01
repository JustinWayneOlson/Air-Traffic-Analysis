def three_dim_astar(origin, dest, grid_res_planar, grid_res_vert, heuristic):

    heuristicModule = __import__(heuristic)

    closedNodes = list()
    openNodes = list()

    grid = create_graph(grid_res_planar, grid_res_vert) // ammend with new grid method
    currLoc = origin
    currNode = grid[origin[0]][origin[1]][origin[2]]
    currNode.priority = 0
    endNode = grid[dest[0]][dest[1]][dest[2]]

    openNodes.append(grid[origin[0]][origin[1]][origin[2]])


    while currLoc[0] != dest[0] or currLoc[1] != dest[1] or currLoc[2] != dest[2]:

        min_index = find_lowest_rank(openNodes)
        node_popped = openNodes.pop(min_index)
        closedNodes.append(node_popped)
        currNode = node_popped
        currLoc = [currNode.coords[0], currNode.coords[1], currNode.coords[2]]

        for neighNode in currNode.neighbors:

            cost = currNode.approxCost + getDist(currNode, neighNode)
            if openNodes.count(neighNode) == 1 and cost < neighNode.approxCost:
                openNodes.remove(neighNode)

            if closedNodes.count(neighNode) == 1 and cost < neighNode.approxCost:
                closedNodes.remove(neighNode)

            if openNodes.count(neighNode) == 0 and closedNodes.count(neighNode) == 0:
                neighNode.approxCost = cost
                openNodes.append(neighNode)
                neighNode.priority = neighNode.approxCost + heuristicModule.h(neighNode, endNode) 
                neighNode.parent = currNode

    return grid
