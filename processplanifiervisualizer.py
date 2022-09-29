from AsciiGraph import *

from process import Process
from processplanifiersimulator import *

class ProcessPlanifierVisualizer:
    # Colors
    MIN_COLOR_CODE = 16
    MAX_COLOR_CODE = 231
    NC = "\033[0m"
    MAX_PROCESSES = 32

    DX = 5

    def __init__(self, processes: list, simulator: ProcessPlanifierSimulator, *modifiers):
        self.ps = processes
        if len(self.ps) == 0:
            raise Exception("Really? Empty array?")
        if len(self.ps) > self.MAX_PROCESSES:
            raise Exception("Too many processes")
        self.simulation = simulator(self.ps, *modifiers)

    def represent_processes(self) -> str:
        t = self.simulation.t
        timeline = [i for i in range(0, t)]
        plots = [
            {
                "values": [0 for _ in range(0, t)],
                "color": self.get_color(i)
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

    def represent(self, verbose: bool = True, unit="ns") -> str:
        # TODO fix the logic to be able to hide any column
        if not self.simulation.ended:
            self.simulation.run()
            if not self.simulation.ended:
                raise Exception("The simulation did not end")
        s = self.represent_processes()

        table = [
            [f" {i}  " for i in ["Process", "t_arrival", "t_cpu", "t_start", "t_end", "t_queue", "t_queue normalized", "t_wait", "priority"]]
        ]

        for p in self.ps:
            p.protected = False

        if all([p.priority == Process.UDF for p in self.ps]):
            table[0][-1] = ""
        for id, p in enumerate(self.ps):
            t = [
                p.name,
                f"{p.t_arrival}{unit}",
                f"{p.t_cpu}{unit}",
                f"{p.t_start}{unit}",
                f"{p.t_end}{unit}",
                f"{p.t_queue}{unit}",
                f"{p.t_queue_normalized:.3f}",
                f"{p.t_wait}{unit}",
                f"{p.priority}",
            ]
            for i, field in enumerate(t):
                t[i] = self.colorize_txt(id, field.center(len(table[0][i])))
            table.append(t)

        table = '\n'.join([''.join(row) for row in table])
        s += f"\n{table}\n"

        s = f"{s}\nAvg t_queue: {Process.avg_t_queue(self.ps):.3f}{unit}\n"
        s = f"{s}Avg  t_wait: {Process.avg_t_wait(self.ps):.3f}{unit}\n"

        for p in self.ps:
            p.protected = True

        if verbose:
            s += f"\nFormulas:\n"
            s += f"  Time queue: Tq = t_end - t_arrival\n"
            s += f"  Tq normalized: normalize(Tq) = Tq / t_cpu\n"
            s += f"  Avg Tq: avg(Tq) = sum(Tq(n)) / n\n\n"
            s += f"  t_wait = (last start time of process) - (t_cpu consumed previously) - t_arrival\n"
            s += f"  Avg t_wait: avg(t_wait) = sum(t_wait(n)) / n\n"

            s += f"\nCheatSheet:\n"
            s += f"  t_arrival: Time the process was created.\n"
            s += f"  t_cpu: Amount of time units the process needs.\n"
            s += f"  t_start: Time the process started.\n"
            s += f"  t_end: Time the process ended.\n"
            s += f"  t_queue: Time took from creation to finalization.\n"
            s += f"  t_queue normalized: t_queue relative to t_cpu.\n"
            s += f"  t_wait: Time waited.\n"

        return s

    def plot(self, verbose: bool = True, unit="ns"):
        print(self.represent(verbose = verbose, unit=unit))

    def colorize_txt(self, color_id: int, txt: str) -> str:
        if txt.strip() == str(Process.UDF):
            txt = "".center(len(txt))
        return f"{self.get_color(color_id)}{txt}{self.NC}"

    def get_color(self, index: int):
        N = len(self.ps)
        step = 64 if N <= 8 else 4

        dColor = 36
        if index % 2 == 0:
            color = self.MAX_COLOR_CODE - (index // 2) * step
        else:
            color = self.MAX_COLOR_CODE - (index - 1) // 2 * step - 5
        color -= (index // 12) * dColor

        if color < self.MIN_COLOR_CODE:
            raise Exception(f"Color not defined {color}")
        if color > self.MAX_COLOR_CODE:
            raise Exception(f"Color not defined max {color}")
        return f"\033[38;5;{color}m"