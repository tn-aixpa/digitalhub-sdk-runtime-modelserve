from __future__ import annotations

import typing

from digitalhub_core.entities.artifact.crud import (
    create_artifact_from_dict,
    delete_artifact,
    get_artifact,
    list_artifacts,
    log_artifact,
    new_artifact,
)
from digitalhub_core.entities.entity_types import EntityTypes
from digitalhub_core.entities.function.crud import (
    create_function_from_dict,
    delete_function,
    get_function,
    list_functions,
    new_function,
)
from digitalhub_core.entities.project.entity.base import CTX_ENTITIES, FUNC_MAP, Project
from digitalhub_core.entities.secret.crud import (
    create_secret_from_dict,
    delete_secret,
    get_secret,
    list_secrets,
    new_secret,
)
from digitalhub_core.entities.workflow.crud import (
    create_workflow_from_dict,
    delete_workflow,
    get_workflow,
    list_workflows,
    new_workflow,
)

if typing.TYPE_CHECKING:
    from digitalhub_core.entities.artifact.entity._base import Artifact
    from digitalhub_core.entities.function.entity import Function
    from digitalhub_core.entities.secret.entity import Secret
    from digitalhub_core.entities.workflow.entity import Workflow


ARTIFACTS = EntityTypes.ARTIFACT.value
FUNCTIONS = EntityTypes.FUNCTION.value
WORKFLOWS = EntityTypes.WORKFLOW.value
SECRETS = EntityTypes.SECRET.value

CTX_ENTITIES.extend(
    [
        ARTIFACTS,
        FUNCTIONS,
        WORKFLOWS,
        SECRETS,
    ]
)
FUNC_MAP[ARTIFACTS] = create_artifact_from_dict
FUNC_MAP[FUNCTIONS] = create_function_from_dict
FUNC_MAP[WORKFLOWS] = create_workflow_from_dict
FUNC_MAP[SECRETS] = create_secret_from_dict


