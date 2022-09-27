class Process:
    UDF = -42

    def __init__(self, name: str, t_arrival = UDF, t_cpu = UDF, priority = UDF):
        self.__name = name
        self.__t_arrival = t_arrival
        self.__t_cpu = t_cpu
        self.__priority = priority

        self.__t_end = self.UDF

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
        if not self.attr_defined(self.t_arrival, self.t_end)
            return self.give_attr(self.UDF)
        return self.give_attr(self.t_end - t_arrival)

    @property
    def t_queue_normalized(self):
        return self.t_queue / self.t_cpu

    @property
    def t_wait(self):
        return self.UDF # TODO

    # CLASS GETTERS

    @classmethod
    def avg_t_queue(cls, processes: list):
        return self.UDF # TODO

    @classmethod
    def avg_t_wait(cls):
        return self.UDF # TODO

    # NON CANONICAL

    @property
    def t_end(self):
        return self.give_attr(self.__t_end)
