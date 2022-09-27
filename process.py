class Process:
    UDF = -42

    def __init__(self, name: str, t_arrival: int = UDF, t_cpu: int = UDF, priority: int = UDF):
        self.__name = name
        self.__t_arrival = t_arrival
        self.__t_cpu = t_cpu
        self.__priority = priority

        self.__history = []
        self.__t_elapsed = 0

    def run_for(self, current_time: int, t: int) -> int:
        if self.ended:
            raise Exception('Process already ended')
        if self.t_remaining < t:
            return self.run_for(current_time, self.t_remaining)
        self.__t_elapsed += t
        self.add2history(current_time, t)
        return t

    def add2history(self, current_time: int, t: int):
        self.__history.append({
            "start": current_time,
            "t": t,
            "end": current_time + t,
        })

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
    def priority(self):
        return self.give_attr(self.__priority)

    @property
    def t_arrival(self):
        return self.give_attr(self.__t_arrival)

    @property
    def t_cpu(self):
        return self.give_attr(self.__t_cpu)

    @property
    def t_queue(self):
        return self.give_attr(self.t_end - self.t_arrival)

    @property
    def t_queue_normalized(self):
        return self.give_attr(self.t_queue / self.t_cpu)

    @property
    def t_wait(self):
        time_executed = sum([h["t"] for h in self.history])
        return self.t_start - self.t_arrival - time_executed
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
    def history(self):
        return self.__history

    @property
    def t_start(self):
        time = self.UDF if not self.ended else self.history[0]["start"]
        return self.give_attr(time)

    @property
    def t_end(self):
        time = self.UDF if not self.ended else self.history[-1]["end"]
        return self.give_attr(time)

    @property
    def ended(self) -> bool:
        return self.t_elapsed == self.t_cpu

    @property
    def t_elapsed(self) -> int:
        return self.__t_elapsed

    @property
    def t_remaining(self):
        return self.t_cpu - self.t_elapsed
