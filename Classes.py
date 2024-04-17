#Quand j'ai fait ce code seul dieu et moi savions ce que je faisais
#maintenant seul dieu le sait
#le code fonctionne si vous voulez le modifier à vos risques et périls
#compteur d'heures perdues sur le projet:
#-----13 heures et 30 minutes-----
#merci d'augmenter le compteur pour chaque heure passée sur cet enfer

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
            alphabet_size = int(file.readline().strip())
            self.alphabet = [chr(i + ord('a')) for i in range(alphabet_size)]
            num_states = int(file.readline().strip())
            for i in range(num_states):
                self.add_state(State(str(i)))
            self.initial_states = [file.readline().strip().split()[1]]
            self.final_states = file.readline().strip().split()[1:]
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
        if 'i0' not in self.states:
            new_initial_state = State('i0')
            self.add_state(new_initial_state)
            for symbol in self.alphabet:
                for initial_state in self.initial_states:
                    self.add_transition(Transition(symbol, 'i0', initial_state))
            self.initial_states = ['i0']

    def make_deterministic(self):
        # Create new DFA from the NFA
        new_states = {}
        new_transitions = []
        new_initial_state = frozenset(self.initial_states)
        queue = [new_initial_state]
        visited = set()
        new_final_states = set()

        # crééer le nom des nouveaux states
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
                    transition.end for state in current for transition in self.states[state].out_transitions if
                    transition.symbol == symbol
                )

                if not next_states:
                    continue
                next_name = get_state_name(next_states)

                if next_name not in new_states:
                    new_states[next_name] = State(next_name)
                    queue.append(next_states)
                    if any(state in self.final_states for state in next_states):
                        new_final_states.add(next_name)

                # Add the transition to the new DFA
                new_transitions.append(Transition(symbol, current_name, next_name))

        # Update automaton to be the constructed DFA
        self.states = new_states
        self.transitions = new_transitions
        self.initial_states = [get_state_name(new_initial_state)]
        self.final_states = list(new_final_states)

    def make_complete(self):
        # Ensure there is a sink state for any missing transitions
        sink_state_added = False
        sink_state_name = 'sink'

        #regarde toutes les transitions possibles
        for state in list(self.states.keys()):
            transitions_symbols = {transition.symbol for transition in self.states[state].out_transitions}
            missing_symbols = set(self.alphabet) - transitions_symbols

            # cherche des transistions manquantes qui doivent aller dans le sink state
            for symbol in missing_symbols:
                if not sink_state_added:
                    self.add_state(State(sink_state_name))
                    sink_state_added = True
                self.add_transition(Transition(symbol, state, sink_state_name))

        if sink_state_added:
            for symbol in self.alphabet:
                self.add_transition(Transition(symbol, sink_state_name, sink_state_name))
