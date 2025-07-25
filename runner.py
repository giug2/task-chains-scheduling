from loader import load_instance
from greedy_round_robin import greedy_allocation_round_robin, evaluate_agent_costs, print_allocation
from greedy_smart import smart_greedy_allocation
from local_search import local_search_critical_agent


'''
Per poter eseguire il codice su una specifica istanza si può modificare questa riga inserendo il path esatto
'''
agents, slot_capacities = load_instance("dataset/MLE/1")


# === STAMPA DELLE INFORMAZIONI PRINCIPALI ===
print("Numero agenti:", len(agents))
print("Numero slot:", len(slot_capacities))
print("Capacità slot:", slot_capacities)
print("Esempio agente:", [(t.index, t.resource) for t in agents[0].tasks])


# === FASE 1: ALGORITMO GREEDY ===
'''
Le due righe di codice sottostante rappresentano i due metodi di approccio greedy:
round robin e smart, in base a ciò che si vuole far eseguire si commenta la riga che non serve
'''

# Per l'algoritmo greedy round robin
#allocation_greedy = greedy_allocation_round_robin(agents, slot_capacities)

# Per l'algoritmo greedy smart
allocation_greedy = smart_greedy_allocation(agents, slot_capacities)

print("=== Soluzione Greedy ===")
print_allocation(allocation_greedy, agents)

# Si individua l'agente peggiore
costs_greedy = evaluate_agent_costs(allocation_greedy, agents)
worst_id = max(costs_greedy, key=costs_greedy.get)
print(f"\nAgente peggiore: {worst_id} (costo medio = {costs_greedy[worst_id]:.2f})")

# === FASE 2: RICERCA LOCALE ===
optimized = local_search_critical_agent(allocation_greedy, agents, slot_capacities)

print("\n=== Dopo Ricerca Locale ===")
print_allocation(optimized, agents)

# === CONFRONTO FINALE ===
costs_opt = evaluate_agent_costs(optimized, agents)
worst_opt = max(costs_opt, key=costs_opt.get)
print(f"\nAgente peggiore dopo local search: {worst_opt} (costo medio = {costs_opt[worst_opt]:.2f})")

# === CHECK ===
same_alloc = allocation_greedy == optimized
print(f"\nCoincidenza allocazione Greedy / Locale? {' Sì' if same_alloc else ' No'}")
