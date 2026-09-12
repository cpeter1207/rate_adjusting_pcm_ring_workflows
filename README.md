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
Debian 12 is manual-only and is not part of ordinary automation.
Workflow validation is intentionally independent: a workflow repair can merge
even when a production-quality defect is outstanding.

The reusable release workflow requires a main revision that already passed the
pull-request gate. It fetches the released sample-rate adapter packages and
publishes the ABI-major-one compatibility facade, canonical-F32 ABI-major-two
library, source archive, and Debian 13 amd64/arm64 packages without rerunning
the quality gate.
