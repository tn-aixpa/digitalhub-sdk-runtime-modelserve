//[x]:
Da env leggere tutte le configurazione di postgres ( CON PYTHON )
POSTGRES_DB
POSTGRES_HOST
... USER
... PASSWORD
... PORT

//[x]:
LEGGERE I DATI DAL BACKEND

//TODO:

- creare i log della run prendendoli da kubernetes
  - da capire se vanno inseriti i log che mostro tramite lo script python o no.
- dovrei creare per la run una state machine per passare da uno stato all'altro

- [x] aggiornare lo state della run monitorando gli Eventi di kuberntesClient

- [x] inserire "state" in status :{...., state:""}. Mettere json ignore in state

- [x]rinomirare output in outputs:[] -> list di referenze di output...(modelli)
- [x]inserire inputs:{dataitems: []} -> lista di referenze di dataitem in input (nome oppure nome:versione)

- [x]inserire {ref(.....)} all'interno della query
- [x]nel wrapper recuperare tutti gli inputs da S3...con versione o il latest, otteniamo quindi un dataitem da importare in postgres. In ogni caso la tabella creata avra' nome*versione : <name>*<version>

- [x] key in dataitems e' il nome dell'output
- [x] la uuid del dataitem va generata nel wrapper e passata alla creazione del dataitem.

- [x]: processEvent deve esser sincronized.( in ogni caso non funziona )

TODO: delete isAuto in StateMachine

TODO: spostare la logica di exit e entry action dallo stato alla StateMachine come mappa di conseguenza quando ho sono in uno stato ed esco ad esempio controllo la mappa delle exit action con quello stato e se presente la eseguo

- [x]: Salvare il log del pod in plain-text.

TODO : Estrarre il builder di kubernetes creando una classe astratta che mi fornisce L'Env di base e chi estende la classe astratta fornisce il dettaglio dei parametri e termina la configurazione del job.
