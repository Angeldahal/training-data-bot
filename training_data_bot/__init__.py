"""
Training Data Curation Bot

Enterprise-grade training data curation bot for LLM fine-tuning
using Decodo + Python automation.
"""

__version__ = "0.1.0"
__author__ = "Angal Dahal"
__email__ = "angeldahal2002@gmail.com"
__description__ = "Enterprise-grade training data curation bot for LLM fine-tuning"

from .core.config import settings
from .core.logging import get_loggers
from .core.exceptions import TrainingDataBotError

from .bot import TrainingDataBot

from .sources import (
    PDFLoader,
    WebLoader,
    DocumentLoader,
    UnifiedLoader,
)

from .tasks import (
    QAGenerator,
    SummarizationGenerator,
    ClassificationGenerator,
    TaskTemplate,
)

from .decodo import DecodoClient
from .preprocessing import TextPreprocessor
from .evaluation import QualityEvaluator
from .storage import DatasetExporter

__all__ = [
    # Core
    "TrainingDataBot",
    "settings",
    "get_logger",
    "TrainingDataBotError",
    # Sources
    "PDFLoader",
    "WebLoader",
    "DocumentLoader",
    "UnifiedLoader",

    # Tasks
    "QAGenerator",
    "ClassificationGenerator",
    "SummarizationGenerator",
    "TaskTemplate",

    # Services
    "DecodoClient",
    "TextPreprocessor",
    "QualityEvaluator",
    "DatasetExporter",
    ]
