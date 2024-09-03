from __future__ import annotations

import typing

from digitalhub_core.entities.artifact.crud import (
    artifact_from_dict,
    delete_artifact,
    get_artifact,
    get_artifact_versions,
    import_artifact,
    list_artifacts,
    log_artifact,
    new_artifact,
    update_artifact,
)
from digitalhub_core.entities.entity_types import EntityTypes
from digitalhub_core.entities.function.crud import (
    delete_function,
    function_from_dict,
    get_function,
    get_function_versions,
    import_function,
    list_functions,
    new_function,
    update_function,
)
from digitalhub_core.entities.project.entity._base import CTX_ENTITIES, FUNC_MAP, Project
from digitalhub_core.entities.secret.crud import (
    delete_secret,
    get_secret,
    get_secret_versions,
    import_secret,
    list_secrets,
    new_secret,
    secret_from_dict,
    update_secret,
)
from digitalhub_core.entities.workflow.crud import (
    delete_workflow,
    get_workflow,
    get_workflow_versions,
    import_workflow,
    list_workflows,
    new_workflow,
    update_workflow,
    workflow_from_dict,
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
FUNC_MAP[ARTIFACTS] = artifact_from_dict
FUNC_MAP[FUNCTIONS] = function_from_dict
FUNC_MAP[WORKFLOWS] = workflow_from_dict
FUNC_MAP[SECRETS] = secret_from_dict


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
        **kwargs,
    ) -> Artifact:
        """
        Create a new object.

        Parameters
        ----------
        name : str
            Object name.
        kind : str
            Kind the object.
        uuid : str
            ID of the object (UUID4, e.g. 40f25c4b-d26b-4221-b048-9527aff291e2).
        description : str
            Description of the object (human readable).
        labels : list[str]
            List of labels.
        embedded : bool
            Flag to determine if object spec must be embedded in project spec.
        path : str
            Object path on local file system or remote storage. It is also the destination path of upload() method.
        **kwargs : dict
            Spec keyword arguments.

        Returns
        -------
        Artifact
            Object instance.

        Examples
        --------
        >>> obj = project.new_artifact(name="my-artifact",
        >>>                            kind="artifact",
        >>>                            path="s3://my-bucket/my-key")
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
            **kwargs,
        )
        self.refresh()
        return obj

    def log_artifact(
        self,
        name: str,
        kind: str,
        source: str,
        path: str | None = None,
        **kwargs,
    ) -> Artifact:
        """
        Create and upload an object.

        Parameters
        ----------
        name : str
            Object name.
        kind : str
            Kind the object.
        source : str
            Artifact location on local path.
        path : str
            Destination path of the artifact. If not provided, it's generated.
        **kwargs : dict
            New artifact spec parameters.

        Returns
        -------
        Artifact
            Object instance.

        Examples
        --------
        >>> obj = project.log_artifact(name="my-artifact",
        >>>                            kind="artifact",
        >>>                            source="./local-path")
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
            Entity key (store://...) or entity name.
        entity_id : str
            Entity ID.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        Artifact
            Object instance.

        Examples
        --------
        Using entity key:
        >>> obj = project.get_artifact("store://my-artifact-key")

        Using entity name:
        >>> obj = project.get_artifact("my-artifact-name"
        >>>                            entity_id="my-artifact-id")
        """
        obj = get_artifact(
            identifier=identifier,
            project=self.name,
            entity_id=entity_id,
            **kwargs,
        )
        self.refresh()
        return obj

    def get_artifact_versions(
        self,
        identifier: str,
        **kwargs,
    ) -> list[Artifact]:
        """
        Get object versions from backend.

        Parameters
        ----------
        identifier : str
            Entity key (store://...) or entity name.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        list[Artifact]
            List of object instances.

        Examples
        --------
        Using entity key:
        >>> obj = project.get_artifact_versions("store://my-artifact-key")

        Using entity name:
        >>> obj = project.get_artifact_versions("my-artifact-name")
        """
        return get_artifact_versions(identifier, project=self.name, **kwargs)

    def list_artifacts(self, **kwargs) -> list[Artifact]:
        """
        List all latest version objects from backend.

        Parameters
        ----------
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        list[Artifact]
            List of object instances.

        Examples
        --------
        >>> objs = project.list_artifacts()
        """
        return list_artifacts(self.name, **kwargs)

    def import_artifact(
        self,
        file: str,
        **kwargs,
    ) -> Artifact:
        """
        Import object from a YAML file.

        Parameters
        ----------
        file : str
            Path to YAML file.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        Artifact
            Object instance.

        Examples
        --------
        >>> obj = project.import_artifact("my-artifact.yaml")
        """
        return import_artifact(file, **kwargs)

    def update_artifact(self, entity: Artifact) -> Artifact:
        """
        Update object. Note that object spec are immutable.

        Parameters
        ----------
        entity : Artifact
            Object to update.

        Returns
        -------
        Artifact
            Entity updated.

        Examples
        --------
        >>> obj = project.update_artifact(obj)
        """
        if entity.project != self.name:
            raise ValueError(f"Entity {entity.name} is not in project {self.name}.")
        return update_artifact(entity)

    def delete_artifact(
        self,
        identifier: str,
        entity_id: str | None = None,
        delete_all_versions: bool = False,
        **kwargs,
    ) -> None:
        """
        Delete object from backend.

        Parameters
        ----------
        identifier : str
            Entity key (store://...) or entity name.
        entity_id : str
            Entity ID.
        delete_all_versions : bool
            Delete all versions of the named entity. If True, use entity name instead of entity key as identifier.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        dict
            Response from backend.

        Examples
        --------
        If delete_all_versions is False:
        >>> project.delete_artifact("store://my-artifact-key")

        Otherwise:
        >>> project.delete_artifact("my-artifact-name",
        >>>                         delete_all_versions=True)
        """
        delete_artifact(
            identifier=identifier,
            project=self.name,
            entity_id=entity_id,
            delete_all_versions=delete_all_versions,
            **kwargs,
        )
        self.refresh()

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
        Create a new object.

        Parameters
        ----------
        name : str
            Object name.
        kind : str
            Kind the object.
        uuid : str
            ID of the object (UUID4, e.g. 40f25c4b-d26b-4221-b048-9527aff291e2).
        description : str
            Description of the object (human readable).
        labels : list[str]
            List of labels.
        embedded : bool
            Flag to determine if object spec must be embedded in project spec.
        **kwargs : dict
            Spec keyword arguments.

        Returns
        -------
        Function
            Object instance.

        Examples
        --------
        >>> obj = project.new_function(name="my-function",
        >>>                            kind="python",
        >>>                            code_src="function.py",
        >>>                            handler="function-handler")
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
            Entity key (store://...) or entity name.
        entity_id : str
            Entity ID.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        Function
            Object instance.

        Examples
        --------
        Using entity key:
        >>> obj = project.get_function("store://my-function-key")

        Using entity name:
        >>> obj = project.get_function("my-function-name"
        >>>                            entity_id="my-function-id")
        """
        obj = get_function(
            identifier=identifier,
            project=self.name,
            entity_id=entity_id,
            **kwargs,
        )
        self.refresh()
        return obj

    def get_function_versions(
        self,
        identifier: str,
        **kwargs,
    ) -> list[Function]:
        """
        Get object versions from backend.

        Parameters
        ----------
        identifier : str
            Entity key (store://...) or entity name.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        list[Function]
            List of object instances.

        Examples
        --------
        Using entity key:
        >>> obj = project.get_function_versions("store://my-function-key")

        Using entity name:
        >>> obj = project.get_function_versions("my-function-name")
        """
        return get_function_versions(identifier, project=self.name, **kwargs)

    def list_functions(self, **kwargs) -> list[Function]:
        """
        List all latest version objects from backend.

        Parameters
        ----------
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        list[Function]
            List of object instances.

        Examples
        --------
        >>> objs = project.list_functions()
        """
        return list_functions(self.name, **kwargs)

    def import_function(
        self,
        file: str,
        **kwargs,
    ) -> Function:
        """
        Import object from a YAML file.

        Parameters
        ----------
        file : str
            Path to YAML file.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        Function
            Object instance.

        Examples
        --------
        >>> obj = project.import_function("my-function.yaml")
        """
        return import_function(file, **kwargs)

    def update_function(self, entity: Function) -> Function:
        """
        Update object. Note that object spec are immutable.

        Parameters
        ----------
        entity : Function
            Object to update.

        Returns
        -------
        Function
            Entity updated.

        Examples
        --------
        >>> obj = project.update_function(obj)
        """
        if entity.project != self.name:
            raise ValueError(f"Entity {entity.name} is not in project {self.name}.")
        return update_function(entity)

    def delete_function(
        self,
        identifier: str,
        entity_id: str | None = None,
        delete_all_versions: bool = False,
        cascade: bool = True,
        **kwargs,
    ) -> None:
        """
        Delete object from backend.

        Parameters
        ----------
        identifier : str
            Entity key (store://...) or entity name.
        entity_id : str
            Entity ID.
        delete_all_versions : bool
            Delete all versions of the named entity. If True, use entity name instead of entity key as identifier.
        cascade : bool
            Cascade delete.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        dict
            Response from backend.

        Examples
        --------
        If delete_all_versions is False:
        >>> project.delete_function("store://my-function-key")

        Otherwise:
        >>> project.delete_function("my-function-name",
        >>>                         delete_all_versions=True)
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
        Create a new object.

        Parameters
        ----------
        name : str
            Object name.
        kind : str
            Kind the object.
        uuid : str
            ID of the object (UUID4, e.g. 40f25c4b-d26b-4221-b048-9527aff291e2).
        description : str
            Description of the object (human readable).
        labels : list[str]
            List of labels.
        embedded : bool
            Flag to determine if object spec must be embedded in project spec.
        **kwargs : dict
            Spec keyword arguments.

        Returns
        -------
        Workflow
            Object instance.

        Examples
        --------
        >>> obj = project.new_workflow(name="my-workflow",
        >>>                            kind="kfp",
        >>>                            code_src="pipeline.py",
        >>>                            handler="pipeline-handler")
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
            Entity key (store://...) or entity name.
        entity_id : str
            Entity ID.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        Workflow
            Object instance.

        Examples
        --------
        Using entity key:
        >>> obj = project.get_workflow("store://my-workflow-key")

        Using entity name:
        >>> obj = project.get_workflow("my-workflow-name"
        >>>                            entity_id="my-workflow-id")
        """
        obj = get_workflow(
            identifier=identifier,
            project=self.name,
            entity_id=entity_id,
            **kwargs,
        )
        self.refresh()
        return obj

    def get_workflow_versions(
        self,
        identifier: str,
        **kwargs,
    ) -> list[Workflow]:
        """
        Get object versions from backend.

        Parameters
        ----------
        identifier : str
            Entity key (store://...) or entity name.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        list[Workflow]
            List of object instances.

        Examples
        --------
        Using entity key:
        >>> obj = project.get_workflow_versions("store://my-workflow-key")

        Using entity name:
        >>> obj = project.get_workflow_versions("my-workflow-name")
        """
        return get_workflow_versions(identifier, project=self.name, **kwargs)

    def list_workflows(self, **kwargs) -> list[Workflow]:
        """
        List all latest version objects from backend.

        Parameters
        ----------
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        list[Workflow]
            List of object instances.

        Examples
        --------
        >>> objs = project.list_workflows()
        """
        return list_workflows(self.name, **kwargs)

    def import_workflow(
        self,
        file: str,
        **kwargs,
    ) -> Workflow:
        """
        Import object from a YAML file.

        Parameters
        ----------
        file : str
            Path to YAML file.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        Workflow
            Object instance.

        Examples
        --------
        >>> obj = project.import_workflow("my-workflow.yaml")
        """
        return import_workflow(file, **kwargs)

    def update_workflow(self, entity: Workflow) -> Workflow:
        """
        Update object. Note that object spec are immutable.

        Parameters
        ----------
        entity : Workflow
            Object to update.

        Returns
        -------
        Workflow
            Entity updated.

        Examples
        --------
        >>> obj = project.update_workflow(obj)
        """
        if entity.project != self.name:
            raise ValueError(f"Entity {entity.name} is not in project {self.name}.")
        return update_workflow(entity)

    def delete_workflow(
        self,
        identifier: str,
        entity_id: str | None = None,
        delete_all_versions: bool = False,
        cascade: bool = True,
        **kwargs,
    ) -> None:
        """
        Delete object from backend.

        Parameters
        ----------
        identifier : str
            Entity key (store://...) or entity name.
        entity_id : str
            Entity ID.
        delete_all_versions : bool
            Delete all versions of the named entity. If True, use entity name instead of entity key as identifier.
        cascade : bool
            Cascade delete.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        dict
            Response from backend.

        Examples
        --------
        If delete_all_versions is False:
        >>> project.delete_workflow("store://my-workflow-key")

        Otherwise:
        >>> project.delete_workflow("my-workflow-name",
        >>>                         delete_all_versions=True)
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
        Create a new object.

        Parameters
        ----------
        name : str
            Object name.
        uuid : str
            ID of the object (UUID4, e.g. 40f25c4b-d26b-4221-b048-9527aff291e2).
        description : str
            Description of the object (human readable).
        labels : list[str]
            List of labels.
        embedded : bool
            Flag to determine if object spec must be embedded in project spec.
        secret_value : str
            Value of the secret.
        **kwargs : dict
            Spec keyword arguments.

        Returns
        -------
        Secret
            Object instance.

        Examples
        --------
        >>> obj = project.new_secret(name="my-secret",
        >>>                          secret_value="my-secret-value")
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
            Entity key (store://...) or entity name.
        entity_id : str
            Entity ID.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        Secret
            Object instance.

        Examples
        --------
        Using entity key:
        >>> obj = project.get_secret("store://my-secret-key")

        Using entity name:
        >>> obj = project.get_secret("my-secret-name"
        >>>                          entity_id="my-secret-id")
        """
        obj = get_secret(
            identifier=identifier,
            project=self.name,
            entity_id=entity_id,
            **kwargs,
        )
        self.refresh()
        return obj

    def get_secret_versions(
        self,
        identifier: str,
        **kwargs,
    ) -> list[Secret]:
        """
        Get object versions from backend.

        Parameters
        ----------
        identifier : str
            Entity key (store://...) or entity name.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        list[Secret]
            List of object instances.

        Examples
        --------
        Using entity key:
        >>> obj = project.get_secret_versions("store://my-secret-key")

        Using entity name:
        >>> obj = project.get_secret_versions("my-secret-name")
        """
        return get_secret_versions(identifier, project=self.name, **kwargs)

    def list_secrets(self, **kwargs) -> list[Secret]:
        """
        List all latest version objects from backend.

        Parameters
        ----------
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        list[Secret]
            List of object instances.

        Examples
        --------
        >>> objs = project.list_secrets()
        """
        return list_secrets(self.name, **kwargs)

    def import_secret(
        self,
        file: str,
        **kwargs,
    ) -> Secret:
        """
        Import object from a YAML file.

        Parameters
        ----------
        file : str
            Path to YAML file.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        Secret
            Object instance.

        Examples
        --------
        >>> obj = project.import_secret("my-secret.yaml")
        """
        return import_secret(file, **kwargs)

    def update_secret(self, entity: Secret) -> Secret:
        """
        Update object. Note that object spec are immutable.

        Parameters
        ----------
        entity : Secret
            Object to update.

        Returns
        -------
        Secret
            Entity updated.

        Examples
        --------
        >>> obj = project.update_secret(obj)
        """
        if entity.project != self.name:
            raise ValueError(f"Entity {entity.name} is not in project {self.name}.")
        return update_secret(entity)

    def delete_secret(
        self,
        identifier: str,
        entity_id: str | None = None,
        delete_all_versions: bool = False,
        **kwargs,
    ) -> None:
        """
        Delete object from backend.

        Parameters
        ----------
        identifier : str
            Entity key (store://...) or entity name.
        entity_id : str
            Entity ID.
        delete_all_versions : bool
            Delete all versions of the named entity. If True, use entity name instead of entity key as identifier.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        dict
            Response from backend.

        Examples
        --------
        If delete_all_versions is False:
        >>> project.delete_secret("store://my-secret-key")

        Otherwise:
        >>> project.delete_secret("my-secret-name",
        >>>                       delete_all_versions=True)
        """
        delete_secret(
            identifier=identifier,
            project=self.name,
            entity_id=entity_id,
            delete_all_versions=delete_all_versions,
            **kwargs,
        )
        self.refresh()
