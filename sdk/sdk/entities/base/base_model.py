"""
Model object module.
"""


class ModelObj:
    """
    Base class for all entities.
    """

    def to_dict(self) -> dict:
        """
        Return object as dict with all non private keys.

        Returns
        -------
        dict
            A dictionary containing the attributes of the entity instance.

        """
        obj = {}
        for k in self.__dict__:
            if k.startswith("_"):
                continue
            val = getattr(self, k, None)
            if val is not None:
                if hasattr(val, "to_dict"):
                    val = val.to_dict()
                    if val:
                        obj[k] = val
                else:
                    obj[k] = val
        return obj

    def __repr__(self) -> str:
        """
        Return string representation of the entity object.

        Returns
        -------
        str
            A string representing the entity instance.

        """
        return str(self.to_dict())
