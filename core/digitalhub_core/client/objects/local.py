"""
Local Client module.
"""
from digitalhub_core.client.objects.base import Client
from digitalhub_core.utils.commons import ARTF, DTIT, FUNC, MDLS, PROJ, RUNS, TASK, WKFL
from digitalhub_core.utils.exceptions import BackendError


class ClientLocal(Client):
    """
    The local client. Use the builder to get an instance.
    It is used to keep objects in memory.
    """

    def __init__(self) -> None:
        super().__init__()
        self._db = {
            PROJ: {},
            FUNC: {},
            WKFL: {},
            RUNS: {},
            TASK: {},
            ARTF: {},
            DTIT: {},
            MDLS: {},
        }

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
        parsed = self._parse_api(api)

        # Project, Task, Run
        if len(parsed) == 1:
            (dto,) = parsed
            name = obj.get("metadata", {}).get("name")
            self._db[dto][name] = obj

        # Artifact, Dataitem, Model, Function, Workflow
        if len(parsed) == 2:
            project, dto = parsed
            name = obj.get("metadata", {}).get("name")
            uuid = obj.get("metadata", {}).get("version")
            self._db[dto].setdefault(project, {}).setdefault(name, {})
            self._db[dto][project][name][uuid] = obj
            self._db[dto][project][name]["latest"] = obj

        return obj

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
        parsed = self._parse_api(api)

        # Project, Task, Run
        if len(parsed) == 2:
            dto, name = parsed
            obj = self._db.get(dto, {}).get(name)
            if dto == PROJ:
                obj = self._get_project_spec(obj, name)
            msg = f"Object '{dto}' named '{name}' not found"

        # Artifact, Dataitem, Model, Function, Workflow
        elif len(parsed) == 4:
            project, dto, name, uuid = parsed
            obj = self._db.get(dto, {}).get(project, {}).get(name, {}).get(uuid)
            msg = f"Object '{dto}' named '{name}:{uuid}' for project '{project}' not found"

        if obj is None or not isinstance(obj, dict):
            raise BackendError(msg)

        return obj

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
        parsed = self._parse_api(api)
        msg = None

        try:
            # Project, Task, Run
            if len(parsed) == 2:
                dto, name = parsed
                self._db[dto][name] = obj
                msg = f"Object '{dto}' named '{name}' not found"

            # Artifact, Dataitem, Model, Function, Workflow
            elif len(parsed) == 4:
                project, dto, name, uuid = parsed
                self._db[dto][project][name][uuid] = obj
                msg = f"Object '{dto}' named '{name}:{uuid}' for project '{project}' not found"

        except KeyError:
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
        parsed = self._parse_api(api)
        fallback = "No element found"

        # Project, Task, Run
        if len(parsed) == 2:
            dto, name = parsed
            deleted = self._db[dto].pop(name, fallback)

        # Artifact, Dataitem, Model, Function, Workflow
        # No uuid
        elif len(parsed) == 3:
            project, dto, name = parsed
            deleted = self._db[dto][project].pop(name, fallback)

        # uuid
        elif len(parsed) == 4:
            project, dto, name, uuid = parsed
            deleted = self._db[dto][project][name].pop(uuid, fallback)

        return {"deleted": deleted}

    @staticmethod
    def _parse_api(api: str) -> list[str]:
        """
        Parse the api to get information about the object.

        Parameters
        ----------
        api : str
            The api to parse.

        Returns
        -------
        list[str]
            The parsed api.
        """
        api = api.removeprefix("/api/v1/")
        splitted = api.split("/")
        if splitted[0] == "-":
            return splitted[1:]
        return splitted

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
        if obj is None or not isinstance(obj, dict):
            raise BackendError(f"Project not found: {name}")
        for i in [FUNC, WKFL, ARTF, DTIT]:
            objs = self._db.get(i, {}).get(name, {})
            obj["spec"][i] = []
            for _, j in objs.items():
                for k, v in j.items():
                    if k != "latest":
                        obj["spec"][i].append(v)
        return obj

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
