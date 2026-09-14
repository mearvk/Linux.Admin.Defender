# Linux.Admin.Defender Kernel File Lock

## Purpose

This directory contains a small, auditable kernel-module reference for administrative file protection on Linux. The module resolves one explicitly supplied absolute path and sets the inode immutable flag.

This is intentionally narrower than a general filesystem interception engine. It does not monitor processes, hide activity, inject code, or attempt to bypass kernel security controls.

## Important distinction

Linux has several different meanings of "file locking":

1. **Advisory POSIX/FLOCK locks** — coordinated through the VFS locking interfaces and normally used by applications.
2. **Filesystem immutable attributes** — prevent ordinary writes, truncation, deletion, and related metadata changes for supported filesystems.
3. **Policy enforcement** — a broader security problem normally addressed with LSMs, SELinux/AppArmor, filesystem permissions, read-only mounts, or verified filesystems.

This reference driver uses the second model. The Linux VFS documents inode locking and filesystem attribute operations; supported filesystems decide how attributes are persisted. citeturn2search0turn3search0

## Build

Install the kernel development package matching the running kernel, then:

```sh
cd kernel/file-locker
make
```

The result is `linux_admin_defender_lock.ko`.

## Load

```sh
sudo ./control.sh load /absolute/path/to/file
```

Equivalent direct command:

```sh
sudo insmod ./linux_admin_defender_lock.ko target=/absolute/path/to/file
```

Check the kernel log:

```sh
dmesg | tail -n 20
```

Check module state:

```sh
./control.sh status
```

## Unload

```sh
sudo ./control.sh unload
```

Unloading does **not** automatically clear the immutable state. This is deliberate: removing a driver should not silently weaken a protection decision that has already been applied.

To explicitly remove the immutable attribute where the filesystem supports `chattr`:

```sh
sudo ./control.sh unlock /absolute/path/to/file
```

## Security model

Kernel modules are privileged executable code. Use signed modules and a trusted build chain on production systems. Linux supports module signature verification and can be configured to reject unsigned modules with `CONFIG_MODULE_SIG_FORCE`. Secure Boot and kernel lockdown can also restrict unsigned module loading. citeturn0search0turn0search6

Do not disable Secure Boot, lockdown, module-signature enforcement, SELinux, AppArmor, or other platform protections merely to make this module load.

## Filesystem compatibility

The immutable flag is filesystem-dependent. Test the target filesystem before adopting this reference in production. For example, ext4 records an immutable inode flag, while other filesystems may implement attributes differently. citeturn3search9

For stronger system-wide protection, prefer read-only mounts, verified filesystems, package-manager integrity, SELinux/AppArmor policy, or LoadPin as appropriate. LoadPin can restrict kernel-loaded files to a trusted filesystem. citeturn0search9

## Kernel compatibility

The module is intended as a source-level reference for modern 6.x kernels. External modules are kernel-version-sensitive: module versioning and vermagic are checked at load time, and a module built for one kernel should not be assumed compatible with another. citeturn0search10turn0search11

For Debian, DKMS is the normal mechanism for building and maintaining additional out-of-tree modules across installed kernels. citeturn0search3

## Production warning

This is an administrative reference driver, not a replacement for a distribution security policy. Test it on a non-critical file and kernel before protecting operating-system files. Never experiment first on `/etc`, `/boot`, `/usr`, `/lib`, or other recovery-critical locations.
