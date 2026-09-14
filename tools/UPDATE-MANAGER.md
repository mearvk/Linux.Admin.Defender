# Linux.Admin.Defender Update Manager

## Purpose

The update manager performs a daily update check using either an HTTPS internet manifest or a named local update folder. Every candidate file is SHA-256 hashed and compared with the manifest before it can enter the staging area or be installed.

## Verification boundary

The sequence is:

1. Obtain the update manifest.
2. Reject manifests that do not declare SHA-256.
3. Reject absolute paths and path traversal.
4. Obtain every listed file.
5. Compute SHA-256 independently for every file.
6. Reject the entire update set if any digest differs.
7. Copy only verified files to staging.
8. Hash the staged copy again.
9. Install only after all files pass verification.
10. Back up an existing destination before replacement.

A failed verification results in no installation from that update set.

## Configuration

`config/update-manager.json` controls the mode. `source_mode` may be:

- `internet` — retrieve the manifest and HTTPS-hosted files.
- `local` — read `updates.json` and update files from `local_update_folder`.

The configured interval is 24 hours. The program itself performs one check per invocation; the operating system scheduler should invoke it once per day.

## Local manifest example

```json
{
  "algorithm": "sha256",
  "version": "2026.09.14",
  "files": [
    {
      "path": "usr/local/lib/example.so",
      "sha256": "64-hexadecimal-character-sha256-digest"
    }
  ]
}
```

The example digest is intentionally not valid update data; replace it with the independently calculated SHA-256 value of the intended file.

## Important security note

SHA-256 proves that a downloaded file matches the digest supplied by the manifest. It does **not**, by itself, prove that the manifest came from a trusted publisher. For internet distribution, the manifest endpoint and update files should be protected with HTTPS and an authenticated distribution channel. A future signed-manifest mode should use a publisher signature in addition to SHA-256.

## Recommended daily scheduling

Use the host operating system's supported scheduler to invoke:

```sh
sudo /usr/bin/python3 /opt/Linux.Admin.Defender/tools/update-manager.py --install
```

Do not run the updater from an untrusted user account, and do not weaken Secure Boot, kernel lockdown, module-signature enforcement, SELinux, AppArmor, or filesystem permissions to make an update succeed.

## Manual verification

Check without installing:

```sh
python3 tools/update-manager.py --check
```

The updater never treats a hash mismatch as a warning. A mismatch is a hard verification failure and prevents installation of the candidate set.
