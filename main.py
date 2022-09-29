from process import *
from processplannersimulator import *
from processplannervisualizer import ProcessPlannerVisualizer

VERBOSE = False

if __name__ == "__main__":
    ps = [
        Process("P1", t_arrival = 1, t_cpu = 1),
        Process("P2", t_arrival = 9, t_cpu = 2),
        Process("P3", t_arrival = 6, t_cpu = 3),
        Process("P4", t_arrival = 3, t_cpu = 5),
        Process("P5", t_arrival = 8, t_cpu = 4),
        Process("P6", t_arrival = 9, t_cpu = 3),
        Process("P7", t_arrival = 1, t_cpu = 1),
        Process("P8", t_arrival = 2, t_cpu = 1),
    ]
    # # ps_priority = [
    # #     Process("P1", priority = 1, t_cpu = 1),
    # #     Process("P2", priority = 1, t_cpu = 2),
    # #     Process("P3", priority = 6, t_cpu = 3),
    # #     Process("P4", priority = 7, t_cpu = 5),
    # #     Process("P5", priority = 8, t_cpu = 4),
    # #     Process("P6", priority = 9, t_cpu = 3),
    # #     Process("P7", priority = 9, t_cpu = 1),
    # #     Process("P8", priority = 9, t_cpu = 1),
    # # ]

    visualizer = ProcessPlannerVisualizer(ps, FCFS, FCFS.BY_TIME)
    # # visualizer = ProcessPlannerVisualizer(ps_priority, FCFS, FCFS.BY_PRIORITY)
    # # visualizer = ProcessPlannerVisualizer(ps, SJF)
    # # visualizer = ProcessPlannerVisualizer(ps, SRJF)
    # # visualizer = ProcessPlannerVisualizer(ps, RR, 2)

    visualizer.plot(verbose=VERBOSE)
