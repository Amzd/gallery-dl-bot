import re
import subprocess
from pathlib import Path
from deltabot_cli import BotCli
from deltachat2 import MessageData, events

cli = BotCli("gallerybot")

URL_RE = re.compile(r"https?://[^\s]+")

@cli.on(events.NewMessage)
def echo(bot, accid, event):
    msg = event.msg

    if not msg.text:
        return

    match = URL_RE.search(msg.text)
    if not match:
        return

    url = match.group(0)

    # React so the user knows we're working
    bot.rpc.send_reaction(accid, msg.id, ["👀"])

    # Download
    result = subprocess.run(
        [
            "gallery-dl",
            "--cookies", "./cookies.txt",
            "--config", "./gallery-dl.conf",
            url,
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        bot.rpc.send_reaction(accid, msg.id, ["⚠️"])
        bot.rpc.send_msg(
            accid,
            msg.chat_id,
            MessageData(text=result.stderr)
        )
        return

    # Send every downloaded file
    files = [
        Path(line.lstrip("# ").strip())
        for line in result.stdout.splitlines()
        if line.strip()
    ]

    for path in files:
        if path.exists() and path.is_file():
            bot.rpc.send_msg(
                accid,
                msg.chat_id,
                MessageData(file=str(path))
            )

    bot.rpc.send_reaction(accid, msg.id, ["✅"])



if __name__ == "__main__":
    cli.start()
