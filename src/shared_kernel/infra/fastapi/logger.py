from datetime import datetime
from src.shared_kernel.infra.fastapi.config import settings
from src.shared_kernel.infra.elasticsearch import ElasticsearchHandler


class Logger:
    def __init__(self, level, message) -> None:
        # LOGGER = logging.getLogger(__name__)
        elasticsearch_handler = ElasticsearchHandler(settings.ELK_STACK_URL)
        elasticsearch_handler.emit({
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'message': message
        })
