# device-scan

Python lib for find devices in own network subnet.

```
~/device-scan$ poetry run device_scan -h

usage: device_scan [-h] {print-domain-names,http-scan,http-test-scan} ...

Device-Scan examples

optional arguments:
  -h, --help            show this help message and exit

Commands:
  {print-domain-names,http-scan,http-test-scan}
    print-domain-names  List all hosts with domain name from current subnet.
    http-scan           List all web servers (port=80 open) from current
                        subnet.
    http-test-scan      List all web servers from current subnet with raw
                        response.

```
