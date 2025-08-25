from saq.types import SettingsDict

from app.bg_jobs import hooks
from app.core.containers import AppContainer

settings: SettingsDict = {
    'queue': AppContainer.saq_queue.resolve_sync(),
    'functions': (),
    'startup': hooks.startup,
    'shutdown': hooks.shutdown,
}
