# Debian Linux

Administrative Defender baseline for Debian systems.

Protect package-managed system locations, boot resources, configuration, logs, service state, and privileged user data according to the installed Debian release.

## Key Controls

- Use APT and Debian package repositories for authorized changes.
- Treat `/etc`, `/usr`, `/var`, and `/boot` as high-impact system resources.
- Account for systemd where it is the installed init/service manager.
- Use filesystem permissions, auditing, backups, and applicable Linux Security Modules.
- Verify distribution-specific package ownership before enforcing integrity rules.
