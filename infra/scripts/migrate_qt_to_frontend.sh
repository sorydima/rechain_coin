#!/usr/bin/env bash
# Simple migration script to move src/qt into frontend/qt with backups.
set -e
SRC_DIR="src/qt"
DEST_DIR="frontend/qt"
BACKUP_DIR="migrate_backups/qt_$(date +%s)"

if [ ! -d "$SRC_DIR" ]; then
  echo "Source directory $SRC_DIR not found."
  exit 1
fi

mkdir -p "$BACKUP_DIR"
mkdir -p "$(dirname $DEST_DIR)"

# Move files with backup
echo "Backing up $SRC_DIR to $BACKUP_DIR"
cp -a "$SRC_DIR" "$BACKUP_DIR/"

echo "Moving $SRC_DIR to $DEST_DIR"
mv "$SRC_DIR" "$DEST_DIR"

echo "Migration complete. If build fails, restore from $BACKUP_DIR"
