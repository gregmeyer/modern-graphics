# CLI Deprecation Policy

This policy defines how legacy CLI commands are retired while keeping migration risk low.

## Default stance

- `modern-graphics create` is the default and preferred CLI surface.
- Legacy commands remain compatibility-only.
- New documentation, examples, and onboarding should use `create` first.

## Deprecation lifecycle

### Stage 1: Warn (current)
- Legacy commands execute successfully.
- CLI prints migration guidance toward `create`.
- Alias remaps remain active for known renamed commands.

### Stage 2: Soft freeze
- No new features added to legacy commands.
- Bug fixes only for high-severity issues.
- Documentation keeps legacy usage only in migration references.

### Stage 3: Error by default
- Legacy commands fail with a clear error and migration example.
- Temporary escape hatch allowed for one release cycle via env flag (if needed).

### Stage 4: Removal
- Legacy command handlers and aliases are removed.
- Migration doc keeps historical mapping table.

## Suggested rollout dates

Use release tags/versions for final enforcement. Initial target windows:

- Warn: active now
- Soft freeze: next minor release
- Error by default: following minor release
- Removal: next major release

## Operator checklist

- Update docs before moving stages.
- Confirm migration examples still run in CI smoke tests.
- Announce timeline changes in release notes.
- Keep `docs/MIGRATION.md` synchronized with live CLI behavior.
