from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Profile, Topic


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # profile = serializers.ReadOnlyField(source='profile.id')
    profile_url = serializers.HyperlinkedIdentityField(
        view_name='profile-detail')
    class Meta:
        model = User
        depth = 1
        fields = ('url', 'id', 'username', 'first_name', 'last_name', 'email',
                  'is_superuser', 'is_staff', 'profile', 'profile_url')


class TopicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Topic
        fields = ('url', 'id', 'name', 'description')


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    user_url = serializers.HyperlinkedIdentityField(view_name='user-detail')
    user = serializers.ReadOnlyField(source='user.id')

    # id = serializers.IntegerField(source='pk', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    # favorite_topics = TopicSerializer(many=True)
    # favorite_topics = serializers.PrimaryKeyRelatedField(
    #     many=True,
    #     read_only=False,
    #     queryset=Topic.objects.all()
    # )
    favorite_topics = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=False,
        queryset=Topic.objects.all(),
        view_name='topic-detail'
    )

    class Meta:
        model = Profile
        fields = ('url', 'id', 'username', 'email', 'first_name', 'last_name',
                  'current_position', 'about_you', 'favorite_topics', 'user',
                  'user_url')

    def get_full_name(self, obj):
        request = self.context['request']
        return request.user.get_full_name()

    def update(self, instance, validated_data):
        # retrieve the User
        user_data = validated_data.pop('user', None)
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)

        # retrieve Topics
        # favorite_topics = validated_data.pop('favorite_topics', [])
        # for attr, value in user_data.items():
        #     setattr(instance.user, attr, value)
        #
        # favorite_topics =

        # retrieve Profile
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.user.save()
        instance.save()
        return instance


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#
#     class Meta:
#         model = User
#         fields = ('url', 'id', 'username', 'first_name', 'last_name', 'email',
#                   'is_superuser', 'is_staff', 'profile')
#
#
# class ProfileSerializer(serializers.HyperlinkedModelSerializer):
#     user_url = serializers.HyperlinkedIdentityField(view_name='user-detail')
#     user = serializers.ReadOnlyField(source='user.id')
#     full_name = serializers.SerializerMethodField(source='get_full_name')
#     email = serializers.ReadOnlyField(source='user.email')
#
#     class Meta:
#         model = Profile
#         depth = 1
#         fields = ('url', 'id', 'full_name', 'email', 'current_position',
#                   'about_you', 'favorite_topics', 'user', 'user_url')
#
#     def get_full_name(self, obj):
#         request = self.context['request']
#         return request.user.get_full_name()
#
#
# class TopicSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Topic
#         fields = ('url', 'id', 'name', 'description')
