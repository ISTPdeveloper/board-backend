import uuid


def image_path(instance, filename):
    filename = uuid.uuid4().hex
    return f"images/{instance}/{filename}"
