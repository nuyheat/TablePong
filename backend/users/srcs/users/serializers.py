from rest_framework import serializers
from .models import User
from friends.models import Friend


class JoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'profile_img']
        extra_kwargs = {
            'profile_img': {'required': True}
        }
        
    def to_internal_value(self, data):
        for fieldname in ["username", "profile_img"]:
            if fieldname not in data:
                raise serializers.ValidationError(
                {
                    "error_code": [400],
                    "detail": ["필드 이름이 잘못되었습니다"]
                }
            )
        ## 잘못된 필드이름 확인
        
        username = data.get('username')
        profile_img = data.get('profile_img')
        if not username or not profile_img:
            raise serializers.ValidationError(
                {
                    "error_code": [400],
                    "detail": ["필드 값이 비어있습니다"]
                }
            )
        ## request의 fieldvalue가 비어있는 경우

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {
                    "error_code": [400],
                    "detail": ["사용중인 username 입니다"]
                }
            )
        ## 중복된 유저이름 확인
        return super().to_internal_value(data)
    def save(self):
        user = User.objects.create(
            username = self.validated_data['username'],
            profile_img = self.validated_data['profile_img'],
        )
        user.save()
        return user
    # database에 user객체를 생성합니다.

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['status_msg', 'macrotext1', 'macrotext2', 'macrotext3', 'macrotext4', 'macrotext5']
        
    def to_internal_value(self, data):
        for fieldname in data:
            if fieldname not in ['status_msg', 'macrotext1', 'macrotext2', 'macrotext3', 'macrotext4', 'macrotext5']:
                raise serializers.ValidationError(
                {
                    "error_code": [400],
                    "detail": ["필드 이름이 잘못되었습니다"]
                }
            )
        ## 잘못된 필드이름 확인
        
        return super().to_internal_value(data)
    def save(self):
        user = self.instance
        for fieldname, fieldvalue in self.validated_data.items():
            if fieldvalue == '':
                fieldvalue = '텍스트를 입력하세요'
            setattr(user, fieldname, fieldvalue)
        user.save()
        return user
class RetrieveSearchUserSerializer(serializers.Serializer):
    search = serializers.CharField()

    def validate(self, data):
        user = self.instance
        if user.status == User.STATUS_MAP['오프라인']:
            raise serializers.ValidationError(
                {
                    "error_code": 403,
                    "detail": "로그인 상태가 아닙니다"
                }
            )
        ## 로그인 하지 않은 경우

        username = data.get('search')
        if not username:
            raise serializers.ValidationError(
                {
                    "error_code": 400,
                    "detail": "유저 이름을 입력해주세요"
                }
            )
        ## 파라미터가 비어있는 경우

        users = User.objects.filter(username__icontains=username).exclude(username=user.username)
        if not users:
            raise serializers.ValidationError(
                {
                    "error_code": 204,
                    "detail": "일치하는 유저가 없습니다"
                }
            )
        ## username이 들어간 user들을 찾지 못한 경우
        
        return {'users': users}
class RetrieveSearchUserResponseSerializer(serializers.ModelSerializer):
    is_friend = serializers.BooleanField()

    class Meta:
        model = User
        fields = ['username', 'status_msg', 'profile_img', 'is_friend']

class CreateFriendshipSerializer(serializers.Serializer):
    friendname = serializers.CharField()

    def to_internal_value(self, data):
        if 'friendname' not in data:
            raise serializers.ValidationError(
                {
                    "error_code": [400],
                    "detail": ["필드 이름이 잘못되었습니다"]
                }
            )
        ## 잘못된 필드이름 확인
        
        friendname = data.get('friendname')
        if not friendname:
            raise serializers.ValidationError(
                {
                    "error_code": [400],
                    "detail": ["필드 값이 비어있습니다"]
                }
            )
        ## request의 fieldvalue가 비어있는 경우

        return super().to_internal_value(data)
    def validate(self, data):
        friendname = data.get('friendname')
        friend = User.objects.filter(username=friendname).first()
        if friend is None:
            raise serializers.ValidationError(
                {
                    "error_code": 400,
                    "detail": "존재하지 않는 friendname입니다"
                }
            )
        ## user테이블에 존재하지 않는 friendname인 경우
        
        user = self.instance
        if user == friend:
            raise serializers.ValidationError(
                {
                    "error_code": 400,
                    "detail": "유저 본인을 친구추가 할 수 없습니다"
                }
            )
        ## 본인을 친구추가 하는 경우
        
        old_friendship = Friend.objects.filter(username=user, friendname=friend).first()
        if old_friendship:
            raise serializers.ValidationError(
                {
                    "error_code": 400,
                    "detail": "이미 친구상태 입니다"
                }
            )
        ## 이미 친구추가 되어있는 경우
        
        return {'friend': friend}
    def save(self):
        new_friendship = Friend(
            username = self.instance,
            friendname = self.validated_data['friend']
        )
        new_friendship.save()
        return new_friendship
class DeleteFriendshipSerializer(serializers.Serializer):
    friendname = serializers.CharField()

    def validate(self, data):
        friendname = data.get('friendname')
        friend = User.objects.filter(username=friendname).first()
        if friend is None:
            raise serializers.ValidationError(
                {
                    "error_code": 400,
                    "detail": "존재하지 않는 friendname입니다"
                }
            )
        ## user테이블에 존재하지 않는 friendname인 경우
        
        old_friendship = Friend.objects.filter(username=self.instance, friendname=friend).first()
        if old_friendship is None:
            raise serializers.ValidationError(
                {
                    "error_code": 400,
                    "detail": "이미 친구상태가 아닙니다"
                }
            )
        ## 이미 친구해제 되어있는 경우
        
        return {'old_friendship': old_friendship}
    def save(self):
        old_friendship = self.validated_data['old_friendship']
        old_friendship.delete()
        return old_friendship

class MacroTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['macrotext1', 'macrotext2', 'macrotext3', 'macrotext4', 'macrotext5']

class RetrieveFriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'status_msg', 'status', 'exp', 'win_cnt', 'lose_cnt', 'profile_img']

class RetrieveUserSerializer(serializers.ModelSerializer):
    macrotext = MacroTextSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'exp', 'profile_img', 'win_cnt', 'lose_cnt', 'status_msg', 'macrotext']