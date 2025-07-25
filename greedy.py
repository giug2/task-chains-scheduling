from collections import defaultdict


def greedy_allocation_round_robin(agents, slot_capacities):
    """
    Assegna i task in modo round-robin: prima tutti i task 1, poi tutti i task 2, ecc.
    Ogni task viene assegnato al primo time slot disponibile che ha capacità sufficiente.
    """
    num_slots = len(slot_capacities)
    slot_usage = [0] * num_slots
    allocation = {}

    max_tasks = max(len(agent.tasks) for agent in agents)

    for task_index in range(max_tasks):  # round
        for agent in agents:
            if task_index < len(agent.tasks):
                task = agent.tasks[task_index]
                for slot in range(num_slots):
                    if slot_usage[slot] + task.resource <= slot_capacities[slot]:
                        allocation[(agent.id, task.index)] = slot
                        slot_usage[slot] += task.resource
                        break

    return allocation


def evaluate_agent_costs(allocation, agents):
    """
    Restituisce un dizionario: agente -> costo medio
    """
    return {a.id: a.cost(allocation) for a in agents}


def print_allocation(allocation, agents):
    """
    Stampa per ogni agente: time slot assegnati (in ordine di task) + costo medio
    """
    agent_slots = defaultdict(list)
    for (agent_id, task_index), slot in allocation.items():
        agent_slots[agent_id].append((task_index, slot))

    for agent in agents:
        slots = sorted(agent_slots[agent.id])  # ordina i task per indice
        only_slots = [s for _, s in slots]
        cost = agent.cost(allocation)
        print(f"Agente {agent.id}: {only_slots} (avg cost = {cost:.2f})")
