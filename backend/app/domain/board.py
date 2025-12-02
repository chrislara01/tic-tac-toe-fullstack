from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional, Sequence, Tuple

from .enums import Player
from .exceptions import InvalidBoardError, InvalidMoveError

# External position mapping (numpad layout):
# 7 8 9
# 4 5 6
# 1 2 3
#
# We store the board string in exactly this order: "789456123"
# This avoids 0-8 row-major order externally while keeping logic simple.
EXTERNAL_ORDER: List[int] = [7, 8, 9, 4, 5, 6, 1, 2, 3]
EXTERNAL_TO_INDEX = {pos: idx for idx, pos in enumerate(EXTERNAL_ORDER)}
INDEX_TO_EXTERNAL = {idx: pos for idx, pos in enumerate(EXTERNAL_ORDER)}

# Winning patterns expressed as internal indices (0..8) matching EXTERNAL_ORDER
WIN_PATTERNS: Tuple[Tuple[int, int, int], ...] = (
    # Rows (top, middle, bottom)
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    # Columns (left, middle, right)
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    # Diagonals
    (0, 4, 8),
    (2, 4, 6),
)

ALLOWED_CHARS = {"x", "o", " "}


@dataclass(frozen=True)
class Board:
    state: str  # 9-char string in EXTERNAL_ORDER with 'x', 'o', or ' '

    def __post_init__(self) -> None:
        if len(self.state) != 9:
            raise InvalidBoardError("Board state must be exactly 9 characters long.")
        if any(c not in ALLOWED_CHARS for c in self.state):
            raise InvalidBoardError("Board contains invalid characters. Allowed: 'x','o',' '.")

    @classmethod
    def empty(cls) -> "Board":
        return cls(" " * 9)

    @classmethod
    def from_string(cls, s: str) -> "Board":
        return cls(s)

    def to_string(self) -> str:
        return self.state

    def cell_by_index(self, index: int) -> str:
        return self.state[index]

    def cell(self, position: int) -> str:
        idx = EXTERNAL_TO_INDEX.get(position)
        if idx is None:
            raise InvalidMoveError("Position must be one of 1..9 in numpad layout.")
        return self.cell_by_index(idx)

    def is_empty_at(self, position: int) -> bool:
        return self.cell(position) == " "

    def available_positions(self) -> List[int]:
        return [INDEX_TO_EXTERNAL[i] for i, c in enumerate(self.state) if c == " "]

    def with_move(self, position: int, player: Player) -> "Board":
        idx = EXTERNAL_TO_INDEX.get(position)
        if idx is None:
            raise InvalidMoveError("Position must be one of 1..9 in numpad layout.")
        if self.state[idx] != " ":
            raise InvalidMoveError("Cell is already occupied.")
        cells = list(self.state)
        cells[idx] = player.value
        return Board("".join(cells))

    def is_full(self) -> bool:
        return " " not in self.state

    def winner(self) -> Optional[Player]:
        for a, b, c in WIN_PATTERNS:
            trio = self.state[a] + self.state[b] + self.state[c]
            if trio == "xxx":
                return Player.X
            if trio == "ooo":
                return Player.O
        return None

    def is_draw(self) -> bool:
        return self.winner() is None and self.is_full()

    def counts(self) -> Tuple[int, int]:
        x_count = self.state.count("x")
        o_count = self.state.count("o")
        return x_count, o_count

    def pretty(self) -> str:
        # For debugging: returns a 3x3 representation in EXTERNAL_ORDER
        lines = [
            " ".join(self.state[0:3]),
            " ".join(self.state[3:6]),
            " ".join(self.state[6:9]),
        ]
        return "\n".join(lines)
