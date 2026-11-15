# Sandbox image for behavior-probe runs: agent tooling preinstalled so each task
# skips ~20 min of installs. Agents' setup.sh still runs and finds everything present.
FROM python:3.12-bookworm
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && apt-get install -y nodejs && rm -rf /var/lib/apt/lists/*
RUN npm i -g @openai/codex
RUN curl -fsSL https://claude.ai/install.sh | bash && ln -sf /root/.local/bin/claude /usr/local/bin/claude
RUN curl -LsSf https://astral.sh/uv/0.13.5/install.sh | env UV_UNMANAGED_INSTALL=/root/.local/bin sh
# Pre-sync the codex agent's venv where its run_cmd expects it (.venv is never uploaded with the bundle).
COPY pyproject.toml uv.lock /bundle/codex-v1.0.0/
RUN cd /bundle/codex-v1.0.0 && /root/.local/bin/uv sync --frozen --no-install-project || /root/.local/bin/uv sync --frozen
