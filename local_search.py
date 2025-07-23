import copy

def is_feasible(allocation, agents, slot_capacities):
    """
    Verifica che l'allocazione rispetti:
    - le capacità di ciascuno slot
    - l'ordine dei task per ogni agente
    """
    slot_usage = [0] * len(slot_capacities)

    for (agent_name, task_index), slot in allocation.items():
        task = next(t for a in agents if a.name == agent_name for t in a.tasks if t.index == task_index)
        slot_usage[slot] += task.resource
        if slot_usage[slot] > slot_capacities[slot]:
            return False

    for agent in agents:
        slots = [allocation[(agent.name, t.index)] for t in agent.tasks if (agent.name, t.index) in allocation]
        if any(slots[i] > slots[i + 1] for i in range(len(slots) - 1)):
            return False

    return True

def find_max_cost_agent(allocation, agents):
    return max(agents, key=lambda a: a.cost(allocation))

def local_search_critical_agent(allocation, agents, slot_capacities, max_iter=1000):
    """
    Ricerca locale sull'agente con il costo medio massimo.
    Prova a spostare uno dei suoi task in uno slot diverso (ammissibile) per ridurre il costo.
    """
    best_alloc = copy.deepcopy(allocation)
    best_costs = {a.name: a.cost(best_alloc) for a in agents}
    worst_agent = max(best_costs, key=best_costs.get)

    for _ in range(max_iter):
        improved = False
        agent = next(a for a in agents if a.name == worst_agent)

        for task in agent.tasks:
            old_slot = best_alloc[(agent.name, task.index)]
            for new_slot in range(len(slot_capacities)):
                if new_slot == old_slot:
                    continue

                new_alloc = copy.deepcopy(best_alloc)
                new_alloc[(agent.name, task.index)] = new_slot

                if not is_feasible(new_alloc, agents, slot_capacities):
                    continue

                new_costs = {a.name: a.cost(new_alloc) for a in agents}
                if new_costs[agent.name] < best_costs[agent.name]:
                    best_alloc = new_alloc
                    best_costs = new_costs
                    improved = True
                    break

            if improved:
                break

        if not improved:
            break

    return best_alloc
