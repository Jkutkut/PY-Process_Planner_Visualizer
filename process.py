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
        return current_time + t

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
        if not self.ended:
            return self.give_attr(self.UDF)
        time_executed = sum([h["t"] for h in self.history[:-1]])
        return self.history[-1]["start"] - self.t_arrival - time_executed
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

if __name__ == '__main__':
    # p1 = Process("p1", 0, 8)
    # p2 = Process("p2", 1, 4)
    # p3 = Process("p3", 2, 9)
    # p4 = Process("p4", 3, 5)
    # p5 = Process("p5", 12, 2)
    p1 = Process("p1", t_arrival=0, t_cpu=8)
    p2 = Process("p2", t_arrival=1, t_cpu=4)
    p3 = Process("p3", t_arrival=2, t_cpu=9)
    p4 = Process("p4", t_arrival=3, t_cpu=5)
    p5 = Process("p5", t_arrival=12, t_cpu=2)

    ps = [p1, p2, p3, p4, p5]

    t = 0
    t = p1.run_for(t, 1)
    t = p2.run_for(t, 4)
    t = p4.run_for(t, 5)
    t = p1.run_for(t, 2)
    t = p5.run_for(t, 2)
    t = p1.run_for(t, 5)
    t = p3.run_for(t, 9)

    print(f'Elapsed time: {t}')
    print("Histories:")
    hist_p = lambda p: [f"{h['start']}-{h['t']}->{h['end']}" for h in p.history]
    for p in ps:
        print(f'{p.name}: {hist_p(p)}')

    print("\nEnded processes:")
    print(*[p.ended for p in ps], sep=" ", end="")
    print(" => All ended:", all([p.ended for p in ps]))

    print("\nT queue:")
    for p in ps:
        print(f'{p.name}: {p.t_queue}')

    print("\nT queue normalized:")
    for p in ps:
        print(f'{p.name}: {p.t_queue_normalized}')
    
    print("\nT wait:")
    for p in ps:
        print(f'{p.name}: {p.t_wait}')