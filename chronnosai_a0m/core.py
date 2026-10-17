"""Core runtime helpers for the Chronnos AI / A0M project.

These helpers intentionally avoid pinning psutil so they remain usable on
Android/Termux and packaging environments where native C-extension builds are
unreliable.
"""

from __future__ import annotations

from .psutil_polyfill import cpu_percent, virtual_memory, pids, process_info

__all__ = [
    "cpu_percent",
    "virtual_memory",
    "pids",
    "process_info",
]
