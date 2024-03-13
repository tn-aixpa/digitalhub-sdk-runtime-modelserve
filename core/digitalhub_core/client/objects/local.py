"""
Local Client module.
"""
from __future__ import annotations

import datetime
from copy import deepcopy

from digitalhub_core.client.objects.base import Client
from digitalhub_core.utils.exceptions import BackendError


class ClientLocal(Client):
    """
    Local client.

    The Local client can be used when a remote Digitalhub backend is not available.
    It handles the creation, reading, updating and deleting of objects in memory,
    storing them in a local dictionary.
    The functionality of the Local client is almost the same as the DHCore client.
    Main differences are:
        - Local client does delete objects on cascade.
        - The run execution are forced to be local.
    """

    def __init__(self) -> None:
        """
        Constructor.
        """
        super().__init__()
        self._db: dict[str, dict[str, dict]] = {}

    ########################
    # CRUD
    ########################

    def create_object(self, api: str, obj: dict, **kwargs) -> dict:
        """
        Create an object.

        Parameters
        ----------
        api : str
            The api to create the object with.
        obj : dict
            The object to create.

        Returns
        -------
        dict
            The created object.
        """
        project, dto, uuid, ctx = self._parse_api(api)
        try:
            # Check if dto is valid
            if dto is None:
                raise TypeError

            # Check if dto exists, if not, create a mapping
            self._db.setdefault(dto, {})

            # Base API
            #
            # POST /api/v1/projects
            #
            # Project are not versioned, everything is stored on "uuid" key
            if not ctx:
                uuid = obj["name"]
                if uuid in self._db[dto]:
                    code = 5
                    raise ValueError
                self._db[dto][uuid] = obj

            # Context API
            #
            # POST /api/v1/-/<project-name>/artifacts
            # POST /api/v1/-/<project-name>/functions
            # POST /api/v1/-/<project-name>/workflows
            #
            # Runs and tasks are not versioned, so we keep name as uuid.
            # We have both "name" and "id" attributes for versioned objects so we use them as storage keys.
            # The "latest" key is used to store the latest version of the object.
            else:
                uuid = obj["id"]
                name = obj.get("name", uuid)
                self._db[dto].setdefault(name, {})
                self._db[dto][name][uuid] = obj
                self._db[dto][name]["latest"] = obj

            # Return the created object
            return obj

        # Key error are possibly raised by accessing invalid objects
        except (KeyError, TypeError):
            msg = self._format_msg(1, dto=dto)
            raise BackendError(msg)

        # If try to create already existing object
        except ValueError:
            msg = self._format_msg(1, dto=dto, name=name)
            raise BackendError(msg)

    def read_object(self, api: str, **kwargs) -> dict:
        """
        Get an object.

        Parameters
        ----------
        api : str
            The api to get the object with.

        Returns
        -------
        dict or None
            The object, or None if it doesn't exist.
        """
        project, dto, uuid, ctx = self._parse_api(api)
        try:
            # Base API
            #
            # GET /api/v1/projects/<uuid>
            #
            # self._parse_api() should return only dto

            if not ctx:
                obj = self._db[dto][uuid]

                # If the object is a project, we need to add the project spec,
                # for example artifacts, functions, workflows, etc.
                # Technically we have only projects that access base apis,
                # we check dto just in case we add something else.
                if dto == "projects":
                    obj = self._get_project_spec(obj, uuid)

            # Context API
            #
            # GET /api/v1/-/<project-name>/runs/<uuid>
            # GET /api/v1/-/<project-name>/artifacts/<uuid>
            # GET /api/v1/-/<project-name>/functions/<uuid>
            #
            # self._parse_api() should return dto and uuid/version

            else:
                for _, v in self._db[dto].items():
                    obj = v[uuid]
                    break

            return obj

        except KeyError:
            msg = self._format_msg(1, project, dto, uuid)
            raise BackendError(msg)

    def update_object(self, api: str, obj: dict, **kwargs) -> dict:
        """
        Update an object.

        Parameters
        ----------
        obj : dict
            The object to update.
        api : str
            The api to update the object with.

        Returns
        -------
        dict
            The updated object.
        """
        project, dto, uuid, ctx = self._parse_api(api)
        try:
            # API example
            #
            # PUT /api/v1/projects/<uuid>

            if not ctx:
                self._db[dto][uuid] = obj

            # Context API
            #
            # PUT /api/v1/-/<project-name>/runs/<uuid>
            # PUT /api/v1/-/<project-name>/artifacts/<uuid>

            else:
                name = obj.get("name", uuid)
                self._db[dto][name][uuid] = obj

        except KeyError:
            msg = self._format_msg(1, project, dto, uuid)
            raise BackendError(msg)

        return obj

    def delete_object(self, api: str, **kwargs) -> dict:
        """
        Delete an object.

        Parameters
        ----------
        api : str
            The api to delete the object with.

        Returns
        -------
        dict
            A generic dictionary.
        """
        project, dto, uuid, ctx = self._parse_api(api)
        try:
            # Base API
            #
            # DELETE /api/v1/projects/<uuid>

            if not ctx:
                obj = self._db[dto].pop(uuid)

            # Context API
            #
            # DELETE /api/v1/-/<project-name>/artifacts/<uuid>
            #
            # We do not handle cascade in local client and
            # in the sdk we selectively delete objects by id,
            # not by name nor dto.

            else:
                reset_latest = False
                name = None
                for _, v in self._db[dto].items():
                    obj = v.pop(uuid)
                    # Handle latest
                    if v["latest"]["id"] == uuid:
                        name = v["latest"].get("name", uuid)
                        v.pop("latest")
                        reset_latest = True
                    break

                if name is not None:
                    # Pop name if empty
                    if not self._db[dto][name]:
                        self._db[dto].pop(name)

                    # Handle latest
                    elif reset_latest:
                        latest_uuid = None
                        latest_date = None
                        for k, v in self._db[dto][name].items():
                            # Accept only ISO format
                            fallback = datetime.datetime.utcfromtimestamp(0).astimezone()
                            try:
                                current_created = datetime.datetime.fromisoformat(v.get("metadata", {}).get("created"))
                            except ValueError:
                                current_created = fallback

                            if latest_date is None or current_created > latest_date:
                                latest_uuid = k
                                latest_date = current_created
                        if latest_uuid is not None:
                            self._db[dto][name]["latest"] = self._db[dto][name][latest_uuid]

        except KeyError:
            msg = self._format_msg(1, project, dto, uuid)
            raise BackendError(msg)
        return {"deleted": obj}

    def list_objects(self, api: str, **kwargs) -> list:
        """
        List objects.

        Parameters
        ----------
        api : str
            The api to list the objects with.

        Returns
        -------
        list | None
            The list of objects.
        """
        _, dto, _, _ = self._parse_api(api)
        name = kwargs.get("params", {}).get("name")
        if name is not None:
            return [self._db[dto][name]["latest"]]
        return [v["latest"] for _, v in self._db[dto].items()]

    ########################
    # Helpers
    ########################

    def _parse_api(self, api: str) -> list[str]:
        """
        Parse the given API.

        Parameters
        ----------
        api : str
            The API to parse.

        Returns
        -------
        list[str]
            The parsed API elements.
        """
        # Remove prefix from API
        api = api.removeprefix("/api/v1/")

        # Set context flag by default to False
        ctx = False

        # Remove context prefix from API and set context flag to True
        if api.startswith("-/"):
            ctx = True
            api = api[2:]

        # Return parsed elements
        return self._parse_api_elements(api, ctx)

    @staticmethod
    def _parse_api_elements(api: str, ctx: bool) -> tuple:
        """
        Parse the elements from the given API.
        Elements returned are: project-name, dto, uuid, context_api.

        Parameters
        ----------
        api : str
            The parsed API.
        ctx : bool
            True if the API is a context API.

        Returns
        -------
        tuple
            The parsed elements from the API.
        """
        # Split API path
        parsed = api.split("/")

        # Base API for versioned objects

        # POST /api/v1/<dto>
        # Returns None, dto, None, False
        if len(parsed) == 1:
            return None, parsed[0], None, ctx

        # GET/DELETE/UPDATE /api/v1/<dto>/<uuid>
        # Return None, dto, name, False
        if len(parsed) == 2 and not ctx:
            return None, parsed[0], parsed[1], ctx

        # Context API for versioned objects

        # POST /api/v1/-/<project>/<dto>
        # Returns project-name, dto, None, True
        if len(parsed) == 2 and ctx:
            return parsed[0], parsed[1], None, ctx

        # GET/DELETE/UPDATE /api/v1/-/<project>/<dto>/<uuid>
        # Return project-name, dto, uuid, True
        if len(parsed) == 3:
            return parsed[0], parsed[1], parsed[2], ctx

    def _get_project_spec(self, obj: dict, name: str) -> dict:
        """
        Read the project spec.

        Parameters
        ----------
        obj : dict
            The project object.
        name : str
            The project name.

        Returns
        -------
        dict
            The project object with the spec.
        """
        # Deepcopy to avoid modifying the original object
        project = deepcopy(obj)
        spec = project.get("spec", {})

        # Get all entities associated with the project specs
        projects_entities = [k for k, _ in self._db.items() if k not in ["projects", "runs", "tasks"]]

        for entity_type in projects_entities:
            # Get all objects of the entity type for the project
            objs = self._db[entity_type]

            # Set empty list
            spec[entity_type] = []

            # Cycle through named objects
            for _, named_entities in objs.items():
                # Get latest version
                for version, entity in named_entities.items():
                    if version != "latest":
                        continue

                    # Deepcopy to avoid modifying the original object
                    copied = deepcopy(entity)

                    # Remove spec if not embedded
                    if not copied.get("metadata", {}).get("embedded", True):
                        copied.pop("spec", None)

                    # Add to project spec
                    if copied["project"] == name:
                        spec[entity_type].append(copied)

        return project

    ########################
    # Utils
    ########################

    @staticmethod
    def _format_msg(
        code: int,
        project: str = None,
        dto: str = None,
        name: str = None,
        uuid: str = None,
    ) -> str:
        """
        Format a message.

        Parameters
        ----------
        code : int
            The code to format the message with.
        project : str
            The project name.
        dto : str
            The DTO name.
        name : str
            The object name.
        uuid : str
            The object uuid.

        Returns
        -------
        str
            The formatted message.
        """
        msg = {
            1: f"Object '{dto}' to create is not valid",
            2: f"Object '{dto}' named '{name}' not found",
            3: f"Object '{dto}' named '{name}' for project '{project}' not found",
            4: f"Object '{dto}' named '{name}:{uuid}' for project '{project}' not found",
            5: f"Object '{dto}' named '{name}' already exists",
        }
        return msg[code]

    ########################
    # Interface methods
    ########################

    @staticmethod
    def is_local() -> bool:
        """
        Declare if Client is local.

        Returns
        -------
        bool
            True
        """
        return True
