import { apiFetch } from "./client";

const TOKEN_KEY = "token";

export interface RegisterBody {
  email: string;
  password: string;
}

export interface LoginBody {
  email: string;
  password: string;
}

export interface UserInfo {
  id: string;
  email: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export function getStoredToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function setStoredToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearStoredToken(): void {
  localStorage.removeItem(TOKEN_KEY);
}

export function register(body: RegisterBody): Promise<UserInfo> {
  return apiFetch<UserInfo>("/api/v1/users/register", {
    method: "POST",
    body: JSON.stringify(body),
  });
}

export function login(body: LoginBody): Promise<TokenResponse> {
  return apiFetch<TokenResponse>("/api/v1/users/login", {
    method: "POST",
    body: JSON.stringify(body),
  });
}

export function fetchMe(): Promise<UserInfo> {
  return apiFetch<UserInfo>("/api/v1/users/me");
}
