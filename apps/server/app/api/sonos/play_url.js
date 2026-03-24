const { Sonos } = require("sonos");

async function run() {
  const sonosIp = process.env.SONOS_IP;
  const streamUrl = process.argv[2];

  if (!sonosIp) {
    console.error("Missing SONOS_IP environment variable");
    process.exit(1);
  }

  if (!streamUrl) {
    console.error("Missing stream URL argument");
    process.exit(1);
  }

  const device = new Sonos(sonosIp);

  try {
    await device.play(streamUrl);
    console.log(`Playing on speaker: ${streamUrl}`);
  } catch (err) {
    console.error(`Sonos playback failed: ${err?.message || String(err)}`);
    process.exit(1);
  }
}

run();
