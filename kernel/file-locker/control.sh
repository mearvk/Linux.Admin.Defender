#!/bin/sh
# Linux.Admin.Defender kernel file-locker control
# Run as root. This script deliberately requires an explicit path.

set -eu

MODULE="linux_admin_defender_lock"
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
MODULE_FILE="$SCRIPT_DIR/${MODULE}.ko"

usage() {
    echo "Usage: $0 load /absolute/path"
    echo "       $0 unload"
    echo "       $0 status"
    echo "       $0 unlock /absolute/path"
    exit 2
}

require_root() {
    if [ "$(id -u)" -ne 0 ]; then
        echo "Run this command as root (for example: sudo $0 ...)." >&2
        exit 1
    fi
}

case "${1:-}" in
    load)
        require_root
        [ "$#" -eq 2 ] || usage
        case "$2" in
            /*) ;;
            *) echo "Path must be absolute." >&2; exit 2 ;;
        esac
        [ -f "$MODULE_FILE" ] || {
            echo "Module not found: $MODULE_FILE" >&2
            echo "Build it first with: make -C $SCRIPT_DIR" >&2
            exit 1
        }
        insmod "$MODULE_FILE" "target=$2"
        ;;

    unload)
        require_root
        [ "$#" -eq 1 ] || usage
        rmmod "$MODULE"
        ;;

    status)
        lsmod | awk -v m="$MODULE" 'NR == 1 || $1 == m'
        ;;

    unlock)
        require_root
        [ "$#" -eq 2 ] || usage
        case "$2" in
            /*) ;;
            *) echo "Path must be absolute." >&2; exit 2 ;;
        esac
        command -v chattr >/dev/null 2>&1 || {
            echo "chattr is required for explicit attribute removal." >&2
            exit 1
        }
        chattr -i -- "$2"
        echo "Immutable flag removed from $2"
        ;;

    *)
        usage
        ;;
esac
