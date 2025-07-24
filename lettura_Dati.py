import os
import pandas as pd

class Task:
    def __init__(self, agent, index, resource):
        self.agent = agent
        self.index = index
        self.resource = resource

    def __repr__(self):
        return f"{self.agent}{self.index}({self.resource})"

class Agent:
    def __init__(self, name, task_resources):
        self.name = name
        self.tasks = [Task(name, i + 1, r) for i, r in enumerate(task_resources)]

    def cost(self, allocation):
        """
        Calcola il costo medio dell’agente come media dei time slot assegnati ai suoi task.
        """
        slots = [allocation[(self.name, t.index)] for t in self.tasks if (self.name, t.index) in allocation]
        return sum(slots) / len(slots) if slots else float('inf')

def load_agents_data(base_dir):
    agents = []
    slot_capacities = None

    for agent_id in sorted(os.listdir(base_dir), key=lambda x: int(x)):
        agent_path = os.path.join(base_dir, agent_id)
        if not os.path.isdir(agent_path):
            continue

        req_path = os.path.join(agent_path, f"I_{agent_id}_requirements.csv")
        cap_path = os.path.join(agent_path, f"I_{agent_id}_capacities.csv")

        # Caricamento dei requirements (prendiamo solo la prima riga come lista dei task)
        requirements_df = pd.read_csv(req_path, header=None)
        requirements_str = requirements_df.iloc[0, 0]
        requirements = [int(x) for x in requirements_str.split(";")]

        agent = Agent(agent_id, requirements)
        agents.append(agent)

        # Caricamento delle capacità (solo una volta, poiché è globale)
        if slot_capacities is None:
            capacities_df = pd.read_csv(cap_path, header=None)
            capacities_str = capacities_df.iloc[0, 0]
            slot_capacities = [int(x) for x in capacities_str.split(";")]

    return agents, slot_capacities
