# Level Up Festival
Creato da Dandolo Giacomo, con matricola S296525.

## Descrizione del progetto
Si noti come l'applicazione risulta essere completamente responsive.

### I - Base
Nell'header, presente all'interno di ogni pagina, sarà possibile cliccare sul logo del festival per tornare alla homepage.

Nel footer sarà presente il nome della compagnia (fittizia) che gestisce il festival e, all'estrema destra, il logo di Spotify, che permette di aprire una playlist contenente ogni brano che sarà riprodotto all'interno del festival.

### II - Homepage
All'interno della homepage è presente un carosello, che mostra i temi delle varie giornate, rispettivamente:
- venerdì: musica metal;
- sabato: musica rock;
- domenica: musica classica.

Successivamente, sarà presente una barra che permette di filtrare le performance presenti nella homepage, identificate dai rispettivi artisti. Il filtro può avvenire rispetto a data, palco e genere.

Ogni scheda dell'artista potrà essere cliccata, in modo da vedere le informazioni riguardanti l'artista, la performance e il palco associato alla performance.

### III - Registrazione
All'interno della pagina di registrazione è possibile inserire le proprie informazioni, in modo da registrarsi. Si può definire la tipologia di utente con cui registrarsi, che può essere "Partecipante" o "Organizzatore".

### IV - Login
All'interno della pagina di login è possibile effettuare il login con delle credenziali utilizzate per registrarsi precedentemente nella pagina di registrazione.

Successivamente al login, è possibile effettuare il logout in qualsiasi momento attraverso il rispettivo pulsante.

### V - Profilo
Il profilo permette di vedere le informazioni riguardanti l'utente attualmente loggato, per cui si evidenzia anche il tipo di utente.

In base al tipo di utente, si possono vedere informazioni differenti:
- partecipante: 
    - se il biglietto è stato acquistato, si possono vedere le informazioni riguardanti la tipologia e i giorni per cui è stato acquistato;
    - se il biglietto non è stato acquistato, verrà mostrato un messaggio di acquisto non ancora effettuato.
- organizzatore: 
    - i guadagni ottenuti per ogni tipologia di biglietto, oltre al guadagno totale;
    - i partecipanti per ogni giorno, con un massimo di 200 partecipanti per giornata;
    - le performance non pubblicate per quel determinato collaboratore;
    - tutte le performance pubblicate.

Nel caso dell'organizzatore, cliccando sulla performance non pubblicata è possibile andare sull'artista in bozza, verificando le sue informazioni che, cliccando sul pulsante di modifica, è possibile aggiornare.

### VI - Performance
All'interno della pagina della performance è possibile inserire tutte le informazioni necessarie, comprendendo le informazioni dell'artista e della rispettiva performance. Inoltre, è possibile evidenziare l'inserimento della performance come bozza, in modo da non pubblicarla nella homepage, ma mantenerla come non pubblicata per il collaboratore che la sta inserendo.

Si deve notare come, per evitare inconsistenze all'interno degli orari, una performance che tenta di essere pubblicata con sovrapposizioni degli orari viene impostata automaticamente cancellata. 

Le immagini possono essere salvate solo se sono con il formato indicato (jpeg, jpg, png o webp), e sono state salvate con le seguenti dimensioni:
- immagine dell'artista 400x400;
- immagine della performance di dimensione pari a quella inserita.

Per renderle univoche all'interno della cartella ```static``` si è utilizzato il timestamp, definendo il nome del file attraverso il seguente formato:
```
<nome_artista>_<timestamp>.<estensione>
```

### VII - Biglietti
All'interno della pagina per l'acquisto dei biglietti è possibile acquistare una delle tre tipologie:
- biglietto singolo: seleziona un singolo giorno del festival;
- biglietto doppio: seleziona un intervallo di due giorni del festival;
- biglietto platino: seleziona, in automatico, tutti e tre i giorni del festival.

Si deve notare come l'acquisto del biglietto è possibile solo per i partecipanti. I collaboratori possono visionare la pagina, ma non possono acquistare alcun biglietto. Ciò è stato fatto per permettere ai collaboratori di conoscere ogni possibile pagina del sito.

## Credenziali disponibili
Le seguenti credenziali saranno inserite mostrando il nome dell'utente, l'email con la quale è necessario eseguire il login e la relativa password.

### Primo Collaboratore
primo.collaboratore@mail.com\
Primo$Collaboratore1
> Nota: sono presenti due performance non pubblicate.

### Secondo Collaboratore
secondo.collaboratore@mail.com\
Secondo$Collaboratore2
> Nota: è presente una performance non pubblicata.

### Primo Partecipante
primo.partecipante@mail.com\
Primo$Partecipante1
> Nota: è presente un biglietto singolo per il giorno 19/07/2025.

### Secondo Partecipante
secondo.partecipante@mail.com\
Secondo$Partecipante2
> Nota: è presente un biglietto doppio per l'intervallo di giorni 19/07/2025 - 20/07/2025.

### Terzo Partecipante
terzo.partecipante@mail.com\
Terzo$Partecipante3
> Nota: è presente un biglietto platino.

## Deploy su PythonAnywhere
Il deploy del sito è disponibile all'indirizzo https://www.doje.pythonanywhere.com.
