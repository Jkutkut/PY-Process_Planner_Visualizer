class ProcessPlanifierSimulator:
    BY_TIME = 0
    BY_PRIORITY = 1

    BY_TIME_FT = lambda p: p.t_arrival
    BY_PRIORITY_FT = lambda p: p.priority

    def __init__(self, processes: list, plan_by = BY_TIME):
        self.processes = processes
        self.planning = plan_by
        self.planning_ft = ProcessPlanifierSimulator.BY_TIME_FT
        if plan_by == self.BY_PRIORITY:
            self.planning_ft = ProcessPlanifierSimulator.BY_PRIORITY_FT
        self.queue = sorted(self.processes, key=self.planning_ft)
        self.t = 0
        self.__ended = False

    def run(self) -> int:
        raise Exception("Not implemented")

    # ************ GETTERS ************

    @property
    def ended(self):
        return self.__ended

    def avalible2run(self, t: int) -> list:
        lst = []
        for p in self.processes:
            if p.ended:
                continue
            if p.t_arrival > t:
                continue
            lst.append(p)
        return lst

    # ************ SETTERS ************

    @ended.setter
    def ended(self, value):
        self.check_end()
        self.__ended = value

    # ************ CHECKERS ************

    def check_end(self):
        if any([not process.ended for process in self.processes]):
            raise Exception("Not all processes have ended")

class FCFS(ProcessPlanifierSimulator):
    def __init__(self, processes: list, plan_by):
        super().__init__(processes, plan_by)

    def run(self) -> int:
        if self.ended:
            return self.t
        for process in self.queue:
            if self.planning == self.BY_TIME and self.t < process.t_arrival:
                self.t = process.t_arrival
            self.t = process.run_for(self.t, process.t_cpu)
        self.ended = True

class SJF(ProcessPlanifierSimulator):
    def __init__(self, processes: list):
        super().__init__(processes, self.BY_TIME)

    def run(self):
        remaining_ft = lambda p: p.t_remaining
        while len(self.queue) > 0:
            lst = self.avalible2run(self.t)
            if len(lst) == 0:
                t += 1
                continue
            # Sortest Job Fist (SJF)
            lst_s = sorted(lst, key = remaining_ft)
            min_t_remaining = lst_s[0].t_remaining
            if len(lst_s) > 1:
                # Get all with t_remaining lowest
                lst_s = list(filter(lambda p: p.t_remaining == min_t_remaining, lst_s))
                if len(lst_s) > 1:
                    lst_s = sorted(lst_s, key=SJF.BY_TIME_FT) # Apply FCFS (smallest t_arrival)
            p = lst_s[0]
            self.t = p.run_for(self.t, p.t_cpu)
            self.queue.remove(p)
        self.ended = True


class SRTF(ProcessPlanifierSimulator):
    def __init__(self, processes: list):
        super().__init__(processes, self.BY_TIME)

    def run(self):
        pass # TODO

class SRJF(SRTF):
    pass

# class RR(ProcessPlanifierSimulator):
#     def __init__(self, processes: list):
#         super().__init__(processes) # TODO Check plan_by

#     def run(self):
#         pass # TODO