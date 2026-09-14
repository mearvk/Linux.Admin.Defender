# Fedora Linux

Administrative Defender baseline for Fedora systems.

Fedora uses a modern Linux userspace with RPM-based package management, systemd, and SELinux integration. Protect package-managed resources and verify any integrity policy against the exact Fedora release.

## Key Controls

- Use DNF and trusted Fedora repositories for authorized software changes.
- Treat `/etc`, `/usr`, `/var`, `/boot`, and privileged service state as high-impact resources.
- Preserve SELinux policy and labels; do not bypass enforcement merely to make administrative changes easier.
- Use auditing, backups, package verification, and least privilege.
