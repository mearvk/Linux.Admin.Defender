# Linux.Admin.Defender

Administrative Protection for Linux Userspace Programs, System Resources, and Yields

## Purpose

Linux.Admin.Defender provides a documented defensive baseline for protecting operating-system files, directories, executables, libraries, service state, user data, boot resources, and kernel interfaces.

The project follows a distribution-aware model. Linux is a family of operating systems rather than one fixed filesystem implementation, so controls are documented by common hierarchy first and distribution second.

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
