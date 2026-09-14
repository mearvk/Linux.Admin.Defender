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

## Administrative Principle

The objective is controlled change, integrity, least privilege, auditing, and recoverability. System protection must not prevent legitimate package updates, kernel updates, service operation, or authorized administration.
