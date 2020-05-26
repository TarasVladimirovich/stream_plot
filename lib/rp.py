import logging

logger = logging.getLogger(__name__)


class COMMAND:
    DING_ID = 'ding.id'
    STREAM_PROBED_BITRATE = 'stream.probed_bitrate'
    STREAM_PCU_SERVER_AVAILABLE = 'stream.pcu_server_available'
    TEST_PROFILE_ID = 'test.profile_id'
    TEST_BITRATE = 'test.bitrate'
    STREAM_RMS_ENABLED = 'stream.rms_enabled'


class RP:
    BINARY_PATH = '/ring/bin/rp'

    def __init__(self, client):
        self.client = client

    def _run_command(self, command):
        command = f'{self.BINARY_PATH} {command}'
        return self.client.execute_command(command)

    def set_profile(self, profile: int):
        """ Set test profile """
        logger.info(f'Set profile {profile}')
        return self._run_command(f'set {COMMAND.TEST_PROFILE_ID} {profile}')

    def unset_profile(self):
        """ Unset test profile """
        logger.info('Unset profile')
        return self._run_command(f'unset {COMMAND.TEST_PROFILE_ID}')

    def set_test_bitrate(self, bitrate: int):
        """ Set test bitrate """
        logger.info(f'Set test bitrate {bitrate}')
        return self._run_command(f'set {COMMAND.TEST_BITRATE} {bitrate}')

    def unset_test_bitrate(self):
        """ Unset test bitrate """
        logger.info('Unset test bitrate')
        return self._run_command(f'unset {COMMAND.TEST_BITRATE}')

    def get_solution(self):
        """ Get solution """
        return self._run_command(f'get {COMMAND.STREAM_RMS_ENABLED} --raw')

    def get_ding_id(self):
        """ Get ding id """
        return self._run_command(f'get {COMMAND.DING_ID} --raw')

    def set_probed_bitrate(self, bitrate: int):
        """ Set probed bitrate """
        logger.info(f'Set probed bitrate {bitrate}')
        return self._run_command(f'set {COMMAND.STREAM_PROBED_BITRATE} {bitrate}')

    def unset_probed_bitrate(self):
        """ Unset probed bitrate """
        logger.info('Unset probed bitrate')
        return self._run_command(f'unset {COMMAND.STREAM_PROBED_BITRATE}')
