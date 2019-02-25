from rest_framework.serializers import ModelSerializer
from .models import User, Group, Post, Event

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id','phone','name', 'car_info', 'email','photo','groups','posts')

class PostSerializer(ModelSerializer):
    users = UserSerializer(read_only=True, many=True)
    class Meta:
        model = Post
        fields = ('id','event','creatorID','isRide', 'third_Party', 'from_addr','seats','time','users')

class GroupSerializer(ModelSerializer):
    users = UserSerializer(read_only=True, many=True)
    class Meta:
        model = Group
        fields = ('id','gid','name','admin', 'users', 'events')
        
class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = ('id','title','to_addr','photo', 'info','posts','time','group')

