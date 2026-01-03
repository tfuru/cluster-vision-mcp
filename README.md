# cluster-vision-mcp
指定パスの画像を LM Studio に送信して、オブジェクト位置や名前などを解析した結果を取得する MCP(Model Context Protocol)サーバー

## 概要

このプロジェクトは、ローカル環境で動作する **LM Studio** の推論機能を利用して、画像の解析を行う **MCP (Model Context Protocol)** サーバーです。
指定されたローカルの画像ファイルを LM Studio のローカルサーバー API (OpenAI 互換) に送信し、画像に映っているオブジェクトの名前や位置、シーンの説明などをテキストで取得することができます。
これにより、Claude などの MCP クライアントから、ローカルのLLMパワーを活用して画像認識タスクを実行可能になります。
## 主な機能 (Tools)

### 画像解析
- `analyze_image`: 指定した画像を解析して、オブジェクト位置や名前などを解析した結果を取得します。

## LM Studio の準備

このサーバーを使用するには、LM Studio が以下の状態で起動している必要があります。

1.  **LM Studio を起動** してください。
2.  **Vision 対応モデル** (例: `gemma-3-4b-it`, `Qwen-VL`, `LLaVA` など) をロードしてください。
    *   ※ 通常のテキスト専用モデルでは画像解析はできません。
3.  **Local Server** を開始してください。
    *   デフォルトのポートは `1234` です。
    *   API URL の例: `http://localhost:1234`
## 仮想環境の作成と有効化

```
# 1. 仮想環境を作成（フォルダ名は 'venv' が一般的です）
python3 -m venv venv

# 2. 仮想環境を有効化（アクティベート）
source venv/bin/activate

# (プロンプトの左側に (venv) と表示されれば成功です)
```

## 依存関係のインストール

```
pip install -r requirements.txt
```

## MCPサーバーの設定

設置場所の venv/bin/python のフルパスを指定してください。  
```
{
  "mcpServers": {
    "cluster-vision-mcp": {
      "command": "[pwd]/server/venv/bin/python",
      "args": [
        "[pwd]/server/main.py"
      ],
      "env": {
        "API_URL": "http://192.168.10.106:1234",
        "MODEL_NAME": "gemma-3n-e4b-it-mlx"
      },
    }
  }
}
```