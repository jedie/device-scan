from device_scan.scanner import get_domain_names
from device_scan.utils import get_ip_address, ip_range_iterator, get_subnet_ips


def print_domain_names(args=None):
    """
    List all hosts with domain name from current subnet.
    """
    ips = get_subnet_ips(exclude_own=True, verbose=True)

    for ip, domain_name in get_domain_names(ips=ips):
        print(f'{ip:<13} -> {domain_name}')


if __name__ == '__main__':
    print_domain_names()
