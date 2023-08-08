/*
 * Decompiled with CFR 0.2.0 (FabricMC d28b102d).
 */

public final class SpawnerAnimals {
    private static Set eligibleChunksForSpawning = new HashSet();
    protected static final Class[] nightSpawnEntities = new Class[]{EntitySpider.class, EntityZombie.class, EntitySkeleton.class};

    protected static ChunkPosition getRandomSpawningPointInChunk(World world, int n, int n2) {
        int n3 = n + world.rand.nextInt(16);
        int n4 = world.rand.nextInt(128);
        int n5 = n2 + world.rand.nextInt(16);
        return new ChunkPosition(n3, n4, n5);
    }

    public static final int performSpawning(World world, boolean bl, boolean bl2) {
        Object object;
        int n;
        if (!bl && !bl2) {
            return 0;
        }
        eligibleChunksForSpawning.clear();
        for (n = 0; n < world.playerEntities.size(); ++n) {
            object = (EntityPlayer)world.playerEntities.get(n);
            int n2 = MathHelper.floor_double(((EntityPlayer)object).posX / 16.0);
            int n3 = MathHelper.floor_double(((EntityPlayer)object).posZ / 16.0);
            int n4 = 8;
            for (int i = -n4; i <= n4; ++i) {
                for (int j = -n4; j <= n4; ++j) {
                    eligibleChunksForSpawning.add(new ChunkCoordIntPair(i + n2, j + n3));
                }
            }
        }
        n = 0;
        object = world.getSpawnPoint();
        for (EnumCreatureType enumCreatureType : EnumCreatureType.values()) {
            if ((enumCreatureType.getPeacefulCreature() && !bl2) || (!enumCreatureType.getPeacefulCreature() && !bl) || (world.countEntities(enumCreatureType.getCreatureClass()) > (enumCreatureType.getMaxNumberOfCreature() * eligibleChunksForSpawning.size() / 256))) continue;
            block6: for (ChunkCoordIntPair chunkCoordIntPair : eligibleChunksForSpawning) {
                SpawnListEntry spawnListEntry2;
                BiomeGenBase biomeGenBase = world.getWorldChunkManager().getBiomeGenAtChunkCoord(chunkCoordIntPair);
                List list = biomeGenBase.getSpawnableList(enumCreatureType);
                if (list == null || list.isEmpty()) continue;
                int n5 = 0;
                for (SpawnListEntry spawnListEntry2 : list) {
                    n5 += spawnListEntry2.spawnRarityRate;
                }
                int n6 = world.rand.nextInt(n5);
                spawnListEntry2 = (SpawnListEntry)list.get(0);
                for (SpawnListEntry spawnListEntry3 : list) {
                    if ((n6 -= spawnListEntry3.spawnRarityRate) >= 0) continue;
                    spawnListEntry2 = spawnListEntry3;
                    break;
                }
                ChunkPosition chunkPosition = SpawnerAnimals.getRandomSpawningPointInChunk(world, chunkCoordIntPair.chunkXPos * 16, chunkCoordIntPair.chunkZPos * 16);
                int n7 = chunkPosition.x;
                int n8 = chunkPosition.y;
                int n9 = chunkPosition.z;
                if (world.isBlockNormalCube(n7, n8, n9) || world.getBlockMaterial(n7, n8, n9) != enumCreatureType.getCreatureMaterial()) continue;
                int n10 = 0;
                for (int i = 0; i < 3; ++i) {
                    int n11 = n7;
                    int n12 = n8;
                    int n13 = n9;
                    int n14 = 6;
                    for (int j = 0; j < 4; ++j) {
                        EntityLiving entityLiving;
                        float f;
                        float f2;
                        float f3;
                        float f4;
                        float f5;
                        float f6;
                        float f7;
                        if (!SpawnerAnimals.canCreatureTypeSpawnAtLocation(enumCreatureType, world, n11 += world.rand.nextInt(n14) - world.rand.nextInt(n14), n12 += world.rand.nextInt(1) - world.rand.nextInt(1), n13 += world.rand.nextInt(n14) - world.rand.nextInt(n14)) || world.getClosestPlayer(f7 = (float)n11 + 0.5f, f6 = (float)n12, f5 = (float)n13 + 0.5f, 24.0) != null || (f4 = (f3 = f7 - (float)((ChunkCoordinates)object).x) * f3 + (f2 = f6 - (float)((ChunkCoordinates)object).y) * f2 + (f = f5 - (float)((ChunkCoordinates)object).z) * f) < 576.0f) continue;
                        try {
                            entityLiving = (EntityLiving)spawnListEntry2.entityClass.getConstructor(World.class).newInstance(world);
                        } catch (Exception exception) {
                            exception.printStackTrace();
                            return n;
                        }
                        entityLiving.setLocationAndAngles(f7, f6, f5, world.rand.nextFloat() * 360.0f, 0.0f);
                        if (entityLiving.getCanSpawnHere()) {
                            world.entityJoinedWorld(entityLiving);
                            SpawnerAnimals.creatureSpecificInit(entityLiving, world, f7, f6, f5);
                            if (++n10 >= entityLiving.getMaxSpawnedInChunk()) continue block6;
                        }
                        n += n10;
                    }
                }
            }
        }
        return n;
    }

