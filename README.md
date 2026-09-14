# Linux.Admin.Defender

Administrative Protection for Linux Userspace Programs, System Resources, and Yields

## Purpose

Linux.Admin.Defender provides a documented defensive baseline for protecting operating-system files, directories, executables, libraries, service state, user data, boot resources, and kernel interfaces.

The project follows a distribution-aware model. Linux is a family of operating systems rather than one fixed filesystem implementation, so controls are documented by common hierarchy first and distribution second.

## Protective Intent

The project intends to protect designated system files and system resources from unauthorized exposure to malicious programs, unauthorized use, unauthorized modification, and unauthorized copying or duplication. Protection is intended to preserve system integrity, administrative control, provenance, and lawful use of protected items.

Any deployment should be implemented consistently with applicable federal law, other applicable law, platform security requirements, licensing obligations, and authorized administrative procedures. This README describes a defensive engineering objective; it does not claim that every particular protective measure is required or authorized by federal law.

## Intelligent Design Principle

The project applies an engineering principle of deliberate, intelligent design: security controls should be designed to identify, constrain, audit, and prevent corporate or organizational fraud rather than to facilitate fraud, concealment, unauthorized appropriation, or the misrepresentation of protected property. The objective is protection of legitimate systems, records, software, and other protected items—not the creation of mechanisms for corporate fraud or the unlawful taking or concealment of assets.

## Protected System Store

Linux.Admin.Defender includes a MySQL-like relational storage model for maintaining a protected copy and integrity record of designated system files. The default implementation uses the Python standard library's SQLite engine so the defender can operate without requiring a separate database server. The schema is relational and is designed so that a future MySQL/MariaDB backend can be substituted without changing the protection model.

The protected-store mode is **enabled by default** in `config/protected-store.json`. It maintains a content-addressed object store keyed by SHA-256 and a relational catalog containing file paths, object hashes, size, ownership, mode, timestamps, protection state, and security events. The default protected roots are `/boot`, `/etc`, `/usr`, `/var/lib`, and `/var/log`; pseudo-filesystems and transient locations such as `/proc`, `/sys`, `/dev`, `/run`, `/tmp`, and `/var/tmp` are excluded.

Initialize and snapshot the configured system set with:

```sh
python3 tools/protected-store.py init
python3 tools/protected-store.py snapshot
python3 tools/protected-store.py status
```

The mode can be controlled by the JSON configuration or overridden for one invocation with `--store-mode on` or `--store-mode off`. The store records a protected copy; it does not silently replace live operating-system files. Restoration or live-file locking remains an explicit administrative action.

The relational schema is documented in `storage/protected-store/schema.sql` and the operational configuration is documented in `config/protected-store.json`.

## Reference Structure

- `digital/lists/protected-files.md` — cross-distribution protected-location baseline.
- `digital/lists/linux-distributions/README.md` — distribution framework.
- `digital/lists/linux-distributions/ubuntu/README.md` — Ubuntu baseline.
- `digital/lists/linux-distributions/debian/README.md` — Debian baseline.
- `digital/lists/linux-distributions/fedora/README.md` — Fedora baseline.
- `digital/lists/linux-distributions/arch/README.md` — Arch Linux baseline.
- `config/protected-store.json` — default protected-store configuration.
- `storage/protected-store/schema.sql` — relational protected-store schema.
- `tools/protected-store.py` — initialization, snapshot, and status utility.

## Kernel File Protection

- `kernel/file-locker/linux_admin_defender_lock.c` — reference kernel module for applying an inode immutable protection to one administrator-selected path.
- `kernel/file-locker/Makefile` — external-module build rules against the running kernel.
- `kernel/file-locker/control.sh` — root-controlled load, unload, status, and explicit unlock commands.
- `kernel/file-locker/README.md` — build, operation, security, and filesystem compatibility notes.
- `kernel/file-locker/VERSION_MATRIX.md` — Debian, Ubuntu, Fedora, Arch, enterprise-family, and kernel compatibility guidance.

The kernel module is deliberately narrow: it does not intercept arbitrary processes or disable platform security controls. For production deployments, use signed modules and the distribution's supported kernel/module mechanism.

## Administrative Principle

The objective is controlled change, integrity, least privilege, auditing, and recoverability. System protection must not prevent legitimate package updates, kernel updates, service operation, or authorized administration.

The project favors high-assurance reasoning and explicit system boundaries: protection should be understandable, auditable, technically constrained, and directed toward legitimate defensive purposes. No numerical intelligence claim is made by this repository; the emphasis is on rigorous engineering and sound judgment.
