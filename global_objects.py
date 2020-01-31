''' global_objects '''

global g_periodic_task_flags
global ant
ant = 0


''' Timer flag declarations '''
global NO_TASK
global TASK_50MS
global TASK_100MS
global TASK_500MS
global TASK_1SEC

global TIME_SLOT0
global TIME_SLOT1
global TIME_SLOT2
global TIME_SLOT3
global TIME_SLOT4
global TIME_SLOT5



''' vars and flags instatiation '''
# periodic defs
NO_TASK = 0
TASK_50MS = 0x01
TASK_100MS = 0x02
TASK_500MS = 0x04
TASK_1SEC = 0x08
TASK_ALL = 0x0F

TIME_SLOT0 = 0
TIME_SLOT1 = 1
TIME_SLOT2 = 2
TIME_SLOT3 = 3
TIME_SLOT4 = 4
TIME_SLOT5 = 5

# reader defs
READER_IDLE = 0
READER_COMM_IDLE = 1
READER_COMM_CONNECTING = 2
READER_COMM_CONNECTED = 3
READER_COMM_ABORT = 4


# global task flags
g_periodic_task_flags = NO_TASK

# global vars


# global timer counters
g_per25ms_counter = 0
g_per100ms_counter = 0
g_per500ms_counter = 0
g_per1SEC_counter = 0

# reader state flags
# reader comm state machine
g_reader_comm_sm = 0

# reader tx state machine
g_reader_tx_sm = 0

# reader rx state machine
g_reader_rx_sm = 0


g_reader_idle_states = 0
g_reader_tx_states = 0
g_reader_rx_states = 0

