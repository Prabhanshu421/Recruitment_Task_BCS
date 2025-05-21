from collections import deque

def bfs(maze, start, goal):
    queue = deque([(start, [])])
    visited = set([start])
    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == goal:
            return path[0] if path else goal
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze) and maze[ny][nx] == 0:
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [(nx, ny)]))
    return start  # fallback
