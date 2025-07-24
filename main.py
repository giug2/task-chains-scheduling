from lettura_Dati import load_agents_data
from greedy import greedy_allocation_round_robin, print_allocation, evaluate_agent_costs
from local_search import local_search_critical_agent


# Caricamento dati
agents, slot_capacities = load_agents_data("MLE")


# Allocazione greedy
allocation = greedy_allocation_round_robin(agents, slot_capacities)


# Visualizza la soluzione
print("=== Soluzione Greedy ===")
print_allocation(allocation, agents)


# Costo massimo tra agenti
costs = evaluate_agent_costs(allocation, agents)
worst_agent = max(costs, key=costs.get)
print(f"\nAgente peggiore: {worst_agent} (costo medio = {costs[worst_agent]:.2f})")


# Local search partendo da soluzione greedy
optimized = local_search_critical_agent(allocation, agents, slot_capacities)


print("\n=== Dopo Ricerca Locale sull'agente peggiore ===")
print_allocation(optimized, agents)