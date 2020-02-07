'''
    Device-Scanner
    ~~~~~~~~~~~~~~
'''
import asyncio
import socket


SOCKET_TIMEOUT = 10

DNS_SERVER = '8.8.8.8'  # Google DNS Server ot get own IP


def get_ip_address():
    '''
    :return: IP address of the host running this script.
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(SOCKET_TIMEOUT)
    s.connect((DNS_SERVER, 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def ip_range_iterator(own_ip, exclude_own):
    ip_prefix, own_no = own_ip.rsplit('.', 1)
    print(f'Scan:.....: {ip_prefix}.X')

    own_no = int(own_no)

    for no in range(1, 255):
        if exclude_own and no == own_no:
            continue

        yield f'{ip_prefix}.{no}'


class Scanner:
    def __init__(self, open_connection, timeout=2, return_exceptions=True):
        self.open_connection = open_connection
        self.timeout = timeout
        self.return_exceptions = return_exceptions

        self.own_ip = get_ip_address()
        print(f'Own IP....: {self.own_ip}')

    async def port_scan_and_serve(self, port):
        ips = tuple(ip_range_iterator(self.own_ip, exclude_own=True))

        connections = [
            asyncio.wait_for(
                self.open_connection(host=ip, port=port),
                timeout=self.timeout
            )
            for ip in ips
        ]
        results = await asyncio.gather(*connections, return_exceptions=self.return_exceptions)
        return zip(ips, results)

    def scan(self, port):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(
            self.port_scan_and_serve(port=port)
        )


if __name__ == '__main__':
    async def open_connection(*, host, port):
        try:
            reader, writer = await asyncio.open_connection(host=host, port=port)
        except ConnectionError:
            return

        # print('Connected to:', host, port, end='...', flush=True)
        writer.write(b'GET / HTTP/1.0\n\n')
        await writer.drain()
        content = await reader.read(50)
        content = content.decode('UTF-8', errors='replace')
        print(f'{host}:{port} get: {content!r}...')
        return content

    scanner = Scanner(open_connection=open_connection)
    results = scanner.scan(port=80)

    for ip, result in results:
        if isinstance(result, asyncio.TimeoutError):
            continue

        print(f'{ip} - {result!r}...')
