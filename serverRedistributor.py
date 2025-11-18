import tkinter as tk
import random
import time

# --- Window Setup ---
root = tk.Tk()
root.title(" Network Overload Manager (Pigeonhole Principle + Graphs)")
root.geometry("800x500")
root.configure(bg="black")

canvas = tk.Canvas(root, width=800, height=420, bg="black", highlightthickness=0)
canvas.pack(pady=10)

# --- Parameters ---
MAX_LOAD = 3               # max users per server before overload
INITIAL_SERVERS = 4
TOTAL_USERS = 20

server_positions = []
server_loads = []
server_nodes = []
user_nodes = []
user_connections = []

# --- Helper Functions ---
def draw_servers():
    """Draw all servers on canvas"""
    canvas.delete("server")
    for i, (x, y) in enumerate(server_positions):
        color = "red" if server_loads[i] > MAX_LOAD else "skyblue"
        s = canvas.create_oval(x-25, y-25, x+25, y+25, fill=color, outline="white", width=2, tags="server")
        canvas.create_text(x, y, text=f"S{i+1}", fill="white", font=("Arial", 10, "bold"), tags="server")
        server_nodes.append(s)

def draw_users():
    """Draw users (bottom row)"""
    for u in user_nodes:
        canvas.delete(u)
    for i, (x, y) in enumerate(user_nodes):
        canvas.create_oval(x-8, y-8, x+8, y+8, fill="limegreen", outline="white", tags="user")
        canvas.create_text(x, y+14, text=f"U{i+1}", fill="white", font=("Arial", 8), tags="user")

def connect_user_to_server(u_index, s_index):
    """Draw a connection line between user and server"""
    ux, uy = user_nodes[u_index]
    sx, sy = server_positions[s_index]
    line = canvas.create_line(ux, uy-10, sx, sy+25, fill="white", width=1, tags="conn")
    user_connections.append((u_index, s_index, line))

def update_server_colors():
    """Change color of overloaded servers"""
    for i, (x, y) in enumerate(server_positions):
        color = "red" if server_loads[i] > MAX_LOAD else "skyblue"
        canvas.create_oval(x-25, y-25, x+25, y+25, fill=color, outline="white", width=2, tags="server")
        canvas.create_text(x, y, text=f"S{i+1}", fill="white", font=("Arial", 10, "bold"), tags="server")

def add_server():
    """Add new server dynamically"""
    new_x = 100 + len(server_positions)*140
    new_y = 100
    server_positions.append((new_x, new_y))
    server_loads.append(0)
    draw_servers()

def redistribute_users():
    """Redistribute users evenly after overload"""
    canvas.delete("conn")
    all_users = len(user_nodes)
    num_servers = len(server_positions)
    per_server = all_users // num_servers
    remainder = all_users % num_servers

    # Clear old loads
    for i in range(len(server_loads)):
        server_loads[i] = per_server + (1 if i < remainder else 0)

    # Redistribute visually
    for i, (ux, uy) in enumerate(user_nodes):
        new_server = i % num_servers
        connect_user_to_server(i, new_server)
        root.update()
        time.sleep(0.05)

    update_server_colors()

def show_message(msg, color="white", delay=1.5):
    """Display a temporary message"""
    text = canvas.create_text(400, 220, text=msg, fill=color, font=("Arial", 16, "bold"))
    root.update()
    time.sleep(delay)
    canvas.delete(text)

# --- Main Simulation ---
def run_simulation():
    canvas.delete("all")
    user_nodes.clear()
    server_positions.clear()
    server_loads.clear()
    user_connections.clear()

    # Setup servers
    for i in range(INITIAL_SERVERS):
        server_positions.append((150 + i*150, 100))
        server_loads.append(0)
    draw_servers()

    # Setup users
    for i in range(TOTAL_USERS):
        x = 60 + i*35
        if x > 750: x = random.randint(60, 740)
        y = 370
        user_nodes.append((x, y))
    draw_users()

    # Simulate user connections
    for i in range(TOTAL_USERS):
        target = server_loads.index(min(server_loads))
        connect_user_to_server(i, target)
        server_loads[target] += 1
        update_server_colors()
        root.update()
        time.sleep(0.3)

        # Detect overload
        if max(server_loads) > MAX_LOAD:
            show_message(" Network Overload Detected!", "red")
            add_server()
            show_message(" Adding New Server...", "yellow")
            redistribute_users()
            show_message("Network Load Balanced Successfully!", "lime")
            update_server_colors()

# --- Button ---
btn = tk.Button(root, text="Start Simulation", command=run_simulation,
                bg="lime", fg="black", font=("Arial", 12, "bold"))
btn.pack(pady=10)

root.mainloop()
