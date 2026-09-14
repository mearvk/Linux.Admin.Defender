# Arch Linux

Administrative Defender baseline for Arch Linux systems.

Arch uses a rolling-release model and a package-managed system centered on pacman. Exact system state can change rapidly, so protection rules must remain aligned with the installed system.

## Key Controls

- Use pacman and trusted repositories for authorized package changes.
- Treat `/etc`, `/usr`, `/var`, `/boot`, and privileged user data as high-impact resources.
- Expect package and kernel updates to change system files over time.
- Use documented configuration management, backups, auditing, permissions, and integrity checks.
- Validate assumptions against current Arch documentation before enforcement.
