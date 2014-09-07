import platform


class SystemDetector:
    def __init__(self):
        self._system = platform.system()

    @property
    def linux(self):
        return self._system == 'Linux'

    @property
    def windows(self):
        return self._system == 'Windows'

    @property
    def macos(self):
        return self._system == 'Darwin'