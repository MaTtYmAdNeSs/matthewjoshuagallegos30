"""psutil_polyfill

Provides a safe, optional wrapper around psutil with pure-Python
/proc-based fallbacks suitable for Android/Termux when psutil
is unavailable or fails to build.
"""

import time
import os

try:
    import psutil  # type: ignore
except Exception:
    psutil = None


def _read_proc_stat():
    """Read /proc/stat and return list of cpu counters (integers).
    Returns None if file is not available.
    """
    try:
        with open("/proc/stat", "r") as f:
            for line in f:
                if line.startswith("cpu "):
                    parts = line.split()
                    vals = [int(x) for x in parts[1:]]
                    return vals
    except Exception:
        return None
    return None


def cpu_percent(interval=0.1):
    """Approximate CPU percentage over an interval using /proc/stat.
    If psutil is available it will be used instead.
    """
    if psutil:
        try:
            return psutil.cpu_percent(interval=interval)
        except Exception:
            pass

    a = _read_proc_stat()
    time.sleep(interval)
    b = _read_proc_stat()
    if not a or not b:
        return None

    idle_a = a[3] + (a[4] if len(a) > 4 else 0)
    idle_b = b[3] + (b[4] if len(b) > 4 else 0)
    total_a = sum(a)
    total_b = sum(b)
    idle = idle_b - idle_a
    total = total_b - total_a
    if total == 0:
        return 0.0
    return (1.0 - idle / total) * 100.0


def virtual_memory():
    """Return a dict with total/available/used/free similar to psutil.virtual_memory().
    Values are in bytes. If psutil available it will be used instead.
    """
    if psutil:
        try:
            vm = psutil.virtual_memory()
            return {"total": vm.total, "available": vm.available, "used": vm.used, "free": vm.free}
        except Exception:
            pass

    info = {}
    try:
        with open("/proc/meminfo", "r") as f:
            for line in f:
                key, val = line.split(":", 1)
                info[key.strip()] = int(val.strip().split()[0])  # kB
    except Exception:
        return None

    total = info.get("MemTotal") * 1024 if info.get("MemTotal") else None
    free = info.get("MemFree") * 1024 if info.get("MemFree") else None
    available = info.get("MemAvailable") * 1024 if info.get("MemAvailable") else free
    used = (total - free) if (total and free) else None
    return {"total": total, "available": available, "used": used, "free": free}


def pids():
    """Return list of process ids by listing /proc. Fallback for psutil.pids()."""
    if psutil:
        try:
            return psutil.pids()
        except Exception:
            pass

    pids = []
    try:
        for name in os.listdir("/proc"):
            if name.isdigit():
                pids.append(int(name))
    except Exception:
        return []
    return sorted(pids)


def process_info(pid):
    """Return basic process info (pid, cmdline, rss) similar to psutil.Process(pid)
    Returns a dict or None if not available.
    """
    if psutil:
        try:
            p = psutil.Process(pid)
            return {"pid": pid, "cmdline": p.cmdline(), "rss": p.memory_info().rss}
        except Exception:
            pass

    proc = {}
    try:
        with open(f"/proc/{pid}/cmdline", "r") as f:
            cmd = f.read().replace('\x00', ' ').strip()
            proc["cmdline"] = cmd
    except Exception:
        proc["cmdline"] = None

    try:
        with open(f"/proc/{pid}/status", "r") as f:
            for line in f:
                if line.startswith("VmRSS:"):
                    parts = line.split()
                    proc["rss"] = int(parts[1]) * 1024
                    break
    except Exception:
        proc["rss"] = None

    proc["pid"] = pid
    return proc
