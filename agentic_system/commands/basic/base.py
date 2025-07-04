class BaseCommand:
    def parse(self, *args, **kwargs):
        raise NotImplementedError("Subclasses should implement the parse method!")

    def execute(self, *args, **kwargs):
        raise NotImplementedError("Subclasses should implement the execute method!") 