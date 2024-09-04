from __future__ import annotations

import typing

from digitalhub_core.entities._base.crud import files_info_get_api, files_info_put_api
from digitalhub_core.entities._base.entity.versioned import VersionedEntity
from digitalhub_core.stores.builder import get_store

if typing.TYPE_CHECKING:
    from digitalhub_core.entities._base.metadata import Metadata
    from digitalhub_core.entities._base.spec.material import MaterialSpec
    from digitalhub_core.entities._base.status.material import MaterialStatus


class MaterialEntity(VersionedEntity):
    """
    A class representing an entity that can be materialized
    as file(s).
    """

    def __init__(
        self,
        project: str,
        name: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: MaterialSpec,
        status: MaterialStatus,
        user: str | None = None,
    ) -> None:
        super().__init__(project, name, uuid, kind, metadata, spec, status, user)
        self.spec: MaterialSpec
        self.status: MaterialStatus

    def save(self, update: bool = False) -> MaterialEntity:
        """
        Save entity into backend.

        Parameters
        ----------
        update : bool
            Flag to indicate update.

        Returns
        -------
        MaterialEntity
            Entity saved.
        """
        obj = self.to_dict()

        files = None
        if self.status.files is not None and len(self.status.files) > 5 and not self._context().local:
            files = obj["status"].pop("files")

        if not update:
            new_obj: MaterialEntity = self._save(obj)
        else:
            new_obj: MaterialEntity = self._update(obj)

        # Handle files info
        if files is not None:
            files_info_put_api(self.project, self.ENTITY_TYPE, self.id, files)
            self.status.add_files_info(files)

        return new_obj

    ##############################
    # I/O Methods
    ##############################

    def as_file(self) -> list[str]:
        """
        Get object as file(s). It downloads the object from storage in
        a temporary folder and returns the list of downloaded files paths.

        Returns
        -------
        list[str]
            List of file paths.
        """
        store = get_store(self.spec.path)
        paths = self._get_paths()
        return store.download(paths)

    def download(
        self,
        destination: str | None = None,
        overwrite: bool = False,
    ) -> list[str]:
        """
        Download file(s) from specified storage.
        This function looks into object's status files attribute. If it finds
        a list of files descriptors, it will download them according to the
        specified path. In case the object does not have files info in status,
        it will fallback on spec path.
        If destination is provided, it will download to that path, otherwise,
        it will download into the root project path, inside a directory named
        after the entity type.

        Parameters
        ----------
        destination : str
            Destination path as filename or directory.
        overwrite : bool
            Specify if overwrite existing file(s). If file(s) already
            exist and overwrite is False, it will raise an error.

        Returns
        -------
        list[str]
            List of downloaded file paths.

        Examples
        --------
        Download a single file:

        >>> entity.status.files[0]
        {
            "path ": "s3://bucket/data.csv",
            "name ": "data.csv",
            "content_type ": "text/csv;charset=utf-8 "
        }
        >>> paths = entity.download()
        >>> print(paths[0])
        dataitem/data.csv
        """
        store = get_store(self.spec.path)
        paths = self._get_paths()

        if destination is None:
            destination = str(self._context().root / self.ENTITY_TYPE)

        return store.download(paths, dst=destination, overwrite=overwrite)

    def upload(self, source: str) -> None:
        """
        Upload object from given local path to spec path destination.
        Source must be a local path. If the path is a folder, destination
        path (object's spec path) must be a folder or a partition ending
        with '/' (s3).

        Parameters
        ----------
        source : str
            Source path is the local path of the object.

        Returns
        -------
        None

        Examples
        --------
        Upload a single file:

        >>> entity.spec.path = 's3://bucket/data.csv'
        >>> entity.upload('./data.csv')

        Upload a folder:
        >>> entity.spec.path = 's3://bucket/data/'
        >>> entity.upload('./data')
        """
        # Get store and upload object
        store = get_store(self.spec.path)
        paths = store.upload(source, self.spec.path)

        # Update files info
        files_info = store.get_file_info(paths)
        self._update_files_info(files_info)

    ##############################
    #  Private Helpers
    ##############################

    def _get_paths(self) -> list[tuple[str, str | None]]:
        """
        Get paths from spec.

        Returns
        -------
        list[tuple[str, str | None]]
            List of paths.
        """
        # Try to download from files info in status
        paths = self.status.get_file_paths()

        # Fallback to spec path
        if not paths:
            paths = [(self.spec.path, None)]

        return paths

    def _update_files_info(self, files_info: list[dict] | None = None) -> None:
        """
        Update files info.

        Parameters
        ----------
        files_info : list[dict] | None
            Files info.

        Returns
        -------
        None
        """
        if files_info is None:
            return
        self.refresh()
        self.status.add_files_info(files_info)
        self.save(update=True)

    def _get_files_info(self) -> None:
        """
        Get files info from backend.

        Returns
        -------
        None
        """
        if not self._context().local and (not self.status.files or self.status.files is None):
            files = files_info_get_api(
                project=self.project,
                entity_type=self.ENTITY_TYPE,
                entity_id=self.id,
            )
            self.status.add_files_info(files)
