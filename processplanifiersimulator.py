class ProcessPlanifierSimulatior:
    BY_TIME = lambda p: p.t_arrival
    BY_PRIORITY = lambda p: p.priority

    def __init__(self, processes: list, plan_by=BY_TIME):
        self.processes = processes
        self.queue = sorted(self.processes, key=plan_by)
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

class FCFS(ProcessPlanifierSimulation):
    def __init__(self, processes: list):
        super().__init__(processes)

    def run(self):
        pass # TODO

class SJF(ProcessPlanifierSimulation):
    def __init__(self, processes: list):
        super().__init__(processes)

    def run(self):
        pass # TODO

class SRTF(ProcessPlanifierSimulation):
    def __init__(self, processes: list):
        super().__init__(processes)

    def run(self):
        pass # TODO

# class RR(ProcessPlanifierSimulatior):
#     def __init__(self, processes: list):
#         super().__init__(processes) # TODO Check plan_by

#     def run(self):
#         pass # TODO