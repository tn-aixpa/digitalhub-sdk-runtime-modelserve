"""
Local Client module.
"""
from sdk.client.objects.base import Client
from sdk.utils.commons import ARTF, DTIT, FUNC, PROJ, WKFL, RUNS, TASK


class ClientLocal(Client):
    """
    The local client. Use the builder to get an instance.
    It is used to keep objects in memory.
    """

    def __init__(self) -> None:
        super().__init__()
        self._db = {}
        self.setup()

    def setup(self) -> None:
        """
        Setup the in-memory database.

        Returns
        -------
        None
        """
        for i in [PROJ, ARTF, DTIT, FUNC, WKFL, RUNS, TASK]:
            self._db[i] = {}

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
        # Artifact, DataItem, Function, Workflow
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
        # Artifact, DataItem, Function, Workflow
        elif len(parsed) == 4:
            project, dto, name, uuid = parsed
            obj = self._db.get(dto, {}).get(project, {}).get(name, {}).get(uuid)
        if obj is None or not isinstance(obj, dict):
            raise ValueError(f"Object not found: {api}")
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
        try:
            if len(parsed) == 2:
                dto, name = parsed
                self._db[dto][name] = obj
            elif len(parsed) == 4:
                project, dto, name, uuid = parsed
                self._db[dto][project][name][uuid] = obj
                self._db[dto][project][name]["latest"] = obj
        except KeyError:
            raise ValueError(f"Object not found: {api}")
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
        if len(parsed) == 2:
            dto, name = parsed
            self._db[dto].pop(name, None)
        elif len(parsed) == 4:
            project, dto, name, uuid = parsed
            self._db[dto][project][name].pop(uuid, None)
            if not self._db[dto][project][name]:
                self._db[dto][project].pop(name, None)
            if not self._db[dto][project]:
                self._db[dto].pop(project, None)
        return {}

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
