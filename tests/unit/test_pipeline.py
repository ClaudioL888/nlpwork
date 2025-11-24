from src.core.nlp.pipeline import NLPPipeline
from src.core.nlp.types import SentimentLabel


def test_pipeline_positive_text():
    pipeline = NLPPipeline()
    text = "I love how awesome this project is, 感激 all the support!"
    result = pipeline.analyze(text)

    assert result.sentiment.label == SentimentLabel.positive
    assert result.sentiment.confidence > 0.34
    assert result.empathy.score > 0
    assert result.text_hash


def test_pipeline_crisis_detection():
    pipeline = NLPPipeline()
    text = "I feel overwhelmed and think about suicide now"
    result = pipeline.analyze(text)

    assert result.crisis.probability >= 0.5
    assert "suicide" in result.crisis.indicators
    assert any(chunk.label == "crisis" for chunk in result.evidence)
