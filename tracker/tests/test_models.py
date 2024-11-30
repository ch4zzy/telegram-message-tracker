from ..models import SourceChannel, TargetChannel, Post
from django.contrib.auth import get_user_model
import pytest


User = get_user_model()


@pytest.mark.django_db
def test_user_creation(user_data, user_instance):
    user = user_instance
    assert User.objects.count() == 1
    assert User.objects.get(username=user_data['username']) == user
    assert user.check_password(user_data['password'])


@pytest.mark.django_db
def test_target_channel_creation(target_channel_data, target_channel_instance_create):
    target_data = target_channel_data
    target = target_channel_instance_create
    assert TargetChannel.objects.count() == 1
    assert TargetChannel.objects.get(name=target_data['name']) == target
    assert target.auto_post == target_data['auto_post']
    assert target.source_link == target_data['source_link']


@pytest.mark.django_db
def test_source_channel_creation(source_channel_data, source_channel_instance_create):
    source_data = source_channel_data
    source = source_channel_instance_create
    assert SourceChannel.objects.count() == 1
    assert SourceChannel.objects.get(name=source_data['name']) == source
    assert source.active_following == source_data['active_following']
    assert source.source_link == source_data['source_link']
    assert source.user == source_data['user']
    assert source.target_channel.first() == source_data['target_channel'][0]
