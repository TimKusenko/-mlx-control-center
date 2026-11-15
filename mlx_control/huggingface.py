"""Hugging Face model management operations."""
import base64
import logging
import re
import shlex
import subprocess
import urllib.parse
import urllib.request
from typing import List, Optional

logger = logging.getLogger(__name__)


class HuggingFaceManager:
    """Manage MLX models from Hugging Face."""

    def __init__(self, ssh_client):
        self.ssh = ssh_client

    def search_mlx_community(self, family: str) -> List[str]:
        """Search for quantized models in mlx-community."""
        if not family or len(family) > 60:
            raise ValueError("Invalid search term")

        if not re.fullmatch(r"[A-Za-z0-9._ -]+", family):
            raise ValueError("Invalid characters in search")

        query = urllib.parse.urlencode({
            "author": "mlx-community",
            "search": family,
            "limit": 100
        })
        url = f"https://huggingface.co/api/models?{query}"

        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "MLX-Control-Center/2.0"}
            )
            with urllib.request.urlopen(req, timeout=18) as response:
                import json
                found = json.load(response)
        except Exception as exc:
            logger.error(f"Hugging Face search failed: {exc}")
            raise

        entries = []
        for item in found:
            repo = item.get("id", "")
            if not repo.startswith("mlx-community/"):
                continue
            if item.get("private") or item.get("gated"):
                continue
            # Only quantized models
            if not re.search(
                r"(?:^|[-_])(?:[348]|5|6)[-_]?bit(?:$|[-_])|(?:^|[-_])(?:Q[34568])(?:$|[-_])",
                repo,
                re.I
            ):
                continue
            entries.append(repo)

        return sorted(set(entries), key=str.lower)[:60]

    def list_cache(self) -> None:
        """List cached models on Mac."""
        script = r'''import json,sys
from pathlib import Path
from huggingface_hub import scan_cache_dir

cache = scan_cache_dir()
for r in sorted(cache.repos, key=lambda r: r.repo_id.lower()):
    if r.repo_type == "model":
        size_gb = round(r.size_on_disk / (1024**3), 2)
        print(f"{r.repo_id} | {size_gb} GiB | {len(r.revisions)} revisions")
if cache.warnings:
    print("WARNING: Cache has unreadable entries", file=sys.stderr)
'''
        self._run_hf_script("list", script)

    def download_model(self, repo_id: str) -> None:
        """Download model from Hugging Face to Mac."""
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*/[A-Za-z0-9][A-Za-z0-9_.-]*", repo_id):
            raise ValueError(f"Invalid repo ID: {repo_id}")

        if not repo_id.startswith("mlx-community/"):
            raise ValueError("Security: Only mlx-community repos allowed")

        script = f'''import json,sys
from pathlib import Path
from huggingface_hub import HfApi, snapshot_download
import shutil

repo = "{repo_id}"
info = HfApi().model_info(repo, files_metadata=True)
files = [x for x in info.siblings if x.rfilename.endswith((".safetensors", ".gguf"))]
if not files or any(x.size is None for x in files):
    sys.exit("Weight files/sizes not verifiable")
required = sum(x.size for x in files)
if required > 10 * 1024**3:
    sys.exit("Model >10 GiB: security limit exceeded")
free = shutil.disk_usage(Path.home()).free
if free < required + 5 * 1024**3:
    sys.exit("Not enough free space (need model size + 5 GiB)")
print(f"Downloading {{repo}}...")
path = snapshot_download(repo_id=repo, repo_type="model", local_files_only=False)
print(f"Done: {{path}}")
'''
        self._run_hf_script("download", script, interactive=True)

    def delete_model(self, repo_id: str) -> None:
        """Delete model from Mac cache."""
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*/[A-Za-z0-9][A-Za-z0-9_.-]*", repo_id):
            raise ValueError(f"Invalid repo ID: {repo_id}")

        script = f'''import json,sys
from huggingface_hub import scan_cache_dir

cache = scan_cache_dir()
if cache.warnings:
    sys.exit("Cache warnings present: delete denied for safety")
matches = [r for r in cache.repos if r.repo_type == "model" and r.repo_id == "{repo_id}"]
if len(matches) != 1:
    sys.exit("Repository not found in cache")
r = matches[0]
revs = [v.commit_hash for v in r.revisions]
if not revs:
    sys.exit("No revisions to delete")
strategy = cache.delete_revisions(*revs)
freed_gb = round(strategy.expected_freed_size / (1024**3), 2)
print(f"Freeing: {{freed_gb}} GiB")
strategy.execute()
print("Cache deleted.")
'''
        self._run_hf_script("delete", script, interactive=True)

    def _run_hf_script(self, action: str, script: str, interactive: bool = False) -> None:
        """Execute Hugging Face operation on Mac."""
        encoded = base64.b64encode(script.encode()).decode()
        launcher = f"import base64;exec(compile(base64.b64decode({repr(encoded)!r}),\"<hf>\",\"exec\"))"
        remote_cmd = f"~/security-ai/.venv/bin/python -c {shlex.quote(launcher)}"

        args = ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=8"]
        args += ["-tt" if interactive else "-T"]
        args += [self.ssh.host, remote_cmd]

        import os
        env = dict(os.environ)
        if interactive:
            env["TERM"] = "xterm-256color"

        result = subprocess.run(args, env=env, check=False)
        if result.returncode and result.returncode != 130:
            logger.error(f"Hugging Face operation failed: {action} (code {result.returncode})")
