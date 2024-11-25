import tkinter as tk
from tkinter import ttk
import os
import sys

class GameLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("PyGames Launcher")
        
        # Set window size and make it fixed
        window_width = 600
        window_height = 500  
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.root.resizable(False, False)
        
        # Configure style
        style = ttk.Style()
        style.configure("Complete.TButton", 
                       foreground="green",
                       font=('Microsoft YaHei UI', 12),
                       padding=(10, 5))
        style.configure("Incomplete.TButton", 
                       foreground="gray",
                       font=('Microsoft YaHei UI', 12),
                       padding=(10, 5))
        
        # Games configuration - Add games and their status here
        self.games = {
            "MineSweeping": {
                "status": "complete",
                "path": "MineSweeping/main.py",
                "chinese_name": "踩地雷"
            },
            "Snake": {
                "status": "complete",
                "path": "Snake/main.py",
                "chinese_name": "貪食蛇"
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
            },
            "BattleCity": {
                "status": "complete",
                "path": "BattleCity/main.py",
                "chinese_name": "坦克大戰"
            }
        }
        
        # Create main frame with padding
        main_frame = ttk.Frame(root, padding="20 20 20 10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, 
                               text="PyGames Collection", 
                               font=('Microsoft YaHei UI', 24, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Create buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        buttons_frame.columnconfigure(0, weight=1)
        
        # Create game buttons
        for idx, (game_name, info) in enumerate(self.games.items(), 0):
            is_complete = info["status"] == "complete"
            button_style = "Complete.TButton" if is_complete else "Incomplete.TButton"
            
            # Create frame for each game
            game_frame = ttk.Frame(buttons_frame)
            game_frame.grid(row=idx, column=0, pady=8, sticky=(tk.W, tk.E))
            game_frame.columnconfigure(0, weight=1)
            
            # Game button
            btn = ttk.Button(
                game_frame,
                text=f"{info['chinese_name']}\n{game_name}",
                style=button_style,
                command=lambda g=game_name: self.launch_game(g) if self.games[g]["status"] == "complete" else None,
                width=30
            )
            btn.grid(row=0, column=0, padx=10, pady=2, sticky=(tk.W, tk.E))
            
            # Status label
            status_text = "Ready to Play" if is_complete else "In Development"
            status_label = ttk.Label(
                game_frame,
                text=status_text,
                font=('Microsoft YaHei UI', 10),
                foreground="green" if is_complete else "gray"
            )
            status_label.grid(row=0, column=1, padx=10)

    def launch_game(self, game_name):
        game_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.games[game_name]["path"])
        if os.path.exists(game_path):
            python_executable = sys.executable
            # Use subprocess.run instead of os.system for better process handling
            import subprocess
            try:
                subprocess.run([python_executable, game_path], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error launching {game_name}: {e}")
            except Exception as e:
                print(f"Unexpected error launching {game_name}: {e}")

def main():
    root = tk.Tk()
    app = GameLauncher(root)
    root.mainloop()

if __name__ == "__main__":
    main()
