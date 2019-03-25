from rest_framework.serializers import ModelSerializer
from .models import User, Hash, Post, Event

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id','car_info','phone', 'events', 'fb_id','messenger_id','fbtoken','name', 'email','photo','join_date',
        'posts','your_posts','events')

class PostSerializer(ModelSerializer):
    users = UserSerializer(read_only=True, many=True)
    class Meta:
        model = Post
        fields = ('id','isRide', 'third_Party', 'from_addr','to_addr','seats','event',
        'creator','time','users')

# serializers used for RESTful responses
class EventSerializer(ModelSerializer):
    members = UserSerializer(read_only=True, many=True)
    class Meta:
        model = Event
        fields = ('id','fb_eid', 'title','to_addr','time','info','photo',
        'posts','members','hash')

class HashSerializer(ModelSerializer):
    class Meta:
        model = Hash
        fields = ('hash_code','whitelist','valid','valid_until','event')
