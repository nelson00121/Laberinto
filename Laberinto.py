import tkinter as tk
import random
import time

def generate_maze(rows, cols):
    maze = [[1] * (2 * cols + 1) for _ in range(2 * rows + 1)]
    
    def carve(x, y):
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 2 * rows + 1 and 0 <= ny < 2 * cols + 1 and maze[nx][ny] == 1:
                maze[x + dx // 2][y + dy // 2] = 0
                maze[nx][ny] = 0
                carve(nx, ny)
    
    maze[1][1] = 0
    carve(1, 1)
    return maze

def draw_maze(canvas, maze):
    canvas.delete("all")
    cell_size = 20
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 1:
                canvas.create_rectangle(j * cell_size, i * cell_size, 
                                        (j + 1) * cell_size, (i + 1) * cell_size, 
                                        fill="black")

def find_path(maze):
    rows, cols = len(maze), len(maze[0])
    start, end = (1, 1), (rows - 2, cols - 2)
    queue = [(start, [start])]
    visited = set()
    
    while queue:
        (x, y), path = queue.pop(0)
        if (x, y) == end:
            return path
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 0 and (nx, ny) not in visited:
                queue.append(((nx, ny), path + [(nx, ny)]))
                visited.add((nx, ny))
    return []

def animate_ball(path):
    cell_size = 20
    for (x, y) in path:
        canvas.coords(ball, y * cell_size + cell_size // 2, x * cell_size + cell_size // 2, 
                      y * cell_size + cell_size, x * cell_size + cell_size)
        root.update()
        time.sleep(0.1)

def generate_and_draw():
    try:
        global maze, ball
        rows = int(row_entry.get())
        cols = int(col_entry.get())
        if rows <= 0 or cols <= 0:
            return
        maze = generate_maze(rows, cols)
        draw_maze(canvas, maze)
        cell_size = 20
        ball = canvas.create_oval(10, 10, 20, 20, fill="red")
    except ValueError:
        pass

def start_animation():
    path = find_path(maze)
    if path:
        animate_ball(path)

root = tk.Tk()
root.title("Generador de Laberintos")

tk.Label(root, text="Filas:").grid(row=0, column=0)
tk.Label(root, text="Columnas:").grid(row=0, column=2)

row_entry = tk.Entry(root, width=5)
row_entry.grid(row=0, column=1)
row_entry.insert(0, "10")

col_entry = tk.Entry(root, width=5)
col_entry.grid(row=0, column=3)
col_entry.insert(0, "10")

generate_button = tk.Button(root, text="Generar Laberinto", command=generate_and_draw)
generate_button.grid(row=0, column=4)

start_button = tk.Button(root, text="Iniciar", command=start_animation)
start_button.grid(row=0, column=5)

canvas = tk.Canvas(root, width=600, height=600, bg="white")
canvas.grid(row=1, column=0, columnspan=6)

maze = []
ball = None

root.mainloop()
