import pathlib
import sys
from enum import Enum
from pathlib import Path
from typing import Iterator


DATA_PATH = "data/part1"


OPCODE = {
    "100010": "mov",
}


class UnsupportedOpcodeException(Exception):
    ...


class Reg(Enum):
    AL = "al"
    AX = "ax"
    AH = "ah"
    BL = "bl"
    BX = "bx"
    BH = "bh"
    BP = "bp"
    CL = "cl"
    CX = "cx"
    CH = "ch"
    DL = "dl"
    DX = "dx"
    DH = "dh"
    DI = "di"
    SI = "si"
    SP = "sp"

    def __str__(self):
        return self.value


def _map_reg(bitfield: int, W: int):
    reg_mapping = {
        "000": Reg.AX if W else Reg.AL,
        "001": Reg.CX if W else Reg.CL,
        "010": Reg.DX if W else Reg.DL,
        "011": Reg.BX if W else Reg.BL,
        "100": Reg.SP if W else Reg.AH,
        "101": Reg.BP if W else Reg.CH,
        "110": Reg.SI if W else Reg.DH,
        "111": Reg.DI if W else Reg.BH,
    }
    return reg_mapping[format(bitfield, "b").zfill(3)]
    

def bitmask(bitmask_str: str) -> int:
    return int(bitmask_str, base=2)


def _is_one_byte_instruction(byte):
    return False


def bitwise_op(byte: int, shift: int, mask: int = None):
    mask = mask or 2**8 - 1
    return byte >> shift & mask


class Instruction:
    def __init__(self, first_byte, second_byte):
        self.opcode = bitwise_op(first_byte, 2)
        self.D = bitwise_op(first_byte, 1, bitmask("1"))
        self.W = bitwise_op(first_byte, 0, bitmask("1"))
        self.MOD = bitwise_op(second_byte, 6, bitmask("11"))
        self.REG = bitwise_op(second_byte, 3, bitmask("111"))
        self.RM = bitwise_op(second_byte, 0, bitmask("111"))

        try:
            self.name = OPCODE.get(format(self.opcode, "b"))
        except ValueError:
            raise UnsupportedOpcodeException(f"opcode {self.opcode} not yet supported")

        self.src_op = _map_reg(self.REG, self.W) if self.D == 0 else _map_reg(self.RM, self.W)
        self.dst_op = _map_reg(self.RM, self.W) if self.D == 0 else _map_reg(self.REG, self.W)

    def __str__(self):
        return f"{self.name} {self.dst_op}, {self.src_op}"


def decode_bytes(byte_stream: Iterator[bytes]):
    result = []

    for byte in byte_stream:
        if _is_one_byte_instruction(byte):
            # decode the one byte instruction, add to results
            continue
        next_byte = next(byte_stream)
        ins = Instruction(byte, next_byte)
        result.append(str(ins))

    return result


def print_asm(decoded_instructions):
    for instruction in decoded_instructions:
        print(instruction)


def run(filepath: Path):
    print_asm(decode_bytes(iter(filepath.read_bytes())))


if __name__ == "__main__":
    default = "0038"
    filename = sys.argv[1] if len(sys.argv) > 1 else f"listing_{default}_many_register_mov"
    file_path = pathlib.Path(f"{DATA_PATH}/{filename}")
    if not file_path.exists():
        print("Invalid input file")
        sys.exit(1)
    run(file_path)
