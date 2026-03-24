// Centralized env config — throws at startup if required vars are missing

function requireEnv(key: string): string {
  const value = process.env[key];
  if (!value) throw new Error(`Missing required environment variable: ${key}`);
  return value;
}

function optionalEnv(key: string, fallback: string): string {
  return process.env[key] ?? fallback;
}

export const config = {
  langGraphApiUrl: optionalEnv("LANGGRAPH_API_URL", "http://localhost:8000"),
  sonosIp: optionalEnv("SONOS_IP", ""),
  spotifyClientId: optionalEnv("SPOTIFY_CLIENT_ID", ""),
  spotifyClientSecret: optionalEnv("SPOTIFY_CLIENT_SECRET", ""),
  spotifyRefreshToken: optionalEnv("SPOTIFY_REFRESH_TOKEN", ""),
  spotifyRedirectUri: optionalEnv("SPOTIFY_REDIRECT_URI", ""),
  spotifyDeviceId: optionalEnv("SPOTIFY_DEVICE_ID", ""),
  sonosDeviceName: optionalEnv("SONOS_DEVICE_NAME", ""),
  // TODO: add provider keys when implementing features
  // anthropicApiKey: requireEnv("ANTHROPIC_API_KEY"),
} as const;
