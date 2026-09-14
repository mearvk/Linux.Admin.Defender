# Linux Distribution and Kernel Version Matrix

This matrix records known distribution generations relevant to building and loading the reference kernel module. Kernel-module compatibility is determined by the **running kernel build**, not merely by the distribution name. Always build against `uname -r` and the matching kernel headers/development package.

## Debian

| Distribution | Release | Kernel family shipped by release | Notes |
|---|---|---|---|
| Debian | 13 Trixie | Linux 6.12 series | Current stable generation; released 2025-08-09. |
| Debian | 12 Bookworm | Linux 6.1 series | Regular support ended 2026-07-12; LTS continues through 2028-06-30. |
| Debian | 11 Bullseye | Linux 5.10 series | LTS period ended 2026-08-31; extended support may differ. |
| Debian | 10 Buster | Linux 4.19 series | Legacy generation; not a recommended build target. |

Debian 13 ships the Linux 6.12 series, while Debian 12 shipped the 6.1 series. Debian's current stable release is Debian 13 (Trixie). citeturn1search1turn1search4turn1search10

## Ubuntu

| Distribution | Release | Kernel family / release line | Notes |
|---|---|---|---|
| Ubuntu | 26.04 LTS Resolute Raccoon | Current 26.04 kernel line | Released 2026-04-23. |
| Ubuntu | 24.04 LTS Noble Numbat | 6.8-based release generation | Current supported LTS generation. |
| Ubuntu | 22.04 LTS Jammy Jellyfish | 5.15-based release generation | Supported LTS generation. |
| Ubuntu | 20.04 LTS Focal Fossa | 5.4-based release generation | Legacy LTS generation; use only when required. |
| Ubuntu | 18.04 LTS Bionic Beaver | 4.15-based release generation | Legacy; not a recommended new target. |

Ubuntu 26.04 LTS was released in April 2026 and is scheduled for standard security maintenance through May 2031. Ubuntu maintains a six-month release cadence with LTS releases every two years. citeturn1search0turn1search3turn1search5

## Fedora

| Distribution | Release | Notes |
|---|---|---|
| Fedora Linux | 44 | Current 2026 generation; released 2026-04-28. |
| Fedora Linux | 43 | Previous generation; released 2025-10-28. |
| Fedora Linux | 42 | Previous generation. |
| Fedora Linux | 41 | Previous generation. |
| Fedora Linux | 40 | Previous generation. |

Fedora releases are short-lived compared with Debian/Ubuntu LTS releases. Fedora Linux 44 was released on 2026-04-28. citeturn4search0turn4search10

## Arch Linux

Arch does not use fixed major releases. It is a rolling-release distribution, so the module must be rebuilt for the currently installed kernel after kernel upgrades when ABI/module compatibility requires it. citeturn4search23

As of 2026-09-01, the current Arch installation image was `2026.09.01` and included Linux kernel `7.2.2`. This is an installation-image snapshot, not a permanent Arch version number. citeturn4search22turn4search18

## RHEL / Rocky / AlmaLinux family

These distributions use enterprise release streams and commonly retain a stable kernel ABI through a major release with vendor backports. Do not infer compatibility from the upstream kernel number alone. Build against the exact installed kernel headers and vendor configuration.

Recommended procedure:

```sh
uname -r
cat /etc/os-release
ls -ld /lib/modules/$(uname -r)/build
```

## openSUSE / SUSE family

openSUSE Leap, openSUSE Tumbleweed, and SUSE Linux Enterprise have different update models. Tumbleweed is rolling; Leap and SLE use more stable release lines. Treat each installed `uname -r` as a separate module build target.

## Kernel compatibility rule

The authoritative build target is:

```sh
uname -r
```

Then verify the kernel build directory:

```sh
test -e /lib/modules/$(uname -r)/build && echo "kernel build tree available"
```

External modules use kernel build metadata, including vermagic and, where enabled, symbol-version CRCs. A module built for one kernel configuration should not be assumed to load into another. citeturn0search10turn0search11

## Secure Boot and signed modules

Production systems should sign out-of-tree modules and keep the private signing key off the build tree. Linux kernel module signing can be configured to require valid signatures, and Debian documents DKMS/MOK workflows for modules on Secure Boot systems. citeturn0search0turn0search6

## Recommended support policy

For Linux.Admin.Defender, maintain source compatibility in tiers:

1. **Primary:** current Debian stable and current Ubuntu LTS.
2. **Secondary:** current Fedora and current Arch.
3. **Enterprise:** RHEL-compatible and SUSE-compatible releases, built on the exact installed vendor kernel.
4. **Legacy:** older distributions only when a specific deployment requires them.

Do not silently reuse a `.ko` compiled for a different kernel release. Rebuild and, where applicable, re-sign the module after kernel upgrades.
