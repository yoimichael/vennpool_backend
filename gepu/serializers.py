from rest_framework.serializers import ModelSerializer
from .models import User, Hash, Post, Event

''' no backward relation from serializer '''

# no need to feedback 'join_date'
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id','car_info','phone', 'fb_id','messenger_id','fbtoken','name', 'email','photo')

class UserPublicSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id','car_info','fb_id','name')

class PostSerializer(ModelSerializer):
    # can access phone number
    users = UserSerializer(read_only=True, many=True)
    class Meta:
        model = Post
        fields = ('id','isRide', 'third_Party', 'from_addr','seats','event',
        'creator','time','users')
    # not using to_addr for now

class PostPublicSerializer(ModelSerializer):
    users = UserPublicSerializer(read_only=True, many=True)
    class Meta:
        model = Post
        fields = ('id','isRide', 'third_Party', 'from_addr','seats','event',
        'creator','time','users')

# serializers used for RESTful responses
class EventSerializer(ModelSerializer):
    members = UserPublicSerializer(read_only=True, many=True)
    hosts = UserPublicSerializer(read_only=True, many=True)
    posts = PostSerializer(read_only=True, many=True)
    class Meta:
        model = Event
        fields = ('id','fb_eid','posts','members','hosts')

class HashSerializer(ModelSerializer):
    class Meta:
        model = Hash
        fields = ('hash_code','whitelist','valid','valid_until','event')
