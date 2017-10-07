maze = [
        [0, 0, 1, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 1, 1, 0],
        [0, 1, 0, 1, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0]]

target_x = 8
target_y = 8

def dfs(maze, x, y, path):
    if x == target_x and y == target_y:
        print(path)
        return True
    # up
    if x > 0:
        if maze[x-1][y] == 0:
            maze[x-1][y] = 2
            path.append((x-1, y))
            t = dfs(maze, x-1, y, path)
            if t == True:
                return True
            path.pop()
            maze[x-1][y] = 0
    # right
    if y < 8:
        if maze[x][y+1] == 0:
            maze[x][y+1] = 2
            path.append((x, y+1))
            t = dfs(maze, x, y+1, path)
            if t == True:
                return True
            path.pop()
            maze[x][y+1] = 0
    # down
    if x < 8:
        if maze[x+1][y] == 0:
            maze[x+1][y] = 2
            path.append((x+1, y))
            t = dfs(maze, x+1, y, path)
            if t == True:
                return True
            path.pop()
            maze[x+1][y] = 0
    # left
    if y > 0:
        if maze[x][y-1] == 0:
            maze[x][y-1] = 2
            path.append((x, y-1))
            t = dfs(maze, x, y-1, path)
            if t == True:
                return True
            path.pop()
            maze[x][y-1] = 0
    return False


dfs(maze, 0, 0, [])

