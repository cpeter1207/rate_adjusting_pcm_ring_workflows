# rate_adjusting_pcm_ring workflows

This repository owns the reusable GitHub Actions implementations for
[rate_adjusting_pcm_ring](https://github.com/cpeter1207/rate_adjusting_pcm_ring).
The production repository contains only thin callers, so workflow-only changes
do not start source builds. Production callers follow this repository's `main`
branch so validated workflow fixes take effect without a production-source
change.

The required quality workflow performs formatting, static analysis, and
Doxygen once, then builds, tests, packages, and stages installation on native
Debian 13 amd64 and arm64 runners. Production coverage is required on amd64.
With `fast_only: true`, pushes run only formatting, lint, and static analysis.
Debian 12 is manual-only and is not part of ordinary automation.
Workflow validation is intentionally independent: a workflow repair can merge
even when a production-quality defect is outstanding. Release artifact contract
tests run with `python3 -m unittest discover -s tests -v` on Linux; they exercise
archive staging and package paths without building or publishing production code.

The reusable release workflow requires an immutable tag at a merged main
revision and the latest successful required quality check on its merged
pull request's head. It fetches the released sample-rate adapter packages and
publishes the canonical-F32 ABI-major-three library, source archive, and Debian
13 amd64/arm64 packages without rerunning the quality gate.

ABI 3 artifacts use the `abi3` archive directory, `rate_adjusting_pcm_ring3`
header/pkg-config namespace, SONAME `librate_adjusting_pcm_ring3.so.3`, and
`librate-adjusting-pcm-ring3` / `librate-adjusting-pcm-ring3-dev` packages.
ABI 2 consumers must migrate before using these artifacts. Quality and release
default to samplerate-adapter `v0.1.0-alpha.3`; its adapter ABI remains 1.

After publication, the workflow refreshes the USBRadioPlus APT index. The
source repository must provide an `APT_INDEX_DISPATCH_TOKEN` fine-grained PAT
with `Contents: write` access only to `cpeter1207/USBRadioPlus`.
