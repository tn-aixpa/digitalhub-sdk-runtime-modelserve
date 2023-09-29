"""
Artifact specification registry module.
"""
from sdk.entities.artifacts.kinds import ArtifactKinds
from sdk.entities.artifacts.spec.models import ArtifactParamsArtifact
from sdk.entities.artifacts.spec.objects import ArtifactSpecArtifact

ARTIFACT_SPEC = {ArtifactKinds.ARTIFACT.value: ArtifactSpecArtifact}
ARTIFACT_MODEL = {ArtifactKinds.ARTIFACT.value: ArtifactParamsArtifact}
