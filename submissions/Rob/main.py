import generator
import input_handling
import play
import solve
from common import Quiting, BackToMenu

try:
    while True:
        print('What would you like to do?')
        print('(s)olve')
        print('(p)lay')
        print('(g)enerate new')
        print('(q)uit')

        choice = input_handling.input_string('Choice', default='s')
        try:
            if choice == 's':
                solve.solve()
            elif choice == 'p':
                play.play_puzzles()
            elif choice == 'g':
                generator.init_generate_puzzles()
            elif choice == 'q':
                break
        except BackToMenu:
            continue
except Quiting:
    print('Quiting!')
    exit()
