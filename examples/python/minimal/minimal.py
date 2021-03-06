import struct
from time import time

BYTES_PER_VALUE = 8
SHARED_MEMORY_HANDLE = "_ppt_hmem_Minimal"


class Minimal:
    """Injected information for ppt read from shared memory.

    Attributes
    ----------
    shared_memory_handle: str (static)
        String indicating the symbol corresponding to the handle to the shared
        memory block
    shmat_id: int (static)
        Id for the shared memory used by shmat
    buffer_address : int (static)
        Memory address for the data portion of the ppt shared memory block
    buffer_size: int  (static)
        Buffer size of the shared memory in bytes
    buffer_offset: int  (static)
        Offset of the buffer from the beginning of the shared memory block to 
        the data portion
    counter_addresses: list  (static)
        List of counter addresses
    sequence_number: int (static)
        The current increment number of the data being written. Always goes up.
    """

    shmat_id = None
    buffer_address = None
    buffer_size = None
    buffer_offset = None
    counter_addresses = None
    sequence_number = 1
    outfile = None  # TODO: For testing only. Remove when memory is enabled.

    def get_next_index():
        """Get the next sequence number."""
        Minimal.sequence_number += 1
        return Minimal.sequence_number

    def check_attach_state():
        """Attach if appropriate, detach if needed."""
        # Not attached
        if not Minimal.shmat_id and not Minimal.buffer_address:
            return False

        # All attached!
        if Minimal.shmat_id and Minimal.buffer_address:
            return True

        # Not attached but should be
        if Minimal.shmat_id and not Minimal.buffer_address:
            return Minimal.try_attach()

        # Just detached, need to clean up
        if not Minimal.shmat_id and Minimal.buffer_address:
            Minimal.try_detach()
            return False

    def try_attach():
        """Try to attach to a shared memory buffer."""
        # TODO: This is placeholder, use schmat to populate. Open file for now.
        Minimal.buffer_address = 1000
        Minimal.buffer_size = 64 * 10
        Minimal.buffer_offset = 1000
        Minimal.counter_addresses = [3, 4, 5]
        Minimal.outfile = open("minimal_test.txt", "wb")

        return True

    def try_detach():
        """Detach from the shared memory buffer."""
        if not Minimal.shmat_id:
            Minimal.buffer_address = None
            Minimal.buffer_size = None
            Minimal.buffer_offset = None
            Minimal.counter_addresses = None

    #            Minimal.outfile = open("minimal_test.txt", "w")  # TODO: placeholder

    def write_block(block):
        """Write a block to the specified offset"""
        # TODO: This is placeholder, use schmat to write to shared memory.
        #       writing to file for now.
        Minimal.outfile.write(block)


class First:
    """Prototype autogenerated code for a hypothetical ppt description."""

    buffer_size = 10

    def __init__(self):
        # TODO: Assume 10 elements for now
        self._counter = 0
        self._duration_start = 0.0
        self._duration_end = 0.0

    def save(self):
        """Save this data to the shared memory block."""
        if not Minimal.check_attach_state():
            return False

        sequence_number = Minimal.get_next_index()
        buffer = struct.pack(
            "llddl",
            sequence_number,
            self._counter,
            self._duration_start,
            self._duration_end,
            sequence_number,
        )

        Minimal.write_block(buffer)

    def duration_start(self):
        self._duration_start = time()

    def duration_end(self):
        self._duration_end = time()

    def increment_counter(self):
        self._counter += 1
