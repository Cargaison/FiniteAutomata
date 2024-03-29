class Transition:
    def __init__(self, language, begin, end):
        self.language = language
        self.begin = begin
        self.end = end

class State:
    def __init__(self, nom):
        self.name = nom
        self.out_transitions = []
        self.in_transitions = []
    def add_outgoing_transition(self, transition):
        self.out_transitions.append(transition)
    def add_incoming_transition(self, transition):
        self.in_transitions.append(transition)

class Automata:
    def __init__(self):
        self.states = []
        self.transitions = []
    def add_state(self, state):
        self.states.append(state)
    def add_transition(self, transition):
        self.transitions.append(transition)
        for state in self.states:
            if state.name == transition.begin:
                state.add_outgoing_transition(transition)
            if state.name == transition.end:
                state.add_incoming_transition(transition)

def creationlangage(x):
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    langage = []
    if x <= 26:
        for i in range(x):
            langage.append(alphabet[i])
    return langage

def print_automata(automata):
    for transition in automata.transitions:
        print(f"{transition.begin} --{transition.language}--> {transition.end}")
def show_automata(automata):
    for state in automata.states:
        print(state.name, end="")
        for transition in range(0, len(state.out_transitions)-1):
            print(f" ->", state.out_transitions[transition].language," ->",end="")
