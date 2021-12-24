class yo():
    def __init__(self):
        self.x = 67

    def __getattr__(self, name):
        return name
