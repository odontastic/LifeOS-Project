---
title: "Backup and Recovery Procedures"
type: "Documentation"
status: "Active"
created: "2025-12-12"
last_updated: "2025-12-12"
tags: ["backup", "recovery", "neo4j", "qdrant", "operations"]
---

# Backup and Recovery Procedures for LifeOS 2.0 Databases

This document outlines the recommended procedures for regularly backing up Neo4j and Qdrant databases, which are critical components of the LifeOS 2.0 backend. Regular backups are essential for data integrity, disaster recovery, and ensuring business continuity.

## Neo4j Database Backup

Neo4j provides built-in tools for creating consistent backups of the database. For a running Neo4j instance, the `neo4j-admin dump` command is typically used.

### Recommended Backup Procedure (Neo4j)

1.  **Stop the Neo4j Database (Recommended for consistency):**
    ```bash
    docker-compose stop neo4j
    ```
    *Note: Online backups are possible with Neo4j Enterprise Edition, but for Community Edition, stopping the database ensures a consistent backup.*

2.  **Execute the Backup Command:**
    ```bash
    docker run --rm \
        --volume /path/to/your/neo4j/data:/data \
        --volume /path/to/your/backup/location:/backup \
        neo4j:5 neo4j-admin dump --database=neo4j --to=/backup/neo4j-backup-$(date +%Y%m%d%H%M%S).dump
    ```
    *   Replace `/path/to/your/neo4j/data` with the actual path where your Neo4j data volume is mounted (e.g., `./neo4j-data` if using Docker Compose from the project root).
    *   Replace `/path/to/your/backup/location` with the host path where you want to store the backup files.
    *   `neo4j-backup-$(date +%Y%m%d%H%M%S).dump` will create a uniquely timestamped backup file.

3.  **Restart the Neo4j Database:**
    ```bash
    docker-compose start neo4j
    ```

## Neo4j Database Recovery

### Recommended Recovery Procedure (Neo4j)

1.  **Stop the Neo4j Database:**
    ```bash
    docker-compose stop neo4j
    ```

2.  **Clear existing data (if starting fresh or recovering from corruption):**
    ```bash
    sudo rm -rf /path/to/your/neo4j/data/*
    ```
    *   **CAUTION:** This command will permanently delete all data in your Neo4j data directory. Use with extreme care.

3.  **Restore the Database from a Dump File:**
    ```bash
    docker run --rm \
        --volume /path/to/your/neo4j/data:/data \
        --volume /path/to/your/backup/location:/backup \
        neo4j:5 neo4j-admin load --database=neo4j --from=/backup/your-backup-file.dump --force
    ```
    *   Replace `your-backup-file.dump` with the name of the backup file you wish to restore.
    *   The `--force` flag is often needed if the database already exists or has some inconsistencies.

4.  **Start the Neo4j Database:**
    ```bash
    docker-compose start neo4j
    ```

## Qdrant Vector Database Backup

Qdrant supports snapshot creation, which is a consistent copy of the collection data.

### Recommended Backup Procedure (Qdrant)

1.  **Create a Snapshot:**
    ```bash
    docker exec -it <qdrant-container-id> sh -c "curl -X POST 'http://localhost:6333/collections/<collection_name>/snapshots' -H 'Content-Type: application/json'"
    ```
    *   Replace `<qdrant-container-id>` with the actual Docker container ID or name of your Qdrant service (e.g., `lifeos-rag-api-qdrant-1`).
    *   Replace `<collection_name>` with the name of the Qdrant collection you want to back up (e.g., `lifeos_notes`, `lifeos_resources`).
    *   This command creates a snapshot *inside* the Qdrant container, typically in `/qdrant/snapshots`.

2.  **Copy the Snapshot to Host Machine:**
    ```bash
    docker cp <qdrant-container-id>:/qdrant/snapshots/<snapshot_filename> /path/to/your/backup/location/
    ```
    *   You'll need to get the `<snapshot_filename>` from the output of the snapshot creation command or by listing the `/qdrant/snapshots` directory inside the container.

### Recommended Recovery Procedure (Qdrant)

1.  **Stop the Qdrant Service (if running):**
    ```bash
    docker-compose stop qdrant
    ```

2.  **Copy the Snapshot into the Qdrant Container's Snapshot Directory:**
    ```bash
    docker cp /path/to/your/backup/location/<snapshot_filename> <qdrant-container-id>:/qdrant/snapshots/
    ```

3.  **Start the Qdrant Service:**
    ```bash
    docker-compose start qdrant
    ```

4.  **Restore the Snapshot:**
    ```bash
    docker exec -it <qdrant-container-id> sh -c "curl -X PUT 'http://localhost:6333/collections/<collection_name>/snapshots/upload?snapshot=<snapshot_filename>' -H 'Content-Type: application/json'"
    ```
    *   This command will restore the collection from the specified snapshot.

### Automation Considerations

*   These commands can be integrated into shell scripts and scheduled using `cron` jobs (on Linux/macOS) or Task Scheduler (on Windows) for automated, regular backups.
*   Consider storing backups in a remote, secure location (e.g., S3, Google Cloud Storage) for off-site disaster recovery.
*   Implement a retention policy to manage the number and age of backup files.
