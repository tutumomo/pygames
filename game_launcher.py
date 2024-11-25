import tkinter as tk
from tkinter import ttk
import os
import subprocess
import sys

class GameLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("PyGames Launcher")
        self.root.geometry("400x500")
        
        # Configure style
        style = ttk.Style()
        style.configure("Complete.TButton", foreground="green")
        style.configure("Incomplete.TButton", foreground="gray")
        
        # Games configuration - Add games and their status here
        self.games = {
            "MineSweeping": {
                "status": "complete",
                "path": "MineSweeping/main.py",
                "chinese_name": "踩地雷"
            },
            "GluttonousSnake": {
                "status": "complete",
                "path": "GluttonousSnake/main.py",
                "chinese_name": "貪吃蛇"
            },
            "Tetris": {
                "status": "complete",
                "path": "Tetris/main.py",
                "chinese_name": "俄羅斯方塊"
            },
            "Gomoku": {
                "status": "complete",
                "path": "Gomoku/ManAndMachine.py",
                "chinese_name": "五子棋"
            }
        }
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="PyGames Collection", font=('Helvetica', 16, 'bold'))
        title_label.grid(row=0, column=0, pady=20)
        
        # Create game buttons
        for idx, (game_name, info) in enumerate(self.games.items(), 1):
            is_complete = info["status"] == "complete"
            button_style = "Complete.TButton" if is_complete else "Incomplete.TButton"
            
            # Create frame for each game
            game_frame = ttk.Frame(main_frame)
            game_frame.grid(row=idx, column=0, pady=10, sticky=(tk.W, tk.E))
            
            # Game button
            btn = ttk.Button(
                game_frame,
                text=f"{game_name}\n{info['chinese_name']}",
                style=button_style,
                command=lambda g=game_name: self.launch_game(g) if self.games[g]["status"] == "complete" else None,
                width=25
            )
            btn.grid(row=0, column=0, padx=10, pady=5, ipady=10)
            
            # Status label
            status_text = "Ready to Play" if is_complete else "In Development"
            status_label = ttk.Label(
                game_frame,
                text=status_text,
                foreground="green" if is_complete else "gray"
            )
            status_label.grid(row=0, column=1, padx=5)
    
    def launch_game(self, game_name):
        game_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.games[game_name]["path"])
        if os.path.exists(game_path):
            subprocess.Popen([sys.executable, game_path])
        else:
            print(f"Error: Could not find game file at {game_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GameLauncher(root)
    root.mainloop()
