from AsciiGraph import *

from process import Process
from processplanifiersimulator import *

class ProcessPlanifierVisualizer:
    COLORS = [
        '\033[0;31m', # Red
        '\033[0;32m', # Green
        '\033[0;33m', # Yellow
        '\033[0;34m', # Blue
        '\033[0;35m', # Purple
        '\033[0;36m', # Cyan
        '\033[0;37m'  # White
    ]

    def __init__(self, processes: list, simulator: ProcessPlanifierSimulator, *modifiers):
        self.ps = processes
        if len(self.ps) == 0:
            raise Exception("Really? Empty array?")
        if len(self.ps) > len(self.COLORS):
            raise Exception("Too many processes")
        self.simulation = simulator(self.ps, *modifiers)

    def represent(self) -> str:
        if not self.simulation.ended:
            self.simulation.run()
        # TODO add verbose mode
        # TODO add units
        s = self.represent_processes()

        s = f"{s}\nTime queue:\n"
        for id, p in enumerate(self.ps):
            s = f'{s}  {self.colorize_txt(id, p.name)}: {p.t_queue:4}'
            s = f'{s}  Normalized: {p.t_queue_normalized:4.3f}\n'
        s = f"{s}\nAvg Time queue: {Process.avg_t_queue(self.ps):.3f}\n"


        s = f"{s}\nTime wait:\n"
        for id, p in enumerate(self.ps):
            s = f'{s}  {self.colorize_txt(id, p.name)}: {p.t_wait:4.3f}\n'
        s = f"{s}Avg Time wait: {Process.avg_t_wait(self.ps):.3f}\n"

        return s

    def plot(self):
        print(self.represent())

    @classmethod
    def colorize_txt(cls, color_id: int, txt: str) -> str:
        return f"{cls.COLORS[color_id % len(cls.COLORS)]}{txt}\033[0m"

    def represent_processes(self) -> str:
        t = self.simulation.t
        timeline = [i for i in range(0, t)]
        plots = [
            {
                "values": [0 for _ in range(0, t)],
                "color": self.COLORS[i % len(self.COLORS)]
            } for i in range(len(self.ps))
        ]

        for id, p in enumerate(self.ps):
            c = p.t_cpu
            for h in p.history:
                start = h["start"]
                end = h["end"]
                for i in range(start, end):
                    plots[id]["values"][i] = c
                    c -= 1

        s = AsciiGraph.plot(
            plots,
            timeline,
            dx=3,
            dy=1,
            min_value_overlap_axis=True,
            hide_horizontal_axis=False,
        )
        s = f"{s}\nLegend:\n"
        legend = []
        for id, p in enumerate(self.ps):
            legend.append(self.colorize_txt(id, p.name))
        s = f"{s}  {' '.join(legend)}\n"
        return s

    def represent_cpu_ownership(self) -> str:
        return "" # TODO

