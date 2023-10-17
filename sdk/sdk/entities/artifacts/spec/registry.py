"""
Artifact specification registry module.
"""
from sdk.entities.artifacts.kinds import ArtifactKinds
from sdk.entities.artifacts.spec.objects.artifact import ArtifactParamsArtifact, ArtifactSpecArtifact
from sdk.entities.base.spec import SpecRegistry

artifact_registry = SpecRegistry()
artifact_registry.register(ArtifactKinds.ARTIFACT, ArtifactSpecArtifact, ArtifactParamsArtifact)
