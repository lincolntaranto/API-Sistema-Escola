class StudentNotFound(Exception):
    """Levantada quando um aluno não existe ou foi deletado."""

    pass


class StudentAlreadyExists(Exception):
    """Levantada quando se tenta cadastrar um aluno já cadastrado."""

    pass
