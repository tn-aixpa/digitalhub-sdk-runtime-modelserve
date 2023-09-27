"""
Artifact specification registry module.
"""
from sdk.entities.artifact.kinds import ArtifactKinds
from sdk.entities.artifact.spec.models import ArtifactParamsArtifact
from sdk.entities.artifact.spec.objects import ArtifactSpecArtifact

ARTIFACT_SPEC = {ArtifactKinds.ARTIFACT.value: ArtifactSpecArtifact}
ARTIFACT_MODEL = {ArtifactKinds.ARTIFACT.value: ArtifactParamsArtifact}
