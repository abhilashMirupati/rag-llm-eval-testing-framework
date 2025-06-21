import time
import random
from functools import wraps
from typing import Any, Callable

def retry_with_exponential_backoff(
    func: Callable,
    initial_delay: float = 1.0,
    exponential_base: float = 2.0,
    max_retries: int = 5,
    jitter: bool = True
) -> Callable:
    """
    Decorator for retrying a function with exponential backoff and optional jitter.

    Args:
        func: The function to be decorated.
        initial_delay: Starting delay between retries (in seconds).
        exponential_base: The base for the exponential backoff.
        max_retries: Maximum number of retry attempts.
        jitter: Whether to add random jitter to the delay.

    Returns:
        The decorated function with retry logic.
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        num_retries = 0
        delay = initial_delay
        while True:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                num_retries += 1
                if num_retries > max_retries:
                    raise Exception(f"Maximum retries ({max_retries}) exceeded. Last error: {e}")
                delay *= exponential_base
                if jitter:
                    delay += random.uniform(0, 1)
                time.sleep(delay)
    return wrapper
