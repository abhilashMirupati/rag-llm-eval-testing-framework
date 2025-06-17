from typing import List
from dataclasses import dataclass
import numpy as np
from deepeval.metrics import (
    FactualConsistencyMetric, ContextualRelevancyMetric, ContextualPrecisionMetric,
    ContextualRecallMetric, FaithfulnessMetric, HallucinationMetric,
    AnswerRelevancyMetric, CoherenceMetric, ConcisenessMetric, CompletenessMetric
)
from sentence_transformers import SentenceTransformer
import spacy

@dataclass
class EvaluationResult:
    score: float
    details: str = ""

class Scorer:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.embedding_model = SentenceTransformer(model_name)
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            spacy.cli.download("en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")

    def evaluate_answer_relevance(self, answer: str, question: str) -> EvaluationResult:
        metric = AnswerRelevancyMetric()
        score = metric.measure(query=question, answer=answer)
        return EvaluationResult(score=score, details=f"Answer relevance score for question: '{question[:50]}...'")

    def evaluate_context_relevance(self, context: str, question: str) -> EvaluationResult:
        metric = ContextualRelevancyMetric()
        score = metric.measure(query=question, context=context)
        return EvaluationResult(score=score, details=f"Context relevance score for question: '{question[:50]}...'")

    def evaluate_faithfulness(self, answer: str, context: str) -> EvaluationResult:
        metric = FaithfulnessMetric()
        score = metric.measure(retrieval_context=[context], answer=answer)
        return EvaluationResult(score=score, details="Faithfulness evaluation complete.")
        
    def evaluate_fluency(self, answer: str) -> EvaluationResult:
        from textblob import TextBlob
        blob = TextBlob(answer)
        errors = len(blob.correct().words) - len(blob.words)
        score = 1.0 - (errors / len(blob.words)) if len(blob.words) > 0 else 1.0
        return EvaluationResult(score=max(0.0, score), details=f"Found {errors} potential spelling errors.")

    def evaluate_redundancy(self, answer: str) -> EvaluationResult:
        doc = self.nlp(answer)
        sentences = [sent.text for sent in doc.sents]
        if len(sentences) < 2:
            return EvaluationResult(score=1.0, details="Answer has less than two sentences; no redundancy.")
        embeddings = self.embedding_model.encode(sentences)
        similarity_matrix = self.embedding_model.similarity(embeddings, embeddings)
        upper_triangle_indices = np.triu_indices(len(sentences), k=1)
        if upper_triangle_indices[0].size == 0:
            return EvaluationResult(score=1.0, details="No sentence pairs to compare.")
        max_similarity = np.max(similarity_matrix[upper_triangle_indices])
        score = 1.0 - max_similarity
        return EvaluationResult(score=float(score), details=f"Max inter-sentence similarity: {max_similarity:.2f}")

    # ... include all other evaluate_* methods from our final scorer version ...