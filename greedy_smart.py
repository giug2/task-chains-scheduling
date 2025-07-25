from collections import defaultdict
import copy


# === ALGORITMO GREEDY SMART ===
def smart_greedy_allocation(agents, slot_capacities):
    """
    Greedy intelligente: assegna ogni task allo slot che riduce al minimo
    il costo medio dell’agente, rispettando capacità e ordine dei task.
    """
    num_slots = len(slot_capacities)
    slot_usage = [0] * num_slots
    allocation = {}
    task_pointers = {agent.id: 0 for agent in agents}

    while True:
        any_assigned = False  # almeno un task assegnato nel giro corrente

        for agent in agents:
            i = task_pointers[agent.id]
            if i >= len(agent.tasks):
                continue  # agente è stato completato

            task = agent.tasks[i]
            prev_slot = allocation.get((agent.id, task.index - 1), -1)
            best_slot = None
            best_cost = float("inf")

            for slot in range(prev_slot + 1, num_slots):
                if slot_usage[slot] + task.resource <= slot_capacities[slot]:
                    # Simula
                    temp_alloc = copy.deepcopy(allocation)
                    temp_alloc[(agent.id, task.index)] = slot
                    cost = agent.cost(temp_alloc)
                    if cost < best_cost:
                        best_cost = cost
                        best_slot = slot

            if best_slot is not None:
                allocation[(agent.id, task.index)] = best_slot
                slot_usage[best_slot] += task.resource
                task_pointers[agent.id] += 1
                any_assigned = True

        if not any_assigned:
            break  # nessun task è stato assegnato in questo giro, esco dal ciclo

    return allocation
