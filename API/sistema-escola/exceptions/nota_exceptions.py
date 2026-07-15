class GradeNotFound(Exception):
    """Levantada quando uma nota não é encontrada."""

    pass


class GradeAlreadyExists(Exception):
    """Levantada quando se tenta cadastrar uma nota já cadastrada."""
