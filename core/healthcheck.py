from django.http import JsonResponse


def health_check(request: object) -> JsonResponse:
    return JsonResponse({"status": "ok"})
