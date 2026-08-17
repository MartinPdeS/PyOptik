import argparse
import logging
from pathlib import Path
import sys

from PyOptik import MaterialCatalog

logger = logging.getLogger(__name__)


def main() -> None:
    """Run the PyOptik material-library command line interface.

    The default command downloads the complete upstream material snapshot.
    Use ``download-all`` for the explicit catalog download command or its
    page-based fallback mode.
    """
    parser = argparse.ArgumentParser(
        description="Set up or download the canonical PyOptik material catalog"
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="setup",
        choices=("setup", "download-all"),
        help="Canonical catalog command (default: setup)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable detailed download and material-loading logs",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-download upstream pages that are already cached",
    )
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="Stop the complete upstream download at the first failed page",
    )
    parser.add_argument(
        "--data-root",
        type=Path,
        default=None,
        help="Root directory for the complete upstream catalog",
    )
    parser.add_argument(
        "--source",
        choices=("snapshot", "pages"),
        default="snapshot",
        help="Download source: one upstream snapshot (default) or individual pages",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=8,
        help="Concurrent page downloads when --source=pages (default: 8)",
    )
    parser.add_argument(
        "--no-progress",
        action="store_true",
        help="Disable the snapshot download progress bar",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    if args.command == "setup" and args.source != "snapshot":
        parser.error("setup always uses the upstream snapshot; use download-all for page mode")
    source = "snapshot" if args.command == "setup" else args.source
    logger.info(
        "Setting up the upstream material catalog"
        if args.command == "setup"
        else "Updating the upstream material catalog"
    )

    def show_progress(downloaded: int, total: int) -> None:
        """Render snapshot download progress on the terminal."""
        width = 30
        if total:
            complete = min(width, int(width * downloaded / total))
            bar = "=" * complete + ">" + " " * max(0, width - complete - 1)
            percent = 100 * downloaded / total
            message = (
                f"\rDownloading snapshot [{bar}] {percent:5.1f}% "
                f"({downloaded / 1024**2:.1f}/{total / 1024**2:.1f} MiB)"
            )
        else:
            message = f"\rDownloading snapshot: {downloaded / 1024**2:.1f} MiB"
        print(message, end="", file=sys.stderr, flush=True)

    progress = None if args.no_progress else show_progress
    if source == "snapshot":
        catalog = MaterialCatalog.from_snapshot(
            data_root=args.data_root,
            force=args.force,
            progress=progress,
        )
    else:
        catalog = MaterialCatalog.from_upstream(data_root=args.data_root)
    if progress:
        print(file=sys.stderr)
    logger.info(
        "Finalizing the complete upstream material catalog"
        if source == "snapshot"
        else "Downloading the complete upstream material catalog"
    )
    if source == "snapshot":
        logger.info("Snapshot download complete; material pages are already available locally")
        return
    catalog.download_all(
        force=args.force,
        continue_on_error=not args.fail_fast,
        workers=args.workers,
    )


if __name__ == "__main__":
    main()
