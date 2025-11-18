from django.http import JsonResponse
from django.core.exceptions import ValidationError
from rest_framework.exceptions import APIException
import traceback

class CustomExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_exception(self, request, exception):
        # 如果请求路径以/api/开头，则返回JSON格式的错误信息
        if request.path.startswith('/api/'):
            # 处理验证错误
            if isinstance(exception, ValidationError):
                return JsonResponse({'error': exception.message_dict}, status=400)
            # 处理API异常
            elif isinstance(exception, APIException):
                return JsonResponse({'error': exception.detail}, status=exception.status_code)
            # 处理其他异常
            else:
                # 在开发环境中可以打印异常堆栈
                print(traceback.format_exc())
                return JsonResponse({'error': str(exception)}, status=500)
        # 非API请求不处理，让Django默认处理
        return None