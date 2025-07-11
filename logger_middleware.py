import json
import requests
from django.utils.deprecation import MiddlewareMixin

def get_location(ip):
    try:
        res = requests.get(f"https://ip-api.com/json/{ip}")
        data = res.json()
        return f"{data.get('country')}, {data.get('regionName')}, {data.get('city')}"
    except Exception:
        return "lookup failed"

class UserLoggerMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
        user_agent = request.META.get('HTTP_USER_AGENT', 'unknown')
        cookies = request.COOKIES
        email = cookies.get('email') or request.META.get('HTTP_X_USER_EMAIL', 'not provided')
        location = get_location(ip)
        path = request.path
        timestamp = request.META.get('HTTP_DATE', 'unknown')

        log_data = {
            "timestamp": timestamp,
            "ip": ip,
            "user_agent": user_agent,
            "cookies": dict(cookies),
            "email": email,
            "location": location,
            "path": path,
        }

        # Guardar en archivo local
        try:
            with open("user_logs.txt", "a", encoding="utf-8") as f:
                f.write(json.dumps(log_data) + "\n")
        except Exception:
            pass

        # (Opcional) Enviar a un endpoint externo
        # try:
        #     requests.post("https://TU_ENDPOINT/api/log", json=log_data)
        # except Exception:
        #     pass 