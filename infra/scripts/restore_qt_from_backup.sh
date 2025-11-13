#!/usr/bin/env bash
# Restore the most recent backup of src/qt
set -e
BACKUP_ROOT="migrate_backups"
if [ ! -d "$BACKUP_ROOT" ]; then
  echo "No backups found"
  exit 1
fi

LAST_BACKUP=$(ls -td $BACKUP_ROOT/qt_* | head -n1)
if [ -z "$LAST_BACKUP" ]; then
  echo "No qt backups found"
  exit 1
fi

echo "Restoring from $LAST_BACKUP"
rm -rf src/qt || true
cp -a "$LAST_BACKUP" "src/qt"

echo "Restore complete"
