import curses
import threading
import time

player_x = 0

def main(stdscr):
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    curses.curs_set(0)
    # Get the height and width of the screen
    screen_height, screen_width = stdscr.getmaxyx()
    global player_x
    player_x = screen_width // 2 - 10
    
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
            return
        if key == 10:  # Enter key
            stdscr.addstr(screen_height - 1, 0, "Game Starting...")
            stdscr.refresh()
            curses.napms(1000)
            win.clear()
            win.refresh()
            break
    
    # Create new windows for enemies and player
    winEnemies = curses.newwin(25, screen_width, 0, 0)
    winEnemies.refresh()

    winPlayer = curses.newwin(8, screen_width, 26, 0)
    winPlayer.refresh()
    
    def drawSingleBattleship(winEnemies, battleships, y):
        evilBattleShip = [
            r"     ____ ",
            r" ___/    \___",
            r"/   '----'   \ ",
            r"'---______---' ",
        ]
        for i, line in enumerate(evilBattleShip):
            x = screen_width // (battleships + 1) - (7 * battleships)
            winEnemies.addstr(i + y, x, line)
        winEnemies.refresh()
    
    def drawBattleship(winEnemies):
        for i in range(0, 23):
            winEnemies.clear()
            drawSingleBattleship(winEnemies, 1, i)
            winEnemies.refresh()
            time.sleep(.25)
        winEnemies.getch()

    # Create and start the thread for battleship animation
    battleship_thread = threading.Thread(target=drawBattleship, args=(winEnemies,))
    battleship_thread.start()

    def drawPlayer(winPlayer):
        global player_x
        player = [
            r"       /\ ",       
            r"      /**\ ",      
            r"     /****\ ",     
            r"  __/------\__ ",  
            r" /  |      |  \ ", 
            r"/---|______|---\ ",
            r"    /  ||  \ ",
            r"    \__||__/ "    
        ]
        for i, line in enumerate(player):
            winPlayer.addstr(i, player_x, line)
        winPlayer.refresh()

    def playerLoop(winPlayer):
        global player_x
        drawPlayer(winPlayer)
        winPlayer.nodelay(True)  # Make getch non-blocking
        while True:
            key = stdscr.getch()
            if key == curses.KEY_LEFT:
                winPlayer.clear()
                player_x = max(0, player_x - 1)  # Move left, but don't go out of bounds
                drawPlayer(winPlayer)
            elif key == curses.KEY_RIGHT:
                winPlayer.clear()
                player_x = min(screen_width - 10, player_x + 1)  # Move right, but don't go out of bounds
                drawPlayer(winPlayer)
            elif key == ord(' '):  # Space key to fire
                fire_shot(winEnemies)
            elif key == 27:  # ESC key to exit
                break
            time.sleep(.01)  # Small delay to reduce CPU usage

    def one_shot(winEnemies, x):
        bullet = '|'
        for i in range(20, 0, -1):
            winEnemies.addstr(i, x, bullet)
            winEnemies.refresh()
            time.sleep(.25)

    def fire_shot(winEnemies):
        global player_x
        one_shot_thread = threading.Thread(target=one_shot, args=(winEnemies, player_x + 7))
        one_shot_thread.start()


    # Create and start the thread for player movement
    player_thread = threading.Thread(target=playerLoop, args=(winPlayer,))
    player_thread.start()


    # Wait for both threads to finish
    battleship_thread.join()
    player_thread.join()

curses.wrapper(main)