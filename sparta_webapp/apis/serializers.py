from rest_framework import serializers
from builtins import object
from sparta_webapp.common.models import ServerInfor, ServerGroup, Credential, CommandsSequence

from sparta_webapp.users.models import UserKey, User
from rest_framework.response import Response

class MessageSerializer(serializers.Serializer):
	message = serializers.CharField()

class UserSerializer(serializers.HyperlinkedModelSerializer):
	userkeys = serializers.PrimaryKeyRelatedField(many=True, queryset=UserKey.objects.all())
	class Meta:
		model = User
		fields = (
			'id', 'username', 'email', 'groups', 'password', 
			'last_login', 'is_superuser', 'first_name',
			'last_name', 'is_staff', 'is_active', 'date_joined', 
			'userkeys' 
		)
		extra_kwargs = {
			'url': {'view_name': 'users', 'lookup_field': 'username'},
			'password': {'write_only': True}
		}

	def create(self, validated_data):
		user = User(
			email = validated_data["email"],
			username = validated_data["username"]
		)
		user.set_password(validated_data["password"])
		user.save()
		return user

class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model =	User 
		fields = ('username', 'location', 'birthdate', 'company', 'role')
		extra_kwargs = {
			'url': {'view_name': 'profiles', 'lookup_field': 'username'}
		}

class SSHKeySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = UserKey
		fields = ('user', 'name', 'key')
		extra_kwargs =  {
			'url': {'view_name': 'sshkeys', 'lookup_field': 'user'},
			'name': {'required': True}, 
			'password': {'write_only': True}
		}

class ServerInforSerializer(serializers.HyperlinkedModelSerializer):
    class Meta(object):
        model = ServerInfor
        fields = '__all__'

class ServerGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta(object):
        model = ServerGroup
        fields = '__all__'
            
class CredentialSerializer(serializers.HyperlinkedModelSerializer):
    class Meta(object):
        model = Credential
        fields = '__all__'            
        
class CommandsSequenceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta(object):
        model = CommandsSequence
        fields = '__all__'                    
