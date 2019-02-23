
from rest_framework.serializers import ModelSerializer
from .models import User, Group, Post, Event

class UserSerializer(ModelSerializer):
    groups = GroupSerializer(read_only=True, many=True)
    posts = PostSerializer(read_only=True, many=True)
    class Meta:
        model = User
        fields = ('id','phone','name', 'car_info', 'email','photo','groups','posts')

class PostSerializer(ModelSerializer):
    users = UserSerializer(read_only=True, many=True)
    class Meta:
        model = Post
        fields = ('eventID','users','isRide', 'third_Party', 'from_addr','count','time')

class EventSerializer(ModelSerializer):
    # not really an id but a lead to the group
    groupID = GroupSerializer(read_only=True, many=False)
    class Meta:
        model = Event
        fields = ('id','title','to_addr','photo', 'info', 'createrID','posts','count','time','groupID')

class GroupSerializer(ModelSerializer):
    users = UserSerializer(read_only=True, many=True)
    events = EventSerializer(read_only=True, many=True)
    class Meta:
        model = Group
        fields = ('id','gid','name','admin', 'users', 'events')
