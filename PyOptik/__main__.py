from PyOptik import MaterialBank
import argparse
import logging

logger = logging.getLogger(__name__)


def main() -> None:
    """Command line entry point for downloading material libraries."""
    parser = argparse.ArgumentParser(description="Download material library")
    parser.add_argument(
        "library",
        nargs="?",
        default="all",
        help="Library name to download (default: 'all')",
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
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    if args.list_libraries:
        for lib in MaterialBank.list_available_libraries():
            print(lib)
        return

    logger.info("Building material library")
    MaterialBank.build_library(args.library, remove_previous=args.remove_previous)


if __name__ == "__main__":
    main()
