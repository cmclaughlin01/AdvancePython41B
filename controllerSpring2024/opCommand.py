class Command:
    def __init__(self, op, argv=None):
        self.op = op
        self.argv = argv

    def _set(self, cmd):
        self.op = cmd.get("op")
        self.argv = cmd.get("argv")

    def _get(self):
        return {"op": self.op, "argv": self.argv}

    def __str__(self):
        return f"Command(op={self.op}, argv={self.argv})"
