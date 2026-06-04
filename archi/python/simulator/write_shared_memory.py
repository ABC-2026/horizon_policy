import mmap
import struct
from pathlib import Path


# Relative path from this Python file
BIN_FILE_PATH = Path(__file__).resolve().parents[1] / "shared_mem" /"shared_memory.bin"

HEADER_SIZE = 8          # uint64 count
RECORD_SIZE = 32         # x, y, z, g = 4 doubles = 32 bytes


def write_shared_memory(points, file_path=BIN_FILE_PATH):
    """
    Writes points to shared_memory.bin.

    Format:
    [count][x,y,z,g][x,y,z,g]...

    count = unsigned long long
    x,y,z,g = double
    """

    count = len(points)
    total_size = HEADER_SIZE + count * RECORD_SIZE

    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w+b") as f:
        f.truncate(total_size)

        mm = mmap.mmap(f.fileno(), total_size)

        try:
            struct.pack_into("Q", mm, 0, count)

            offset = HEADER_SIZE

            for x, y, z, g in points:
                struct.pack_into("dddd", mm, offset, x, y, z, g)
                offset += RECORD_SIZE

            mm.flush()

        finally:
            mm.close()


def read_shared_memory(file_path=BIN_FILE_PATH):
    """
    Reads points from shared_memory.bin.
    """

    points = []

    with open(file_path, "r+b") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

        try:
            count = struct.unpack_from("Q", mm, 0)[0]

            offset = HEADER_SIZE

            for _ in range(count):
                x, y, z, g = struct.unpack_from("dddd", mm, offset)
                points.append((x, y, z, g))
                offset += RECORD_SIZE

        finally:
            mm.close()

    return points


if __name__ == "__main__":
    data = [
        (1.0, 2.0, 3.0, 0.5),
        (4.0, 5.0, 6.0, 1.0),
        (7.0, 8.0, 9.0, 1.5),
    ]

    write_shared_memory(data)

    result = read_shared_memory()

    print("Read from shared memory:")
    for item in result:
        print(item)