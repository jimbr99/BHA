''' reader_vars.py
    Contains global vars for the reader module
'''

# reader vars
class ReaderVars:
    
    READER_COMM_IDLE = 0
    READER_COMM_CONNECTING = 1
    READER_COMM_CONNECTED = 2
    READER_COMM_ABORT = 3
    
    READER_TXRX_IDLE = 0
    READER_TXRX_TX = 1
    READER_TXRX_RX = 2
    READER_TXRX_ABORT = 3
    
    sv = 0
    st = []
    svcomm = 0
    stcomm = []
    svtxrx = 0
    sttxrx = []

    reader_comm_states = 0  # comm state flags
    reader_txrx_states = 0    # txrx state flags
    reader_abort_states = 0 # abort state flags
    def __init__(self):
        pass
