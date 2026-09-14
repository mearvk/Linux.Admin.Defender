# Ubuntu Linux

Administrative Defender baseline for Ubuntu systems.

Ubuntu follows the conventional Linux hierarchy while adding Ubuntu-specific package, boot, service, and security integration. Protect `/etc`, `/usr`, `/var`, `/boot`, `/home`, `/root`, and runtime interfaces according to the installed Ubuntu release and administrator policy.

## Key Controls

- Use APT and Ubuntu package repositories for authorized software changes.
- Preserve package-managed files and verify changes through package metadata and integrity tooling.
- Treat `/boot`, `/etc`, `/usr`, and service state under `/var` as high-impact administrative resources.
- Account for systemd services and Ubuntu security controls such as AppArmor.
- Keep recovery media and backups available before major system changes.
