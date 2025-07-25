import copy

def is_feasible(allocation, agents, slot_capacities):
    """
    Verifica che l'allocazione:
    - non superi la capacità di ogni slot
    - rispetti l'ordine dei task per ciascun agente
    """
    num_slots = len(slot_capacities)
    slot_usage = [0] * num_slots

    # Calcola uso slot
    for (agent_id, task_index), slot in allocation.items():
        agent = next(a for a in agents if a.id == agent_id)
        task = next(t for t in agent.tasks if t.index == task_index)
        slot_usage[slot] += task.resource
        if slot_usage[slot] > slot_capacities[slot]:
            return False

    # Rispetta l'ordine dei task
    for agent in agents:
        assigned = [allocation[(agent.id, t.index)] for t in agent.tasks if (agent.id, t.index) in allocation]
        if any(assigned[i] > assigned[i + 1] for i in range(len(assigned) - 1)):
            return False

    return True

def find_max_cost_agent(allocation, agents):
    return max(agents, key=lambda a: a.cost(allocation))

def local_search_critical_agent(allocation, agents, slot_capacities, max_iter=1000):
    """
    Ricerca locale che cerca di migliorare il costo medio dell'agente peggiore.
    Sposta i suoi task in slot alternativi ammissibili.
    """
    best_alloc = copy.deepcopy(allocation)
    best_costs = {a.id: a.cost(best_alloc) for a in agents}
    worst_agent_id = max(best_costs, key=best_costs.get)

    for _ in range(max_iter):
        improved = False
        agent = next(a for a in agents if a.id == worst_agent_id)

        for task in agent.tasks:
            current_slot = best_alloc[(agent.id, task.index)]
            for new_slot in range(len(slot_capacities)):
                if new_slot == current_slot:
                    continue

                new_alloc = copy.deepcopy(best_alloc)
                new_alloc[(agent.id, task.index)] = new_slot

                if not is_feasible(new_alloc, agents, slot_capacities):
                    continue

                new_costs = {a.id: a.cost(new_alloc) for a in agents}
                if new_costs[agent.id] < best_costs[agent.id]:
                    best_alloc = new_alloc
                    best_costs = new_costs
                    improved = True
                    break

            if improved:
                break

        if not improved:
            break  # nessun miglioramento possibile

    return best_alloc
