import logging
import os
import libhoney

from iopipe.plugins import Plugin
from .send_honeycomb import send_honeycomb

logger = logging.getLogger(__name__)

class HoneycombReport(Plugin):
    def __init__(self):
        config = {}
        config['writekey'] = os.getenv('IOPIPE_HONEYCOMB_WRITEKEY', 'unsetwk')
        config['dataset'] = os.getenv('IOPIPE_HONEYCOMB_DATASET', 'unsetds')
        config['sample_rate'] = os.getenv('IOPIPE_HONEYCOMB_SAMPLE_RATE', 1)
        self.config = config
        logger.debug("initializing Honeycomb plugin with {}".format(config))

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
        for c in ['writekey', 'dataset', 'sample_rate', 'api_host']:
            if c in iopipe.config:
                self.config[c] = iopipe.config[c]

        # default sample rate to 1
        try:
            self.config['sample_rate'] = int(self.config['sample_rate'])
        except ValueError:
            self.config['sample_rate'] = 1
        if self.config['sample_rate'] < 1:
            self.config['sample_rate'] = 1

        libhoney.init(**self.config)

    def pre_invoke(self, event, context):
        pass

    def post_invoke(self, event, context):
        pass

    def pre_report(self, report):
        pass

    def send_report(self, report):
        try:
            send_honeycomb(report.report, self.config)
        except Exception as e:
            logger.debug("caught exception while sending report: {}".format(e))
            raise e
        finally:
            logger.debug("iopreport sent report")

    def post_report(self):
        responses = libhoney.responses()
        resp = responses.get()
        if resp == None:
            logger.info("no response from honeycomb")
        else:
            logger.debug("got response from Honeycomb: {}".format(resp))
        libhoney.close()
