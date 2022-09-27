class Process:
    UDF = -1

    def __init__(self, name: str, t_arrival = UDF):
        self.__name = name
        self.__t_arrival = t_arrival

    @classmethod
    def attr_defined(self, attr):
        return attr == -1

    # ************ GETTERS ************

    @property
    def name(self):
        return self.__name

    @property
    def t_arrival(self):
        return self.__t_arrival

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
