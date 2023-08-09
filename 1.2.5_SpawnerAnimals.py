import random
from dataclasses import dataclass
from enum import Enum, auto


def performSpawning(players, spawnHostileMobs, spawnPeacefulMobs):
    eligibleChunksForSpawning = set()

    # Add the chunks surrounding every player to eligibleChunksForSpawning
    # A radius of 8 chunks are added, so 17^2 or 289 chunks per player
    for player in players:
        chunk_x = player.x // 16
        chunk_z = player.z // 16

        radius = 8
        for chunk_x_offset in range(-radius, radius + 1):
            for chunk_z_offset in range(-radius, radius + 1):
                neighbor_chunk_x = chunk_x + chunk_x_offset
                neighbor_chunk_z = chunk_z + chunk_z_offset

                eligibleChunksForSpawning.add(
                    ChunkCoord(neighbor_chunk_x, neighbor_chunk_z)
                )

    spawnPoint = getSpawnPoint()

    # Spawn Hostile mobs, then Passive mobs, then Squid
    for mobType in MobType:
        # Don't spawn Hostile mobs if spawnHostileMobs is False
        if mobType == MobType.Hostile and not spawnHostileMobs:
            continue

        # Don't spawn Hostile mobs if spawnHostileMobs is False
        # spawnPeacefulMobs is only True every 400 ticks
        if (
            mobType == MobType.Passive or mobType == MobType.Squid
        ) and not spawnPeacefulMobs:
            continue

        # In singleplayer this will always be 1!
        # 256 is roughly the 289 chunks that get added per player,
        # with 289 assuming all players are standing far away from each other
        roughlyPlayerCount = len(eligibleChunksForSpawning) // 256

        if getMobTypeCount(mobType) > (
            getMaxMobTypeCount(mobType) * roughlyPlayerCount
        ):
            continue

        for chunkCoord in eligibleChunksForSpawning:
            performSpawningNearChunk(chunkCoord, mobType, spawnPoint)


def performSpawningNearChunk(chunkCoord, mobType, spawnPoint):
    biome = getBiomeAtChunk(chunkCoord)
    spawnableMobs = getSpawnableMobs(biome, mobType)

    # Get random spawnpoint in chunk
    # Chunks have a width and length of 16
    pack_center_x = chunkCoord.x * 16 + random.randrange(16)

    chunk = getChunkFromChunkCoord(chunkCoord)

    # The original source code really uses max(), not min(),
    # so the spawn rate of a single platform at Y=1 isn't higher than one at Y=128
    # getHighestBlockYInChunk(chunk) can return up to 255,
    # so to maximize spawns in your mob farms you should remove any blocks above Y=128
    pack_center_y = random.randrange(max(128, getHighestBlockYInChunk(chunk)))

    pack_center_z = chunkCoord.z * 16 + random.randrange(16)

    blockType = getBlockType(pack_center_x, pack_center_y, pack_center_z)

    # Can't spawn inside of a normal block
    if blockType == BlockType.Normal:
        return

    # Squid can't spawn in air
    if blockType == BlockType.Air and mobType == MobType.Squid:
        return

    # Other mobs can't spawn in water
    if blockType == BlockType.Water and mobType != MobType.Squid:
        return

    spawnedNearChunk = 0

    # Do at most 3 mob pack spawn attempts
    for _ in range(3):
        x = pack_center_x
        y = pack_center_y
        z = pack_center_z

        # Up to 3 different mob kind packs can spawn per chunk, per tick
        mobName = getRandomMobName(spawnableMobs)

        # Spawn at most 4 mobs per pack
        for _ in range(4):
            # Running this 100k times using offset_distribution.py gives this pyramid shape of occurrences, where 0 is the most likely:
            # {-5: 2813, -4: 5607, -3: 8282, -2: 11174, -1: 13888, 0: 16578, 1: 13841, 2: 11116, 3: 8295, 4: 5614, 5: 2792}
            # This means that 2 mobs from a pack of 4 mobs can spawn up to 5 * (4 - 1) = 15 blocks apart on the X axis from one another
            maxOffset = 6
            x += random.randrange(maxOffset) - random.randrange(maxOffset)
            z += random.randrange(maxOffset) - random.randrange(maxOffset)

            # If mobType is Squid, this function returns true if (x, y, z) is water/lava, AND (x, y+1, z) is not a normal block
            # Otherwise, this function returns true if (x, y-1, z) is a normal block, AND (x, y, z) isn't a normal block/water/lava,
            # AND (x, y+1, z) isn't a normal block
            if canMobTypeSpawnAtLocation(mobType, x, y, z):
                mobCenterX = x + 0.5
                mobCenterZ = z + 0.5

                # If the mob would be spawned within 24 blocks of any player
                if getClosestPlayer(mobCenterX, y, mobCenterZ, 24) != None:
                    continue

                if isTooCloseToSpawn(mobCenterX, y, mobCenterZ, spawnPoint):
                    continue

                mobInstance = createMob(mobName)

                # Yaw between 0 and 360, pitch of 0
                setLocationAndAngles(
                    mobInstance, mobCenterX, y, mobCenterZ, random.uniform(0, 360), 0
                )

                # Animals require spawning on grass, and spawning inside of air with light level > 8
                # For ghasts, this function has a has 1 in 20 chance to return True
                # There are other kinds of checks you'll have to decompile the code yourself for
                if canSpawnHere(mobInstance):
                    spawnedNearChunk += 1

                    spawnMob(mobInstance, mobCenterX, y, mobCenterZ)

                    # This check makes sure only 1 ghast can be spawned per tick, for each chunk
                    # It does not take into account that mobs can be spawned outside of the original chunk!
                    if spawnedNearChunk >= getMaxSpawnedInChunk(mobName):
                        return


