import random
from dataclasses import dataclass
from enum import Enum, auto

# def getRandomSpawningPointInChunk(x_offset, z_offset):
#     # Chunks have a width and length of 16
#     x = x_offset + random.randrange(16)
#     # The world is only 128 blocks high in Beta 1.7.3
#     y = random.randrange(128)
#     z = z_offset + random.randrange(16)
#     return ChunkPosition(x, y, z)


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
        if mobType == MobType.Monster and not spawnMonsters:
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

            # Get random spawnpoint in chunk
            # Chunks have a width and length of 16
            x = chunkCoord.x * 16 + random.randrange(16)
            # The world is only 128 blocks high in Beta 1.7.3
            y = random.randrange(128)
            z = chunkCoord.z * 16 + random.randrange(16)

            blockType = getBlockType(x, y, z)

            if blockType == BlockType.Normal:
                continue

            if blockType == BlockType.Air and mobType == MobType.WaterCreature:
                continue

            if blockType == BlockType.Water and mobType != MobType.WaterCreature:
                continue

            n10 = 0

            x_copy = x
            y_copy = y
            z_copy = z

            for i in range(3):
                x = x_copy
                y = y_copy
                z = z_copy

                unknown = 6

                for j in range(4):

                    if not SpawnerAnimals.canCreatureTypeSpawnAtLocation(enumCreatureType, world, n11 += world.rand.nextInt(n14) - world.rand.nextInt(n14), n12 += world.rand.nextInt(1) - world.rand.nextInt(1), n13 += world.rand.nextInt(n14) - world.rand.nextInt(n14)):
                        continue

                    # if (!SpawnerAnimals.canCreatureTypeSpawnAtLocation(enumCreatureType, world, n11 += world.rand.nextInt(n14) - world.rand.nextInt(n14), n12 += world.rand.nextInt(1) - world.rand.nextInt(1), n13 += world.rand.nextInt(n14) - world.rand.nextInt(n14)) || world.getClosestPlayer(f7 = (float)n11 + 0.5f, f6 = (float)n12, f5 = (float)n13 + 0.5f, 24.0) != null || (f4 = (f3 = f7 - (float)((ChunkCoordinates)object).x) * f3 + (f2 = f6 - (float)((ChunkCoordinates)object).y) * f2 + (f = f5 - (float)((ChunkCoordinates)object).z) * f) < 576.0f) continue;

                    # try {
                    #     entityLiving = (EntityLiving)spawnListEntry2.entityClass.getConstructor(World.class).newInstance(world);
                    # } catch (Exception exception) {
                    #     exception.printStackTrace();
                    #     return n;
                    # }

                    # entityLiving.setLocationAndAngles(f7, f6, f5, world.rand.nextFloat() * 360.0f, 0.0f);
                    
                    # if (entityLiving.getCanSpawnHere()) {
                    #     world.entityJoinedWorld(entityLiving);
                    #     SpawnerAnimals.creatureSpecificInit(entityLiving, world, f7, f6, f5);
                    #     if (++n10 >= entityLiving.getMaxSpawnedInChunk()) continue block6;
                    # }
                    
                    # n += n10;


def getSpawnPoint():
    pass


@dataclass
class ChunkCoord:
    x: int
    y: int


class MobType(Enum):
    Monster = auto()
    Creature = auto()
    WaterCreature = auto()


def getMobTypeCount(mobType):
    pass


def getMaxMobTypeCount(mobType):
    if mobType == MobType.Monster:
        return 70
    elif mobType == MobType.Creature:
        return 15
    elif mobType == MobType.WaterCreature:
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
    if mobType == MobType.Monster:
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
    elif mobType == MobType.Creature:
        mobs = [
            MobWithWeight(MobName.Sheep, 12),
            MobWithWeight(MobName.Pig, 10),
            MobWithWeight(MobName.Chicken, 10),
            MobWithWeight(MobName.Cow, 8),
        ]
        if biome == Biome.Forest or biome == Biome.Taiga:
            mobs.append(MobWithWeight(MobName.Wolf, 2))
        return mobs
    elif mobType == MobType.WaterCreature:
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


def getBlockType(x, y, z):
    pass


class BlockType(Enum):
    Normal = auto()
    Air = auto()
    Water = auto()
