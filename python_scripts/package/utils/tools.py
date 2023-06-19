import uuid


def generate_branch_name() -> str:
    """
    Generate a unique hash
    """
    return uuid.uuid4().hex
