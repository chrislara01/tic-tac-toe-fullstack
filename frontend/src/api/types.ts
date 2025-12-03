export type Player = 'x' | 'o';
export type Difficulty = 'easy' | 'medium' | 'hard';
export type GameStatus = 'in_progress' | 'x_won' | 'o_won' | 'draw';

export interface CreateGameRequest {
  difficulty: Difficulty;
  first_player: 'human' | 'computer';
  human_symbol: Player;
}

export interface GameRead {
  id: string;
  board: string; // 9-char string in numpad order "789456123", with 'x' | 'o' | ' '
  next_player: Player;
  difficulty: Difficulty;
  status: GameStatus;
  human_symbol: Player;
  computer_symbol: Player;
  moves: number[];
  created_at: string;
  updated_at: string;
}

export type CreateGameResponse = GameRead;

export interface MoveRequest {
  position: number; // 1..9 in numpad layout
}

export interface MoveResponse extends GameRead {
  ai_move?: number | null;
}

// Mapping index (0..8) -> numpad position (1..9) according to backend encoding
export const INDEX_TO_POSITION: number[] = [7, 8, 9, 4, 5, 6, 1, 2, 3];
export const POSITION_TO_INDEX: Record<number, number> = {
  7: 0,
  8: 1,
  9: 2,
  4: 3,
  5: 4,
  6: 5,
  1: 6,
  2: 7,
  3: 8,
};
