import sys
from timeit import default_timer

from ..pipeline import Result, Status
from ..pipeline import run as run_pipeline


def command(args):
    if len(args.allowed_types) == 0:
        print(
            "Error: No allowed document types passed. Specify them with `-t`.",
            file=sys.stderr,
        )
        sys.exit(1)

    start = default_timer()

    print("Starting processing pipeline...")

    for value in run_pipeline(args.document_path, args.allowed_types, args.model):
        if isinstance(value, Status):
            print(f"Status: {value}")
        elif isinstance(value, Result):
            print("Processing results:")
            print(f"  * document type: {value.type}")
            print(f"  * has signature: {value.signature}")
            print(f"  * has stamp: {value.stamp}")

            end = default_timer()
            print(f"Took {end - start:.2f}s")