def getSpawnPoint():
    pass


@dataclass
class ChunkCoord:
    x: int
    y: int


class MobType(Enum):
    Hostile = auto()
    Passive = auto()
    Squid = auto()


def getMobTypeCount(mobType):
    pass


def getMaxMobTypeCount(mobType):
    if mobType == MobType.Hostile:
        return 70
    elif mobType == MobType.Passive:
        return 15
    elif mobType == MobType.Squid:
        return 5
    else:
        raise Unreachable()


class Unreachable(Exception):
    pass


def getBiomeAtChunk(chunkCoord):
    pass


class Biome(Enum):
    Desert = auto()
    Forest = auto()
    Nether = auto()
    End = auto()
    Rainforest = auto()
    Swamp = auto()
    Taiga = auto()
    Jungle = auto()
    MushroomIsland = auto()
    NetherBridge = auto()


def getSpawnableMobs(biome, mobType):
    if biome == Biome.MushroomIsland:
        if mobType == MobType.Passive:
            return [
                MobWithWeight(MobName.Mooshroom, 8),
            ]
        else:
            return []
    elif biome == Biome.Nether:
        if mobType == MobType.Hostile:
            return [
                MobWithWeight(MobName.Ghast, 50),
                MobWithWeight(MobName.ZombiePigman, 100),
                MobWithWeight(MobName.MagmaCube, 1),
            ]
        else:
            return []
    elif biome == Biome.NetherBridge:
        if mobType == MobType.Hostile:
            return [
                MobWithWeight(MobName.Blaze, 10),
                MobWithWeight(MobName.ZombiePigman, 10),
                MobWithWeight(MobName.MagmaCube, 3),
            ]
        else:
            return []
    elif biome == Biome.End:
        if mobType == MobType.Hostile:
            return [
                MobWithWeight(MobName.Enderman, 10),
            ]
        else:
            return []

    if mobType == MobType.Hostile:
        mobs = [
            MobWithWeight(MobName.Spider, 10),
            MobWithWeight(MobName.Zombie, 10),
            MobWithWeight(MobName.Skeleton, 10),
            MobWithWeight(MobName.Creeper, 10),
            MobWithWeight(MobName.Slime, 10),
            MobWithWeight(MobName.Enderman, 1),
        ]

        if biome == Biome.Jungle:
            mobs.append(MobWithWeight(MobName.Ocelot, 2))

        return mobs
    elif mobType == MobType.Passive:
        mobs = [
            MobWithWeight(MobName.Sheep, 12),
            MobWithWeight(MobName.Pig, 10),
            MobWithWeight(MobName.Chicken, 10),
            MobWithWeight(MobName.Cow, 8),
        ]

        if biome == Biome.Forest:
            mobs.append(MobWithWeight(MobName.Wolf, 5))
        elif biome == Biome.Taiga:
            mobs.append(MobWithWeight(MobName.Wolf, 8))
        elif biome == Biome.Jungle:
            mobs.append(MobWithWeight(MobName.Chicken, 10))

        return mobs
    elif mobType == MobType.Squid:
        return [
            MobWithWeight(MobName.Squid, 10),
        ]
    else:
        raise Unreachable()


class MobName(Enum):
    Spider = auto()
    Zombie = auto()
    Skeleton = auto()
    Creeper = auto()
    Slime = auto()
    Enderman = auto()
    Sheep = auto()
    Pig = auto()
    Chicken = auto()
    Cow = auto()
    Squid = auto()
    Wolf = auto()
    Ghast = auto()
    ZombiePigman = auto()
    MagmaCube = auto()
    Mooshroom = auto()
    Blaze = auto()


@dataclass
class MobWithWeight:
    mobName: MobName
    weight: int


def getRandomMobName(mobs):
    weight = 0
    for mob in mobs:
        weight += mob.weight

    randomWeight = random.randrange(weight)

    for mob in mobs:
        randomWeight -= mob.weight

        if randomWeight >= 0:
            continue

        return mob.modName

    return mobs[0].modName


def getChunkFromChunkCoord(chunkCoord):
    pass


def getHighestBlockYInChunk(chunk):
    pass


def getBlockType(x, y, z):
    pass


class BlockType(Enum):
    Normal = auto()
    Air = auto()
    Water = auto()


def canMobTypeSpawnAtLocation(mobType, x, y, z):
    pass


def getClosestPlayer(x, y, z, maxPlayerDistance):
    pass


def isTooCloseToSpawn(mobCenterX, y, mobCenterZ, spawnPoint):
    spawnDiffX = mobCenterX - spawnPoint.x
    spawnDiffY = y - spawnPoint.y
    spawnDiffZ = mobCenterZ - spawnPoint.z

    squaredDistanceToSpawn = (
        spawnDiffX * spawnDiffX + spawnDiffY * spawnDiffY + spawnDiffZ * spawnDiffZ
    )

    # sqrt(576) is 24, so this makes sure mobs don't spawn within 24 blocks of the world spawn
    return squaredDistanceToSpawn < 576


def createMob(mobName):
    pass


def setLocationAndAngles(mobInstance, x, y, z, yaw, pitch):
    pass


def canSpawnHere(mobInstance):
    pass


def spawnMob(mobInstance):
    pass


def mobSpecificInit(mobInstance, x, y, z):
    pass


def getMaxSpawnedInChunk(mobName):
    if mobName == MobName.Ghast:
        return 1
    elif mobName == MobName.Wolf:
        return 8
    else:  # Assuming everything else inherits EntityLiving
        return 4
