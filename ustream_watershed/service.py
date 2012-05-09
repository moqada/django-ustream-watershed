# -*- coding: utf-8 -*-
import re
import datetime
from pysimplesoap.server import SoapDispatcher
from ustream_watershed import signals


datetime_local_regex = re.compile(r'-07:00$')


def phpserialized(serialized):
    """ convert to python string list
    """
    from phpserialize import loads
    from phpserialize import dict_to_list
    try:
        serialized = loads(serialized)
        serialized = dict_to_list(serialized)
    except ValueError:
        pass
    return serialized


def datetime_mst(datetime_str):
    """ convert to datetime for local time zone
    """
    from dateutil import tz
    frmt = '%Y-%m-%d %H:%M:%S'
    if datetime_local_regex.search(datetime_str):
        frmt = '%Y-%m-%dT%H:%M:%S-07:00'
    return datetime.datetime.strptime(datetime_str, frmt).replace(
        tzinfo=tz.gettz('MST')).astimezone(tz.tzlocal()).replace(tzinfo=None)


class BaseWatershedService(object):
    """ WatershedService
    """
    dispatch_methods = {
        'validateBroadcasterSession': {
            'method': 'validate_broadcaster_session',
            'signal': signals.receive_validate_broadcaster_session,
            'args': {
                'brandId': str,
                'channelCode': str,
                'sessionId': str,
            },
            'returns': {
                'authStatus': bool,
                'authMessage': str,
                'moduleConfigOfBroadcaster': dict,
            },
        },
        'notifySystemMessage': {
            'method': 'notify_system_message',
            'signal': signals.receive_notify_system_message,
            'args': {
                'brandId': str,
                'message': str,
                'priority': str,
            },
            'returns': {
                'acknowledged': bool
            },
        },
        'loginBroadcaster': {
            'method': 'login_broadcaster',
            'signal': signals.receive_login_broadcaster,
            'args': {
                'brandId': str,
                'userName': str,
                'password': str,
            },
            'returns': {
                'sessionId': str,
                'authMessage': str,
                'channels': [{
                    'title': str,
                    'channelCode': str
                }],
            },
        },
        'loginBroadcasterByChannelToken': {
            'method': 'login_broadcaster_by_channel_token',
            'signal': signals.receive_login_broadcaster_by_channel_token,
            'args': {
                'brandId': str,
                'channelCode': str,
                'channelToken': str,
            },
            'returns': {
                'sessionId': str,
                'authMessage': str,
            },
        },
        'notifyChannelStatusChanged': {
            'method': 'notify_channel_status_changed',
            'signal': signals.receive_notify_channel_status_changed,
            'args': {
                'brandId': str,
                'channelCode': str,
                'status': str,
                'changedAt': datetime_mst,
            },
            'returns': {
                'acknowledged': bool,
            },
        },
        'validateViewerSession': {
            'method': 'validate_viewer_session',
            'signal': signals.receive_validate_viewer_session,
            'args': {
                'brandId': str,
                'channelCode': str,
                'sessionId': str,
            },
            'returns': {
                'authStatus': bool,
                'authMessage': str,
            },
        },
        'notifyRecordingCompleted': {
            'method': 'notify_recording_completed',
            'signal': signals.receive_notify_recording_completed,
            'args': {
                'brandId': str,
                'channelCode': str,
                'videoId': int,
                'createdAt': datetime_mst,
                'videoAttributes': {
                    'duration': int,
                    'fileSize': int,
                    'rtmpUrl': str,
                    'flvUrl': str,
                    'title': str,
                    'description': str,
                    'tags': phpserialized,
                    'isPrivate': bool,
                },
            },
            'returns': {
                'acknowledged': bool,
            }
        },
    }

    def __init__(self):
        self.dispatcher = SoapDispatcher(
            'UstreamWatershed',
            namespace='http://watershed.ustream.tv/soap/apiuser/',
            trace=True, ns=True)
        self._dispatch()

    def validate_broadcaster_session(self, brandId, channelCode, sessionId):
        """ validateBroadcasterSession
        """
        return {
            'authStatus': True,
            'authMessage': 'Success!',
            'moduleConfigOfBroadcaster': {
                'passwordLock': {
                    'PasswordModule': {
                        'password': 'hoge',
                    }
                },
                'meta': {
                    'ModuleTurnOff': False,
                },
                'disableModules': {
                    'passwordLock': False,
                }
            },
        }

    def notify_system_message(self, brandId, message, priority):
        """ notifySystemMessage
        """
        return True  # Acknowledge(boolean)

    def login_broadcaster(self, brandId, userName, password):
        """ loginBroadcaster
        """
        return {
            'sessionId': 'test-id',
            'authMessage': 'login success!',
            'channels': ['test-ch', 'test-ch2']
        }

    def login_broadcaster_by_channel_token(self, brandId, channelCode, channelToken):
        """ loginBroadcasterByChannelToken
        """
        return {
            'sessionId': 'test-id',
            'authMessage': 'login success!',
        }

    def notify_channel_status_changed(self, brandId, channelCode, status, changedAt):
        """ notifyChannelStatusChanged
        """
        return True  # Acknowledge(boolean)

    def validate_viewer_session(self, brandId, channelCode, sessionId):
        """ validateViewerSession
        """
        return {
            'authStatus': True,
            'authMessage': 'Success!',
        }

    def notify_recording_completed(
        self, brandId, channelCode, videoId, createdAt, videoAttributes):
        """ notifyRecordingCompleted
        """
        return True  # Acknowledge(boolean)

    def _decorate_signal(self, function, signal):
        def _decorated(**args):
            signal.send(sender=self, **args)
            return function(**args)
        return _decorated

    def _dispatch(self):
        for name, values in self.dispatch_methods.items():
            func = getattr(self, values['method'])
            if 'signal' in values:
                func = self._decorate_signal(func, values['signal'])
            self.dispatcher.register_function(
                name, func,
                args=values['args'],
                returns=values['returns'])
