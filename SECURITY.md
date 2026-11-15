# Security Policy

## API Key Storage

The API key is stored securely at `~/.config/mlx-api/api-key` with permissions `0600` (readable only by owner).

**Never**:
- Commit the key file to version control
- Share the key in issues or pull requests
- Export it to environment variables in production

**Always**:
- Use `mlx init` to set up credentials
- Keep your SSH key protected (key-based auth only)
- Rotate the API key if compromised

## SSH Access

This tool communicates with your Mac mini over SSH. Security best practices:

1. **Use SSH keys**, not passwords
   ```bash
   ssh-copy-id user@your-mac
   ```

2. **Restrict SSH access** on Mac:
   ```bash
   # Edit /etc/ssh/sshd_config
   PermitRootLogin no
   PasswordAuthentication no
   PubkeyAuthentication yes
   ```

3. **Use SSH config** for convenience:
   ```bash
   # ~/.ssh/config
   Host mac
     HostName your-mac.local
     User tim
     IdentityFile ~/.ssh/id_ed25519
   ```

4. **Firewall**: Restrict SSH to trusted networks only

## Reporting Vulnerabilities

If you discover a security vulnerability, please email:
**timkusenko.tk@gmail.com**

Do NOT open a public GitHub issue for security vulnerabilities.

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact

## Dependencies

This tool has **zero runtime dependencies** (uses Python standard library only):
- `urllib` – HTTP requests
- `json` – Data parsing
- `subprocess` – SSH execution
- `pathlib` – File handling

No external packages to audit or update.

## Security Scanning

The project uses GitHub Actions to run:
- `pytest` – Unit tests
- `black` – Code formatting
- `mypy` – Type checking

All commits are scanned for secrets before merge.
