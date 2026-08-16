from PyOptik import MaterialBank
import argparse
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def main() -> None:
    """Run the PyOptik material-library command line interface.

    The default command downloads one of PyOptik's curated libraries.  Use
    ``download-all`` to mirror every material page exposed by the upstream
    refractiveindex.info catalog into the local hierarchical data store.
    """
    parser = argparse.ArgumentParser(
        description="Download curated or upstream PyOptik material libraries"
    )
    parser.add_argument(
        "library",
        nargs="?",
        default="all",
        help="Library name, or 'download-all' for the complete upstream catalog",
    )
    parser.add_argument(
        "--remove-previous",
        action="store_true",
        help="Remove previously downloaded files before downloading",
    )
    parser.add_argument(
        "--list-libraries",
        action="store_true",
        help="List available library names and exit",
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
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    if args.list_libraries:
        for lib in MaterialBank.list_available_libraries():
            print(lib)
        return

    if args.library == "download-all":
        if args.remove_previous:
            parser.error(
                "--remove-previous cannot be combined with the download-all command; "
                "use --force to refresh cached upstream pages"
            )
        logger.info("Updating the upstream material catalog")
        MaterialBank.update_catalog(data_root=args.data_root)
        logger.info("Downloading the complete upstream material catalog")
        MaterialBank.download_all(
            force=args.force,
            continue_on_error=not args.fail_fast,
        )
        return

    logger.info("Building material library")
    MaterialBank.build_library(args.library, remove_previous=args.remove_previous)


if __name__ == "__main__":
    main()
