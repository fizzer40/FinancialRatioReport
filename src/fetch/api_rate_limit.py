import time

def safe_api_call(func, retries=3, wait=2):
    for attempt in range(retries):
        try:
            return func()
        except Exception:
            if attempt == retries - 1:
                raise
            time.sleep(wait)