class ProjectCore(Project):
    ##############################
    #  Artifacts
    ##############################

    def new_artifact(
        self,
        name: str,
        kind: str,
        uuid: str | None = None,
        description: str | None = None,
        labels: list[str] | None = None,
        embedded: bool = True,
        path: str | None = None,
        src_path: str | None = None,
        **kwargs,
    ) -> Artifact:
        """
        Create an instance of the Artifact class with the provided parameters.

        Parameters
        ----------
        name : str
            Object name.
        kind : str
            Kind the object.
        uuid : str
            ID of the object (UUID4).
        description : str
            Description of the object (human readable).
        labels : list[str]
            List of labels.
        embedded : bool
            Flag to determine if object must be embedded in project.
        path : str
            Object path on local file system or remote storage.
            If not provided, it's generated.
        src_path : str
            Local object path.
        **kwargs : dict
            Spec keyword arguments.

        Returns
        -------
        Artifact
            Object instance.
        """
        obj = new_artifact(
            project=self.name,
            name=name,
            kind=kind,
            uuid=uuid,
            description=description,
            labels=labels,
            embedded=embedded,
            path=path,
            src_path=src_path,
            **kwargs,
        )
        self.refresh()
        return obj

    def get_artifact(
        self,
        identifier: str,
        entity_id: str | None = None,
        **kwargs,
    ) -> Artifact:
        """
        Get object from backend.

        Parameters
        ----------
        identifier : str
            Entity key or name.
        entity_id : str
            Entity ID.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        Artifact
            Instance of Artifact class.
        """
        obj = get_artifact(
            identifier=identifier,
            project=self.name,
            entity_id=entity_id,
            **kwargs,
        )
        self.refresh()
        return obj

    def delete_artifact(
        self,
        identifier: str,
        entity_id: str | None = None,
        delete_all_versions: bool = False,
        **kwargs,
    ) -> None:
        """
        Delete a Artifact from project.

        Parameters
        ----------
        identifier : str
            Entity key or name.
        entity_id : str
            Entity ID.
        delete_all_versions : bool
            Delete all versions of the named entity.
            Use entity name instead of entity key as identifier.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        None
        """
        delete_artifact(
            identifier=identifier,
            project=self.name,
            entity_id=entity_id,
            delete_all_versions=delete_all_versions,
            **kwargs,
        )
        self.refresh()

    def list_artifacts(self, **kwargs) -> list[dict]:
        """
        List artifacts associated with the project.

        Parameters
        ----------
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        list[dict]
            List of objects related to project.
        """
        return list_artifacts(self.name, **kwargs)

    def log_artifact(
        self,
        name: str,
        kind: str,
        source: str,
        path: str | None = None,
        **kwargs,
    ) -> Artifact:
        """
        Create and upload an artifact.

        Parameters
        ----------
        name : str
            Object name.
        kind : str
            Kind the object.
        source : str
            Artifact location on local machine.
        path : str
            Destination path of the artifact.
        **kwargs : dict
            New artifact parameters.

        Returns
        -------
        Artifact
            Instance of Artifact class.
        """
        obj = log_artifact(
            project=self.name,
            name=name,
            kind=kind,
            source=source,
            path=path,
            **kwargs,
        )
        self.refresh()
        return obj

    ##############################
    #  Functions
    ##############################

    def new_function(
        self,
        name: str,
        kind: str,
        uuid: str | None = None,
        description: str | None = None,
        labels: list[str] | None = None,
        embedded: bool = True,
        **kwargs,
    ) -> Function:
        """
        Create a Function instance with the given parameters.

        Parameters
        ----------
        name : str
            Object name.
        kind : str
            Kind the object.
        uuid : str
            ID of the object (UUID4).
        description : str
            Description of the object (human readable).
        labels : list[str]
            List of labels.
        embedded : bool
            Flag to determine if object must be embedded in project.
        **kwargs : dict
            Spec keyword arguments.

        Returns
        -------
        Function
            Object instance.
        """
        obj = new_function(
            project=self.name,
            name=name,
            kind=kind,
            uuid=uuid,
            description=description,
            labels=labels,
            embedded=embedded,
            **kwargs,
        )
        self.refresh()
        return obj

    def get_function(
        self,
        identifier: str,
        entity_id: str | None = None,
        **kwargs,
    ) -> Function:
        """
        Get object from backend.

        Parameters
        ----------
        identifier : str
            Entity key or name.
        entity_id : str
            Entity ID.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        Function
            Instance of Function class.
        """
        obj = get_function(
            identifier=identifier,
            project=self.name,
            entity_id=entity_id,
            **kwargs,
        )
        self.refresh()
        return obj

    def delete_function(
        self,
        identifier: str,
        entity_id: str | None = None,
        delete_all_versions: bool = False,
        cascade: bool = False,
        **kwargs,
    ) -> None:
        """
        Delete a Function from project.

        Parameters
        ----------
        identifier : str
            Entity key or name.
        entity_id : str
            Entity ID.
        delete_all_versions : bool
            Delete all versions of the named entity.
            Use entity name instead of entity key as identifier.
        cascade : bool
            Cascade delete.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        None
        """
        delete_function(
            identifier=identifier,
            project=self.name,
            entity_id=entity_id,
            delete_all_versions=delete_all_versions,
            cascade=cascade,
            **kwargs,
        )
        self.refresh()

    def list_functions(self, **kwargs) -> list[dict]:
        """
        List functions associated with the project.

        Parameters
        ----------
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        list[dict]
            List of objects related to project.
        """
        return list_functions(self.name, **kwargs)

    ##############################
    #  Workflows
    ##############################

    def new_workflow(
        self,
        name: str,
        kind: str,
        uuid: str | None = None,
        description: str | None = None,
        labels: list[str] | None = None,
        embedded: bool = True,
        **kwargs,
    ) -> Workflow:
        """
        Create a new Workflow instance with the specified parameters.

        Parameters
        ----------
        name : str
            Object name.
        uuid : str
            ID of the object (UUID4).
        description : str
            Description of the object (human readable).
        labels : list[str]
            List of labels.
        embedded : bool
            Flag to determine if object must be embedded in project.
        **kwargs : dict
            Spec keyword arguments.

        Returns
        -------
        Workflow
            An instance of the created workflow.
        """
        obj = new_workflow(
            project=self.name,
            name=name,
            kind=kind,
            uuid=uuid,
            description=description,
            labels=labels,
            embedded=embedded,
            **kwargs,
        )
        self.refresh()
        return obj

    def get_workflow(
        self,
        identifier: str,
        entity_id: str | None = None,
        **kwargs,
    ) -> Workflow:
        """
        Get object from backend.

        Parameters
        ----------
        identifier : str
            Entity key or name.
        entity_id : str
            Entity ID.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        Workflow
            Instance of Workflow class.
        """
        obj = get_workflow(
            identifier=identifier,
            project=self.name,
            entity_id=entity_id,
            **kwargs,
        )
        self.refresh()
        return obj

    def delete_workflow(
        self,
        identifier: str,
        entity_id: str | None = None,
        delete_all_versions: bool = False,
        cascade: bool = False,
        **kwargs,
    ) -> None:
        """
        Delete a Workflow from project.

        Parameters
        ----------
        identifier : str
            Entity key or name.
        entity_id : str
            Entity ID.
        delete_all_versions : bool
            Delete all versions of the named entity.
            Use entity name instead of entity key as identifier.
        cascade : bool
            Cascade delete.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        None
        """
        delete_workflow(
            identifier=identifier,
            project=self.name,
            entity_id=entity_id,
            delete_all_versions=delete_all_versions,
            cascade=cascade,
            **kwargs,
        )
        self.refresh()

    def list_workflows(self, **kwargs) -> list[dict]:
        """
        List workflows associated with the project.

        Parameters
        ----------
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        list[dict]
            List of objects related to project.
        """
        return list_workflows(self.name, **kwargs)

    ##############################
    #  Secrets
    ##############################

    def new_secret(
        self,
        name: str,
        uuid: str | None = None,
        description: str | None = None,
        labels: list[str] | None = None,
        embedded: bool = True,
        secret_value: str | None = None,
        **kwargs,
    ) -> Secret:
        """
        Create a new Secret instance with the specified parameters.

        Parameters
        ----------
        name : str
            Object name.
        uuid : str
            ID of the object (UUID4).
        description : str
            Description of the object (human readable).
        labels : list[str]
            List of labels.
        embedded : bool
            Flag to determine if object must be embedded in project.
        secret_value : str
            Value of the secret.
        **kwargs : dict
            Spec keyword arguments.

        Returns
        -------
        Secret
            An instance of the created secret.
        """
        obj = new_secret(
            project=self.name,
            name=name,
            uuid=uuid,
            description=description,
            labels=labels,
            embedded=embedded,
            secret_value=secret_value,
            **kwargs,
        )
        self.refresh()
        return obj

    def get_secret(
        self,
        identifier: str,
        entity_id: str | None = None,
        **kwargs,
    ) -> Secret:
        """
        Get object from backend.

        Parameters
        ----------
        identifier : str
            Entity key or name.
        entity_id : str
            Entity ID.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        Secret
            Instance of Secret class.
        """
        obj = get_secret(
            identifier=identifier,
            project=self.name,
            entity_id=entity_id,
            **kwargs,
        )
        self.refresh()
        return obj

    def delete_secret(
        self,
        identifier: str,
        entity_id: str | None = None,
        delete_all_versions: bool = False,
        **kwargs,
    ) -> None:
        """
        Delete a Secret from project.

        Parameters
        ----------
        identifier : str
            Entity key or name.
        entity_id : str
            Entity ID.
        delete_all_versions : bool
            Delete all versions of the named entity.
            Use entity name instead of entity key as identifier.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        None
        """
        delete_secret(
            identifier=identifier,
            project=self.name,
            entity_id=entity_id,
            delete_all_versions=delete_all_versions,
            **kwargs,
        )
        self.refresh()

    def list_secrets(self, **kwargs) -> list[dict]:
        """
        List secrets associated with the project.

        Parameters
        ----------
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        list[dict]
            List of objects related to project.
        """
        return list_secrets(self.name, **kwargs)
