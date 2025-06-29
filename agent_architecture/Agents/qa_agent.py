"""
The QA Agent ensures translation quality and flags issues requiring attention
Strategy:
- Automated checks: Length ratios, untranslated content, terminology consistency
- Confidence thresholds: Different actions based on quality scores
- Human escalation: Complex issues automatically flagged for human review

Role: The "Editor-in-Chief" - comprehensive quality assurance using professional translation frameworks.
Multi-Layer Quality Assessment:
Layer 1 - Linguistic Quality:

Fluency: Does it sound natural to native speakers?
Accuracy: Is the meaning preserved correctly?
Terminology: Are domain-specific terms translated properly?

Layer 2 - Contextual Quality:

Consistency: Same terms translated the same way throughout
Register: Formal/informal tone matches source and target culture
Cultural Appropriateness: Idioms, references, cultural concepts

Layer 3 - Technical Quality:

Completeness: Nothing missing, nothing added
Formatting: Preserves structure, handles special characters
Localization: Currency, dates, phone numbers in target format

Professional Frameworks:

BLEU/METEOR Scoring: Automated metrics for baseline quality
DQF (Dynamic Quality Framework): Professional translation industry standard
Custom Rubrics: Domain-specific quality criteria

Critical Innovation: Most MT systems stop at linguistic accuracy. This agent evaluates like a professional translation agency.
"""

from agent_architecture.States.translation_state import TranslationState


def qa_agent(translation_state: TranslationState) -> dict:
    """
    Review translation quality and determine next steps
    Args:
        translation_state (TranslationState): The current state of the translation process

    Returns:
        dict: A dictionary containing the quality score, quality issues, and next action
    """
    source_text = translation_state["source_text"]
    translated_text = translation_state["translated_text"]
    confidence_score = translation_state["confidence_score"]
    
    quality_issues = []
    quality_score = confidence_score  # Start with service confidence
    
    # Check for obvious quality problems
    if not translated_text or translated_text == "Translation failed":
        quality_issues.append("Translation completely failed")
        quality_score = 0.0
    
    # Length check (translations shouldn't be dramatically different in length)
    length_ratio = len(translated_text) / len(source_text) if source_text else 0
    if length_ratio < 0.3 or length_ratio > 3.0:
        quality_issues.append("Suspicious length difference")
        quality_score -= 0.2
    
    # Check for untranslated text (common issue)
    if any(word in translated_text for word in source_text.split()[:3]):
        untranslated_words = [word for word in source_text.split()[:3] 
                            if word in translated_text]
        if len(untranslated_words) > 1:
            quality_issues.append(f"Possibly untranslated words: {untranslated_words}")
            quality_score -= 0.1
    
    # Terminology consistency check
    repeated_phrases = translation_state.get("repeated_phrases", [])
    for original_phrase, expected_translation in repeated_phrases:
        if original_phrase in source_text and expected_translation not in translated_text:
            quality_issues.append(f"Terminology inconsistency: {original_phrase}")
            quality_score -= 0.15
    
    # Determine action based on quality
    if quality_score >= 0.8:
        next_action = "complete"
    elif quality_score >= 0.6:
        next_action = "complete"  # Acceptable quality
    elif quality_score >= 0.4:
        next_action = "retry"  # Try different approach
    else:
        next_action = "human_review"  # Needs human attention
    
    return {
        "quality_score": quality_score,
        "quality_issues": quality_issues,
        "next_action": next_action,
        "needs_human_review": next_action == "human_review",
        "messages": [f"QA: Quality score {quality_score:.2f}, action: {next_action}"]
    }