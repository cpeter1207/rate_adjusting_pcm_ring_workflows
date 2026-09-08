# Workflow development rules

Validate workflow edits with Actionlint. Keep workflow validation independent
from production quality so a broken workflow can be repaired without requiring
an unrelated production build to pass. Required production quality must run
platform-independent checks once and native platform checks on Debian 12 and
13 for amd64 and arm64.
