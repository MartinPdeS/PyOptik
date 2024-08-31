
class Material:
    def __str__(self) -> str:
        """
        Provides an informal string representation of the Material object.

        Returns:
            str: Informal representation of the Material object.
        """
        return f"Material: {self.filename}"

    def __repr__(self) -> str:
        """
        Provides a formal string representation of the Material object, including key attributes.

        Returns:
            str: Formal representation of the Material object.
        """
        return self.__str__()