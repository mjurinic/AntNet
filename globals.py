from enum import Enum

# Host IP
HOST = '127.0.0.1'

# Host password
PASSWORD = 'secret'

# Maximum number of ants in a node
NODE_CAPACITY = 10

# Number of ants
ANT_COUNT = 5

# Tick period in seconds
TICK_PERIOD = 1


class AntDirection(Enum):
    # 0 comes first in PQ
    BACKWARD_ANT = 0
    FORWARD_ANT = 1

