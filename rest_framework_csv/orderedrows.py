class OrderedRows(list):
    """
    Maintains original header/field ordering.
    """
    def __init__(self, header):
        self.header = header
