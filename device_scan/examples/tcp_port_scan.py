import asyncio

from device_scan.scanner import Scanner, connect_scan
from device_scan.utils import get_subnet_ips


def http_scan(args):
    """
    List all web servers (port=80 open) from current subnet.
    """
    ips = get_subnet_ips(exclude_own=True, verbose=True)
    for ip in connect_scan(ips, port=80):
        print(f' * {ip}')


def http_test_scan(args):
    """
    List all web servers from current subnet with raw response.
    """
    async def async_callback(*, ip):
        reader, writer = await asyncio.open_connection(host=ip, port=80)
        print(end='.', flush=True)

        writer.write(b'GET / HTTP/1.0\n\n')
        await writer.drain()
        content = await reader.read(50)
        content = content.decode('UTF-8', errors='replace')
        return content

    ips = get_subnet_ips(exclude_own=True, verbose=True)
    scanner = Scanner(ips=ips, async_callback=async_callback)
    results = scanner.scan()

    print()

    for ip, content in results:
        if isinstance(content, asyncio.TimeoutError):
            continue

        print(f'{ip:<13} -> {content!r}')
