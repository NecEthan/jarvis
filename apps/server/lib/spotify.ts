import { config } from "@/lib/config";
import { AppError, ValidationError } from "@/lib/errors";

interface SpotifyDevice {
  id: string;
  name: string;
  is_active: boolean;
}

interface SpotifyTokenResponse {
  access_token?: string;
  refresh_token?: string;
  token_type?: string;
  expires_in?: number;
  error?: string;
  error_description?: string;
}

const SPOTIFY_ACCOUNTS_BASE = "https://accounts.spotify.com";
const SPOTIFY_AUTH_BASE = `${SPOTIFY_ACCOUNTS_BASE}/authorize`;
const SPOTIFY_TOKEN_URL = `${SPOTIFY_ACCOUNTS_BASE}/api/token`;
const SPOTIFY_SCOPES = [
  "user-read-playback-state",
  "user-modify-playback-state",
  "user-read-currently-playing",
];

function requireClientCredentials(): { clientId: string; clientSecret: string } {
  const clientId = config.spotifyClientId;
  const clientSecret = config.spotifyClientSecret;

  if (!clientId || !clientSecret) {
    throw new ValidationError(
      "Missing SPOTIFY_CLIENT_ID or SPOTIFY_CLIENT_SECRET"
    );
  }

  return { clientId, clientSecret };
}

function requireRedirectUri(): string {
  const redirectUri = config.spotifyRedirectUri;
  if (!redirectUri) {
    throw new ValidationError("Missing SPOTIFY_REDIRECT_URI");
  }
  return redirectUri;
}

function buildBasicAuthHeader(clientId: string, clientSecret: string): string {
  return `Basic ${Buffer.from(`${clientId}:${clientSecret}`).toString("base64")}`;
}

async function exchangeSpotifyToken(
  body: URLSearchParams,
  errorCode: string,
  errorPrefix: string
): Promise<SpotifyTokenResponse> {
  const { clientId, clientSecret } = requireClientCredentials();

  const response = await fetch(SPOTIFY_TOKEN_URL, {
    method: "POST",
    headers: {
      Authorization: buildBasicAuthHeader(clientId, clientSecret),
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body,
  });

  const data = (await response.json()) as SpotifyTokenResponse;
  if (!response.ok) {
    throw new AppError(
      `${errorPrefix}: ${data.error_description ?? data.error ?? response.statusText}`,
      502,
      errorCode
    );
  }

  return data;
}

export function getSpotifyAuthUrl(): string {
  const { clientId } = requireClientCredentials();
  const redirectUri = requireRedirectUri();

  const query = new URLSearchParams({
    response_type: "code",
    client_id: clientId,
    redirect_uri: redirectUri,
    scope: SPOTIFY_SCOPES.join(" "),
    show_dialog: "true",
  });

  return `${SPOTIFY_AUTH_BASE}?${query.toString()}`;
}

export async function exchangeSpotifyCode(code: string): Promise<SpotifyTokenResponse> {
  const redirectUri = requireRedirectUri();
  const body = new URLSearchParams({
    grant_type: "authorization_code",
    code,
    redirect_uri: redirectUri,
  });

  return exchangeSpotifyToken(
    body,
    "SPOTIFY_CALLBACK_EXCHANGE_FAILED",
    "Spotify callback exchange failed"
  );
}

function requireSpotifyEnv(): {
  clientId: string;
  clientSecret: string;
  refreshToken: string;
} {
  const clientId = config.spotifyClientId;
  const clientSecret = config.spotifyClientSecret;
  const refreshToken = config.spotifyRefreshToken;

  if (!clientId || !clientSecret || !refreshToken) {
    throw new ValidationError(
      "Missing SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, or SPOTIFY_REFRESH_TOKEN"
    );
  }

  return { clientId, clientSecret, refreshToken };
}

export async function getSpotifyAccessTokenFromRefreshToken(): Promise<string> {
  const { refreshToken } = requireSpotifyEnv();

  const body = new URLSearchParams({
    grant_type: "refresh_token",
    refresh_token: refreshToken,
  });

  const data = await exchangeSpotifyToken(
    body,
    "SPOTIFY_TOKEN_EXCHANGE_FAILED",
    "Spotify token exchange failed"
  );
  if (!data.access_token) {
    throw new AppError(
      "Spotify token exchange failed: missing access token",
      502,
      "SPOTIFY_TOKEN_EXCHANGE_FAILED"
    );
  }

  return data.access_token;
}

async function listDevices(accessToken: string): Promise<SpotifyDevice[]> {
  const response = await fetch("https://api.spotify.com/v1/me/player/devices", {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });

  const data = (await response.json()) as {
    devices?: SpotifyDevice[];
    error?: { message?: string };
  };

  if (!response.ok) {
    throw new AppError(
      `Spotify device list failed: ${data.error?.message ?? response.statusText}`,
      502,
      "SPOTIFY_DEVICE_LIST_FAILED"
    );
  }

  return data.devices ?? [];
}

function normalize(text: string): string {
  return text.trim().toLowerCase();
}

async function resolveDeviceId(
  accessToken: string,
  requestedDeviceId?: string,
  requestedDeviceName?: string
): Promise<string> {
  const devices = await listDevices(accessToken);
  if (!devices.length) {
    throw new AppError(
      "No Spotify Connect devices available. Open Spotify on Sonos first.",
      409,
      "SPOTIFY_NO_DEVICES"
    );
  }

  if (requestedDeviceId) {
    const byId = devices.find((d) => d.id === requestedDeviceId);
    if (byId) return byId.id;
  }

  if (requestedDeviceName) {
    const needle = normalize(requestedDeviceName);
    const byName = devices.find((d) => normalize(d.name) === needle);
    if (byName) return byName.id;

    const byContains = devices.find((d) => normalize(d.name).includes(needle));
    if (byContains) return byContains.id;
  }

  if (config.spotifyDeviceId) {
    const configured = devices.find((d) => d.id === config.spotifyDeviceId);
    if (configured) return configured.id;
  }

  if (config.sonosDeviceName) {
    const needle = normalize(config.sonosDeviceName);
    const configuredByName = devices.find((d) => normalize(d.name) === needle);
    if (configuredByName) return configuredByName.id;
  }

  const active = devices.find((d) => d.is_active);
  if (active) return active.id;

  return devices[0].id;
}

export async function playSpotifyUri(params: {
  spotifyUri: string;
  deviceId?: string;
  deviceName?: string;
}): Promise<{ deviceId: string }> {
  const accessToken = await getSpotifyAccessTokenFromRefreshToken();
  const deviceId = await resolveDeviceId(
    accessToken,
    params.deviceId,
    params.deviceName
  );

  const query = new URLSearchParams({ device_id: deviceId });
  const response = await fetch(
    `https://api.spotify.com/v1/me/player/play?${query.toString()}`,
    {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${accessToken}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ uris: [params.spotifyUri] }),
    }
  );

  if (!response.ok) {
    const text = await response.text();
    throw new AppError(
      `Spotify playback failed: ${text || response.statusText}`,
      502,
      "SPOTIFY_PLAYBACK_FAILED"
    );
  }

  return { deviceId };
}
