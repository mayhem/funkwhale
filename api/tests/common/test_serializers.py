import os
import PIL

from django.core.files.uploadedfile import SimpleUploadedFile

import django_filters

from funkwhale_api.common import serializers
from funkwhale_api.users import models


class TestActionFilterSet(django_filters.FilterSet):
    class Meta:
        model = models.User
        fields = ["is_active"]


class TestSerializer(serializers.ActionSerializer):
    actions = [serializers.Action("test", allow_all=True)]
    filterset_class = TestActionFilterSet

    def handle_test(self, objects):
        return {"hello": "world"}


class TestDangerousSerializer(serializers.ActionSerializer):
    actions = [
        serializers.Action("test", allow_all=True),
        serializers.Action("test_dangerous"),
    ]

    def handle_test(self, objects):
        pass

    def handle_test_dangerous(self, objects):
        pass


class TestDeleteOnlyInactiveSerializer(serializers.ActionSerializer):
    actions = [
        serializers.Action(
            "test", allow_all=True, qs_filter=lambda qs: qs.filter(is_active=False)
        )
    ]
    filterset_class = TestActionFilterSet

    def handle_test(self, objects):
        pass


def test_action_serializer_validates_action():
    data = {"objects": "all", "action": "nope"}
    serializer = TestSerializer(data, queryset=models.User.objects.none())

    assert serializer.is_valid() is False
    assert "action" in serializer.errors


def test_action_serializer_validates_objects():
    data = {"objects": "nope", "action": "test"}
    serializer = TestSerializer(data, queryset=models.User.objects.none())

    assert serializer.is_valid() is False
    assert "objects" in serializer.errors


def test_action_serializers_objects_clean_ids(factories):
    user1 = factories["users.User"]()
    factories["users.User"]()

    data = {"objects": [user1.pk], "action": "test"}
    serializer = TestSerializer(data, queryset=models.User.objects.all())

    assert serializer.is_valid(raise_exception=True) is True
    assert list(serializer.validated_data["objects"]) == [user1]


def test_action_serializers_objects_clean_all(factories):
    user1 = factories["users.User"]()
    user2 = factories["users.User"]()

    data = {"objects": "all", "action": "test"}
    serializer = TestSerializer(data, queryset=models.User.objects.all())

    assert serializer.is_valid(raise_exception=True) is True
    assert list(serializer.validated_data["objects"]) == [user1, user2]


def test_action_serializers_save(factories, mocker):
    handler = mocker.spy(TestSerializer, "handle_test")
    factories["users.User"]()
    factories["users.User"]()

    data = {"objects": "all", "action": "test"}
    serializer = TestSerializer(data, queryset=models.User.objects.all())

    assert serializer.is_valid(raise_exception=True) is True
    result = serializer.save()
    assert result == {"updated": 2, "action": "test", "result": {"hello": "world"}}
    handler.assert_called_once()


def test_action_serializers_filterset(factories):
    factories["users.User"](is_active=False)
    user2 = factories["users.User"](is_active=True)

    data = {"objects": "all", "action": "test", "filters": {"is_active": True}}
    serializer = TestSerializer(data, queryset=models.User.objects.all())

    assert serializer.is_valid(raise_exception=True) is True
    assert list(serializer.validated_data["objects"]) == [user2]


def test_action_serializers_validates_at_least_one_object():
    data = {"objects": "all", "action": "test"}
    serializer = TestSerializer(data, queryset=models.User.objects.none())

    assert serializer.is_valid() is False
    assert "non_field_errors" in serializer.errors


def test_dangerous_actions_refuses_all(factories):
    factories["users.User"]()
    data = {"objects": "all", "action": "test_dangerous"}
    serializer = TestDangerousSerializer(data, queryset=models.User.objects.all())

    assert serializer.is_valid() is False
    assert "non_field_errors" in serializer.errors


def test_action_serializers_can_require_filter(factories):
    user1 = factories["users.User"](is_active=False)
    factories["users.User"](is_active=True)

    data = {"objects": "all", "action": "test"}
    serializer = TestDeleteOnlyInactiveSerializer(
        data, queryset=models.User.objects.all()
    )

    assert serializer.is_valid(raise_exception=True) is True
    assert list(serializer.validated_data["objects"]) == [user1]


def test_track_fields_for_update(mocker):
    @serializers.track_fields_for_update("field1", "field2")
    class S(serializers.serializers.Serializer):
        field1 = serializers.serializers.CharField()
        field2 = serializers.serializers.CharField()

        def update(self, obj, validated_data):
            for key, value in validated_data.items():
                setattr(obj, key, value)
            return obj

        on_updated_fields = mocker.stub()

    class Obj(object):
        field1 = "value1"
        field2 = "value2"

    obj = Obj()
    serializer = S(obj, data={"field1": "newvalue1", "field2": "newvalue2"})
    assert serializer.is_valid(raise_exception=True)
    serializer.save()

    serializer.on_updated_fields.assert_called_once_with(
        obj,
        {"field1": "value1", "field2": "value2"},
        {"field1": "newvalue1", "field2": "newvalue2"},
    )


def test_strip_exif_field():
    source_path = os.path.join(os.path.dirname(__file__), "exif.jpg")
    source = PIL.Image.open(source_path)

    assert bool(source._getexif())

    with open(source_path, "rb") as f:
        uploaded = SimpleUploadedFile("source.jpg", f.read(), content_type="image/jpeg")
    field = serializers.StripExifImageField()

    cleaned = PIL.Image.open(field.to_internal_value(uploaded))
    assert cleaned._getexif() is None
