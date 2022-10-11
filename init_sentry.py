import os
import sentry_sdk


IGNORED_EXCEPTIONS = [
    "'NoneType' object has no attribute 'status'"
]


def before_send(event, hint):
    exception_message = hint['exc_info'][1].args[0]
    if exception_message in IGNORED_EXCEPTIONS:
        return None

    return event


sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    traces_sample_rate=0.5,
    before_send=before_send
)
