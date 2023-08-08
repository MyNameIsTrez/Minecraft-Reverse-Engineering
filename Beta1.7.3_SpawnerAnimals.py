import random
from dataclasses import dataclass
from enum import Enum, auto


def performSpawning(players, spawnMonsters):
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

    spawned = 0
    spawnPoint = getSpawnPoint()

    for mobType in MobType:
        if mobType == MobType.MONSTER and not spawnMonsters:
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
            biome = getBiomeAtChunk(chunkCoord)
            spawnableMobs = getSpawnableMobs(biome, mobType)
            mob = getRandomMob(spawnableMobs)


def getRandomSpawningPointInChunk(world, x_offset, z_offset):
    # Chunks have a width and length of 16
    x = x_offset + random.randrange(16)
    # The world is only 128 blocks high in Beta 1.7.3
    y = random.randrange(128)
    z = z_offset + random.randrange(16)
    return ChunkPosition(x, y, z)


class ChunkCoord:
    pass


class MobType(Enum):
    MONSTER = auto()
    CREATURE = auto()
    WATER_CREATURE = auto()


def getMobTypeCount(mobType):
    pass


def getMaxMobTypeCount(mobType):
    if mobType == MobType.MONSTER:
        return 70
    elif mobType == MobType.CREATURE:
        return 15
    elif mobType == MobType.WATER_CREATURE:
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
    Rainforest = auto()
    Swamp = auto()
    Taiga = auto()


def getSpawnableMobs(biome, mobType):
    if mobType == MobType.MONSTER:
        mobs = [
            MobWithWeight(MobName.Spider, 10),
            MobWithWeight(MobName.Zombie, 10),
            MobWithWeight(MobName.Skeleton, 10),
            MobWithWeight(MobName.Creeper, 10),
            MobWithWeight(MobName.Slime, 10),
        ]
        if biome == Biome.Nether:
            mobs.append(MobWithWeight(MobName.Ghast, 10))
            mobs.append(MobWithWeight(MobName.ZombiePigman, 10))
        return mobs
    elif mobType == MobType.CREATURE:
        mobs = [
            MobWithWeight(MobName.Sheep, 12),
            MobWithWeight(MobName.Pig, 10),
            MobWithWeight(MobName.Chicken, 10),
            MobWithWeight(MobName.Cow, 8),
        ]
        if biome == Biome.Forest or biome == Biome.Taiga:
            mobs.append(MobWithWeight(MobName.Wolf, 2))
        return mobs
    elif mobType == MobType.WATER_CREATURE:
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
    Sheep = auto()
    Pig = auto()
    Chicken = auto()
    Cow = auto()
    Squid = auto()
    Wolf = auto()
    Ghast = auto()
    ZombiePigman = auto()


@dataclass
class MobWithWeight:
    mobName: MobName
    weight: int


def getRandomMob(mobs):
    weight = 0
    for mob in mobs:
        weight += mob.weight

    randomWeight = random.randrange(weight)

    for mob in mobs:
        randomWeight -= mob.weight

        if randomWeight >= 0:
            continue

        return mob

    return mobs[0]
