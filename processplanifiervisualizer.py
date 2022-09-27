from AsciiGraph import *

from process import Process
from processplanifiersimulator import *

class ProcessPlanifierVisualizer:
    COLORS = {
        '\033[0;31m', # Red
        '\033[0;32m', # Green
        '\033[0;33m', # Yellow
        '\033[0;34m', # Blue
        '\033[0;35m', # Purple
        '\033[0;36m', # Cyan
        '\033[0;37m'  # White
    }

    def __init__(self, processes: list, simulator: ProcessPlanifierSimulator, *modifiers):
        self.ps = processes
        if len(self.ps) > len(self.COLORS):
            raise Exception("Too many processes") # TODO allow inf processes
        self.simulation = simulator(self.ps, *modifiers)

    def represent(self) -> str:
        if not self.simulation.ended:
            self.simulation.run()
        s = ""
        # TODO

        # "\nT queue:")
        # for p in ps:
        #     f'{p.name}: {p.t_queue}')

        # "\nT queue normalized:")
        # for p in ps:
        #     f'{p.name}: {p.t_queue_normalized}')
        
        # "\nT wait:")
        # for p in ps:
        #     f'{p.name}: {p.t_wait}')

        s = f"{s}\nAvg Time queue: {Process.avg_t_queue(self.ps)}\n"
        s = f"{s}Avg Time wait: {Process.avg_t_wait(self.ps)}\n"

        return s

    def plot(self):
        print(self.represent())

