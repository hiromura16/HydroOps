FROM python:3.12-slim
WORKDIR /app

# tzdata をインストールしてタイムゾーンを設定
RUN apt-get update \
 && apt-get install -y tzdata \
 && ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime \
 && dpkg-reconfigure --frontend noninteractive tzdata \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
 
# uv を公式インストーラーで追加
RUN apt-get update \
 && apt-get install -y curl \
 && rm -rf /var/lib/apt/lists/* \
 && curl -LsSf https://astral.sh/uv/install.sh | sh

# uv のバイナリパスを通す
ENV PATH="/root/.local/bin:${PATH}"

# 依存定義ファイルを先にコピー（ロックファイルが必要）
COPY pyproject.toml uv.lock ./

# uv で仮想環境作成＆依存インストール
RUN uv venv && uv sync

# アプリケーションコードをコピー
COPY main.py requirements.txt config.json config.csv ./

# Entrypoint
CMD ["uv", "run", "--", "python", "main.py", "--config", "config.json"]
