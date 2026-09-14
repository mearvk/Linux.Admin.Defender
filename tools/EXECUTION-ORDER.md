# Verification-First Execution Order

Linux.Admin.Defender treats SHA-256 verification as a mandatory security gate for protected software.

## Required order

1. Obtain the trusted SHA-256 manifest.
2. Verify source files and required dependencies.
3. **Do not build** if verification fails.
4. Build the program only after verification succeeds.
5. Verify generated binaries and other build artifacts before execution.
6. Verify diagnostic tools, scripts, libraries, and related files before diagnostics.
7. Execute or diagnose only after the applicable verification gates pass.

Any missing file, malformed digest, or SHA-256 mismatch is a fail-closed condition. The caller must stop rather than continuing to build, execute, or diagnose.

## Existing verifier

Use `tools/verify-before-execution.py` with a trusted manifest. The verifier returns a non-zero status on failure so build and diagnostic automation can use it as a hard prerequisite.

SHA-256 confirms integrity against the trusted manifest; it does not independently authenticate the manifest publisher. Internet update channels should therefore use authenticated HTTPS and, for a stronger trust chain, signed manifests.
