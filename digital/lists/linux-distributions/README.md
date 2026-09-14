# Linux Distribution Baseline

The Linux Administrative Defender collection uses distribution-specific documents rather than assuming that every Linux system has identical files, packages, services, or security policies.

## Covered Baselines

- Ubuntu
- Debian
- Fedora
- Arch Linux

Each distribution document should record protected paths, package-managed locations, service configuration, boot resources, logging, user data, and security mechanisms appropriate to the release.

## Cross-Distribution Rule

The Filesystem Hierarchy Standard provides a useful common vocabulary, but distribution documentation remains authoritative for implementation details. A protection policy should identify the exact distribution and release before enforcing machine-specific controls.
