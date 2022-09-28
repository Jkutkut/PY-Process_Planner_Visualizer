from AsciiGraph import *

from process import Process
from processplanifiersimulator import *

class ProcessPlanifierVisualizer:
    COLORS = [
        # TODO add more colors
        '\033[0;31m', # Red
        '\033[0;32m', # Green
        '\033[0;33m', # Yellow
        '\033[0;34m', # Blue
        '\033[0;35m', # Purple
        '\033[0;36m', # Cyan
        '\033[0;37m'  # White
    ]

    DX = 5

    def __init__(self, processes: list, simulator: ProcessPlanifierSimulator, *modifiers):
        self.ps = processes
        if len(self.ps) == 0:
            raise Exception("Really? Empty array?")
        if len(self.ps) > len(self.COLORS):
            raise Exception("Too many processes")
        self.simulation = simulator(self.ps, *modifiers)

    def represent(self, verbose: bool = True, unit="ns") -> str:
        if not self.simulation.ended:
            self.simulation.run()
        s = self.represent_processes()

        if verbose:
            s += f"\nFormulas:\n"
            s += f"  Time queue: Tq = t_end - t_arrival\n"
            s += f"  Tq normalized: normalize(Tq) = Tq / t_cpu\n"
            s += f"  Avg Tq: avg(Tq) = sum(Tq(n)) / n\n\n"
            s += f"  t_wait = (last start time of process) - (t_cpu consumed previously) - t_arrival\n"
            s += f"  Avg t_wait: avg(t_wait) = sum(t_wait(n)) / n\n"

        table = [
            [f" {i}  " for i in ["Process", "t_arrival", "t_cpu", "Tq", "Tq normalized", "t_wait"]]
        ]

        for id, p in enumerate(self.ps):
            name = self.colorize_txt(id, p.name.center(len(table[0][0])))
            t_arrival = self.colorize_txt(id, f"{p.t_arrival}{unit}".center(len(table[0][1])))
            t_cpu = self.colorize_txt(id, f"{p.t_cpu}{unit}".center(len(table[0][2])))
            t_queue = self.colorize_txt(id, f"{p.t_queue}{unit}".center(len(table[0][3])))
            t_queue_normalized = self.colorize_txt(id, f"{p.t_queue_normalized}".center(len(table[0][4])))
            t_wait = self.colorize_txt(id, f"{p.t_wait}{unit}".center(len(table[0][5])))
            
            table.append([
                name, t_arrival, t_cpu, t_queue, t_queue_normalized, t_wait
            ])
        table = '\n'.join([''.join(row) for row in table])
        s += f"\n{table}\n"

        s = f"{s}\nAvg Time queue: {Process.avg_t_queue(self.ps):.3f}{unit}\n"
        s = f"{s}Avg Time wait: {Process.avg_t_wait(self.ps):.3f}{unit}\n"

        return s

    def plot(self, unit="ns"):
        print(self.represent(unit=unit))

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

        legend = ["".center(self.DX) for _ in range(0, t)]
        for id, p in enumerate(self.ps):
            c = p.t_cpu
            for h in p.history:
                name = p.name.center(self.DX)
                for i in range(h["start"], h["end"]):
                    plots[id]["values"][i] = c
                    legend[i] = f"{self.colorize_txt(id, name)}"
                    c -= 1

        graph = AsciiGraph.plot(
            plots,
            timeline,
            dx=self.DX,
            dy=1,
            min_value_overlap_axis=True,
            hide_horizontal_axis=False,
        )
        graph = f"\n{graph}\n       {''.join(legend)}\n"
        return graph

