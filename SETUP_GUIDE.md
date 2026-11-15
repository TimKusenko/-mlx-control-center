# Setup Guide

How to get MLX Control Center running from scratch.

---

## Overview – What You'll Have

```
Your Computer          SSH          Your Mac
┌─────────────────────┐       ┌───────┐      ┌──────────────┐
│ $ mlx chat          │       │ SSH   │      │ MLX Server   │
│ > Ask questions     │──────►│       │─────►│ AI Model     │
│ < Get answers       │◄──────│ Tunnel│◄─────│ (Llama, etc) │
└─────────────────────┘       └───────┘      └──────────────┘
```

**Result**: Chat with AI models from your computer. Models run on your Mac.

---

## Prerequisites – What You Already Have

- ✅ A Mac mini (or any Mac)
- ✅ A Linux laptop/PC (or Mac)
- ✅ Both on same WiFi
- ✅ SSH enabled on Mac (default: yes)
- ✅ Python 3.9+ installed

---

## Step 1: Prepare Your Mac – Install MLX

### What is MLX?

MLX = Machine Learning on Apple Silicon. It's the framework that runs the AI models efficiently on Mac.

**On your Mac (open Terminal or SSH into it):**

### 1a. Install Homebrew (if you don't have it)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 1b. Install MLX and dependencies

```bash
# Install MLX
brew install python@3.11

# Create a working directory for MLX
mkdir -p ~/mlx-server
cd ~/mlx-server

# Create Python environment
python3.11 -m venv venv
source venv/bin/activate

# Install ML libraries
pip install mlx mlx-lm huggingface_hub

# Download a model (this takes 5-10 min, ~4 GB)
huggingface-cli download mlx-community/Llama-2-7b-4bit --repo-type model
```

Now you have:
- ✅ MLX installed
- ✅ Python environment ready
- ✅ Llama 2 model downloaded

### 1c. Start the MLX API Server

**Still on Mac, in Terminal:**

```bash
cd ~/mlx-server
source venv/bin/activate

# Create a simple API server script (or use your existing one)
cat > server.py << 'EOF'
from mlx_lm import load, generate
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import threading

model, tokenizer = load("mlx-community/Llama-2-7b-4bit")

class APIHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/v1/chat/completions":
            content_length = int(self.headers['Content-Length'])
            body = json.loads(self.rfile.read(content_length))
            
            prompt = body['messages'][-1]['content']
            response = generate(model, tokenizer, prompt=prompt, verbose=False)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "choices": [{"message": {"content": response}}]
            }).encode())
        elif self.path == "/status":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "model": "llama-2-7b"}).encode())

server = HTTPServer(('127.0.0.1', 8080), APIHandler)
print("MLX Server running on http://127.0.0.1:8080")
server.serve_forever()
EOF

# Run the server
python server.py
```

**Leave this Terminal open!** The server is now running.

You'll see:
```
MLX Server running on http://127.0.0.1:8080
```

✅ **Mac side is done!** Keep this terminal open.

---

## Step 2: Prepare Your Laptop – Install the Control Tool

**On your Linux/Mac laptop, open Terminal (new one, NOT the Mac one):**

### 2a. Make sure Python is installed

```bash
python3 --version
# Should show 3.9 or higher
```

### 2b. Install the MLX Control Center

```bash
pip install mlx-control-center
```

### 2c. First-time setup

```bash
mlx init
```

It will ask:

```
=== MLX CONTROL CENTER SETUP ===

Step 1: SSH to Mac mini
SSH host [user@your-mac.local]: tim@192.168.178.49
```

(Replace `tim` with your Mac username, `192.168.178.49` with your Mac's IP)

Find your Mac's IP:
```bash
# On your Mac:
ifconfig | grep inet
```

Then it asks:
```
Step 2: API URL
API URL [http://127.0.0.1:8080]: http://192.168.178.49:8080
```

(Change the IP to your Mac's IP, NOT localhost!)

Then:
```
Step 3: API Key
API key (hidden): test-key
```

(Just type anything for now, we'll make it proper later)

Done!

---

## Step 3: Test It

**Still on your laptop:**

```bash
mlx status
```

You should see:
```
============================================================
       MLX CONTROL CENTER v2.0
============================================================
🌐 API: ONLINE  |  Model: llama-2-7b-4bit  |  Backend: 🟢 running
🖥️  Mac: your-mac-name | 8 cores
   RAM: 4.2 / 16.0 GB  |  SSD: 245.3 / 500.0 GB
------------------------------------------------------------
```

If you see **"API: OFFLINE"**, check:
1. Is the Mac terminal still running `python server.py`?
2. Is the IP address correct?
3. Is SSH working? Test: `ssh tim@192.168.178.49 'echo hello'`

---

## Step 4: Chat!

**On your laptop:**

```bash
mlx chat
```

Follow the menu:
```
=== Select model family ===
 1. Llama
 0. Cancel

Choice > 1

=== Select size ===
 1. 7B
 0. Cancel

Choice > 1

=== Select quantization ===
 1. 4-bit   mlx-community/Llama-2-7b-4bit
 0. Cancel

Choice > 1

Model: mlx-community/Llama-2-7b-4bit
Commands: /exit /clear /stats

Du > Explain Python in one sentence

Generiere...

KI > Python is a high-level programming language known for 
     its simplicity and readability, widely used in data 
     science and web development.

Du > /exit
```

✅ **It works!**

---

## Common Commands

Once you've done setup, just use:

```bash
mlx              # Open menu (all options)
mlx chat         # Quick chat
mlx status       # Check if everything works
mlx monitor      # Watch Mac CPU/RAM
mlx logs         # See errors
```

---

## Troubleshooting

### "API: OFFLINE"

**On your Mac**, check the server is still running:
```bash
curl http://127.0.0.1:8080/status
```

Should show: `{"status": "ok"}`

If not, restart the server:
```bash
cd ~/mlx-workspace
source venv/bin/activate
python server.py
```

### "Mac: Unreachable"

Test SSH:
```bash
ssh tim@192.168.178.49 'uname -a'
```

Should show Mac OS info. If fails, check:
- Is the IP correct?
- Is SSH enabled on Mac? (System Preferences → Sharing → Remote Login)

### Very slow responses

Normal for first response (model loads). After that should be ~1-2 seconds.

If very slow every time:
- Mac might not have enough RAM
- Model might be too big for your Mac

Try a smaller model:
```bash
mlx models
# Download a smaller model (1B instead of 7B)
```

---

## Advanced: More Models

Want more models? On your laptop:

```bash
mlx models
# → "Search & download"
# → Search for "Llama-3.2-1B" 
# → Download
```

Or on Mac directly:
```bash
cd ~/mlx-workspace
source venv/bin/activate
huggingface-cli download mlx-community/Mistral-7B-4bit
```

---

## Summary – What Happened

1. **Mac**: Installed MLX + started API server
2. **Laptop**: Installed control tool + connected to Mac
3. **Result**: Chat with AI from laptop, models run on Mac

Everything stays on your Mac. Nobody else sees your data. Just you and your models.

---

## What's Next?

- Edit system prompts: `mlx config` → "Set system prompt"
- Monitor Mac: `mlx monitor`
- Check errors: `mlx logs`
- Add more models: `mlx models` → "Search & download"

**Happy chatting!** 🚀
