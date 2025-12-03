from __future__ import annotations

import logging
import re
import json
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

    @staticmethod
    def _opponent(me: Player) -> Player:
        return Player.O if me == Player.X else Player.X

    @staticmethod
    def _find_immediate_win(board: Board, me: Player) -> Optional[int]:
        for pos in board.available_positions():
            try:
                if board.with_move(pos, me).winner() == me:
                    return pos
            except Exception:
                continue
        return None

    @staticmethod
    def _find_block(board: Board, me: Player) -> Optional[int]:
        opp = GeminiStrategy._opponent(me)
        for pos in board.available_positions():
            try:
                if board.with_move(pos, opp).winner() == opp:
                    return pos
            except Exception:
                continue
        return None

    def _build_prompt(self, board: Board, me: Player) -> str:
        avail = board.available_positions()
        # Use a strongly constrained instruction to elicit only JSON output
        prompt = (
            "You are a perfect Tic-Tac-Toe engine playing as '"
            + me.value
            + "'.\n"
            "Board is a 9-char string in NUMPAD order (rows: 7 8 9 / 4 5 6 / 1 2 3).\n"
            "Each char is 'x', 'o', or space for empty.\n\n"
            f"Board: \"{board.to_string()}\"\n"
            f"Available positions (numpad): {avail}\n\n"
            "Respond ONLY as JSON with this schema and nothing else:\n"
            "{\n  \"position\": <integer 1..9 that is in Available positions>\n}\n"
        )
        return prompt.strip()

    def select_move(self, board: Board, me: Player) -> int:
        # Ensure an API key is configured
        if not self.api_key:
            logger.warning("The Gemini API key is missing")
            return self._fallback(board, me)

        try:
            import google.generativeai as genai
        except Exception:
            logger.exception("gemini_sdk_not_available")
            return self._fallback(board, me)

        try:
            genai.configure(api_key=self.api_key)
            generation_config = {
                "temperature": 0.0,
                "top_p": 0.0,
                "top_k": 1,
                "max_output_tokens": 16,
                "response_mime_type": "application/json",
            }
            model = genai.GenerativeModel(self.model_name, generation_config=generation_config)

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

            pos: Optional[int] = None
            try:
                data = json.loads(text)
                if isinstance(data, dict) and isinstance(data.get("position"), int):
                    pos = int(data["position"])
            except Exception:
                pos = None

            if pos is None:
                m = re.search(r"\b([1-9])\b", text)
                if m:
                    pos = int(m.group(1))

            # Validate availability
            if pos is None or pos not in board.available_positions():
                return self._fallback(board, me)

            # Guardrails: don't miss immediate win; block immediate opponent win
            win = self._find_immediate_win(board, me)
            if win and win in board.available_positions() and win != pos:
                logger.info("gemini_guard_override_win", extra={"chosen": pos, "override": win})
                return win
            block = self._find_block(board, me)
            if block and block in board.available_positions() and block != pos:
                logger.info("gemini_guard_override_block", extra={"chosen": pos, "override": block})
                return block

            # Early-game preference: take center if available (strong heuristic)
            total_marks = board.to_string().count("x") + board.to_string().count("o")
            if total_marks <= 1 and 5 in board.available_positions() and pos != 5:
                logger.info("gemini_guard_prefer_center", extra={"chosen": pos, "override": 5})
                return 5

            return pos
        except Exception:
            logger.exception("gemini_inference_error")
            return self._fallback(board, me)
