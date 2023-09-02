class OrderedRows(list):
    """
    Maintains original header/field ordering.
    """

    def __init__(self, header: list[str] | None = None):
        self.header = [c.strip() for c in header] if (header is not None) else None
