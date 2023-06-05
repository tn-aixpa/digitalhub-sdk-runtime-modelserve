# creare nuova context api

// [x] Done
Any object has a context that is the 'project'

- project + name -> List of all version
- project + name + uuid -> Specific element
- project + name + '/latest' get latest specific element for the the project.

This pattern is applied to all Models

Artifact:

/api/v1/-/ProjectName/artifacts/ArtifactName -> List of Artifact
/api/v1/-/ProjectName/artifacts/ArtifactName/90i23o-fdkfjl-fdkjfkld-fjdhfkn -> Artifact
/api/v1/-/ProjectName/artifacts/ArtifactName/latest -> Artifact

// TODO: EMBEDDED
Project : quando prendo il progetto mostro tutte le functions, workflows, artifacts. Se quest ultime contengono il campo embedded : true, mostro i dati completi con spec e extra, altrimenti mostro solamente il kind ed il name.

// TODO: SYNC WITH MLRUN

- CAll mlrun api to sync data
  - Mlrun -> DHCORE
  - DHCORE <- Mlrun

Check DB and API for DATA sync, write service for sync

- Project
- Function
- Artifact
- Dataitem
- Workflow
