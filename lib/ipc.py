import logging

logger = logging.getLogger(__name__)


class COMMAND:
    AUDIO_PLAY = 'audioPlay'
    AUDIO_STOP = 'audioStop'
    CHIME_SETTINGS = 'chimeSettings'
    DING_ACCEPT = 'dingAccept'
    DING_AUDIO_VOLUME = 'dingAudioSettings'
    DING_END = 'dingEnd'
    DING_FAILED = 'dingFailed'
    DING_REQUEST = 'dingRequest'
    DING_SWITCH = 'dingSwitch'
    DING_Start = 'dingStart'
    FLOODLIGHT_TOGGLE = 'floodlightToggle'
    GCOV_FLUSH = 'gcovFlush'
    IPERF = 'iperf'
    IR_LED_ENABLE = 'IrLedEnable'
    LED_PATTERN = 'ledPattern'
    LIGHT_STATE_C2 = 'lightsStateC2'
    LIGHT_STATE_IV = 'lightsStateIV'
    LOAD_STREAM_CONFIG = 'loadStreamConfig'
    LOGGER_LOG = 'loggerLog'
    LOG_LEVEL = 'logLevel'
    MOTION_DATA = 'motionData'
    MSU = 'msu'
    NITH_MODE_STATE = 'nightModeStateToIV'
    PIR_MOTION = 'pirMotion'
    PM_RUN_NOW = 'pmRunNow'
    PM_UPDATE = 'pmUpdate'
    POST_CALL_UPLOAD = 'postCallUpload'
    REBOOT = 'reboot'
    REKEY_STREAMS = 'rekeyStreams'
    REQUEST_SNAPSHOT = 'requestSnapshot'
    REQUEST_SSRC = 'requestSSRC'
    RESET_BUTTON = 'resetButton'
    RESPOND_SNAPSHOT = 'respondSnapshot'
    REST_SEND = 'restSend'
    RNM_EVT = 'enmEvt'
    RNM_REQ = 'rnmReq'
    SETUP_STARTED = 'setupStarted'
    SIREN = 'sirenSettings'
    SNAPSHOT_SETTINGS = 'snapshotSettings'
    SOUND = 'sound'
    STREAM_QUALITY = 'streamQuality'
    STREAM_START = 'streamStart'
    STREAM_STOP = 'streamStop'
    STREAM_THROUGHPUT = 'streamThroughput'
    THROUGHPUT = 'throughput'
    TRIAC_ENABLE = 'triacEnable'
    UPGRADE_CHECK = 'upgradeCheck'
    UPGRADE_START = 'upgradeStart'


class DingType:
    BUTTON = 'button'
    MOTION = 'motion'


class IPC:
    BINARY_PATH = '/ring/bin/ipc_cli'

    def __init__(self, client):
        self.client = client

    def _run_command(self, command):
        command = f'{self.BINARY_PATH} {command}'
        return self.client.execute_command(command)

    def ding_end(self):
        """ Stops active ding """
        return self._run_command(f'{COMMAND.DING_END}')

    def ding_request(self, type_: DingType):
        """
        :param type_: ding type
        """
        return self._run_command(f'{COMMAND.DING_REQUEST} {type_}')

    def stream_stop(self):
        logger.info('Stream stop')
        return self._run_command(f'{COMMAND.STREAM_STOP}')

    def broadcast(self, message: int):
        return self._run_command(f'broadcast {message}')

    def load_stream_config(self):
        return self._run_command(COMMAND.LOAD_STREAM_CONFIG)
