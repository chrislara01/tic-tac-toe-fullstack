import type {
  CreateGameRequest,
  CreateGameResponse,
  MoveRequest,
  MoveResponse,
} from '@/api/types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000';

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers || {}),
    },
    ...init,
  });
  const text = await res.text();
  let data: any = undefined;
  try {
    data = text ? JSON.parse(text) : undefined;
  } catch (_) {
    // ignore
  }
  if (!res.ok) {
    const detail = (data && (data.detail || data.error)) || res.statusText;
    throw new Error(detail);
  }
  return data as T;
}

export async function createGame(payload: CreateGameRequest): Promise<CreateGameResponse> {
  return request<CreateGameResponse>('/games', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function getGame(gameId: string): Promise<CreateGameResponse> {
  return request<CreateGameResponse>(`/games/${gameId}`);
}

export async function postMove(gameId: string, payload: MoveRequest): Promise<MoveResponse> {
  return request<MoveResponse>(`/games/${gameId}/moves`, {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}
