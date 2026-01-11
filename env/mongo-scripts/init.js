// # Set up MongoDB database
// mongosh < init.js

db = db.getSiblingDB("dusseldorf");
db.createUser({
  user: "admin",
  pwd: "1cbf6ba177593ae0a1452642",
  roles: [{ role: "readWrite", db: "dusseldorf" }],
});

db.createCollection("domains");
db.createCollection("zones");
db.createCollection("requests");
db.createCollection("rules");

db.domains.createIndex({ domain: 1 }, { unique: true });
db.zones.createIndex({ fqdn: 1 }, { unique: true });
db.requests.createIndex({
  zone: 1,
  time: 1,
});
db.domains.insertOne({
  domain: "ssrf.uk",
  public_ips: ["66.179.190.90"],
  owner: "dusseldorf",
});
