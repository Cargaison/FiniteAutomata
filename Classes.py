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

def creationlangage(x):
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    langage = []
    if x <= 26:
        for i in range(x):
            langage.append(alphabet[i])
    return langage


def show_automata(automata):
    max_level =0
    for level in range(0,len(automata.states)):
        if len(automata.states[level].out_transitions) > max_level:
            max_level = len(automata.states[level].out_transitions)
    for state in automata.states:
        print(state.name, end="")
        if state.out_transitions:
            print(f" ->", state.out_transitions[0].language," ->",end="")
    print("")
