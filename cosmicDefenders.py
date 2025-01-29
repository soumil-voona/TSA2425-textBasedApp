import curses

def main(stdscr):
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    
    # Get the height and width of the screen
    screen_height, screen_width = stdscr.getmaxyx()
    
    # Define the text to display
    text = [
        r"      ________  ________  ________  ________  _______                        ",
        r"     |\   ____\|\   __  \|\   __  \|\   ____\|\  ___ \                       ",
        r"     \ \  \___|\ \  \|\  \ \  \|\  \ \  \___|\ \   __/|                      ",
        r"      \ \_____  \ \   ____\ \   __  \ \  \    \ \  \_|/__                    ",
        r"       \|____|\  \ \  \___|\ \  \ \  \ \  \____\ \  \_|\ \                   ",
        r"         ____\_\  \ \__\    \ \__\ \__\ \_______\ \_______\                  ",
        r"        |\_________\|__|     \|__|\|__|\|_______|\|_______|                  ",
        r" ___  ________ \|____________ ________  ________  _______   ________  ________      ",
        r"|\  \|\   ___  \|\  \    /  /|\   __  \|\   ___ \|\  ___ \ |\   __  \|\   ____\     ",
        r"\ \  \ \  \\ \  \ \  \  /  / \ \  \|\  \ \  \_|\ \ \   __/|\ \  \|\  \ \  \___|_    ",
        r" \ \  \ \  \\ \  \ \  \/  / / \ \   __  \ \  \ \\ \ \  \_|/_\ \   _  _\ \_____  \   ",
        r"  \ \  \ \  \\ \  \ \    / /   \ \  \ \  \ \  \_\\ \ \  \_|\ \ \  \\  \\|____|\  \  ",
        r"   \ \__\ \__\\ \__\ \__/ /     \ \__\ \__\ \_______\ \_______\ \__\\ _\ ____\_\  \ ",
        r"    \|__|\|__| \|__|\|__|/       \|__|\|__|\|_______|\|_______|\|__|\|__|\_________\\",
        r"                                                                        \|_________\\"
    ]
    
    # Create a new window
    win = curses.newwin(screen_height, screen_width, 0, 0)
    
    # Display the text in the window
    for i, line in enumerate(text):
        if i < screen_height:  # Ensure we don't write outside the window height
          win.addstr(i, 0, line[:screen_width])  # Ensure we don't write outside the window width
          stdscr.refresh()
    
    win.refresh()
    
    # Debugging: Display a message to indicate that the text has been added
    stdscr.addstr(screen_height - 3, 0, "Press enter to continue or ESC to exit")
    stdscr.refresh()
    
    # Wait for the ESC key to exit
    while True:
        key = stdscr.getch()
        
        if key == 27:  # ESC key
            curses.nocbreak()
            stdscr.keypad(False)
            curses.echo()
            curses.endwin()
            break
        if key == 10:  # Enter key
            stdscr.addstr(screen_height - 1, 0, "Game Starting...")
            stdscr.refresh()
            curses.napms(1000)
            win.clear()
            win.refresh()
            break
    
    # Create new windows for enemies and player
    winEnemies = curses.newwin(10, screen_width, 0, 0)
    winEnemies.refresh()
    winEnemies.getch()

    winPlayer = curses.newwin(10, screen_width, 11, 0)
    winPlayer.refresh()
    evilBattleShip = [
        r"     ___ ",
        r" ___/   \___",
        r"/   '---'   \ ",
        r"'--_______--' ",
    ]
    for i, line in enumerate(evilBattleShip):
        winEnemies.addstr(i, 0, line)
        stdscr.refresh()
    winEnemies.refresh()
    winEnemies.addstr(0, screen_height-1, "New Enemy")
    winEnemies.refresh()

curses.wrapper(main)
