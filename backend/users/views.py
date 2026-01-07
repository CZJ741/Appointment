from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from .models import User
from .serializers import UserSerializer, UserRegisterSerializer, UserLoginSerializer
from rest_framework.authtoken.models import Token

@api_view(['POST'])
@permission_classes([AllowAny])
def user_register(request):
    """用户注册接口"""
    try:
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # 移除自动登录，让用户注册后自行登录
            return Response({'message': '注册成功，请登录'}, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    """用户登录接口"""
    try:
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                # 移除login()调用，避免session相关操作
                # 直接生成或获取token
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'message': '登录成功',
                    'token': token.key,
                    'user_id': user.id,
                    'username': user.username,
                    'full_name': user.full_name,
                    'is_staff': user.is_staff
                }, status=status.HTTP_200_OK)
            return Response({'error': '用户名或密码错误'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    """用户登出接口"""
    try:
        # 移除logout()调用，直接删除token
        request.user.auth_token.delete()
        return Response({'message': '登出成功'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    """获取当前登录用户信息接口"""
    try:
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request, user_id):
    """
    删除用户接口
    在删除用户前先清理相关的token和其他关联数据，避免外键约束错误
    """
    try:
        # 获取要删除的用户
        user = User.objects.get(id=user_id)
        
        # 删除用户关联的token
        Token.objects.filter(user=user).delete()
        
        # 删除用户关联的session（如果使用了session认证）
        from django.contrib.sessions.models import Session
        sessions = Session.objects.filter(expire_date__gte=timezone.now())
        for session in sessions:
            try:
                session_data = session.get_decoded()
                if session_data.get('_auth_user_id') == str(user.id):
                    session.delete()
            except:
                pass
        
        # 删除用户（Appointment模型已经设置了级联删除，会自动删除相关的预约记录）
        user.delete()
        
        return Response({'message': '用户删除成功'}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
