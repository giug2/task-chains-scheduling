from loader import load_instance
from greedy import greedy_allocation_round_robin, evaluate_agent_costs, print_allocation
from greedy_v2 import smart_greedy_allocation
from local_search import local_search_critical_agent


# Carica l'istanza da una cartella, es: "MLE/1"
agents, slot_capacities = load_instance("MLE/7")

print("Numero agenti:", len(agents))
print("Numero slot:", len(slot_capacities))
print("Capacità slot:", slot_capacities)
print("Esempio agente:", [(t.index, t.resource) for t in agents[0].tasks])


# Fase 1: Greedy
#allocation_greedy = greedy_allocation_round_robin(agents, slot_capacities)
allocation_greedy = smart_greedy_allocation(agents, slot_capacities)

print("=== Soluzione Greedy ===")
print_allocation(allocation_greedy, agents)

# Individua l'agente peggiore
costs_greedy = evaluate_agent_costs(allocation_greedy, agents)
worst_id = max(costs_greedy, key=costs_greedy.get)
print(f"\nAgente peggiore: {worst_id} (costo medio = {costs_greedy[worst_id]:.2f})")

# Fase 2: Ricerca locale sull'agente peggiore
optimized = local_search_critical_agent(allocation_greedy, agents, slot_capacities)

print("\n=== Dopo Ricerca Locale ===")
print_allocation(optimized, agents)

# === Confronto finale ===
costs_opt = evaluate_agent_costs(optimized, agents)
worst_opt = max(costs_opt, key=costs_opt.get)
print(f"\nAgente peggiore dopo local search: {worst_opt} (costo medio = {costs_opt[worst_opt]:.2f})")

# === CHECK: greedy == locale?
same_alloc = allocation_greedy == optimized
print(f"\nCoincidenza allocazione Greedy / Locale? {' Sì' if same_alloc else ' No'}")
