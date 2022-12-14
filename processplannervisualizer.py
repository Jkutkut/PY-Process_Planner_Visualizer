from AsciiGraph import *

from process import Process
from processplannersimulator import *

class ProcessPlannerVisualizer:
    '''
    Class with the logic to visualize a Processplannersimulator.
    '''

    # ******** COLUMNS ********

    PROCESS = 0
    T_ARRIVAL = 1
    T_CPU = 2
    T_START = 3
    T_END = 4
    T_QUEUE = 5
    T_QUEUE_NORMALIZED = 6
    T_WAIT = 7
    PRIORITY = 8

    _COLUMNS = ["Process", "t_arrival", "t_cpu", "t_start", "t_end", "t_queue", "t_queue normalized", "t_wait", "priority"]

    # ******** COLORS ********
    _MIN_COLOR_CODE = 16
    _MAX_COLOR_CODE = 231
    _NC = "\033[0m"
    _MAX_PROCESSES = 32

    _DX = 5 # Graph horizontal size of each element

    def __init__(self, processes: list, simulator: ProcessPlannerSimulator, *modifiers):
        self._ps = processes
        if len(self._ps) == 0:
            raise Exception("Really? Empty array?")
        if len(self._ps) > self._MAX_PROCESSES:
            raise Exception("Too many processes")
        self._simulation = simulator(self._ps, *modifiers)
        self._columns2show = [True for _ in range(len(self._COLUMNS))]

    # ******** METHODS ********

    def represent(self, verbose: bool = True, unit="ns") -> str:
        if not self._simulation.ended:
            self._simulation.run()
            if not self._simulation.ended:
                raise Exception("The simulation did not end")
        s = self._represent_processes()

        table = [
            [f" {i}  " for i in self._COLUMNS]
        ]

        for p in self._ps:
            p.protected = False

        if all([p.priority == Process.UDF for p in self._ps]):
            self.hide_column(self.PRIORITY)

        for id, p in enumerate(self._ps):
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
                t[i] = self._colorize_txt(id, field.center(len(table[0][i])))
            table.append(t)

        # Hide fields
        for r in range(len(table)):
            table[r] = [table[r][c] for c in range(len(table[r])) if self._columns2show[c]]

        table = '\n'.join([''.join(row) for row in table])
        s += f"\n{table}\n"

        s = f"{s}\nAvg t_queue: {Process.avg_t_queue(self._ps):.3f}{unit}\n"
        s = f"{s}Avg  t_wait: {Process.avg_t_wait(self._ps):.3f}{unit}\n"

        for p in self._ps:
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

    def hide_column(self, column: int):
        self._set_column_visibility(column, False)

    def show_column(self, column: int):
        self._set_column_visibility(column, False)

    # ******** TOOLS ********

    def _represent_processes(self) -> str:
        t = self._simulation.t
        timeline = [i for i in range(0, t)]
        plots = [
            {
                "values": [0 for _ in range(0, t)],
                "color": self._get_color(i)
            } for i in range(len(self._ps))
        ]

        legend = ["".center(self._DX) for _ in range(0, t)]
        for id, p in enumerate(self._ps):
            c = p.t_cpu
            for h in p.history:
                name = p.name.center(self._DX)
                for i in range(h["start"], h["end"]):
                    plots[id]["values"][i] = c
                    legend[i] = f"{self._colorize_txt(id, name)}"
                    c -= 1

        graph = AsciiGraph.plot(
            plots,
            timeline,
            dx=self._DX,
            dy=1,
            min_value_overlap_axis=True,
            hide_horizontal_axis=False,
        )
        graph = f"\n{graph}\n       {''.join(legend)}\n"
        return graph

    def _set_column_visibility(self, column: int, value: bool):
        if column < 0 or column >= len(self._COLUMNS):
            raise Exception("Invalid column.")
        self._columns2show[column] = value

    def _colorize_txt(self, color_id: int, txt: str) -> str:
        if txt.strip() == str(Process.UDF):
            txt = "".center(len(txt))
        return f"{self._get_color(color_id)}{txt}{self._NC}"

    def _get_color(self, index: int):
        N = len(self._ps)
        step = 64 if N <= 8 else 4

        dColor = 36
        if index % 2 == 0:
            color = self._MAX_COLOR_CODE - (index // 2) * step
        else:
            color = self._MAX_COLOR_CODE - (index - 1) // 2 * step - 5
        color -= (index // 12) * dColor

        if color < self._MIN_COLOR_CODE:
            raise Exception(f"Color not defined {color}")
        if color > self._MAX_COLOR_CODE:
            raise Exception(f"Color not defined max {color}")
        return f"\033[38;5;{color}m"