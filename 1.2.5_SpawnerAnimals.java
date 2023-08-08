/*
 * Decompiled with CFR 0.2.0 (FabricMC d28b102d).
 */

public final class SpawnerAnimals {
    private static HashMap eligibleChunksForSpawning = new HashMap();
    protected static final Class[] nightSpawnEntities = new Class[]{EntitySpider.class, EntityZombie.class, EntitySkeleton.class};

    protected static ChunkPosition getRandomSpawningPointInChunk(World world, int n, int n2) {
        Chunk chunk = world.getChunkFromChunkCoords(n, n2);
        int n3 = n * 16 + world.rand.nextInt(16);
        int n4 = world.rand.nextInt(chunk == null ? 128 : Math.max(128, chunk.getTopFilledSegment()));
        int n5 = n2 * 16 + world.rand.nextInt(16);
        return new ChunkPosition(n3, n4, n5);
    }

    public static final int performSpawning(World world, boolean bl, boolean bl2) {
        Object object;
        Object object2;
        int n;
        if (!bl && !bl2) {
            return 0;
        }
        eligibleChunksForSpawning.clear();
        for (n = 0; n < world.playerEntities.size(); ++n) {
            object2 = (EntityPlayer)world.playerEntities.get(n);
            int n2 = MathHelper.floor_double(((EntityPlayer)object2).posX / 16.0);
            int n3 = MathHelper.floor_double(((EntityPlayer)object2).posZ / 16.0);
            int n4 = 8;
            for (int i = -n4; i <= n4; ++i) {
                for (int j = -n4; j <= n4; ++j) {
                    boolean bl3 = i == -n4 || i == n4 || j == -n4 || j == n4;
                    object = new ChunkCoordIntPair(i + n2, j + n3);
                    if (!bl3) {
                        eligibleChunksForSpawning.put(object, false);
                        continue;
                    }
                    if (eligibleChunksForSpawning.containsKey(object)) continue;
                    eligibleChunksForSpawning.put(object, true);
                }
            }
        }
        n = 0;
        object2 = world.getSpawnPoint();
        for (EnumCreatureType enumCreatureType : EnumCreatureType.values()) {
            if (enumCreatureType.getPeacefulCreature() && !bl2 || !enumCreatureType.getPeacefulCreature() && !bl || world.countEntities(enumCreatureType.getCreatureClass()) > enumCreatureType.getMaxNumberOfCreature() * eligibleChunksForSpawning.size() / 256) continue;
            block6: for (ChunkCoordIntPair chunkCoordIntPair : eligibleChunksForSpawning.keySet()) {
                if (((Boolean)eligibleChunksForSpawning.get(chunkCoordIntPair)).booleanValue()) continue;
                object = SpawnerAnimals.getRandomSpawningPointInChunk(world, chunkCoordIntPair.chunkXPos, chunkCoordIntPair.chunkZPos);
                int n5 = ((ChunkPosition)object).x;
                int n6 = ((ChunkPosition)object).y;
                int n7 = ((ChunkPosition)object).z;
                if (world.isBlockNormalCube(n5, n6, n7) || world.getBlockMaterial(n5, n6, n7) != enumCreatureType.getCreatureMaterial()) continue;
                int n8 = 0;
                block7: for (int i = 0; i < 3; ++i) {
                    int n9 = n5;
                    int n10 = n6;
                    int n11 = n7;
                    int n12 = 6;
                    SpawnListEntry spawnListEntry = null;
                    for (int j = 0; j < 4; ++j) {
                        EntityLiving entityLiving;
                        float f;
                        float f2;
                        float f3;
                        float f4;
                        float f5;
                        float f6;
                        float f7;
                        if (!SpawnerAnimals.canCreatureTypeSpawnAtLocation(enumCreatureType, world, n9 += world.rand.nextInt(n12) - world.rand.nextInt(n12), n10 += world.rand.nextInt(1) - world.rand.nextInt(1), n11 += world.rand.nextInt(n12) - world.rand.nextInt(n12)) || world.getClosestPlayer(f7 = (float)n9 + 0.5f, f6 = (float)n10, f5 = (float)n11 + 0.5f, 24.0) != null || (f4 = (f3 = f7 - (float)((ChunkCoordinates)object2).posX) * f3 + (f2 = f6 - (float)((ChunkCoordinates)object2).posY) * f2 + (f = f5 - (float)((ChunkCoordinates)object2).posZ) * f) < 576.0f) continue;
                        if (spawnListEntry == null && (spawnListEntry = world.getRandomMob(enumCreatureType, n9, n10, n11)) == null) continue block7;
                        try {
                            entityLiving = (EntityLiving)spawnListEntry.entityClass.getConstructor(World.class).newInstance(world);
                        } catch (Exception exception) {
                            exception.printStackTrace();
                            return n;
                        }
                        entityLiving.setLocationAndAngles(f7, f6, f5, world.rand.nextFloat() * 360.0f, 0.0f);
                        if (entityLiving.getCanSpawnHere()) {
                            world.spawnEntityInWorld(entityLiving);
                            SpawnerAnimals.creatureSpecificInit(entityLiving, world, f7, f6, f5);
                            if (++n8 >= entityLiving.getMaxSpawnedInChunk()) continue block6;
                        }
                        n += n8;
                    }
                }
            }
        }
        return n;
    }

