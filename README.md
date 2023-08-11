# Minecraft-Reverse-Engineering

Rewriting parts of Minecraft in Python to understand the game better.

# Facts shared by 1.7.3 and 1.2.5
- A chunk is 16 blocks wide and long
- Mobs can't spawn within 24 blocks of any player or the world spawn
- For roughly every player, there can only be 70 hostile mobs, 15 passive mobs, and 5 squid until they stop spawning
- First hostile mobs, then passive mobs, then squid spawn
- 4 mob spawn attempts happen per pack
- For every mob in the pack, a random offset of -5 to 5 blocks gets applied to their X and Z separately, where an offset of 0 is six times more likely than 5. This means the last mob in the pack can spawn up to 5 blocks * 4 mobs per pack = 20 blocks away from the pack's center X
- This means the name of the getMaxSpawnedInChunk() method that returns 1 for ghasts, 8 for wolfs, and 4 for any other mob type is misleading, since those max mob counts spawnable by a chunk can be spread over several chunks

# Beta 1.7.3 specific facts
- A chunk is 128 blocks tall
- Mobs spawn in every 17x17 chunk centered on every player
- Hostile mobs, passive mobs, and squid spawn every game tick (20 game ticks in a second)
- Mobs attempt to spawn in a random block for every chunk. Digging out a perimeter won't give crazy spawn rates: just light up caves/remove grass/remove water
- 3 mob pack spawn attempts, with the same mob name, are made per chunk

# Release 1.2.5 specific facts
- A chunk is 256 blocks tall
- Mobs spawn in every 15x15 chunk centered on every player
- Hostile mobs spawn every game tick, whereas passive mobs and squid spawn every 400 game ticks (20 game ticks in a second)
- Mobs attempt to spawn in a random block for every chunk up to Y=128, but if you have any opaque (non-transparent) blocks above Y=128, mobs will be able to spawn up to that height. This means you should remove any opaque blocks above Y=128 in your mob farm chunks, and also the chunks directly next to them due to the mob offset explained in the shared section. Digging out a perimeter won't give crazy spawn rates: just light up caves/remove grass/remove water
- 3 mob pack spawn attempts, with possibly different mob names, are made per chunk
