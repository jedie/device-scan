from pathlib import Path

from poetry_publish.publish import poetry_publish
from poetry_publish.utils.subprocess_utils import verbose_check_call

import device_scan


def publish():
    """
        Publish to PyPi via poetry-publish
        Call this via:
            $ poetry run publish
    """
    verbose_check_call('make', 'fix-code-style')  # don't publish if code style wrong

    poetry_publish(
        package_root=Path(device_scan.__file__).parent.parent,
        version=device_scan.__version__,
    )
