db = db.getSiblingDB("database");

if (!db.getCollectionNames().includes("programs")) {
    db.createCollection("programs");
    print("✅ Collection 'programs' created.");
} else {
    print("⚠️ Collection 'programs' already exists. Skipping.");
}