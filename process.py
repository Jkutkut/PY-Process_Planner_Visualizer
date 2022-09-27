class Process:
    UDF = -42

    def __init__(self, name: str, t_arrival = UDF, t_cpu = UDF, priority = UDF):
        self.__name = name
        self.__t_arrival = t_arrival
        self.__t_cpu = t_cpu
        self.__priority = priority

        self.__t_start = self.UDF
        self.__t_end = self.UDF
        self.__history = []

    @classmethod
    def attr_defined(cls, *attrs):
        return all([attr != cls.UDF for attr in attrs])

    # ************ GETTERS ************

    @classmethod
    def give_attr(cls, attr):
        if not cls.attr_defined(attr):
            raise Exception("This field is not defined")
        return attr

    # CANONICAL

    @property
    def name(self):
        return self.give_attr(self.__name)

    @property
    def t_arrival(self):
        return self.give_attr(self.__t_arrival)

    @property
    def t_cpu(self):
        return self.give_attr(self.__t_cpu)

    @property
    def t_queue(self):
        if not self.attr_defined(self.t_arrival, self.t_end):
            return self.give_attr(self.UDF)
        return self.give_attr(self.t_end - self.t_arrival)

    @property
    def t_queue_normalized(self):
        return self.t_queue / self.t_cpu

    @property
    def t_wait(self):
        return self.UDF
        # TODO
        # Time start last interval - time arrival -
        # time spent previously executing this process

    # CLASS GETTERS

    @classmethod
    def avg_t_queue(cls, processes: list):
        s = sum([p.t_queue for p in processes])
        return s / len(processes)

    @classmethod
    def avg_t_wait(cls, processes):
        s = sum([p.t_wait for p in processes])
        return s / len(processes)

    # NON CANONICAL

    @property
    def t_start(self): # TODO refactor with history system
        return self.give_attr(self.__t_start)

    @property
    def t_end(self): # TODO refactor with history system
        return self.give_attr(self.__t_end)
