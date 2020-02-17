import generator
import input_handling
import play
import solve

print('What would you like to do?')
print('(s)olve')
print('(p)lay')
print('(g)enerate new')

choice = input_handling.input_string('Choice', default='s')
if choice == 's':
    solve.solve()
elif choice == 'p':
    play.play_puzzles()
elif choice == 'g':
    generator.init_generate_puzzles()
