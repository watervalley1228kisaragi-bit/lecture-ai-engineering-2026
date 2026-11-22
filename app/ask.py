"""第1回: 素のLLMに質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする
    uv run python -m app.ask --interactive "LoRAとは何ですか？"

通常モードは1回だけ質問する。--interactive を指定すると会話履歴を保って
続けて質問できる。どちらもツールを持たない「素の」呼び出し。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse
import time

from google import genai
from google.genai.chats import Chat
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"

# グローバルでクライアントを生成して保持する
client = genai.Client(api_key=get_api_key())

def create_chat() -> Chat:
    # 保持しているグローバルな client からチャットを作成する
    return client.chats.create(model=MODEL)


def ask(question: str, chat: Chat | None = None) -> str:
    if chat is None:
        chat = create_chat()
    started_at = time.perf_counter()
    response = chat.send_message(question)
    elapsed = time.perf_counter() - started_at

    print(f"[応答時間] {elapsed:.2f} 秒")
    usage = response.usage_metadata
    if usage is None:
        print("[トークン数] 利用情報なし")
    else:
        print(
            f"[トークン数] 入力: {usage.prompt_token_count}, "
            f"出力: {usage.candidates_token_count}"
        )

    return response.text


def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMに質問する")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    parser.add_argument("-i", "--interactive", action="store_true", help="会話履歴を保って続けて質問する")
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    print(f"[質問] {args.question}\n")
    try:
        if not args.interactive:
            print(ask(args.question))
            return

        chat = create_chat()
        print(ask(args.question, chat))
        print("\n追加の質問を入力してください（exit / quit / 終了 で終了）。")
        while True:
            try:
                question = input("質問> ").strip()
            except EOFError:
                print()
                break
            if question.lower() in {"exit", "quit", "終了"}:
                break
            if question:
                print(f"\n[質問] {question}\n")
                print(f"{ask(question, chat)}\n")
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
