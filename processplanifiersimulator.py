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

# class SJF(ProcessPlanifierSimulator):
#     def __init__(self, processes: list):
#         super().__init__(processes, self.BY_TIME)

#     def run(self):
#         pass # TODO

# class SRTF(ProcessPlanifierSimulator):
#     def __init__(self, processes: list):
#         super().__init__(processes, self.BY_TIME)

#     def run(self):
#         pass # TODO

# class RR(ProcessPlanifierSimulator):
#     def __init__(self, processes: list):
#         super().__init__(processes) # TODO Check plan_by

#     def run(self):
#         pass # TODO