    public static boolean canCreatureTypeSpawnAtLocation(EnumCreatureType enumCreatureType, World world, int n, int n2, int n3) {
        if (enumCreatureType.getCreatureMaterial() == Material.water) {
            return world.getBlockMaterial(n, n2, n3).isLiquid() && !world.isBlockNormalCube(n, n2 + 1, n3);
        }
        int n4 = world.getBlockId(n, n2 - 1, n3);
        return Block.isNormalCube(n4) && n4 != Block.bedrock.blockID && !world.isBlockNormalCube(n, n2, n3) && !world.getBlockMaterial(n, n2, n3).isLiquid() && !world.isBlockNormalCube(n, n2 + 1, n3);
    }

    private static void creatureSpecificInit(EntityLiving entityLiving, World world, float f, float f2, float f3) {
        if (entityLiving instanceof EntitySpider && world.rand.nextInt(100) == 0) {
            EntitySkeleton entitySkeleton = new EntitySkeleton(world);
            entitySkeleton.setLocationAndAngles(f, f2, f3, entityLiving.rotationYaw, 0.0f);
            world.spawnEntityInWorld(entitySkeleton);
            entitySkeleton.mountEntity(entityLiving);
        } else if (entityLiving instanceof EntitySheep) {
            ((EntitySheep)entityLiving).setFleeceColor(EntitySheep.getRandomFleeceColor(world.rand));
        } else if (entityLiving instanceof EntityOcelot && world.rand.nextInt(7) == 0) {
            for (int i = 0; i < 2; ++i) {
                EntityOcelot entityOcelot = new EntityOcelot(world);
                entityOcelot.setLocationAndAngles(f, f2, f3, entityLiving.rotationYaw, 0.0f);
                entityOcelot.setGrowingAge(-24000);
                world.spawnEntityInWorld(entityOcelot);
            }
        }
    }

    public static void performWorldGenSpawning(World world, BiomeGenBase biomeGenBase, int n, int n2, int n3, int n4, Random random) {
        List list = biomeGenBase.getSpawnableList(EnumCreatureType.creature);
        if (list.isEmpty()) {
            return;
        }
        while (random.nextFloat() < biomeGenBase.getSpawningChance()) {
            SpawnListEntry spawnListEntry = (SpawnListEntry)WeightedRandom.getRandomItem(world.rand, list);
            int n5 = spawnListEntry.minGroupCount + random.nextInt(1 + spawnListEntry.maxGroupCount - spawnListEntry.minGroupCount);
            int n6 = n + random.nextInt(n3);
            int n7 = n2 + random.nextInt(n4);
            int n8 = n6;
            int n9 = n7;
            for (int i = 0; i < n5; ++i) {
                boolean bl = false;
                for (int j = 0; !bl && j < 4; ++j) {
                    int n10 = world.getTopSolidOrLiquidBlock(n6, n7);
                    if (SpawnerAnimals.canCreatureTypeSpawnAtLocation(EnumCreatureType.creature, world, n6, n10, n7)) {
                        EntityLiving entityLiving;
                        float f = (float)n6 + 0.5f;
                        float f2 = n10;
                        float f3 = (float)n7 + 0.5f;
                        try {
                            entityLiving = (EntityLiving)spawnListEntry.entityClass.getConstructor(World.class).newInstance(world);
                        } catch (Exception exception) {
                            exception.printStackTrace();
                            continue;
                        }
                        entityLiving.setLocationAndAngles(f, f2, f3, random.nextFloat() * 360.0f, 0.0f);
                        world.spawnEntityInWorld(entityLiving);
                        SpawnerAnimals.creatureSpecificInit(entityLiving, world, f, f2, f3);
                        bl = true;
                    }
                    n6 += random.nextInt(5) - random.nextInt(5);
                    n7 += random.nextInt(5) - random.nextInt(5);
                    while (n6 < n || n6 >= n + n3 || n7 < n2 || n7 >= n2 + n3) {
                        n6 = n8 + random.nextInt(5) - random.nextInt(5);
                        n7 = n9 + random.nextInt(5) - random.nextInt(5);
                    }
                }
            }
        }
    }
}