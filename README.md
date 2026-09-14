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

## Reference Structure

- `digital/lists/protected-files.md` — cross-distribution protected-location baseline.
- `digital/lists/linux-distributions/README.md` — distribution framework.
- `digital/lists/linux-distributions/ubuntu/README.md` — Ubuntu baseline.
- `digital/lists/linux-distributions/debian/README.md` — Debian baseline.
- `digital/lists/linux-distributions/fedora/README.md` — Fedora baseline.
- `digital/lists/linux-distributions/arch/README.md` — Arch Linux baseline.

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
