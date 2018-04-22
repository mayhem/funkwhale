from django.db import transaction
from rest_framework import serializers
from taggit.models import Tag

from funkwhale_api.activity import serializers as activity_serializers
from funkwhale_api.federation import utils as federation_utils
from funkwhale_api.federation.models import LibraryTrack
from funkwhale_api.federation.serializers import AP_CONTEXT
from funkwhale_api.users.serializers import UserBasicSerializer

from . import models


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')


class SimpleArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Artist
        fields = ('id', 'mbid', 'name', 'creation_date')


class ArtistSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = models.Artist
        fields = ('id', 'mbid', 'name', 'tags', 'creation_date')


class TrackFileSerializer(serializers.ModelSerializer):
    path = serializers.SerializerMethodField()

    class Meta:
        model = models.TrackFile
        fields = (
            'id',
            'path',
            'duration',
            'source',
            'filename',
            'mimetype',
            'track')

    def get_path(self, o):
        url = o.path
        return url


class SimpleAlbumSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Album
        fields = ('id', 'mbid', 'title', 'release_date', 'cover')


class AlbumSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = models.Album
        fields = ('id', 'mbid', 'title', 'cover', 'release_date', 'tags')


class LyricsMixin(serializers.ModelSerializer):
    lyrics = serializers.SerializerMethodField()

    def get_lyrics(self, obj):
        return obj.get_lyrics_url()


class TrackSerializer(LyricsMixin):
    files = TrackFileSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = models.Track
        fields = (
            'id',
            'mbid',
            'title',
            'artist',
            'files',
            'tags',
            'position',
            'lyrics')


class TrackSerializerNested(LyricsMixin):
    artist = ArtistSerializer()
    files = TrackFileSerializer(many=True, read_only=True)
    album = SimpleAlbumSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = models.Track
        fields = ('id', 'mbid', 'title', 'artist', 'files', 'album', 'tags', 'lyrics')


class AlbumSerializerNested(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True, read_only=True)
    artist = SimpleArtistSerializer()
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = models.Album
        fields = ('id', 'mbid', 'title', 'cover', 'artist', 'release_date', 'tracks', 'tags')


class ArtistSerializerNested(serializers.ModelSerializer):
    albums = AlbumSerializerNested(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = models.Artist
        fields = ('id', 'mbid', 'name', 'albums', 'tags')


class LyricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Lyrics
        fields = ('id', 'work', 'content', 'content_rendered')


class ImportJobSerializer(serializers.ModelSerializer):
    track_file = TrackFileSerializer(read_only=True)

    class Meta:
        model = models.ImportJob
        fields = (
            'id',
            'mbid',
            'batch',
            'source',
            'status',
            'track_file',
            'audio_file')
        read_only_fields = ('status', 'track_file')


class ImportBatchSerializer(serializers.ModelSerializer):
    submitted_by = UserBasicSerializer(read_only=True)

    class Meta:
        model = models.ImportBatch
        fields = (
            'id',
            'submitted_by',
            'source',
            'status',
            'creation_date',
            'import_request')
        read_only_fields = (
            'creation_date', 'submitted_by', 'source')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        try:
            repr['job_count'] = instance.job_count
        except AttributeError:
            # Queryset was not annotated
            pass
        return repr


class TrackActivitySerializer(activity_serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    name = serializers.CharField(source='title')
    artist = serializers.CharField(source='artist.name')
    album = serializers.CharField(source='album.title')

    class Meta:
        model = models.Track
        fields = [
            'id',
            'local_id',
            'name',
            'type',
            'artist',
            'album',
        ]

    def get_type(self, obj):
        return 'Audio'


class SubmitFederationTracksSerializer(serializers.Serializer):
    library_tracks = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=LibraryTrack.objects.filter(local_track_file__isnull=True),
    )

    @transaction.atomic
    def save(self, **kwargs):
        batch = models.ImportBatch.objects.create(
            source='federation',
            **kwargs
        )
        for lt in self.validated_data['library_tracks']:
            models.ImportJob.objects.create(
                batch=batch,
                library_track=lt,
                mbid=lt.mbid,
                source=lt.url,
            )
        return batch
