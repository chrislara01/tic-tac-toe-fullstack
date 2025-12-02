class InvalidBoardError(ValueError):
    """Raised when the board state string is malformed."""


class InvalidMoveError(ValueError):
    """Raised when a move is invalid, e.g., cell occupied or out of range."""


class GameOverError(RuntimeError):
    """Raised when attempting to play on a finished game."""
