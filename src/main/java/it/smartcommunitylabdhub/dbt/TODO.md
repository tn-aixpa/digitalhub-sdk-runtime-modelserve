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
