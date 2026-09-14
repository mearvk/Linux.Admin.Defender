# Linux Protected Files and Directories

A cross-distribution administrative baseline for Linux system locations that commonly require elevated privileges, integrity controls, backup, or careful change management.

| Location | What it does | Why it is important |
|---|---|---|
| `/` | Filesystem root containing the operating-system hierarchy. | Damage can affect the entire system namespace. |
| `/boot` | Bootloader, kernel, initramfs, and related boot assets on many distributions. | Required to start the operating system. |
| `/etc` | System-wide configuration files. | Configuration controls services, networking, authentication, mounts, and system behavior. |
| `/usr` | Primary hierarchy for installed userland programs, libraries, documentation, and shared resources. | Core operating-system and package-managed software resides here. |
| `/usr/bin` | Common executable programs. | Corruption or replacement can disrupt normal administration and user operation. |
| `/usr/sbin` | System-administration executables. | Contains privileged administrative tooling. |
| `/usr/lib` | Shared libraries and supporting program data. | Many executables depend on these components. |
| `/var` | Variable system data such as logs, caches, queues, databases, and package state. | Operational history and service state frequently depend on it. |
| `/var/log` | System and application logs. | Important for auditing, troubleshooting, incident response, and accountability. |
| `/var/lib` | Persistent application and service state. | Package managers, databases, services, and system components may depend on its contents. |
| `/var/spool` | Queued work such as mail, print, and scheduled jobs. | Unauthorized modification can alter pending system operations. |
| `/home` | Ordinary users' home directories on conventional installations. | Contains user data, credentials/configuration files, and application state. |
| `/root` | Home directory of the root administrator account. | Contains privileged administrative configuration and data. |
| `/run` | Volatile runtime state created during boot and service operation. | Service coordination and runtime state can depend on it; it should not be treated like persistent storage. |
| `/sys` | Kernel-provided sysfs interface to devices, drivers, and kernel subsystems. | Changes can affect live kernel/device behavior and require great care. |
| `/proc` | Kernel-provided process and system information interface. | Exposes critical runtime state and control interfaces. |
| `/dev` | Device-node hierarchy, normally managed dynamically. | Provides processes access to hardware and kernel device interfaces. |
| `/tmp` | Temporary files shared according to system policy. | Important to secure because applications routinely exchange transient data there. |
| `/var/tmp` | Temporary files intended to persist across reboots more often than `/tmp`. | Can contain application state that survives a restart and therefore needs controlled access. |

## Important Qualification

Linux is not a single operating-system implementation. Exact paths, permissions, mount points, service managers, boot arrangements, and package ownership vary between distributions and releases. This document is a defensive baseline, not a claim that every path is immutable or equally protected.

## Administrative Controls

Use root privileges only when necessary. Prefer package-manager transactions, signed packages, distribution-supported service management, filesystem permissions, Linux Security Modules such as SELinux or AppArmor where applicable, auditing, backups, and integrity monitoring. Do not disable security controls merely to modify protected system resources.

## Trusted Standards and References

- Filesystem Hierarchy Standard (FHS), Linux Foundation.
- systemd filesystem hierarchy and system directories documentation.
- Distribution-specific documentation for Ubuntu, Debian, Fedora, and Arch Linux.
