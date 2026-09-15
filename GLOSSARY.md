# Glossary

Definitions of the terms and tools used across Linux Admin Defender — the
kernel module, the Python tooling, the build/CI pipeline, and this
repository's own concepts. Grouped by area for quick reference.

## Linux kernel / module concepts

- **LKM (Loadable Kernel Module).** Kernel code (a `.ko` file) that can be
  loaded into and unloaded from the running kernel at runtime. This project's
  file-locker is an out-of-tree LKM.
- **Out-of-tree module.** A module built separately from the mainline kernel
  source, against an installed kernel's headers. It must be rebuilt for each
  kernel it targets.
- **`.ko` file.** The compiled kernel object (module) produced by the build —
  here, `linux_admin_defender_lock.ko`.
- **`module_init` / `module_exit`.** Macros registering the functions the
  kernel calls when the module is loaded and unloaded.
- **`module_param`.** Declares a parameter passed at load time
  (e.g. `insmod ... target=/path`). Here `target` names the file to protect.
- **VFS (Virtual File System).** The kernel's abstraction layer over concrete
  filesystems (ext4, xfs, …). The module uses VFS interfaces such as
  `kern_path`, `d_inode`, and `inode_lock`.
- **inode.** The kernel structure holding a file's metadata (owner, mode,
  flags, size). Protection here is applied by setting an inode flag.
- **Immutable flag (`S_IMMUTABLE` / `chattr +i`).** An inode attribute that
  prevents ordinary writes, truncation, deletion, and rename. The module sets
  the in-kernel `S_IMMUTABLE` flag; `chattr -i` removes it where the filesystem
  supports it. Support is filesystem-dependent.
- **`insmod` / `rmmod` / `modinfo` / `depmod`.** User-space tools to insert,
  remove, inspect, and index kernel modules. `control.sh` wraps `insmod`/`rmmod`.
- **vermagic.** Version-magic metadata baked into a module (kernel version,
  config flags) that the kernel checks at load time. A mismatch prevents
  loading — why a `.ko` built for one kernel should not be reused on another.
- **DKMS (Dynamic Kernel Module Support).** A framework that automatically
  rebuilds out-of-tree modules when the kernel is upgraded. The recommended way
  to maintain this module across kernel updates on Debian/Ubuntu.
- **Kernel headers / build tree.** The development files
  (`/lib/modules/$(uname -r)/build`) needed to compile a module for the running
  kernel. The build is `make -C $KDIR M=$(pwd) modules`.
- **`obj-m`.** The kbuild variable in the `Makefile` naming the module object
  to build (`obj-m += linux_admin_defender_lock.o`).
- **Module signing / MOK.** Signing a module so the kernel will accept it under
  signature enforcement or Secure Boot. **MOK** (Machine Owner Key) is the
  key-enrollment mechanism used on Secure Boot systems. Not performed in CI.
- **LSM (Linux Security Module).** The kernel framework behind SELinux,
  AppArmor, etc. Referenced as the broader, policy-level alternative to this
  narrow inode-immutability approach.
- **Kernel lockdown / Secure Boot.** Platform protections that restrict loading
  unsigned modules and other privileged operations. This project does not
  disable them.
- **LoadPin.** An LSM that restricts kernel-loaded files (modules, firmware) to
  a single trusted filesystem.

## Python tooling

- **`protected-store.py`.** Builds a content-addressed store of protected system
  files: hashes each file (SHA-256), deduplicates content as objects, and
  records metadata in SQLite. Commands: `init`, `snapshot`, `status`.
- **`update-manager.py`.** Verifies (SHA-256) and optionally installs updates
  from a local folder or an HTTPS manifest, staging and backing up before
  replacing files. Fails closed on any digest mismatch.
- **`verify-before-execution.py`.** The verification gate: hashes each file
  listed in a manifest and compares to the expected SHA-256, returning non-zero
  on any mismatch, missing file, unsafe path, or bad digest.
- **`generate-manifest.py`.** Regenerates `updates/build-manifest.json` with the
  current SHA-256 digests of the protected build inputs.
- **`preflight-build.sh`.** Shell wrapper that runs the verification gate before
  a build, refusing to proceed if verification fails.
- **Content-addressed store.** A store where each object is keyed by the hash of
  its content (here SHA-256), so identical content is stored once.
- **SQLite.** The embedded, serverless SQL database (Python standard library)
  used for the protected-store catalog. The schema is designed so a MySQL/
  MariaDB backend could be substituted later.

## Build / CI terms

- **kbuild.** The kernel's `make`-based build system used to compile modules
  against a kernel build tree.
- **`build-essential` / `linux-headers-$(uname -r)`.** Debian/Ubuntu packages
  providing the compiler toolchain and the running kernel's headers, installed
  in CI so the module can be built.
- **GitHub Actions.** GitHub's CI/CD system that runs workflows on hosted
  machines in response to events (push, pull request, manual dispatch).
- **Workflow / job / step.** A workflow (`.github/workflows/build.yml`) contains
  jobs; each job runs on a runner and is a sequence of steps. This workflow has
  a `verify-and-python` job and a `build-kernel-module` job.
- **Runner.** The machine executing a job. `ubuntu-latest` is GitHub's hosted
  Linux image.
- **Artifact.** Files uploaded from a run for later download — here the built
  `linux_admin_defender_lock.ko`.
- **ruff.** A fast Python linter, run non-blocking in CI to surface style/lint
  findings without failing the build.

## Linux Admin Defender concepts

- **Protected roots.** The default directories the store snapshots and protects
  (`/boot`, `/etc`, `/usr`, `/var/lib`, `/var/log`), while pseudo/transient
  filesystems (`/proc`, `/sys`, `/dev`, `/run`, `/tmp`, `/var/tmp`) are excluded.
- **Protected system store (stored-protected mode).** A local, MySQL-like
  relational model (default SQLite) keeping content-addressed reference copies
  and integrity records of protected files. It records a copy; it never silently
  replaces live OS files. See `storage/protected-store/schema.sql`.
- **Verification gate / verification-first execution.** The mandatory,
  fail-closed SHA-256 check run before build, execution, and diagnostics: any
  mismatch, missing file, or malformed digest stops the pipeline. See
  `tools/EXECUTION-ORDER.md`.
- **Build manifest.** `updates/build-manifest.json` — lists each protected build
  input with its expected SHA-256 digest, consumed by the verification gate.
- **Fail closed.** A safety posture where, on any error or ambiguity, the system
  stops rather than proceeding. The verification gate and update manager both
  fail closed.
- **SHA-256.** The cryptographic hash used for integrity verification and object
  identity. It proves a file's bytes are unchanged; it does not by itself
  authenticate who published the file (that needs a signed manifest / signing).
- **Distribution-aware model.** The project documents protections by common
  filesystem hierarchy first and per-distribution specifics second, because
  Linux is a family of systems rather than one fixed layout. See
  `kernel/file-locker/VERSION_MATRIX.md` for kernel/distro build targets.
