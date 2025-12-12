"""Create a GUI to run the python applications in the subdirectories."""

import os
import subprocess
import tkinter as tk


def run_main_py(directory):
    """Function to run main.py in the selected directory."""
    subprocess.run(
        [
            # os.path.join(directory, "../../../.venv/Scripts/python"),
            "./.venv/Scripts/python",
            os.path.join(directory, "main.py"),
        ]
    )


# Create the main window
root = tk.Tk()
root.title("Game Launcher")

# Set the window size to 800x600 and position at (100, 100)
root.geometry("300x225+100+100")

# Get the list of subdirectories
base_dir = os.path.join("days_of_code", "turtle_games")
subdirs = [
    d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))
]

# Create buttons for each subdirectory
for subdir in subdirs:
    button = tk.Button(
        root,
        text=[word.capitalize() for word in subdir.split("_")],
        bg="lightgray",
        fg="black",
        command=lambda d=subdir: run_main_py(os.path.join(base_dir, d)),
    )
    button.pack(pady=5)

# Run the GUI loop
root.mainloop()
