# creare nuova context api

Any object has a context that is the 'project'

- project + name -> List of all version
- project + name + uuid -> Specific element
- project + name + '/latest' get latest specific element for the the project.

This pattern is applied to all Models

Artifact:

/api/v1/-/ProjectName/artifacts/ArtifactName -> List of Artifact

/api/v1/-/ProjectName/artifacts/ArtifactName/90i23o-fdkfjl-fdkjfkld-fjdhfkn -> Artifact

/api/v1/-/ProjectName/artifacts/ArtifactName/latest -> Artifact
