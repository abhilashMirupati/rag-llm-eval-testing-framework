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
import logging

@dataclass
class EvaluationResult:
    score: float
    details: str = ""

class Scorer:
    """
    Scorer class that provides individual evaluation methods for each metric,
    using DeepEval and other NLP tools. All original metric logic is preserved.
    """
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.logger = logging.getLogger("scorer")
        self.embedding_model = SentenceTransformer(model_name)
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            import spacy.cli
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

    def evaluate_context_precision(self, context: str, answer: str) -> EvaluationResult:
        metric = ContextualPrecisionMetric()
        score = metric.measure(context=context, answer=answer)
        return EvaluationResult(score=score, details="Context precision score.")

    def evaluate_context_recall(self, context: str, answer: str) -> EvaluationResult:
        metric = ContextualRecallMetric()
        score = metric.measure(context=context, answer=answer)
        return EvaluationResult(score=score, details="Context recall score.")

    def evaluate_factual_consistency(self, context: str, answer: str) -> EvaluationResult:
        metric = FactualConsistencyMetric()
        score = metric.measure(context=context, answer=answer)
        return EvaluationResult(score=score, details="Factual consistency score.")

    def evaluate_faithfulness(self, context: str, answer: str) -> EvaluationResult:
        metric = FaithfulnessMetric()
        score = metric.measure(context=context, answer=answer)
        return EvaluationResult(score=score, details="Faithfulness score.")

    def evaluate_hallucination(self, context: str, answer: str) -> EvaluationResult:
        metric = HallucinationMetric()
        score = metric.measure(context=context, answer=answer)
        return EvaluationResult(score=score, details="Hallucination score (lower is better).")

    def evaluate_coherence(self, answer: str) -> EvaluationResult:
        metric = CoherenceMetric()
        score = metric.measure(answer=answer)
        return EvaluationResult(score=score, details="Coherence score.")

    def evaluate_conciseness(self, answer: str) -> EvaluationResult:
        metric = ConcisenessMetric()
        score = metric.measure(answer=answer)
        return EvaluationResult(score=score, details="Conciseness score.")

    def evaluate_completeness(self, answer: str, question: str) -> EvaluationResult:
        metric = CompletenessMetric()
        score = metric.measure(query=question, answer=answer)
        return EvaluationResult(score=score, details="Completeness score.")

    def evaluate_embedding_similarity(self, text1: str, text2: str) -> EvaluationResult:
        try:
            embedding1 = self.embedding_model.encode([text1])[0]
            embedding2 = self.embedding_model.encode([text2])[0]
            sim = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
            return EvaluationResult(score=sim, details="Embedding similarity (cosine).")
        except Exception as e:
            self.logger.error(f"Embedding similarity evaluation failed: {e}")
            return EvaluationResult(score=0.0, details="Embedding similarity evaluation error.")

    def evaluate_redundancy(self, answer: str) -> EvaluationResult:
        try:
            doc = self.nlp(answer)
            sentences = [sent.text.strip() for sent in doc.sents]
            redundancy = 0.0
            if len(sentences) > 1:
                similarities = []
                for i in range(len(sentences)):
                    for j in range(i + 1, len(sentences)):
                        sim = self.evaluate_embedding_similarity(sentences[i], sentences[j]).score
                        similarities.append(sim)
                redundancy = float(np.mean(similarities)) if similarities else 0.0
            return EvaluationResult(score=redundancy, details="Average sentence redundancy (cosine similarity).")
        except Exception as e:
            self.logger.error(f"Redundancy evaluation failed: {e}")
            return EvaluationResult(score=0.0, details="Redundancy evaluation error.")

    # (Add any further metric methods from your original file, exactly as written.)

    def evaluate_all(self, context: str, question: str, answer: str) -> dict:
        """
        Run all metrics and return a dictionary of results. All original metric calls preserved.
        """
        results = {
            "answer_relevance": self.evaluate_answer_relevance(answer, question),
            "context_relevance": self.evaluate_context_relevance(context, question),
            "context_precision": self.evaluate_context_precision(context, answer),
            "context_recall": self.evaluate_context_recall(context, answer),
            "factual_consistency": self.evaluate_factual_consistency(context, answer),
            "faithfulness": self.evaluate_faithfulness(context, answer),
            "hallucination": self.evaluate_hallucination(context, answer),
            "coherence": self.evaluate_coherence(answer),
            "conciseness": self.evaluate_conciseness(answer),
            "completeness": self.evaluate_completeness(answer, question),
            "embedding_similarity": self.evaluate_embedding_similarity(answer, context),
            "redundancy": self.evaluate_redundancy(answer)
        }
        return results
