from process import *
from processplanifiersimulator import FCFS
from processplanifiervisualizer import ProcessPlanifierVisualizer


if __name__ == "__main__":
    # TODO
    ps = [
        Process("P1", t_arrival = 1, t_cpu = 1),
        Process("P2", t_arrival = 1, t_cpu = 2),
        Process("P3", t_arrival = 6, t_cpu = 3),
        Process("P4", t_arrival = 7, t_cpu = 5),
        Process("P5", t_arrival = 8, t_cpu = 4),
        Process("P6", t_arrival = 9, t_cpu = 3),
        Process("P7", t_arrival = 9, t_cpu = 1),
    ]

    ps = [
        Process("P1",  t_arrival = 0, t_cpu = 1),
        Process("P2",  t_arrival = 1, t_cpu = 2),
        Process("P3",  t_arrival = 1, t_cpu = 3),
        Process("P4",  t_arrival = 1, t_cpu = 1),
        Process("P5",  t_arrival = 1, t_cpu = 2),
        Process("P6",  t_arrival = 1, t_cpu = 1),
        Process("P7",  t_arrival = 1, t_cpu = 1),
        Process("P8",  t_arrival = 1, t_cpu = 2),
        Process("P9",  t_arrival = 1, t_cpu = 1),
        Process("P10", t_arrival = 1, t_cpu = 1),
        Process("P11", t_arrival = 1, t_cpu = 3),
        Process("P12", t_arrival = 1, t_cpu = 1),
        Process("P13", t_arrival = 1, t_cpu = 1),
        Process("P14", t_arrival = 1, t_cpu = 1),
        Process("P15", t_arrival = 1, t_cpu = 1),
        Process("P16", t_arrival = 1, t_cpu = 1),
        Process("P16", t_arrival = 1, t_cpu = 1),
        Process("P16", t_arrival = 1, t_cpu = 1),
        Process("P16", t_arrival = 1, t_cpu = 1),
        Process("P16", t_arrival = 1, t_cpu = 1),
        Process("P16", t_arrival = 1, t_cpu = 1),
        Process("P16", t_arrival = 1, t_cpu = 1),
        Process("P16", t_arrival = 1, t_cpu = 1),
        Process("P16", t_arrival = 1, t_cpu = 1),
        Process("P16", t_arrival = 1, t_cpu = 1),
        Process("P16", t_arrival = 1, t_cpu = 1),
        Process("P16", t_arrival = 1, t_cpu = 1),
        Process("P16", t_arrival = 1, t_cpu = 1),
        Process("P16", t_arrival = 1, t_cpu = 1),
        Process("P16", t_arrival = 1, t_cpu = 1),
        Process("P16", t_arrival = 1, t_cpu = 1),
        Process("P16", t_arrival = 1, t_cpu = 1),
        Process("P16", t_arrival = 1, t_cpu = 1),
    ]

    # ps = [
    #     Process("P1", t_arrival = 3, t_cpu = 2),
    # ]

    visualizer = ProcessPlanifierVisualizer(ps, FCFS, FCFS.BY_TIME)
    visualizer.plot()
