"""Console entrypoint for the PigeonYang cover MCP server.

The package entrypoint keeps the installable command stable while the product
repo owns the actual workflow implementation.
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import sys
from pathlib import Path

from . import __version__


PRODUCT_ROOT_ENV = "PIGEONYANG_COVER_PRODUCT_ROOT"


def source_product_root() -> Path | None:
    """Return the source checkout product root when running from this repo."""
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "mcp-server" / "cover_project_server.py").exists():
            return parent
    return None


def resolve_product_root(value: str | None) -> Path:
    raw = value or os.environ.get(PRODUCT_ROOT_ENV)
    if raw:
        root = Path(raw).expanduser().resolve()
    else:
        root = source_product_root()
        if root is None:
            raise FileNotFoundError(
                "product root is required. Pass --product-root or set "
                f"{PRODUCT_ROOT_ENV}."
            )

    server_file = root / "mcp-server" / "cover_project_server.py"
    coverctl_file = root / "scripts" / "coverctl.py"
    if not server_file.exists():
        raise FileNotFoundError(f"MCP server not found: {server_file}")
    if not coverctl_file.exists():
        raise FileNotFoundError(f"coverctl gate not found: {coverctl_file}")
    return root


def load_project_server(product_root: Path):
    server_file = product_root / "mcp-server" / "cover_project_server.py"
    spec = importlib.util.spec_from_file_location(
        "pigeonyang_cover_project_server",
        server_file,
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"could not load MCP server from {server_file}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    module.PRODUCT_ROOT = product_root
    module.SCRIPT = product_root / "scripts" / "manage_cover_project.py"
    module.COVERCTL = product_root / "scripts" / "coverctl.py"
    return module


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pigeonyang-cover-mcp",
        description="Run the PigeonYang cover workflow MCP stdio server.",
    )
    parser.add_argument(
        "--product-root",
        help=(
            "Path to J:\\PigeonYang\\cover-style-distiller\\product. "
            f"Can also be set with {PRODUCT_ROOT_ENV}."
        ),
    )
    parser.add_argument(
        "--print-config",
        action="store_true",
        help="Print resolved product root and exit.",
    )
    parser.add_argument("--version", action="store_true", help="Print version and exit.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.version:
        print(__version__)
        return 0

    try:
        product_root = resolve_product_root(args.product_root)
    except Exception as exc:  # noqa: BLE001 - CLI should fail with a clear line.
        print(f"pigeonyang-cover-mcp error: {exc}", file=sys.stderr)
        return 2

    if args.print_config:
        print(f"product_root={product_root}")
        print(f"server={product_root / 'mcp-server' / 'cover_project_server.py'}")
        print(f"coverctl={product_root / 'scripts' / 'coverctl.py'}")
        return 0

    module = load_project_server(product_root)
    return int(module.main())


if __name__ == "__main__":
    raise SystemExit(main())
