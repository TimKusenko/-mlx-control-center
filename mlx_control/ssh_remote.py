"""SSH operations for remote Mac control."""
import base64
import json
import logging
import os
import shlex
import subprocess
from typing import Any, Dict

logger = logging.getLogger(__name__)


class SSHClient:
    """Execute commands on remote Mac via SSH."""

    def __init__(self, host: str):
        self.host = host

    def run(self, command: str, interactive: bool = False) -> int:
        """Execute command on remote host."""
        args = ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=8"]
        env = dict(os.environ)

        if interactive:
            env["TERM"] = "xterm-256color"
            args += ["-tt"]
        else:
            args += ["-T"]

        args += [self.host, command]

        logger.debug(f"Running SSH: {' '.join(args)}")
        result = subprocess.run(args, env=env, check=False)

        if result.returncode == 255:
            logger.warning("SSH connection failed")

        return result.returncode

    def run_json(self, script: str) -> Dict[str, Any]:
        """Execute Python script and return JSON output."""
        cmd = "python3 -c " + shlex.quote(script)
        args = [
            "ssh",
            "-T",
            "-o",
            "BatchMode=yes",
            "-o",
            "ConnectTimeout=5",
            self.host,
            cmd,
        ]

        logger.debug(f"Running remote script ({len(script)} bytes)")
        result = subprocess.run(args, capture_output=True, text=True, timeout=12, check=False)

        if result.returncode:
            error_msg = result.stderr.strip() or "Remote host unreachable"
            logger.error(f"Remote execution failed: {error_msg}")
            raise RuntimeError(error_msg)

        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            logger.error(f"Invalid JSON from remote: {result.stdout}")
            raise RuntimeError("Remote returned invalid JSON") from exc

    def get_hardware_info(self) -> Dict[str, Any]:
        """Fetch hardware info from Mac."""
        script = '''import json,os,platform,subprocess,re

def sysctl(k):
    p = subprocess.run(['/usr/sbin/sysctl', '-n', k], capture_output=True, text=True)
    return p.stdout.strip() if p.returncode == 0 else '?'

def cmd(a):
    p = subprocess.run(a, capture_output=True, text=True)
    return p.stdout.strip() if p.returncode == 0 else '?'

mem = int(sysctl('hw.memsize'))
page = cmd(['/usr/bin/vm_stat'])
page_size = 4096
m = re.search(r'page size of (\\d+) bytes', page)
if m: page_size = int(m.group(1))
values = {k: int(v.replace('.', '')) for k, v in re.findall(r'^([^:]+):\\s*(\\d+)\\.', page, re.M)}
free = (values.get('Pages free', 0) + values.get('Pages speculative', 0)) * page_size
used = max(0, mem - free)
st = os.statvfs(os.path.expanduser('~'))
print(json.dumps({
    'machine': platform.machine(),
    'cpu': sysctl('machdep.cpu.brand_string'),
    'cores': sysctl('hw.ncpu'),
    'memory_total': mem,
    'memory_approx_used': used,
    'disk_total': st.f_blocks * st.f_frsize,
    'disk_free': st.f_bavail * st.f_frsize,
    'hostname': platform.node()
}))'''
        return self.run_json(script)

    def btop(self) -> int:
        """Run btop on remote Mac."""
        return self.run("/opt/homebrew/bin/btop", interactive=True)

    def nettop(self) -> int:
        """Run nettop on remote Mac."""
        return self.run("/usr/bin/nettop", interactive=True)

    def tail_log(self, log_path: str) -> int:
        """Tail a log file interactively."""
        return self.run(f"tail -n 80 -f {log_path}", interactive=True)
