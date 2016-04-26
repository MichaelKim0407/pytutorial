from interact import InteractiveConsole

__author__ = 'Michael'

InteractiveConsole.add_scene_global(
    "Main Menu",
    """Welcome to Michael Kim's Interactive Python tutorial!

Enter start to start learning!
Enter python to bring out the interactive console.
Enter help for usage tips.
"""
)

InteractiveConsole.add_scene_global(
    "Help",
    """A list of useful commands:
\tName\t\tNotes"""
)

InteractiveConsole.add_scene_global(
    "Help (Advanced)",
    """A list of available commands:
\tName\t\tNotes"""
)