    private static boolean canCreatureTypeSpawnAtLocation(EnumCreatureType enumCreatureType, World world, int n, int n2, int n3) {
        if (enumCreatureType.getCreatureMaterial() == Material.water) {
            return world.getBlockMaterial(n, n2, n3).getIsLiquid() && !world.isBlockNormalCube(n, n2 + 1, n3);
        }
        return world.isBlockNormalCube(n, n2 - 1, n3) && !world.isBlockNormalCube(n, n2, n3) && !world.getBlockMaterial(n, n2, n3).getIsLiquid() && !world.isBlockNormalCube(n, n2 + 1, n3);
    }

    private static void creatureSpecificInit(EntityLiving entityLiving, World world, float f, float f2, float f3) {
        if (entityLiving instanceof EntitySpider && world.rand.nextInt(100) == 0) {
            EntitySkeleton entitySkeleton = new EntitySkeleton(world);
            entitySkeleton.setLocationAndAngles(f, f2, f3, entityLiving.rotationYaw, 0.0f);
            world.entityJoinedWorld(entitySkeleton);
            entitySkeleton.mountEntity(entityLiving);
        } else if (entityLiving instanceof EntitySheep) {
            ((EntitySheep)entityLiving).setFleeceColor(EntitySheep.getRandomFleeceColor(world.rand));
        }
    }

    public static boolean performSleepSpawning(World world, List list) {
        boolean bl = false;
        Pathfinder pathfinder = new Pathfinder(world);
        for (EntityPlayer entityPlayer : list) {
            Class[] classArray = nightSpawnEntities;
            if (classArray == null || classArray.length == 0) continue;
            boolean bl2 = false;
            for (int i = 0; i < 20 && !bl2; ++i) {
                PathEntity pathEntity;
                EntityLiving entityLiving;
                int n;
                int n2 = MathHelper.floor_double(entityPlayer.posX) + world.rand.nextInt(32) - world.rand.nextInt(32);
                int n3 = MathHelper.floor_double(entityPlayer.posZ) + world.rand.nextInt(32) - world.rand.nextInt(32);
                int n4 = MathHelper.floor_double(entityPlayer.posY) + world.rand.nextInt(16) - world.rand.nextInt(16);
                if (n4 < 1) {
                    n4 = 1;
                } else if (n4 > 128) {
                    n4 = 128;
                }
                int n5 = world.rand.nextInt(classArray.length);
                for (n = n4; n > 2 && !world.isBlockNormalCube(n2, n - 1, n3); --n) {
                }
                while (!SpawnerAnimals.canCreatureTypeSpawnAtLocation(EnumCreatureType.monster, world, n2, n, n3) && n < n4 + 16 && n < 128) {
                    ++n;
                }
                if (n >= n4 + 16 || n >= 128) {
                    n = n4;
                    continue;
                }
                float f = (float)n2 + 0.5f;
                float f2 = n;
                float f3 = (float)n3 + 0.5f;
                try {
                    entityLiving = (EntityLiving)classArray[n5].getConstructor(World.class).newInstance(world);
                } catch (Exception exception) {
                    exception.printStackTrace();
                    return bl;
                }
                entityLiving.setLocationAndAngles(f, f2, f3, world.rand.nextFloat() * 360.0f, 0.0f);
                if (!entityLiving.getCanSpawnHere() || (pathEntity = pathfinder.createEntityPathTo(entityLiving, entityPlayer, 32.0f)) == null || pathEntity.pathLength <= 1) continue;
                PathPoint pathPoint = pathEntity.func_22328_c();
                if (!(Math.abs((double)pathPoint.xCoord - entityPlayer.posX) < 1.5) || !(Math.abs((double)pathPoint.zCoord - entityPlayer.posZ) < 1.5) || !(Math.abs((double)pathPoint.yCoord - entityPlayer.posY) < 1.5)) continue;
                ChunkCoordinates chunkCoordinates = BlockBed.getNearestEmptyChunkCoordinates(world, MathHelper.floor_double(entityPlayer.posX), MathHelper.floor_double(entityPlayer.posY), MathHelper.floor_double(entityPlayer.posZ), 1);
                if (chunkCoordinates == null) {
                    chunkCoordinates = new ChunkCoordinates(n2, n + 1, n3);
                }
                entityLiving.setLocationAndAngles((float)chunkCoordinates.x + 0.5f, chunkCoordinates.y, (float)chunkCoordinates.z + 0.5f, 0.0f, 0.0f);
                world.entityJoinedWorld(entityLiving);
                SpawnerAnimals.creatureSpecificInit(entityLiving, world, (float)chunkCoordinates.x + 0.5f, chunkCoordinates.y, (float)chunkCoordinates.z + 0.5f);
                entityPlayer.wakeUpPlayer(true, false, false);
                entityLiving.playLivingSound();
                bl = true;
                bl2 = true;
            }
        }
        return bl;
    }
}