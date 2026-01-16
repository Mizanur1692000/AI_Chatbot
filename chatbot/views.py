from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import secrets
from .ai_utils import get_ai_response
from .models import ChatMessage, UserSession

@method_decorator(csrf_exempt, name="dispatch")
class SetEmailView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            email = data.get('email')

            if not email:
                return JsonResponse({'error': 'Email not provided'}, status=400)

            # Store email in session for browser clients (optional)
            request.session['user_email'] = email

            # Issue or rotate a token for API clients (Postman/mobile)
            token = secrets.token_hex(32)
            UserSession.objects.update_or_create(
                email=email,
                defaults={"token": token},
            )

            return JsonResponse({'message': 'Email set successfully', 'token': token})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

@method_decorator(csrf_exempt, name="dispatch")
class ChatView(View):
    def post(self, request, *args, **kwargs):
        # Allow auth via Bearer token or X-Session-Token header; fall back to session
        auth_header = request.headers.get('Authorization', '')
        token_header = request.headers.get('X-Session-Token')
        email = None

        token = None
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ', 1)[1].strip()
        elif token_header:
            token = token_header.strip()

        if token:
            session = UserSession.objects.filter(token=token).first()
            if session:
                email = session.email

        if not email and 'user_email' in request.session:
            email = request.session.get('user_email')

        if not email:
            return JsonResponse({'error': 'Unauthorized. Provide token or set email first.'}, status=401)
        
        try:
            data = json.loads(request.body)
            user_message = data.get('message')

            if not user_message:
                return JsonResponse({'error': 'Message not provided'}, status=400)

            # Get AI response
            bot_response = get_ai_response(user_message)

            # Save chat to database
            ChatMessage.objects.create(
                user_message=user_message,
                bot_response=bot_response
            )

            return JsonResponse({'response': bot_response})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

