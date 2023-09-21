"""
Artifact specification registry module.
"""
from sdk.entities.artifact.kinds import ArtifactKinds
from sdk.entities.artifact.spec.models import ArtifactParamsArtifact
from sdk.entities.artifact.spec.objects import ArtifactSpecArtifact

REGISTRY_SPEC = {ArtifactKinds.ARTIFACT.value: ArtifactSpecArtifact}
REGISTRY_MODEL = {ArtifactKinds.ARTIFACT.value: ArtifactParamsArtifact}
