"""Setup coverage tracking for subprocesses.

Any ImportError is silently ignored.
Requires COVERAGE_PROCESS_START in the environments, which gets set in
tox.ini.
"""
import coverage

coverage.process_startup()
