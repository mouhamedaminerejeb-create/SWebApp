
### Applicazione web per eventi sportivi live

Si richiede di realizzare una web application che mostri risultati, tempo di gioco ed eventi di match sportivi, con aggiornamenti automatici in tempo reale.

---

**Specifiche e indicazioni generali**

L’applicazione deve gestire almeno 5 match.
Si lascia libertà nella scelta:

- dello sport (calcio, basket, tennis, ecc) ed eventualmente più di una scelta.
- del numero e del tipo di eventi associati ai match (punti/goal, ammonizioni, interrruzioni ecc..)
- dell’organizzazione dei dati
- dell’aspetto grafico e della struttura del progetto

--- 
**Pagina principale**

L'utente visita la pagina principale e visualizza lo stato di tutti i match (terminati, programmati e **live**).

In particolare gli aggiornamenti della pagina principale devono mostrare:
- tempo di gioco (cronometro o minuto)
- indicazioni visive del risultato live e degli eventi principali del match (Ad esempio con icone, emojii, simboli)

🏀  🎾  ❌ ⚽ 🔁 ⏸️ 🟥 🟨 🟦 ⏱️ ⏰ ▶️ ⏹️ 🔴 ⚪ 🔔 📢 ⭐ 🔥 👁️
 
I dati devono aggiornarsi automaticamente, senza ricaricare la pagina.

---
**Dettaglio del match**

Cliccando su un match si deve accedere a una pagina di dettaglio, dove visualizzare:

- informazioni complete del match
- elenco degli eventi in ordine temporale
- aggiornamenti coerenti in tempo reale

---

**Il tempo di gioco e relativi aggiornamenti (tempo, punteggio, eventi) deve essere gestito dal backend, simulando l'evoluzione del match.**

**Il frontend si limita a visualizzare i dati ricevuti.**


Il backend può essere progettato in modo da:
- mantenere in memoria lo stato dei match (tempo, punteggio, eventi) in run-time
- simulare il passare del tempo tramite un meccanismo periodico
- generare eventi in modo automatico o semi-casuale
- inviare aggiornamenti tramite WebSocket
- fornire i dati iniziali tramite richieste HTTP/Ajax come ad esempio l'elenco dei match e lo stato iniziale (tempo, punteggio, eventi già avvenuti)

Non è richiesto l’uso di database.


**Le scelte implementative sono libere, purché coerenti con il funzionamento richiesto.**

---

Richieste facoltative:
- classifica aggiornata in tempo reale (simulando un campionato/competizione)
- gestione di match programmati / in corso / terminati
- notifiche visive o sonore
