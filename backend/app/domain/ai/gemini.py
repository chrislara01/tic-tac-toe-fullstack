from __future__ import annotations

import logging
import re
from typing import Optional

from ..board import Board
from ..enums import Player
from .base import Strategy

# Lazy imports for the Gemini SDK to avoid hard dependency at import time
# We'll import inside the strategy call and gracefully fallback if unavailable.

logger = logging.getLogger(__name__)


class GeminiStrategy(Strategy):
    def __init__(self, api_key: Optional[str], model: str = "gemini-2.0-flash") -> None:
        self.api_key = api_key
        self.model_name = model

    def _fallback(self, board: Board, me: Player) -> int:
        # Local import to avoid circular dependency
        from .medium import HeuristicStrategy

        logger.warning("gemini_fallback_to_heuristic")
        return HeuristicStrategy().select_move(board, me)

    def _build_prompt(self, board: Board, me: Player) -> str:
        avail = board.available_positions()
        prompt = f"""
You are a Tic-Tac-Toe grandmaster AI playing as '{me.value}'.
The board state is a 9-character string in NUMPAD order (top row is 7 8 9, middle 4 5 6, bottom 1 2 3).
Each character is one of: 'x', 'o', or a single space for empty.

Board string: "{board.to_string()}"
Available positions (numpad): {avail}

Task:
- Choose the best move for '{me.value}'.
- Output ONLY a single integer between 1 and 9 that is one of the available positions.
- Do not include any additional text or explanation.
"""
        return prompt.strip()

    def select_move(self, board: Board, me: Player) -> int:
        # Ensure an API key is configured
        if not self.api_key:
            logger.warning("gemini_api_key_missing")
            return self._fallback(board, me)

        try:
            import google.generativeai as genai
        except Exception:
            logger.exception("gemini_sdk_not_available")
            return self._fallback(board, me)

        try:
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(self.model_name)

            prompt = self._build_prompt(board, me)
            response = model.generate_content(prompt)
            text = (getattr(response, "text", None) or "").strip()
            if not text:
                try:
                    if response.candidates and response.candidates[0].content.parts:
                        text = "".join(p.text for p in response.candidates[0].content.parts if getattr(p, "text", None))
                        text = text.strip()
                except Exception:
                    pass

            logger.info("gemini_raw_response", extra={"text": text[:200]})

            m = re.search(r"\b([1-9])\b", text)
            if not m:
                return self._fallback(board, me)
            pos = int(m.group(1))

            # Validate availability
            if pos not in board.available_positions():
                return self._fallback(board, me)

            return pos
        except Exception:
            logger.exception("gemini_inference_error")
            return self._fallback(board, me)
