import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
from uuid import UUID

from .core.config import settings
from .core.logging import get_logger, LogContext
from .core.exceptions import TrainingDataBotError, ConfigurationError

from .sources import UnifiedLoader
from .decodo import DecodoClient
from .ai import AIClient
from .tasks import TaskManager
from .preprocessing import TextPreprocessor
from .evaluation import QualityEvaluator
from .storage import DatasetExporter, DatabaseManager
from .models import (
    Document,
    DocumentType,
    ProcessingJob,
    Dataset,
    TaskType,
    QualityReport
)

class TrainingDataBot:
    """
    Main Training Data Bot Class.

    This class provides high-level interface for:
    - Loading documents from various sources.
    - Processing text with task templates.
    - Quality assessment and filtering.
    - Dataset creation and export.
    """
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the training data bot.
        Args:
            config: Optional configuration overrides.
        """
        self.logger = get_logger("training_data_bot")
        self.config = config or {}
        self._init_components()
        self.logger.info("Training Data Bot initialized successfully.")
    

    def _init_components(self):
        """Initialize all bot components"""
        try:
            self.loader = UnifiedLoader()
            self.decodo_client = DecodoClient()
            self.ai_client = AIClient()
            self.task_manager = TaskManager()
            self.preprocessor = TextPreprocessor()
            self.evaluator = QualityEvaluator()
            self.exporter = DatasetExporter()
            self.db_manager = DatabaseManager()
            
            self.documents: Dict[UUID, Document] = {}
            self.datasets: Dict[UUID, Dataset] = {}
            self.jobs: Dict[UUID, ProcessingJob] = {}
        except Exception as e:
            raise ConfigurationError("Failed to initialize bot components", ...)
    
    async def load_documents(
            self,
            sources: Union[str, Path, List[Union[str, Path]]],
            doc_types: Optional[List[DocumentType]] = None,
            **kwargs,
    ) -> List[Document]:
        if isinstance(sources, (str, Path)):
            sources = [sources]
        
        documents = []
        for source in sources:
            if source.is_dir():
                dir_docs = await self.loader.load_directory(source)
                documents.extend(dir_docs)
            else:
                doc = await self.loader.load_single(source)
                documents.append(doc)
        for doc in documents:
            self.documents[doc.id] = doc
    
    async def process_documents(
            self,
            documents: Optional[List[Document]] = None,
            task_types: Optional[List[TaskType]] = None,
            quality_filter: bool = True,
            **kwargs,
    ) -> Dataset:
        pass

    async def evaluate_dataset(
            self,
            dataset: Dataset,
            detailed_report: bool = True,
    ) -> QualityReport:
        pass

    async def export_dataset(
            self,
            dataset: Dataset,
            output_path: Union[str, Path],
            format: ExportFormat = ExportFormat.JSONL,
            split_data: bool = True,
            **kwargs,
    ) -> Path:
        pass

    def get_statistics(self) -> Dict[str, Any]:
         return {
             "documents": {
                 "total": len(self.documents),
                 "by_type": self._count_by_type(...),
                 "total_size": sum(doc.size for doc in ...)
             },
             "datasets": {
                 "total": len(self.datasets),
                 "total_example": sum(len(ds.examples)),
                 "by_task_type": self._count_examples_by_task_type()
             },
             "jobs": {
                 "total": len(self.jobs),
                 "by_status": self._count_by_type(...),
                 "active": len([j for j in self.jobs.values()])
             }
         }
    
    async def cleanup(self):
        """Cleanup resources and close connections."""
        try:
            await self.db_manager.close()
            if hasattr(self.decodo_client, 'close'):
                await self.decodo_client.close()
            if hasattr(self.ai_client, 'close'):
                await self.ai_client.close()
            self.logger.info("Bot cleanup completed.")
        except Exception as e:
            pass
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.cleanup()

    async def quick_process(
            self,
            source: Union[str, Path],
            output_path: Union[str, Path],
            task_types: Optional[List[TaskType]] = None,
            export_format: ExportFormat = ExportFormat.JSONL,
    ) -> Dataset:
        documents = await self.load_documents([source])
        dataset = await self.process_documents(documents=documents, task_types=task_types)
        await self.export_dataset(dataset=dataset, output_path=output_path, format=export_format)
        return dataset
