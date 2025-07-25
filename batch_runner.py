import os
import sys
import csv
from io import StringIO
from loader import load_instance
from greedy import greedy_allocation_round_robin, evaluate_agent_costs, print_allocation
from greedy_v2 import smart_greedy_allocation
from local_search import local_search_critical_agent


OUTPUT_DIR = "output_round_robin"
summary_rows = []

def run_instance_and_capture(path, label):
    agents, slot_capacities = load_instance(path)
    output_lines = []
    output_lines.append(f" Istanza: {label}")
    output_lines.append(f"- Agenti: {len(agents)}")
    output_lines.append(f"- Slot: {len(slot_capacities)}")
    
    # === GREEDY ===
    allocation_greedy = greedy_allocation_round_robin(agents, slot_capacities)
    # allocation_greedy = smart_greedy_allocation(agents, slot_capacities)
    output_lines.append("\n=== Soluzione Greedy ===")
    
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

    # === CHECK: greedy == locale?
    same_alloc = allocation_greedy == allocation_opt
    output_lines.append(f"\nCoincidenza allocazione Greedy / Locale? {' Sì' if same_alloc else ' No'}")

    # === RIGA RIASSUNTIVA ===
    summary_rows.append({
        "istanza": label,
        "agente_peggiore_greedy": worst,
        "costo_greedy": round(costs_greedy[worst], 2),
        "agente_peggiore_locale": worst_opt,
        "costo_locale": round(costs_opt[worst_opt], 2),
        "stesso_agente": worst == worst_opt,
        "guadagno": round(costs_greedy[worst] - costs_opt[worst_opt], 2)
    })

    return "\n".join(output_lines)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for base in ["MLE", "MMLE"]:
        for i in range(1, 11):
            folder = os.path.join(base, str(i))
            label = f"{base}_{i}"
            output_text = run_instance_and_capture(folder, label)
            out_path = os.path.join(OUTPUT_DIR, f"{label}.txt")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(output_text)
            print(f"Completata {label} → salvato in {out_path}")
    
    summary_path = os.path.join(OUTPUT_DIR, "riassunto.csv")
    with open(summary_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["istanza", "agente_peggiore_greedy", "costo_greedy",
                    "agente_peggiore_locale", "costo_locale", "stesso_agente", "guadagno"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summary_rows)

    print(f"\nFile riassuntivo salvato in: {summary_path}")


if __name__ == "__main__":
    main()
