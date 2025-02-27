class GraphIdentifier:
    _instance = None  # Stores the single instance
    _count = 0

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        cls._count += 1
        return cls._instance

    def __init__(self):
        self.id = self._count