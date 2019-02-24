from rest_framework.serializers import ModelSerializer
from .models import User, Group, Post, Event

class UserInfoSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id','phone','name', 'car_info', 'email','photo')

class PostSerializer(ModelSerializer):
    users = UserInfoSerializer(read_only=True, many=True)
    class Meta:
        model = Post
        fields = ('id','eventID','users','isRide', 'third_Party', 'from_addr','count','time')

class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = ('id','title','to_addr','photo', 'info', 'createrID','posts','count','time','groupID')

class GroupSerializer(ModelSerializer):
    users = UserInfoSerializer(read_only=True, many=True)
    events = EventSerializer(read_only=True, many=True)
    class Meta:
        model = Group
        fields = ('id','gid','name','admin', 'users', 'events')

class UserSerializer(UserInfoSerializer):
    groups = GroupSerializer(read_only=True, many=True)
    posts = PostSerializer(read_only=True, many=True)
    class Meta:
        model = User
        fields = ('id','phone','name', 'car_info', 'email','photo','groups','posts')
