import socket


DNS_SERVER = '8.8.8.8'  # Google DNS Server to get own IP


def get_ip_address(timeout=10):
    """
    :return: IP address of the host running this script.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(timeout)
    s.connect((DNS_SERVER, 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def ip_range_iterator(own_ip, exclude_own):
    ip_prefix, own_no = own_ip.rsplit('.', 1)
    own_no = int(own_no)

    for no in range(1, 255):
        if exclude_own and no == own_no:
            continue

        yield f'{ip_prefix}.{no}'


def get_subnet_ips(exclude_own=True, verbose=False):
    own_ip = get_ip_address()

    if verbose:
        print(f'Own IP....: {own_ip}')
        print(f'Scan:.....: {own_ip.rsplit(".", 1)[0]}.X')
        print('-' * 100)

    return ip_range_iterator(own_ip, exclude_own=exclude_own)
