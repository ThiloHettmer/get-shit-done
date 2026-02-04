# GSD Local Usage & OpenCode Guide

This guide explains how to use your modified version of GSD across projects and how to set it up with local models via LM Studio.

## 1. Using Your Modified GSD

Since you've modified the source code, you need to "install" your local version so that the runtimes (Claude Code, Gemini, OpenCode) can see your changes.

### Option A: Update Global Installation (Recommended)

This makes your changes available to **all** projects on your machine by updating the global config directories (`~/.claude`, `~/.gemini`, etc.).

```bash
# Run from the root of your modified get-shit-done repo
node bin/install.js --global --all
```

### Option B: Local Project Installation

If you want to install your modified version into a specific project without affecting your global setup:

```bash
# 1. Go to your target project folder
cd /path/to/your/project

# 2. Run the installer from your modified repo
node /run/media/thilo/projects/ai/get-shit-done/bin/install.js --local --claude
```

---

## 2. Using OpenCode with LM Studio

OpenCode is the open-source runner for GSD that supports local models.

### Step 1: Install OpenCode GSD Support

```bash
node bin/install.js --opencode --global
```

### Step 2: Configure opencode.json

Edit your OpenCode configuration at `~/.config/opencode/opencode.json` (for Mac/Linux) to point to your LM Studio server.

```json
{
  "provider": "openai",
  "openai": {
    "baseUrl": "http://localhost:1234/v1",
    "apiKey": "lm-studio"
  },
  "model": "YOUR_LOADED_MODEL_ID"
}
```

_Note: Extract the `model` ID from the LM Studio "AI Chat" or "Local Server" tab._

### Step 3: Run OpenCode

In your project directory, simply run:

```bash
opencode
```

All GSD commands (like `/gsd-execute-plan`) will now use your local LM Studio model.

---

## 3. Dynamic Configuration (Your New Features)

In your project's `.planning/config.json`, you can now use the new keys you added:

```json
{
  "agent_type": "gsd-granular",
  "executor_model": "your-specific-model-string"
}
```

- **agent_type**: Switches between executors (e.g., standard vs granular).
- **executor_model**: Forces the executor to use a specific model string, overriding the default quality/balanced/budget mapping.
