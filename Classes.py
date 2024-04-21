class Transition:
    def __init__(self, symbol, begin, end):
        self.symbol = symbol
        self.begin = begin
        self.end = end

class State:
    def __init__(self, name):
        self.name = name
        self.out_transitions = []

    def add_outgoing_transition(self, transition):
        self.out_transitions.append(transition)

class Automata:
    def __init__(self):
        self.states = {}
        self.initial_states = []
        self.final_states = []
        self.transitions = []
        self.alphabet = []

    def add_state(self, state):
        self.states[state.name] = state

    def add_transition(self, transition):
        self.transitions.append(transition)
        self.states[transition.begin].add_outgoing_transition(transition)

    def read_from_file(self, file_path):
        with open(file_path, 'r') as file:
            alphabet_size = int(file.readline().strip())  # Nombre de lettres dans l'alphabet
            self.alphabet = [chr(i + ord('a')) for i in range(alphabet_size)]
            num_states = int(file.readline().strip())  # Nombre total d'états
            for i in range(num_states):
                self.add_state(State(str(i)))


            initial_states_info = file.readline().strip().split()
            num_initial_states = int(initial_states_info[0])  # Le premier élément est le nombre d'états initiaux
            self.initial_states = initial_states_info[1:1 + num_initial_states]


            final_states_info = file.readline().strip().split()
            num_final_states = int(final_states_info[0])  # Le premier élément est le nombre d'états finaux
            self.final_states = final_states_info[1:1 + num_final_states]


            num_transitions = int(file.readline().strip())
            for _ in range(num_transitions):
                begin, symbol, end = file.readline().strip().split()
                self.add_transition(Transition(symbol, begin, end))

    def display(self):
        print("States:", list(self.states.keys()))
        print("Initial State:", self.initial_states)
        print("Final States:", self.final_states)
        print("Transitions:")
        for transition in self.transitions:
            print(f"{transition.begin} --{transition.symbol}--> {transition.end}")

    def standardize(self):
        if len(self.initial_states) != 1 or any(transition.end == self.initial_states[0] for state in self.states.values() for transition in state.out_transitions):
            new_initial_state = State('i0')
            self.add_state(new_initial_state)
            for symbol in self.alphabet:
                for initial_state in self.initial_states:
                    self.add_transition(Transition(symbol, 'i0', initial_state))
            self.initial_states = ['i0']

    def make_deterministic(self):
        if not all(len({transition.symbol for transition in state.out_transitions}) == len(state.out_transitions) for state in self.states.values()):
            new_states = {}
            new_transitions = []
            new_initial_state = frozenset(self.initial_states)
            queue = [new_initial_state]
            visited = set()
            new_final_states = set()

            def get_state_name(states):
                return '.'.join(sorted(states))

            new_states[get_state_name(new_initial_state)] = State(get_state_name(new_initial_state))
            if any(state in self.final_states for state in new_initial_state):
                new_final_states.add(get_state_name(new_initial_state))

            while queue:
                current = queue.pop(0)
                visited.add(current)
                current_name = get_state_name(current)

                for symbol in self.alphabet:
                    next_states = frozenset(
                        transition.end for state in current for transition in self.states[state].out_transitions if transition.symbol == symbol
                    )

                    if not next_states:
                        continue
                    next_name = get_state_name(next_states)

                    if next_name not in new_states:
                        new_states[next_name] = State(next_name)
                        queue.append(next_states)
                        if any(state in self.final_states for state in next_states):
                            new_final_states.add(next_name)

                    new_transitions.append(Transition(symbol, current_name, next_name))

            self.states = new_states
            self.transitions = new_transitions
            self.initial_states = [get_state_name(new_initial_state)]
            self.final_states = list(new_final_states)

    def make_complete(self):
        if not all(len({transition.symbol for transition in state.out_transitions}) == len(self.alphabet) for state in self.states.values()):
            sink_state_added = False
            sink_state_name = 'sink'

            for state in list(self.states.keys()):
                transitions_symbols = {transition.symbol for transition in self.states[state].out_transitions}
                missing_symbols = set(self.alphabet) - transitions_symbols

                for symbol in missing_symbols:
                    if not sink_state_added:
                        self.add_state(State(sink_state_name))
                        sink_state_added = True
                    self.add_transition(Transition(symbol, state, sink_state_name))

            if sink_state_added:
                for symbol in self.alphabet:
                    self.add_transition(Transition(symbol, sink_state_name, sink_state_name))

    def is_standardized(self):
        # Un automate est standardisé si et seulement si il a un seul état initial
        # et aucun autre état ne le mène à cet état initial.
        if len(self.initial_states) != 1:
            return False
        initial_state = self.initial_states[0]
        for state in self.states.values():
            for transition in state.out_transitions:
                if transition.end == initial_state:
                    return False
        return True

    def is_complete(self):
        # Un automate est complet si chaque état a une transition pour chaque symbole dans l'alphabet.
        for state in self.states.values():
            symbols = {transition.symbol for transition in state.out_transitions}
            if symbols != set(self.alphabet):
                return False
        return True

    def is_deterministic(self):
        # Un automate est déterministe si pour chaque état et chaque symbole,
        # il n'y a qu'une seule transition correspondante.
        for state in self.states.values():
            seen_symbols = set()
            for transition in state.out_transitions:
                if transition.symbol in seen_symbols:
                    return False
                seen_symbols.add(transition.symbol)
        return True


# Example usage
automata = Automata()
file_number = input("Which FA do you want to use? ")
file_name = f"{file_number}.txt"
automata.read_from_file(file_name)  # Assume 'automata.txt' has the correct content
print("Is standardized? ", automata.is_standardized())
print("Is complete? ", automata.is_complete())
print("Is deterministic? ", automata.is_deterministic())

print("Initial Automaton:")
automata.display()



automata.standardize()
print("\nStandardized Automaton:")
automata.display()

automata.make_deterministic()
print("\nDeterministic Automaton:")
automata.display()

automata.make_complete()
print("\nComplete Automaton:")
automata.display()
print("Is standardized? ", automata.is_standardized())
print("Is complete? ", automata.is_complete())
print("Is deterministic? ", automata.is_deterministic())