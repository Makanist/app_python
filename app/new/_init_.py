"""New SMS module"""
from .providers import PrimarySmsApiProvider, SecondarySmsApiProvider


def sms_factory(provider):
    """Implement a factory that creates appropriate objects based on the `api` argument.
    When `api` is unknown, throw NotImplementedError exception."""
    if provider == 'primary':
        return PrimarySmsApiProvider()
    elif provider == 'secondary':
        return SecondarySmsApiProvider()
    else:
        raise NotImplementedError(f"Unknown provider: {provider}")
    
    return