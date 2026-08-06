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
                MessageData(file=str(compress_if_video(path)))
            )

    bot.rpc.send_reaction(accid, msg.id, ["✅"])


def compress_if_video(path: Path) -> Path:
    video_extensions = {
        ".mp4", ".mkv", ".webm", ".mov", ".avi",
        ".flv", ".wmv", ".m4v", ".ts", ".mts",
    }

    if path.suffix.lower() not in video_extensions:
        return path

    output = path.with_suffix(".mp4")

    if output.exists() and output.is_file():
        return output

    subprocess.run(
        [
            "ffmpeg",
            "-nostdin",
            "-loglevel", "error",
            "-y",
            "-i", str(path),
            "-map", "0:v:0",
            "-map", "0:a?",
            "-c:v", "libx264",
            "-crf", "27",
            "-preset", "slow",
            "-c:a", "copy",
            "-movflags", "+faststart",
            str(output),
        ],
        check=True,
    )

    if output != path:
        path.unlink()

    return output


if __name__ == "__main__":
    cli.start()
