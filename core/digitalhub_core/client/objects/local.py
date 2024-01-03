"""
Local Client module.
"""
from copy import deepcopy

from digitalhub_core.client.objects.base import Client
from digitalhub_core.utils.commons import ARTF, DTIT, FUNC, PROJ, RUNS, TASK, WKFL
from digitalhub_core.utils.exceptions import BackendError


class ClientLocal(Client):
    """
    The local client. Use the builder to get an instance.
    It is used to keep objects in memory.
    """

    def __init__(self) -> None:
        super().__init__()
        self._db: dict[str, dict[str, dict]] = {
            # unversioned
            PROJ: {},
            TASK: {},
            RUNS: {},
            # versioned
            ARTF: {},
            DTIT: {},
            FUNC: {},
            WKFL: {},
        }

    ########################
    # CRUD
    ########################

    def create_object(self, obj: dict, api: str) -> dict:
        """
        Create an object.

        Parameters
        ----------
        obj : dict
            The object to create.
        api : str
            The api to create the object with.

        Returns
        -------
        dict
            The created object.
        """
        project, dto, name, uuid, code = self._parse_api(api)
        try:
            if project is None:
                name = obj["name"] if dto == PROJ else obj["id"]
                if name in self._db[dto]:
                    code = 5
                    raise ValueError
                self._db[dto][name] = obj
            else:
                name = obj["name"]
                uuid = obj["id"]
                self._db[dto].setdefault(name, {})
                self._db[dto][name][uuid] = obj
                self._db[dto][name]["latest"] = obj  # For versioned objects set also latest version
            return obj
        except (KeyError, TypeError):
            msg = self._format_msg(code)
            raise BackendError(msg)
        except ValueError:
            msg = self._format_msg(code, dto=dto, name=name)
            raise BackendError(msg)

    def read_object(self, api: str) -> dict:
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
        project, dto, name, uuid, code = self._parse_api(api)
        try:
            if project is None:
                obj = self._db[dto][name]
                if dto == PROJ:
                    obj = self._get_project_spec(obj, name)
            else:
                obj = self._db[dto][name][uuid]
            return obj
        except KeyError:
            msg = self._format_msg(code, project, dto, name, uuid)
            raise BackendError(msg)

    def update_object(self, obj: dict, api: str) -> dict:
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
        project, dto, name, uuid, code = self._parse_api(api)
        try:
            if project is None:
                self._db[dto][name] = obj
            else:
                self._db[dto][name][uuid] = obj
        except KeyError:
            msg = self._format_msg(code, project, dto, name, uuid)
            raise BackendError(msg)

        return obj

    def delete_object(self, api: str) -> dict:
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
        # We do not handle cascade in local client
        project, dto, name, uuid, code = self._parse_api(api)
        try:
            if uuid is None:
                obj = self._db[dto].pop(name)
            else:
                obj = self._db[dto][name].pop(uuid)
        except KeyError:
            msg = self._format_msg(code, project, dto, name, uuid)
            raise BackendError(msg)
        return {"deleted": obj}

    ########################
    # Logic for CRUD
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
            The parsed API.
        """
        # Remove prefix from API
        api = api.removeprefix("/api/v1/")

        # Set context flag by default to False
        ctx = False

        # Remove context prefix from API and set context flag to True
        if api.startswith("-/"):
            ctx = True
            api = api[2:]

        # Remove delete flag from API. Local client does not handle cascade
        if api.endswith("?cascade=true") or api.endswith("?cascade=false"):
            api = api.removesuffix("?cascade=true").removesuffix("?cascade=false")

        # Return parsed elements
        return self._parse_api_elements(api, ctx)

    @staticmethod
    def _parse_api_elements(api: str, ctx: bool) -> tuple:
        """
        Parse the elements from the given API.
        Elements returned are: project-name, dto, name, uuid, error_code.

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
        if len(parsed) == 1:
            return None, parsed[0], None, None, 1

        # GET/DELETE/UPDATE /api/v1/<dto>/<name>
        if len(parsed) == 2 and not ctx:
            return None, parsed[0], parsed[1], None, 2

        # Context API for versioned objects

        # POST /api/v1/-/<project>/<dto>
        if len(parsed) == 2 and ctx:
            return parsed[0], parsed[1], None, None, 1

        # GET/DELETE/UPDATE /api/v1/-/<project>/<dto>/<name>
        if len(parsed) == 3:
            return parsed[0], parsed[1], parsed[2], None, 3

        # GET/DELETE/UPDATE /api/v1/-/<project>/<dto>/<name>/<uuid>
        if len(parsed) == 4:
            return parsed[0], parsed[1], parsed[2], parsed[3], 4

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

        for entity_type in [ARTF, DTIT, FUNC, WKFL]:
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

    def _format_msg(
        self,
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
        if code == 1:
            return "Object to create is not valid"
        if code == 2:
            return "Object '{}' named '{}' not found".format(dto, name)
        if code == 3:
            return "Object '{}' named '{}' for project '{}' not found".format(dto, name, project)
        if code == 4:
            return "Object '{}' named '{}:{}' for project '{}' not found".format(dto, name, uuid, project)
        if code == 5:
            return "Object '{}' named '{}' already exists".format(dto, name)

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
