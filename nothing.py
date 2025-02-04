import curses

def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.addstr(5, 10, "Hello, Ncurses!", curses.A_BOLD)
    stdscr.refresh()
    stdscr.getch()  # Wait for keypress

curses.wrapper(main)
