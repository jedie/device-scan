"""
    Device-Scanner
    ~~~~~~~~~~~~~~
"""
import asyncio
import socket


class Scanner:
    def __init__(self,
                 ips,  # IPs to scan
                 async_callback,  # the asyncio wait for callback to test the host
                 async_callback_kwargs=None,  # additional keyword arguments for callback
                 timeout=2,  # asyncio.wait_for() timeout
                 return_exceptions=True  # asyncio.gather() return_exceptions
                 ):
        self.ips = tuple(ips)
        self.async_callback = async_callback

        if async_callback_kwargs is None:
            self.async_callback_kwargs = {}
        else:
            self.async_callback_kwargs = async_callback_kwargs

        self.timeout = timeout
        self.return_exceptions = return_exceptions

    async def _scan(self):
        connections = [
            asyncio.wait_for(
                self.async_callback(ip=ip, **self.async_callback_kwargs),
                timeout=self.timeout
            )
            for ip in self.ips
        ]
        results = await asyncio.gather(*connections, return_exceptions=self.return_exceptions)
        return zip(self.ips, results)

    def scan(self):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(
            self._scan()
        )


def get_domain_names(ips):
    async def async_callback(*, ip):
        domain_name = socket.getfqdn(ip)
        if domain_name != ip:
            return domain_name

    scanner = Scanner(ips=ips, async_callback=async_callback)
    results = scanner.scan()

    for ip, result in results:
        if isinstance(result, asyncio.TimeoutError):
            continue

        if result is not None:
            yield ip, result


def connect_scan(ips, port=80):
    """
    Try to open a connection to ip:port
    yields ip and reader/writer streams
    """
    async def async_callback(*, ip, port):
        reader, writer = await asyncio.open_connection(host=ip, port=port)
        return True

    scanner = Scanner(ips=ips, async_callback=async_callback, async_callback_kwargs={'port': port})
    results = scanner.scan()

    for ip, ok in results:
        if isinstance(ok, asyncio.TimeoutError):
            continue

        if ok is True:
            yield ip
