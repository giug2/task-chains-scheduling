from collections import defaultdict

def greedy_allocation_round_robin(agents, slot_capacities):
    """
    Algoritmo greedy: assegna i task a round (prima i task 1 di tutti, poi i task 2, ecc.).
    Rispetta capacità degli slot e ordine dei task.
    """
    T = len(slot_capacities)
    slot_usage = [0] * T
    allocation = {}
    max_tasks = max(len(a.tasks) for a in agents)

    for i in range(max_tasks):
        for agent in agents:
            if i < len(agent.tasks):
                task = agent.tasks[i]
                for t in range(T):
                    if slot_usage[t] + task.resource <= slot_capacities[t]:
                        allocation[(agent.name, task.index)] = t
                        slot_usage[t] += task.resource
                        break

    return allocation

def evaluate_agent_costs(allocation, agents):
    return {a.name: a.cost(allocation) for a in agents}

def print_allocation(allocation, agents):
    agent_slots = defaultdict(list)
    for (agent, i), slot in allocation.items():
        agent_slots[agent].append((i, slot))

    for agent in agents:
        sorted_tasks = sorted(agent_slots[agent.name])
        cost = agent.cost(allocation)
        print(f"{agent.name}: {[s for _, s in sorted_tasks]} (avg cost = {cost:.2f})")
