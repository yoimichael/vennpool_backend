from rest_framework.serializers import ModelSerializer
from .models import User, Hash, Post, Event

''' no backward relation from serializer '''

# no need to feedback 'join_date'
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id','car_info','phone', 'fb_id','messenger_id','fbtoken','name', 'email','photo')

class DriverUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id','car_info','fb_id','name','phone')

class RiderPublicSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id','fb_id','name','phone')

class PostSerializer(ModelSerializer):
    # can access phone number
    users = RiderPublicSerializer(read_only=True, many=True)
    creator = DriverUserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ('id', 'event', 'from_addr','seats','creator','time','users')
    # not using ,'isRide', 'third_Party', to_addr for now

class PostPublicSerializer(ModelSerializer):
    creator = DriverUserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ('id', 'event', 'from_addr','seats','creator','time','users')

    # users will only be a list of ids

# serializers used for RESTful responses
class EventSerializer(ModelSerializer):
    posts = PostPublicSerializer(read_only=True, many=True)
    class Meta:
        model = Event
        fields = ('id','fb_eid','posts')

class HashSerializer(ModelSerializer):
    class Meta:
        model = Hash
        fields = ('hash_code','whitelist','valid','valid_until','event')
