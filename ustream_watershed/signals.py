# -*- coding: utf-8 -*-
from django.dispatch import Signal


receive_validate_broadcaster_session = Signal(
    providing_args=['brandId', 'channelCode', 'sessionId'])

receive_notify_system_message = Signal(
    providing_args=['brandId', 'message', 'priority'])

receive_login_broadcaster = Signal(
    providing_args=['brandId', 'userName', 'password'])

receive_login_broadcaster_by_channel_token = Signal(
    providing_args=['brandId', 'channelCode', 'channelToken'])

receive_notify_channel_status_changed = Signal(
    providing_args=['brandId', 'channelCode', 'status', 'changedAt'])

receive_validate_viewer_session = Signal(
    providing_args=['brandId', 'channelCode', 'sessionId'])

receive_notify_recording_completed = Signal(
        providing_args=[
            'brandId', 'channelCode', 'videoId', 'createdAt', 'videoAttributes'])
