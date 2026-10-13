# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.6.x   | yes       |
| 0.5.x   | security fixes only |
| < 0.5   | no        |

## Reporting a vulnerability

Email `security@youtube-thumbnail-studio.dev` with a description, a
minimal repro (a `.ytthumb` spec is ideal), and the affected version.
Do not open a public issue for exploitable bugs.

We aim to acknowledge within 72 hours and ship a patch within 14 days
for confirmed high-severity issues.

## Threat model

The studio loads third-party Python extensions from
`~/.ytthumb/plugins` and from installed entry points. **Extensions run
with full process privileges.** Treat plugin folders like any other
untrusted code path:

- Only install plugins you have read.
- The host sandboxes nothing — a malicious plugin is a malicious
  process.
- Entry points declared in installed packages are auto-loaded at start.

Report anything that lets a `.ytthumb` spec execute code, escape the
plugin directory, or write outside `out/`.