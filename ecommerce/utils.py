from django.http import JsonResponse
import logging

logger = logging.getLogger("django")

# grab JS's console.logs adn pass them to the Python logger for logging
def log_js(request):
    level = request.GET.get("level", "info").lower()
    message = request.GET.get("message", "No message received.")

    # Log the message based on severity level
    if level == "error":
        logger.error(f"JS: {message}")
    elif level == "warning":
        logger.warning(f"JS: {message}")
    else:
        logger.info(f"JS: {message}")

    return JsonResponse({"status": "success"})