class Process:
    # TODO
    def __init__(self, name: str):
        self.__name = name

    @property
    def name(self):
        return self.__name

    @property
    def t_arrival(self):
        return None # TODO

    @property
    def t_cpu(self):
        return None # TODO

    @property
    def t_queue(self):
        return None # TODO

    @property
    def t_queue_normalized(self):
        return None # TODO

    @property
    def t_e(self): # TODO find out the meaning
        return None # TODO

    @classmethod
    def avg_t_queue(cls, processes: list):
        return None # TODO

    @classmethod
    def avg_t_e(cls): # TODO find out the meaning
        return None # TODO
