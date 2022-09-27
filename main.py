from process import *
from processplanifiersimulator import FCFS
from processplanifiervisualizer import ProcessPlanifierVisualizer


if __name__ == "__main__":
    # plots = [
    #     {
    #         "values": [i for i in range(0, 10)],
    #     }
    # ]
    # keys = [i for i in range(0, 10)]

    # graph = AsciiGraph.plot(plots, keys)
    # print(graph)

    # TODO
    ps = [
        Process("P1", t_arrival = 2, t_cpu = 2),
        Process("P2", t_arrival = 1, t_cpu = 4),
        Process("P3", t_arrival = 2, t_cpu = 6),
    ]

    visualizer = ProcessPlanifierVisualizer(ps, FCFS, FCFS.BY_TIME)
    visualizer.plot()
