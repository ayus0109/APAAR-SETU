export const API_BASE = (
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000"
).replace(/\/+$/, "");

const ACCESS_TOKEN_KEY = "apaar_access_token";

export function saveAccessToken(token: string): void {
  window.localStorage.setItem(ACCESS_TOKEN_KEY, token);
}

export function clearAccessToken(): void {
  window.localStorage.removeItem(ACCESS_TOKEN_KEY);
}

export async function apiFetch(
  input: RequestInfo | URL,
  init: RequestInit = {},
): Promise<Response> {
  const headers = new Headers(init.headers);
  const token =
    typeof window === "undefined"
      ? null
      : window.localStorage.getItem(ACCESS_TOKEN_KEY);

  if (token) {
    headers.set("Authorization", "Bearer " + token);
  }

  const response = await fetch(input, { ...init, headers });
  if (response.status === 401 && typeof window !== "undefined") {
    clearAccessToken();
  }
  return response;
}
