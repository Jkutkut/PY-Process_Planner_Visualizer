from AsciiGraph import *

from process import *


if __name__ == "__main__":
    plots = [
        {
            "values": [i for i in range(0, 10)],
        }
    ]
    keys = [i for i in range(0, 10)]

    graph = AsciiGraph.plot(plots, keys)
    print(graph)


    # TODO
    p = Process(
        "P1",
        t_arrival = 0,
        t_cpu = 2
    )
    print(p)
    print(p.name)
    print(p.t_arrival)
