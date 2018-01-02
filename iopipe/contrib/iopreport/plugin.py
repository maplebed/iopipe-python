import logging

from iopipe.plugins import Plugin
from iopipe.collector import get_collector_path, get_hostname
from .send_report import send_report

logger = logging.getLogger(__name__)

try:
    import requests
except ImportError:
    from botocore.vendored import requests

class IopipeReport(Plugin):
    def __init__(self):
        self.config = {
            "host": get_hostname(),
            "path": get_collector_path(),
            "network_timeout": 5,
        }

    @property
    def name(self):
        return 'ioreport'

    @property
    def version(self):
        return '0.1.0'

    @property
    def homepage(self):
        return 'https://github.com/iopipe/iopipe-python'

    @property
    def enabled(self):
        return True

    def pre_setup(self, iopipe):
        pass

    def post_setup(self, iopipe):
        # if there's iopipe config, override our defaults.
        for c in ['host', 'path', 'network_timeout']:
            if c in iopipe.config:
                self.config[c] = iopipe.config[c]

        try:
            self.config['network_timeout'] = int(self.config['network_timeout'])
        except ValueError:
            self.config['network_timeout'] = 5

    def pre_invoke(self, event, context):
        pass

    def post_invoke(self, event, context):
        pass

    def pre_report(self, report):
        pass

    def send_report(self, report):
        try:
            send_report(report, self.config)
        except Exception as e:
            logger.debug("caught exception while sending report: {}".format(e))
            raise e
        finally:
            logger.debug("iopreport sent report")

    def post_report(self):
        pass
