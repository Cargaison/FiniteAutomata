from Classes import (Transition, State, Automata)
automata = Automata()
automata.read_from_file('automata.txt')  # The file must have the correct content

print("Initial Automaton:")
automata.display()

automata.make_deterministic()
print("\nDeterministic Automaton:")
automata.display()

automata.standardize()
print("\nStandardize Automaton:")
automata.display()

automata.make_complete()
print("\nDeterministic Automaton:")
automata.display()