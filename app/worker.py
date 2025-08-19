from saq import CronJob
from saq.types import SettingsDict

from app.bg_jobs import hooks
from app.bg_jobs.add_money import add_money
from app.bg_jobs.complete_withdrawal import complete_withdrawal
from app.bg_jobs.create_agent_customer import create_agent_customer
from app.bg_jobs.debarred.update_names import update_debarred_names
from app.bg_jobs.export.invoices import export_invoices
from app.bg_jobs.withdraw import withdraw
from app.core.containers import AppContainer

settings: SettingsDict = {
    'queue': AppContainer.saq_queue.resolve_sync(),
    'functions': (
        update_debarred_names,
        add_money,
        withdraw,
        complete_withdrawal,
        create_agent_customer,
        export_invoices,
    ),
    'concurrency': 10,
    'cron_jobs': (
        # WorldBank updates the debarred list every three hours (three minutes for any delays)
        CronJob(
            update_debarred_names,
            cron='3 0-23/3 * * *',  # every 3 hours starting from 00:03
            retries=10,
        ),
    ),
    'startup': hooks.startup,
    'shutdown': hooks.shutdown,
}
