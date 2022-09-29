class Process:
    UDF = -42

    def __init__(self, name: str, t_arrival: int = UDF, t_cpu: int = UDF, priority: int = UDF):
        self.__name = name
        self.__t_arrival = t_arrival
        self.__t_cpu = t_cpu
        self.__priority = priority

        self.__history = []
        self.__t_elapsed = 0
        self.protected = True

    def run_for(self, current_time: int, t: int) -> int:
        if self.ended:
            raise Exception('Process already ended')
        if self.attr_defined(self.__t_arrival) and current_time < self.t_arrival:
            raise Exception(f'Process not arrived yet -> t: {t}\n{self}')
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

    def give_attr(self, attr):
        if self.protected and not self.attr_defined(attr):
            raise Exception(f"This field is not defined: {attr}, protected: {self.protected}")
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
        '''
        Time spent waiting in the queue.

        t_wait = start time last interval - time arrival -
        time spent previously executing this process
        '''
        if not self.ended:
            return self.give_attr(self.UDF)
        time_executed = sum([h["t"] for h in self.history[:-1]])
        return self.history[-1]["start"] - self.t_arrival - time_executed

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

    def __str__(self):
        self.protected = False
        s = f'Process {self.name}\n'
        s = f'{s}  Arrived at {self.__t_arrival}\n'
        s = f'{s}  CPU time {self.__t_cpu}\n'
        start = self.t_start if self.t_start == self.UDF else 'not started'
        s = f'{s}  Started at {start}\n'
        end = self.t_end if self.t_end == self.UDF else 'not ended'
        s = f'{s}  Ended at {end}\n'
        s = f'{s}  Priority {self.__priority}\n'
        s = f'{s}  Time elapsed {self.t_elapsed}\n'
        s = f'{s}  Time remaining {self.t_remaining}\n'
        s = f'{s}  Has ended {self.ended}\n'
        s = f'{s}  History {self.history}\n'
        self.protected = True
        return s



if __name__ == '__main__':
    ps = [
        Process("p1", t_arrival=0, t_cpu=8),
        Process("p2", t_arrival=1, t_cpu=4),
        Process("p3", t_arrival=2, t_cpu=9),
        Process("p4", t_arrival=3, t_cpu=5),
        Process("p5", t_arrival=12, t_cpu=2)
    ]

    t = 0
    t = ps[1 - 1].run_for(t, 1)
    t = ps[2 - 1].run_for(t, 4)
    t = ps[4 - 1].run_for(t, 5)
    t = ps[1 - 1].run_for(t, 2)
    t = ps[5 - 1].run_for(t, 2)
    t = ps[1 - 1].run_for(t, 5)
    t = ps[3 - 1].run_for(t, 9)

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

    print("\nAvg T queue:", Process.avg_t_queue(ps))
    print("Avg T wait:", Process.avg_t_wait(ps))