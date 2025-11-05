from dataclasses import Field
import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4


class BaseEntity(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime.datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime.datetime] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class DocumentType(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    MD = "md"
    TXT = "txt"
    HTML = "html"
    JSON = "json"
    CSV = "csv"
    URL = "url"


class TaskType(str, Enum):
    QA_GENERATION = "qa_generation"
    CLASSIFICATION = "classification"
    SUMMARIZATION = "summarization"
    NER = "named_entity_recognition"
    RED_TEAMING = "red_teaming"
    INSTRUCTION_RESPONSE = "instruction_response"


class QualityMetric(str, Enum):
    TOXICITY = "toxicity"
    BIAS = "bias"
    DIVERSITY = "diversity"
    COHERENCE = "coherence"
    RELEVANCE = "relevance"


class Document(BaseEntity):
    title: str
    content: str
    source: str
    doc_type: DocumentType
    word_count: int
    char_count: int


class TextChunk(BaseEntity):
    document_id: UUID
    content: str
    start_index: int
    end_index: int
    chunk_index: int
    token_count: int


class TaskTemplate(BaseEntity):
    name: str
    task_type: TaskType
    description: str
    prompt_template: str
    parameters: dict


class TaskResult(BaseEntity):
    task_id: UUID
    input_chunk_id: UUID
    output: str
    confidence: float
    quality_scores: dict
    processing_time: float


class TrainingExample(BaseEntity):
    input_text: str
    output_text: str
    task_type: TaskType
    source_document_id: UUID
    quality_scores: int


class Dataset(BaseEntity):
    name: str
    description: str
    examples: List[TrainingExample]
    total_examples: int
    train_split: float
    validation_split: float
    test_split: float


class QualityReport(BaseEntity):
    target_id: UUID
    overall_score: float
    passed: bool
    metric_scores: dict
    issues: List[str]
    warnings: List[str]


class ProcessingJob(BaseEntity):
    name: str
    job_type: str
    status: ProcessingStatus
    total_items: int
    processed_items: int
    started_at: datetime.datetime
    estimated_completion: datetime.datetime

class ExportFormat(str, Enum):
    JSONL = "jsonl"
    JSON = "json"
