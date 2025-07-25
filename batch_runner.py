import os
from loader import load_instance
from greedy import greedy_allocation_round_robin, evaluate_agent_costs, print_allocation
from local_search import local_search_critical_agent

OUTPUT_DIR = "output"

def run_instance_and_capture(path, label):
    agents, slot_capacities = load_instance(path)
    output_lines = []
    output_lines.append(f" Istanza: {label}")
    output_lines.append(f"- Agenti: {len(agents)}")
    output_lines.append(f"- Slot: {len(slot_capacities)}")
    
    # === GREEDY ===
    allocation_greedy = greedy_allocation_round_robin(agents, slot_capacities)
    output_lines.append("\n=== Soluzione Greedy ===")
    
    from io import StringIO
    import sys
    temp_out = StringIO()
    sys.stdout = temp_out
    print_allocation(allocation_greedy, agents)
    sys.stdout = sys.__stdout__
    output_lines.append(temp_out.getvalue().strip())

    costs_greedy = evaluate_agent_costs(allocation_greedy, agents)
    worst = max(costs_greedy, key=costs_greedy.get)
    output_lines.append(f"\nAgente peggiore: {worst} (costo medio = {costs_greedy[worst]:.2f})")

    # === LOCAL SEARCH ===
    allocation_opt = local_search_critical_agent(allocation_greedy, agents, slot_capacities)
    output_lines.append("\n=== Dopo Ricerca Locale ===")
    temp_out = StringIO()
    sys.stdout = temp_out
    print_allocation(allocation_opt, agents)
    sys.stdout = sys.__stdout__
    output_lines.append(temp_out.getvalue().strip())

    costs_opt = evaluate_agent_costs(allocation_opt, agents)
    worst_opt = max(costs_opt, key=costs_opt.get)
    output_lines.append(f"\nAgente peggiore dopo local search: {worst_opt} (costo medio = {costs_opt[worst_opt]:.2f})")

    return "\n".join(output_lines)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for base in ["MLE", "MMLE"]:
        for i in range(1, 11):
            folder = os.path.join(base, str(i))
            label = f"{base}_{i}"
            output_text = run_instance_and_capture(folder, label)
            out_path = os.path.join(OUTPUT_DIR, f"{label}.txt")
            with open(out_path, "w") as f:
                f.write(output_text)
            print(f"Completata {label} → salvato in {out_path}")

if __name__ == "__main__":
    main()
