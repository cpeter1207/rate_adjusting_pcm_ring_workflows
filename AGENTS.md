# Workflow development rules

## Shared rpt_advanced project baseline

This baseline applies to every production, shared-library, and workflow
repository in the rpt_advanced project. Repository-specific rules may add
constraints but must not weaken it.

Before a push, run only platform-independent formatting, lint, and static
analysis—including Cppcheck—without rewriting source files. Production
repositories repeat only those fast checks on ordinary pushes. Do not run
Cppcheck in each platform job.

The full quality gate is required for a production pull request to merge. It
runs platform-independent formatting, lint, static analysis, and Doxygen once,
concurrently where independent; then it runs platform-dependent build, tests,
packaging, and staged-install checks concurrently on native Debian 13 amd64
and arm64. It requires 100% line and branch coverage of production code only
on Debian 13 amd64; test code is excluded from coverage. Treat compiler
warnings as errors and fail applicable formatting, Ruff, ShellCheck, Cppcheck,
Clang-Tidy, Doxygen, tests, installation checks, and coverage. Remove
unreachable or dead code instead of suppressing diagnostics or excluding it
from coverage.

Debian 12 support is aspirational: do not run automated Debian 12 tests or
build Debian 12 packages as part of ordinary pushes, pull requests, or
releases. Build Debian 12 packages manually only when explicitly requested.
Automated releases publish Debian 13 packages only; node installations use
Debian 13 arm64 packages. Release workflows run only artifact-specific build
and packaging validation because their main-branch input already passed the
required pull-request gate.

Update concise Doxygen comments, tests, user documentation, examples, and
build, install, and package artifacts whenever an interface changes. Consumers
of a shared project library must use its released, versioned dynamic shared
object rather than vendor or statically link a duplicate implementation.
Preserve published ABI/API compatibility whenever practical; when a change is
necessary, document its compatibility, SONAME/package consequences, and
migration. Start and clean only project-owned, labeled test containers
deterministically. Never deploy to a node or alter its configuration without
explicit approval.

Validate workflow edits with Actionlint. Keep workflow validation independent
from production quality so a broken workflow can be repaired without requiring
an unrelated production build to pass. Required production quality must run
platform-independent checks once and native Debian 13 platform checks on amd64
and arm64, with production coverage on amd64 only.
