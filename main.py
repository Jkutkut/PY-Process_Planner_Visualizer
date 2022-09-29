from process import *
from processplanifiersimulator import *
from processplanifiervisualizer import ProcessPlanifierVisualizer


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
    # ps_priority = [
    #     Process("P1", priority = 1, t_cpu = 1),
    #     Process("P2", priority = 1, t_cpu = 2),
    #     Process("P3", priority = 6, t_cpu = 3),
    #     Process("P4", priority = 7, t_cpu = 5),
    #     Process("P5", priority = 8, t_cpu = 4),
    #     Process("P6", priority = 9, t_cpu = 3),
    #     Process("P7", priority = 9, t_cpu = 1),
    #     Process("P8", priority = 9, t_cpu = 1),
    # ]

    visualizer = ProcessPlanifierVisualizer(ps, FCFS, FCFS.BY_TIME)
    # visualizer = ProcessPlanifierVisualizer(ps_priority, FCFS, FCFS.BY_PRIORITY)
    # visualizer = ProcessPlanifierVisualizer(ps, SJF)
    # visualizer = ProcessPlanifierVisualizer(ps, SRJF)
    # visualizer = ProcessPlanifierVisualizer(ps, RR, 2)
    
    visualizer.plot(verbose=True)
    # visualizer.plot(verbose=False)
