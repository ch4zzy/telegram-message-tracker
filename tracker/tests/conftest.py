import pytest
from ..models import SourceChannel, TargetChannel
from django.contrib.auth import get_user_model


User = get_user_model()

@pytest.fixture
def user_data():
    return {
        'username': 'testuser',
        'email': 'user@user.com',
        'password': 'testpassword'
    }


@pytest.fixture
def user_instance(user_data):
    return User.objects.create_user(**user_data)


@pytest.fixture
def target_channel_data(user_instance):
    return {
        'user': user_instance,
        'name': 'testchannel',
        'source_link': 'https://t.me/testchannel3214',
        'auto_post': False
    }


@pytest.fixture
def target_channel_instance_create(target_channel_data):
    return TargetChannel.objects.create(**target_channel_data)


@pytest.fixture
def source_channel_data(user_instance, target_channel_instance_create):
    return {
        'user': user_instance,
        'name': 'testchannel',
        'source_link': 'https://t.me/testchannel3214',
        'active_following': True,
        'target_channel': [target_channel_instance_create]
    }


@pytest.fixture
def source_channel_instance_create(user_instance, source_channel_data):
    source_channel, created = SourceChannel.objects.get_or_create(
        user=user_instance,
        name=source_channel_data['name'],
        source_link=source_channel_data['source_link'],
        active_following=source_channel_data['active_following'],
    )
    source_channel.target_channel.set(source_channel_data['target_channel'])
    return source_channel
