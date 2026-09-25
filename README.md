# rate_adjusting_pcm_ring workflows

This repository owns the reusable GitHub Actions implementations for
[rate_adjusting_pcm_ring](https://github.com/cpeter1207/rate_adjusting_pcm_ring).
The production repository contains only thin callers, so workflow-only changes
do not start source builds. Production callers follow this repository's `main`
branch so validated workflow fixes take effect without a production-source
change.

Production thin callers invoke the reusable push-check workflow for ordinary
pushes. It runs only formatting, lint, and static analysis. Pull-request
callers invoke the required full quality workflow: it performs formatting,
lint, static analysis, and Doxygen once, then verifies native Debian 13 amd64
and arm64 builds, tests, packaging, and staged installation, with production
coverage on amd64. A production repository must require its `Required quality
gate` status before merging a pull request.

The Rust ABI-major-2 ring uses the independently released
`rptadv-samplerate-adapter` shared object. Reusable workflows download one
matching released runtime package and one development package for each native
architecture, install them only in a disposable quality image, and then build
both the frozen ABI-major-1 and Rust ABI-major-2 packages together. The
adapter repository and immutable tag are workflow inputs; their defaults are
`cpeter1207/rptadv-samplerate-adapter` and `v0.1.0-alpha.1`.

After a validated change reaches `main`, a separate reusable documentation
workflow rebuilds and publishes its Doxygen Pages site. Workflow validation is
intentionally independent: a workflow repair can merge even when a production
quality defect is outstanding.

The reusable release workflow does not rerun the full quality gate. It assumes
the merged main revision has already passed the required pull-request gate and
first verifies that the requested revision is an ancestor of `main`. It then
performs only artifact-specific source/archive, co-installable ABI-major-1 and
ABI-major-2 shared-library, and Debian 13 amd64/arm64 package build validation
before publishing. Debian 12 artifacts remain manual-only.
