import curses
import threading
import time
import random

player_x = 0

def main(stdscr):
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    curses.curs_set(0)
    # Get the height and width of the screen
    screen_height, screen_width = stdscr.getmaxyx()
    global player_x
    player_x = (screen_width // 2 - 8)//5*5

    text = ""\
    r"·························································"\
    r": ______    __   __  __    _  _     _  _______  __   __ :"\
    r":|    _ |  |  | |  ||  |  | || | _ | ||   _   ||  | |  |:"\
    r":|   | ||  |  | |  ||   |_| || || || ||  |_|  ||  |_|  |:"\
    r":|   |_||_ |  |_|  ||       ||       ||       ||       |:"\
    r":|    __  ||       ||  _    ||       ||       ||_     _|:"\
    r":|   |  | ||       || | |   ||   _   ||   _   |  |   |  :"\
    r":|___|  |_||_______||_|  |__||__| |__||__| |__|  |___|  :"\
    r":         ______    __   __  _______  __   __           :"\
    r":        |    _ |  |  | |  ||       ||  | |  |          :"\
    r":        |   | ||  |  | |  ||  _____||  |_|  |          :"\
    r":        |   |_||_ |  |_|  || |_____ |       |          :"\
    r":        |    __  ||       ||_____  ||       |          :"\
    r":        |   |  | ||       | _____| ||   _   |          :"\
    r":        |___|  |_||_______||_______||__| |__|          :"\
    r"·························································"
        
    # Create a new window
    win = curses.newwin(screen_height, screen_width, 0, 0)
    
    # Display the text in the window
    y = screen_height//2-8
    for a in range(0, 16):
        try:
            win.addstr(y, screen_width//2-27, text[a*57:(a+1)*57])
        except Exception as e:
            print(e.args)
        y += 1
        stdscr.refresh()
    
    win.refresh()
    stdscr.addstr(y, screen_width//2-18, "Press enter to continue or ESC to exit")
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
            stdscr.addstr(screen_height - 1, 0, "Game Loading...")
            stdscr.refresh()
            curses.napms(1000)
            win.clear()
            win.refresh()
            break
    
    instructions = curses.newwin(screen_height, screen_width, 0, 0)
    def centerText(win, y, text):
        x = screen_width//2 - len(text)//2
        win.addstr(y, x, text)
        instructions.refresh()

    instructions.clear()

    centerText(instructions, screen_height//2-4, "***********************************************************************")
    centerText(instructions, screen_height//2-3, "*                           Instructions:                             *")
    centerText(instructions, screen_height//2-2, "* 1. Use the left and right arrow keys to move the player             *")
    centerText(instructions, screen_height//2-1, "* 2. Your goal is to land the plane on the air strip without crashing *")
    centerText(instructions, screen_height//2,   "* 3. As the game progresses, the levels will get harder and faster    *")
    centerText(instructions, screen_height//2+1, "* 4. Press the ESC key to exit                                        *")
    centerText(instructions, screen_height//2+2, "*                                                                     *")
    centerText(instructions, screen_height//2+3, "*                    Press enter to start the game                    *")
    centerText(instructions, screen_height//2+4, "***********************************************************************")
    
    instructions.refresh()
    
    while True:
        key = stdscr.getch()
        if key == 27:  # ESC key
            curses.nocbreak()
            stdscr.keypad(False)
            curses.echo()
            curses.endwin()
            return
        if key == 10:  # Enter key
            instructions.addstr(screen_height-1, 0, "Game Starting...")
            instructions.refresh()
            time.sleep(.5)
            instructions.clear()
            instructions.refresh()
            break

    game = curses.newwin(screen_height, screen_width, 0, 0)
    game.keypad(True)  # Enable keypad mode
    game.clear()
    
    def drawPlayer(game, x):
        player = [
            r"       /\ ",       
            r"      /**\ ",      
            r"     /****\ ",     
            r"  __/------\__ ",  
            r" /  |      |  \ ", 
            r"/___|______|___\ ",
            r"   \   ||   / ",
            r"    \__||__/ "    
        ]
        game.clear()
        for i, line in enumerate(player):
            game.addstr(screen_height-10+i, x, line)
        game.refresh()

    def playerLoop(game):
        global player_x
        drawPlayer(game, player_x)
        game.nodelay(True)  # Make getch non-blocking
        while True:
            key = game.getch()
            if key == curses.KEY_LEFT:
                player_x = max(6, (player_x - 5)//5*5+1)  # Move left, but don't go out of bounds
                drawPlayer(game, player_x)
            elif key == curses.KEY_RIGHT:
                player_x = min((screen_width - 20)//5*5-1, (player_x + 5)//5*5)  # Move right, but don't go out of bounds
                drawPlayer(game, player_x)
            elif key == 27 or key == ord('q'):  # ESC key to exit
                break
            time.sleep(.01)  # Small delay to reduce CPU usage
    def clear(game):
        game.clear()
        drawPlayer(game, player_x)
        game.refresh()
    def drawFlightStrip(game, space, speed):
        x = random.randint(space//5+1, (screen_width-20)//5)*5-space//2-5
        for i in range(0, (screen_height-5)//5):
            for j in range(0, 5):
                game.addstr(i*5+j, x, "|||||"+" "*space+"|||||")
            game.refresh()
            time.sleep(speed)
            clear(game)
    
    def gameLoop(game):
        for i in range (4, 1, -1):
            for j in range (5, 1, -1):
                drawFlightStrip(game, 5*i, .2*j)
            
    playerThread = threading.Thread(target=playerLoop, args=(game,))
    playerThread.start()
    gameThread = threading.Thread(target=gameLoop, args=(game,))
    gameThread.start()
    
    playerThread.join()  # Ensure the thread completes before exiting
    gameThread.join()  # Ensure the thread completes before exiting
curses.wrapper(main)