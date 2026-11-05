"""企业微信群机器人 Webhook 通知。"""

from __future__ import annotations

import argparse
import sys

import httpx


def send_markdown(webhook_url: str, content: str, *, verify_ssl: bool = True) -> None:
    resp = httpx.post(
        webhook_url,
        json={"msgtype": "markdown", "markdown": {"content": content}},
        timeout=30.0,
        verify=verify_ssl,
    )
    resp.raise_for_status()
    body = resp.json()
    if body.get("errcode", 0) != 0:
        raise RuntimeError(f"企业微信返回错误: {body}")


def main() -> int:
    parser = argparse.ArgumentParser(description="发送企业微信 Webhook 通知")
    parser.add_argument("--webhook", required=True, help="Webhook 完整 URL")
    parser.add_argument("--content", required=True, help="Markdown 正文")
    parser.add_argument(
        "--insecure",
        action="store_true",
        help="跳过 HTTPS 证书校验（与 VERIFY_SSL=false 一致时使用）",
    )
    args = parser.parse_args()
    try:
        send_markdown(args.webhook, args.content, verify_ssl=not args.insecure)
    except Exception as exc:  # noqa: BLE001 — 通知脚本需汇总任意失败
        print(f"通知发送失败: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
