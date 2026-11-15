# Agent container. Tooling preinstalled so each task starts in seconds.
FROM python:3.12-bookworm
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && apt-get install -y nodejs && rm -rf /var/lib/apt/lists/*
RUN npm i -g @openai/codex
RUN curl -fsSL https://claude.ai/install.sh | bash && ln -sf /root/.local/bin/claude /usr/local/bin/claude
RUN curl -LsSf https://astral.sh/uv/0.13.5/install.sh | env UV_UNMANAGED_INSTALL=/root/.local/bin sh
COPY pyproject.toml uv.lock /bundle/codex-v1.0.0/
RUN cd /bundle/codex-v1.0.0 && (/root/.local/bin/uv sync --frozen --no-install-project || /root/.local/bin/uv sync --frozen)
COPY probe /usr/local/bin/probe
RUN chmod +x /usr/local/bin/probe && ln -s /usr/local/bin/probe /usr/local/bin/snapshot
WORKDIR /workspace
