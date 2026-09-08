# rate_adjusting_pcm_ring workflows

This repository owns the reusable GitHub Actions implementations for
[rate_adjusting_pcm_ring](https://github.com/cpeter1207/rate_adjusting_pcm_ring).
The production repository contains only thin callers, so workflow-only changes
do not start source builds. Production callers follow this repository's `main`
branch so validated workflow fixes take effect without a production-source
change.

The required quality workflow performs formatting, static analysis, and
Doxygen once, then tests Debian 12 and 13 on native amd64 and arm64 runners.
Workflow validation is intentionally independent: a workflow repair can merge
even when a production-quality defect is outstanding.

The reusable release workflow reruns that exact quality gate before publishing
a source archive and native Debian 12/13 amd64/arm64 shared-library archives.
