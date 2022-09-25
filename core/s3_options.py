import uuid


def profile_image_path(instance, filename):
    filename = uuid.uuid4().hex
    return f"images/profile/{filename}"


def content_image_path(instance, filename):
    filename = uuid.uuid4().hex
    return f"images/content/{filename}"
