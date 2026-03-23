// play-test.js
const { Sonos } = require("sonos");

const device = new Sonos("192.168.68.114");

async function run() {
  try {
    await device.play(
      "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
    );
    console.log("Playing on speaker");
  } catch (e) {
    console.error(e);
  }
}

run();