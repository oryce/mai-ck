#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import Path

from dotenv import load_dotenv

from .command.process import command as process_cmd
from .command.run import command as run_cmd


def main():
    load_dotenv()

    parser = ArgumentParser(description="Document analysis worker")
    subparsers = parser.add_subparsers()

    run_parser = subparsers.add_parser("run")
    run_parser.set_defaults(func=run_cmd)

    process_parser = subparsers.add_parser("process")
    process_parser.set_defaults(func=process_cmd)
    process_parser.add_argument(
        "document_path",
        metavar="<document_path>",
        type=Path,
        help="Filesystem path (absolute or relative) to the document to process",
    )
    process_parser.add_argument(
        "-t",
        dest="allowed_types",
        metavar="<document_type>",
        action="append",
        help="Allowed document types (e.g. 'счёт', 'накладная')",
    )
    process_parser.add_argument(
        "model",
        metavar="<model>",
        help="Name of the Ollama model to use for document processing",
    )

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
