import curses
import time
from curses import wrapper
import combathandler
import party
import character


def main(stdscr:curses.window):

    p1 = party.Party()
    p1.addPartymember(character.Character())
    p1.addPartymember(character.Character())
    p1.addPartymember(character.Character())
    p2 = party.Party()
    p2.addPartymember(character.Character())
    p2.addPartymember(character.Character())
    p2.addPartymember(character.Character())

    ch = combathandler.CombatHandler(p1,p2)
    print(ch.printSelf())
    for _ in range (10):
        stdscr.clear()
        ch.processTurn()
        stdscr.addstr(ch.printSelf())
        time.sleep(0.5)
        stdscr.refresh()
        #stdscr.getch()
wrapper(main)