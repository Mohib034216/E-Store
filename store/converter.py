import uuid

class UUIDConverter:
    regex = '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
    # regex = '[0-9a-f]{32}'

    def to_python(self, value):
        return uuid.UUID(value)

    def to_url(self, value):
        return str(value)