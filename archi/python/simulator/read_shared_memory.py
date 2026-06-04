import mmap
import struct
from pathlib import Path

BIN_FILE_PATH = Path(__file__).resolve().parents[1] / "shared_mem" /"shared_memory.bin"
HEADER_SIZE = 8      # uint64 count
RECORD_SIZE = 32     # 4 doubles (x,y,z,g)


def read_shared_memory(file_path=BIN_FILE_PATH):
    points = []

    with open(file_path, "rb") as f:
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
    points = read_shared_memory()

    print(f"Found {len(points)} points")

    for x, y, z, g in points:
        print(f"x={x}, y={y}, z={z}, g={g}")