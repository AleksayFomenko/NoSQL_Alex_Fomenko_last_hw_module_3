#!/bin/bash

echo "Waiting for MongoDB containers..."

until mongosh --host configsvr:27017 --eval "db.runCommand({ ping: 1 })" >/dev/null 2>&1
do
  sleep 2
done

echo "Init config server replica set"

mongosh --host configsvr:27017 <<EOF
rs.initiate({
  _id: "configReplSet",
  configsvr: true,
  members: [
    { _id: 0, host: "configsvr:27017" }
  ]
})
EOF

until mongosh --host shard1:27017 --eval "db.runCommand({ ping: 1 })" >/dev/null 2>&1
do
  sleep 2
done

echo "Init shard1 replica set"

mongosh --host shard1:27017 <<EOF
rs.initiate({
  _id: "shard1ReplSet",
  members: [
    { _id: 0, host: "shard1:27017" }
  ]
})
EOF

until mongosh --host shard2:27017 --eval "db.runCommand({ ping: 1 })" >/dev/null 2>&1
do
  sleep 2
done

echo "Init shard2 replica set"

mongosh --host shard2:27017 <<EOF
rs.initiate({
  _id: "shard2ReplSet",
  members: [
    { _id: 0, host: "shard2:27017" }
  ]
})
EOF

until mongosh --host mongos:27017 --eval "db.runCommand({ ping: 1 })" >/dev/null 2>&1
do
  sleep 2
done

echo "Adding shards to cluster"

mongosh --host mongos:27017 <<EOF

sh.addShard("shard1ReplSet/shard1:27017")
sh.addShard("shard2ReplSet/shard2:27017")

sh.enableSharding("university")

sh.shardCollection("university.courses", { _id: "hashed" })
sh.shardCollection("university.grades", { _id: "hashed" })
sh.shardCollection("university.students", { _id: "hashed" })
sh.shardCollection("university.usertable", { _id: "hashed" })

EOF

echo "Cluster ready, start import..."

for file in /scripts/data/*.json
do
    collection=$(basename "$file" .json)
    echo "Importing $file -> $collection"

    mongoimport \
        --host mongos:27017 \
        --db university \
        --collection "$collection" \
        --file "$file" \
        --type json
done

echo "Import done"