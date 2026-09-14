# Linux Administrative Defender Lists

Administrative reference lists for protected Linux operating-system locations, configuration, executables, libraries, user data, service state, recovery resources, and security-sensitive system interfaces.

This collection is intentionally distribution-aware: Linux does not have one universal filesystem layout. Entries should be verified against the target distribution, release, filesystem hierarchy, init system, package manager, and security framework.

## Baseline Documents

- `protected-files.md` — core protected locations and rationale.
- `linux-distributions/README.md` — distribution and release planning baseline.
- `linux-distributions/ubuntu/README.md` — Ubuntu-focused baseline.
- `linux-distributions/debian/README.md` — Debian-focused baseline.
- `linux-distributions/fedora/README.md` — Fedora-focused baseline.
- `linux-distributions/arch/README.md` — Arch Linux-focused baseline.

## Administrative Principle

Protection means controlled administration, integrity monitoring, least privilege, documented change, and recovery—not indiscriminate immutability. Package managers, system updates, service management, boot processes, and authorized administrators must be able to perform legitimate changes.
