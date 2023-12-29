from pathlib import Path

from binary_wheel_builder.api import create_all_supported_platform_wheels
import sys
from argparse import ArgumentParser, Namespace


def parse_args(args) -> Namespace:
    parser = ArgumentParser("CLI Wheel Builder")
    parser.add_argument("--wheel-spec", type=str, required=True)
    parser.add_argument("--dist-folder", default="dist/", type=str)
    return parser.parse_args(args)


def main(argv=None) -> None:
    try:
        import yaml
    except:
        raise SystemExit("PyYAML not installed, can not use CLI.")

    if argv is None:
        argv = sys.argv[1:] if sys.argv else []

    args = parse_args(argv)

    dist_path = Path(args.dist_folder)
    dist_path.mkdir(exist_ok=True)

    from binary_wheel_builder.cli.config_file import load_wheel_spec_from_yaml
    wheel = load_wheel_spec_from_yaml(Path(args.wheel_spec))
    for result in create_all_supported_platform_wheels(wheel, dist_path):
        print(f"> {result.checksum} - {result.file_path}")