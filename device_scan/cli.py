import argparse

from device_scan.examples.ips2domain_name import print_domain_names
from device_scan.examples.tcp_port_scan import http_scan, http_test_scan


def func2arg_name(func):
    return func.__name__.replace('_', '-')


def main():
    print()
    parser = argparse.ArgumentParser(description='Device-Scan examples')

    subparsers = parser.add_subparsers(title='Commands')

    subparsers.add_parser(
        name=func2arg_name(print_domain_names),
        help=print_domain_names.__doc__
    ).set_defaults(
        func=print_domain_names
    )

    subparsers.add_parser(
        name=func2arg_name(http_scan),
        help=http_scan.__doc__
    ).set_defaults(
        func=http_scan
    )

    subparsers.add_parser(
        name=func2arg_name(http_test_scan),
        help=http_test_scan.__doc__
    ).set_defaults(
        func=http_test_scan
    )

    args = parser.parse_args()
    if not hasattr(args, 'func'):
        parser.error('Unknown command')

    print('_' * 100)
    print(f'{func2arg_name(args.func)}\n')

    args.func(args)


if __name__ == "__main__":
    main()
