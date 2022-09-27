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

    def __init__(self, processes: list):
        self.processes = processes
        self.simulation = None
        # TODO

