from Classes import (Transition, State, Automata, creationlangage,
                     print_automata, show_automata)



t1 = Transition(creationlangage(2), "1", "2")
t2 = Transition(creationlangage(1), "2", "1")
t3 = Transition(["b"], "2","3")
state1 = State("1")
state2 = State("2")
state3 = State("3")
state1.add_outgoing_transition(t1)
state2.add_incoming_transition(t1)
state3.add_incoming_transition(t3)
state2.add_outgoing_transition(t3)
auto1 = Automata()
auto1.add_state(state1)
auto1.add_state(state2)
auto1.add_state(state3)
auto1.add_transition(t1)
auto1.add_transition(t2)
auto1.add_transition(t3)
show_automata(auto1)