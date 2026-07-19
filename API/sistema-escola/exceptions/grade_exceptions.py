class GradeNotFound(Exception):
    """Levantada quando uma grade não é encontrada."""

    pass


class GradeAlreadyExists(Exception):
    """Levantada quando se tenta cadastrar uma grade já cadastrada."""
