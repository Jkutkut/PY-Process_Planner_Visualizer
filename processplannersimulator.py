class ProcessPlannerSimulator:
    '''
    Class with the logic to simulate a group of processes.
    '''

    BY_ENTRY = -1
    BY_TIME = 0
    BY_PRIORITY = 1

    _PLANNING_FTS = [
        lambda p: p.t_arrival,
        lambda p: p.priority
    ]

    def __init__(self, processes: list, plan_by = BY_TIME):
        self._processes = processes
        self._queue = [p for p in processes]

        self._planning = plan_by
        if self._planning != self.BY_ENTRY:
            self._queue = sorted(self._queue, key = self._PLANNING_FTS[self._planning])

        self._t = 0
        self.__ended = False

    # ******** METHODS ********

    def run(self) -> int:
        raise Exception("Not implemented")

    def _end(self):
        self.check_end()
        self.__ended = True

    # ******** GETTERS ********

    @property
    def t(self):
        return self._t

    @property
    def ended(self):
        return self.__ended

    def _available2run(self, t: int) -> list:
        lst = []
        for p in self._processes:
            if p.ended:
                continue
            if p.t_arrival > t:
                continue
            lst.append(p)
        return lst

    # ******** CHECKERS ********

    def check_end(self):
        if any([not process.ended for process in self._processes]):
            raise Exception("Not all processes have ended")


# ******** Planifiers ********

class FCFS(ProcessPlannerSimulator):
    def __init__(self, processes: list, plan_by):
        super().__init__(processes, plan_by)

    def run(self) -> int:
        if self.ended:
            return self.t
        for process in self._queue:
            if self._planning == self.BY_TIME and self.t < process.t_arrival:
                self._t = process.t_arrival
            self._t = process.run_for(self.t, process.t_cpu)
        self._end()
        return self.t

class SJF(ProcessPlannerSimulator):
    def __init__(self, processes: list):
        super().__init__(processes, self.BY_TIME)

    def run(self):
        if self.ended:
            return self.t
        remaining_ft = lambda p: p.t_remaining
        while len(self._queue) > 0:
            lst = self._available2run(self.t)
            if len(lst) == 0:
                self._t += 1
                continue
            # Sortest Job Fist (SJF)
            lst_s = sorted(lst, key = remaining_ft)
            min_t_remaining = lst_s[0].t_remaining
            if len(lst_s) > 1:
                # Get all with t_remaining lowest
                lst_s = list(filter(lambda p: p.t_remaining == min_t_remaining, lst_s))
                if len(lst_s) > 1:
                    lst_s = sorted(lst_s, key=SJF._PLANNING_FTS[SJF.BY_TIME]) # Apply FCFS (smallest t_arrival)
            p = lst_s[0]
            self._t = p.run_for(self.t, p.t_cpu)
            self._queue.remove(p)
        self._end()
        return self.t

class SRTF(ProcessPlannerSimulator):
    def __init__(self, processes: list):
        super().__init__(processes, self.BY_ENTRY)

    def run(self):
        if self.ended:
            return self.t
        remaining_ft = lambda p: p.t_remaining
        while len(self._queue) > 0:
            lst = self._available2run(self.t)
            if len(lst) == 0:
                self._t += 1
                print(self.t)
                continue
            # Sortest Job Fist (SJF)
            lst_s = sorted(lst, key = remaining_ft)
            min_t_remaining = lst_s[0].t_remaining
            if len(lst_s) > 1:
                # Get all with t_remaining lowest
                lst_s = list(filter(lambda p: p.t_remaining == min_t_remaining, lst_s))
                if len(lst_s) > 1:
                    lst_s = sorted(lst_s, key=SJF._PLANNING_FTS[SJF.BY_TIME]) # Apply FCFS (smallest t_arrival)
            p = lst_s[0]
            self._t = p.run_for(self.t, 1)
            if p.ended:
                self._queue.remove(p)
        self._end()
        return self.t

class SRJF(SRTF):
    pass

class RR(ProcessPlannerSimulator):
    def __init__(self, processes: list, quantum: int):
        super().__init__(processes, self.BY_TIME)
        self.quantum = quantum

    def run(self):
        if self.ended:
            return self.t
        i = -1
        while len(self._queue) > 0:
            i += 1
            lst = self._available2run(self.t)
            if len(lst) == 0:
                self._t += 1
                continue
            if i >= len(lst):
                i = 0
            p = lst[i]
            self._t = p.run_for(self.t, self.quantum)
            if p.ended:
                self._queue.remove(p)
                lst.remove(p)
                i -= 1
        self._end()
        return self.t