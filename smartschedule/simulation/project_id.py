import uuid
from typing import NewType

ProjectId = NewType("ProjectId", uuid.UUID)


def project_id() -> ProjectId:
    return ProjectId(uuid.uuid4())
