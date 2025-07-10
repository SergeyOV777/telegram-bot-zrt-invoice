import logging

def safe_execute(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except Exception:
        logging.exception(f"Ошибка при выполнении {fn.__name__}")
        return None
