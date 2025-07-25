import os
import pandas as pd


# === CLASSE TASK ===
class Task:
    def __init__(self, agent_id, index, resource):
        self.agent_id = agent_id
        self.index = index
        self.resource = resource

    def __repr__(self):
        return f"{self.agent_id}{self.index}({self.resource})"


# === CLASSE AGENT ===
class Agent:
    def __init__(self, agent_id, task_resources):
        self.id = agent_id
        self.tasks = [Task(agent_id, i + 1, r) for i, r in enumerate(task_resources)]

    # Costo medio: media dei time slot assegnati ai suoi task.
    def cost(self, allocation):
        slots = [allocation.get((self.id, t.index), 0) for t in self.tasks]
        return sum(slots) / len(slots) if slots else float('inf')


# Carica un'istanza del problema dalla cartella `MLE/<id>/`
def load_instance(instance_dir):
    # Trova l'id dell'istanza
    instance_id = os.path.basename(instance_dir)

    # Percorsi dei file
    size_path = os.path.join(instance_dir, f"I_{instance_id}_size.csv")
    cap_path = os.path.join(instance_dir, f"I_{instance_id}_capacities.csv")
    req_path = os.path.join(instance_dir, f"I_{instance_id}_requirements.csv")

    # Caricamento size.csv: numero agenti, numero slot
    size_values = pd.read_csv(size_path, header=None).iloc[0, 0]
    num_agents, num_slots = map(int, size_values.split(";"))

    # Caricamento capacities.csv: capacità di ogni slot
    capacities_line = pd.read_csv(cap_path, header=None).iloc[0, 0]
    slot_capacities = list(map(int, capacities_line.split(";")))
    assert len(slot_capacities) == num_slots

    # Caricamento requirements.csv: ogni riga = un agente, ogni valore = un task
    requirements_df = pd.read_csv(req_path, header=None)
    agents = []
    for i, row in enumerate(requirements_df.itertuples(index=False)):
        task_str = row[0]  # riga come stringa "10;12;5;8"
        task_resources = list(map(int, task_str.split(";")))
        agent = Agent(str(i), task_resources)
        agents.append(agent)

    return agents, slot_capacities
