# 🔎 Ricerca Greedy e Ricerca Locale
Progetto per la tesina del corso di Decision Support Systems and Analytics dell'A.A. 2024/2025.
## Problema
Il progetto si propone di affrontare un problema di allocazione di sequenze di task agent-based vincolati da capacità temporali.  
L’obiettivo principale è quello di pianificare l’allocazione di tali task agli slot temporali in modo da rispettare i vincoli di capacità e sequenzialità, minimizzando al tempo stesso il costo medio dell’agente che termina più tardi, come misura di equità nel sistema.
## Dataset
All'interno della cartella dataset sono presenti due diverse cartelle: MLE e MMLE, ciascuna contenente dieci diverse istanze del problema.  
Ogni istanza è descritta da tre diversi file csv:
- size.csv:  contiene due valori interi che rappresentano, in ordine, il numero di agenti e il numero di time slot disponibili per l’allocazione;
- capacities.csv: specifica la capacit`a disponibile in ciascun time slot, ossia ogni valore indica quante risorse possono essere allocate in quello slot:
- requirement.csv: descrive i task assegnati a ciascun agente. Ogni riga rappresenta un agente e contiene una sequenza di valori, dove ciascun valore indica la quantit`a di risorse richieste da un task specifico in sequenza.
## Approccio
Per risolvere il problema, si divide l’approccio in due fasi:
- una prima fase di costruzione basata su un algoritmo greedy,
- una seconda fase seguente di ricerca locale che cerca di migliorare la situazione dell’agente risultato peggiore.

## Autore
[Gaglione Giulia](https://github.com/giug2)
