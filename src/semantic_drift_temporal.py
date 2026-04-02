"""
Temporal Semantic Drift Analysis Module

Research-based implementation of semantic drift tracking over time.
Based on:
- Kulkarni et al. (2015): "Statistically Significant Detection of Linguistic Change"
- Bamler & Mandt (2017): "Dynamic Word Embeddings"
- Hamilton et al. (2016): "Cultural shift or linguistic drift? Comparing two computational measures"

This module extends semantic drift analysis to track how concepts evolve 
across time segments or iterations, providing insights into whether:
1. Student understanding improves or degrades over time
2. Answer quality maintains consistency
3. Concept drift indicates learning or confusion
"""

import numpy as np
from typing import List, Dict, Tuple
import re


class TemporalSemanticDrift:
    """
    Analyze semantic drift over time segments.
    
    Tracks how a student's understanding of concepts evolves across:
    - Multiple submission attempts
    - Different time periods
    - Sequential segments of an answer
    """
    
    def __init__(self, model=None):
        """
        Initialize temporal drift analyzer.
        
        Args:
            model: SentenceTransformer model (optional, falls back to TF similarity)
        """
        self.model = model
        self.drift_history = []
        self.similarity_trajectory = []
        
    def compute_temporal_drift(
        self,
        reference: str,
        student_answers: List[str],
        time_points: List[float] = None
    ) -> Dict:
        """
        Compute semantic drift across multiple time points.
        
        This implements the temporal drift framework where we measure
        how a student's answer deviates from reference at different times.
        
        Args:
            reference: The reference/correct answer
            student_answers: List of student answers at different times
            time_points: Optional list of timestamps (0-100 scale)
        
        Returns:
            Dict with:
            - drift_trajectory: List of drift values over time
            - average_drift: Mean drift across all time points
            - drift_trend: Whether drift increases (learning) or decreases (confusion)
            - improvement_score: How much student improved (-1 to 1)
            - consistency_score: How stable the understanding is (0-1)
        """
        if not student_answers:
            return {
                'drift_trajectory': [],
                'average_drift': 0.0,
                'drift_trend': 'null',
                'improvement_score': 0.0,
                'consistency_score': 0.0,
                'volatility': 0.0
            }
        
        # Set time points if not provided
        if time_points is None:
            time_points = np.linspace(0, 100, len(student_answers)).tolist()
        
        # Compute similarity at each time point
        similarities = []
        for answer in student_answers:
            sim = self._compute_similarity(reference, answer)
            similarities.append(sim)
        
        # Convert similarities to drifts
        drifts = [1.0 - s for s in similarities]
        
        # Analyze trajectory
        improvement_score = self._compute_improvement_trend(drifts)
        consistency_score = self._compute_consistency(drifts)
        drift_trend = self._classify_trend(improvement_score)
        volatility = self._compute_volatility(drifts)
        
        return {
            'drift_trajectory': [round(d, 3) for d in drifts],
            'similarity_trajectory': [round(s, 3) for s in similarities],
            'time_points': time_points,
            'average_drift': round(np.mean(drifts), 3),
            'average_similarity': round(np.mean(similarities), 3),
            'drift_trend': drift_trend,
            'improvement_score': round(improvement_score, 3),
            'consistency_score': round(consistency_score, 3),
            'volatility': round(volatility, 3),
            'peak_similarity_time': time_points[np.argmax(similarities)] if similarities else 0,
            'lowest_similarity_time': time_points[np.argmin(similarities)] if similarities else 0,
        }
    
    def compute_segment_temporal_drift(
        self,
        reference: str,
        student_answer: str,
        num_segments: int = 5
    ) -> Dict:
        """
        Split answer into time segments and analyze drift progression.
        
        This treats an answer as developing over time (from beginning to end),
        analyzing how well each segment aligns with the reference.
        
        Args:
            reference: Reference answer
            student_answer: Full student answer
            num_segments: Number of time segments to divide answer into
        
        Returns:
            Dict with segment-by-segment drift analysis
        """
        if not student_answer.strip():
            return {
                'segment_drifts': [],
                'segment_similarities': [],
                'temporal_pattern': 'empty',
                'understanding_trajectory': 'flat'
            }
        
        words = student_answer.split()
        segment_size = max(1, len(words) // num_segments)
        
        drifts = []
        similarities = []
        
        for i in range(num_segments):
            start_idx = i * segment_size
            if i == num_segments - 1:
                # Include remaining words in last segment
                end_idx = len(words)
            else:
                end_idx = (i + 1) * segment_size
            
            segment_text = ' '.join(words[start_idx:end_idx])
            if segment_text.strip():
                sim = self._compute_similarity(reference, segment_text)
                similarities.append(sim)
                drifts.append(1.0 - sim)
        
        # Analyze pattern
        trajectory = self._classify_temporal_pattern(drifts)
        
        return {
            'segment_drifts': [round(d, 3) for d in drifts],
            'segment_similarities': [round(s, 3) for s in similarities],
            'num_segments': len(drifts),
            'average_drift': round(np.mean(drifts), 3) if drifts else 0.0,
            'temporal_pattern': trajectory,
            'understanding_trajectory': self._classify_understanding(similarities),
            'improvement_within_answer': round(
                (similarities[-1] - similarities[0]) if similarities else 0,
                3
            ),
            'consistency_within_answer': round(
                self._compute_consistency(drifts),
                3
            )
        }
    
    def compute_concept_evolution(
        self,
        reference: str,
        student_answers: List[str],
        concepts: List[str] = None
    ) -> Dict:
        """
        Track how specific concept understanding evolves over time.
        
        Implementation of concept drift detection where we monitor whether
        a student maintains understanding of key concepts across submissions.
        
        Args:
            reference: Reference answer
            student_answers: Multiple student submissions over time
            concepts: List of key concepts to track (auto-extracted if None)
        
        Returns:
            Dict with concept-level drift tracking
        """
        if not concepts:
            concepts = self._extract_key_concepts(reference)
        
        if not concepts:
            return {
                'concept_tracking': {},
                'concepts_strengthening': [],
                'concepts_weakening': [],
                'concept_stability': 0.0
            }
        
        concept_coverage_over_time = {}
        
        for concept in concepts:
            coverage = []
            for answer in student_answers:
                # Simple concept presence detection
                concept_lower = concept.lower()
                answer_lower = answer.lower()
                is_present = 1.0 if concept_lower in answer_lower else 0.0
                coverage.append(is_present)
            concept_coverage_over_time[concept] = coverage
        
        # Analyze trends
        strengthening = []
        weakening = []
        
        for concept, coverage in concept_coverage_over_time.items():
            if len(coverage) > 1:
                trend = coverage[-1] - coverage[0]
                if trend > 0.3:
                    strengthening.append(concept)
                elif trend < -0.3:
                    weakening.append(concept)
        
        stability = self._compute_concept_stability(concept_coverage_over_time)
        
        return {
            'concept_tracking': concept_coverage_over_time,
            'concepts_strengthening': strengthening,
            'concepts_weakening': weakening,
            'concept_stability': round(stability, 3),
            'monitored_concepts': concepts
        }
    
    def detect_concept_drift(
        self,
        reference: str,
        student_answers: List[str],
        threshold: float = 0.3
    ) -> Dict:
        """
        Detect concept drift - significant change in similarity pattern.
        
        Based on concept drift detection literature (Gama et al., 2014),
        identifies when a student's understanding pattern changes significantly.
        
        Args:
            reference: Reference answer
            student_answers: Sequential submissions
            threshold: Significance threshold for drift detection
        
        Returns:
            Dict with concept drift events
        """
        if len(student_answers) < 2:
            return {
                'concept_drift_detected': False,
                'drift_points': [],
                'drift_magnitude': 0.0,
                'drift_direction': 'none'
            }
        
        similarities = [self._compute_similarity(reference, ans) for ans in student_answers]
        drifts = [1.0 - s for s in similarities]
        
        # Detect significant changes
        drift_changes = []
        for i in range(1, len(drifts)):
            change = abs(drifts[i] - drifts[i-1])
            if change > threshold:
                drift_changes.append({
                    'position': i,
                    'previous_drift': round(drifts[i-1], 3),
                    'current_drift': round(drifts[i], 3),
                    'magnitude': round(change, 3)
                })
        
        # Determine overall direction
        if similarities:
            overall_change = similarities[-1] - similarities[0]
            direction = 'improving' if overall_change > 0.1 else 'degrading' if overall_change < -0.1 else 'stable'
        else:
            direction = 'none'
        
        return {
            'concept_drift_detected': len(drift_changes) > 0,
            'drift_points': drift_changes,
            'num_drift_events': len(drift_changes),
            'drift_magnitude': round(max([d['magnitude'] for d in drift_changes]) if drift_changes else 0.0, 3),
            'drift_direction': direction,
            'average_drift_magnitude': round(
                np.mean([d['magnitude'] for d in drift_changes]) if drift_changes else 0.0,
                3
            )
        }
    
    # ─────── Helper Methods ───────
    
    def _compute_similarity(self, text1: str, text2: str) -> float:
        """Compute similarity between two texts."""
        if self.model:
            # Use transformer if available
            try:
                emb1 = self.model.encode(text1, convert_to_numpy=True)
                emb2 = self.model.encode(text2, convert_to_numpy=True)
                return float(np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2) + 1e-10))
            except:
                pass
        
        # Fallback: simple token overlap (Jaccard similarity)
        tokens1 = set(re.findall(r'\b\w+\b', text1.lower()))
        tokens2 = set(re.findall(r'\b\w+\b', text2.lower()))
        
        if not tokens1 and not tokens2:
            return 1.0
        if not tokens1 or not tokens2:
            return 0.0
        
        intersection = len(tokens1 & tokens2)
        union = len(tokens1 | tokens2)
        return intersection / union
    
    def _compute_improvement_trend(self, drifts: List[float]) -> float:
        """
        Compute improvement trend from drift trajectory.
        
        Range: -1 (worsening) to +1 (improving)
        """
        if len(drifts) < 2:
            return 0.0
        
        # Linear regression-like trend
        x = np.arange(len(drifts))
        y = np.array(drifts)
        
        # Inverse because lower drift is better
        slope = np.polyfit(x, -y, 1)[0]
        
        return np.clip(slope, -1, 1)
    
    def _compute_consistency(self, drifts: List[float]) -> float:
        """Compute consistency score (lower stddev = higher consistency)."""
        if len(drifts) < 2:
            return 1.0
        
        stddev = np.std(drifts)
        # Normalize: 0 = completely inconsistent, 1 = perfectly consistent
        return 1.0 / (1.0 + stddev)
    
    def _compute_volatility(self, drifts: List[float]) -> float:
        """Compute volatility (instability) in drift trajectory."""
        if len(drifts) < 2:
            return 0.0
        
        differences = np.abs(np.diff(drifts))
        return float(np.mean(differences))
    
    def _classify_trend(self, improvement_score: float) -> str:
        """Classify trend as improving, stable, or degrading."""
        if improvement_score > 0.1:
            return 'improving'
        elif improvement_score < -0.1:
            return 'degrading'
        else:
            return 'stable'
    
    def _classify_temporal_pattern(self, drifts: List[float]) -> str:
        """Classify the pattern of drift over segments."""
        if not drifts:
            return 'empty'
        
        if len(drifts) < 2:
            return 'single'
        
        # Check if improving (decreasing drift)
        improvement = drifts[-1] - drifts[0]
        
        if improvement > 0.2:
            return 'improving'
        elif improvement < -0.2:
            return 'degrading'
        else:
            # Check for consistency
            changes = [abs(drifts[i] - drifts[i+1]) for i in range(len(drifts)-1)]
            if np.mean(changes) < 0.1:
                return 'consistent'
            else:
                return 'volatile'
    
    def _classify_understanding(self, similarities: List[float]) -> str:
        """Classify understanding trajectory."""
        if not similarities:
            return 'empty'
        
        if similarities[-1] > 0.7:
            return 'strong_understanding'
        elif similarities[-1] > 0.5:
            return 'moderate_understanding'
        elif similarities[-1] > 0.3:
            return 'weak_understanding'
        else:
            return 'poor_understanding'
    
    def _extract_key_concepts(self, text: str) -> List[str]:
        """Extract key concepts from text (simple TF-based approach)."""
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Simple stopword removal
        stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'is', 'are', 'was', 'were', 'be', 'been', 'is', 'have', 'has', 'had'
        }
        
        concepts = [w for w in words if w not in stopwords and len(w) > 3]
        
        # Count frequency
        from collections import Counter
        freq = Counter(concepts)
        
        # Return top 5 concepts
        return [word for word, _ in freq.most_common(5)]
    
    def _compute_concept_stability(self, concept_coverage: Dict[str, List[float]]) -> float:
        """Compute how stable concept understanding is across time."""
        if not concept_coverage:
            return 0.0
        
        stabilities = []
        for coverage in concept_coverage.values():
            if len(coverage) < 2:
                stabilities.append(1.0)
            else:
                changes = [abs(coverage[i] - coverage[i+1]) for i in range(len(coverage)-1)]
                stability = 1.0 / (1.0 + np.mean(changes))
                stabilities.append(stability)
        
        return float(np.mean(stabilities)) if stabilities else 0.0


# ─────────────────────────────────────────────
# Function interface for integration
# ─────────────────────────────────────────────

def analyze_temporal_drift(
    reference: str,
    student_answers: List[str],
    model=None
) -> Dict:
    """
    High-level function to analyze temporal semantic drift.
    
    Args:
        reference: Reference answer
        student_answers: List of student answers over time
        model: Optional SentenceTransformer model
    
    Returns:
        Complete temporal drift analysis
    """
    analyzer = TemporalSemanticDrift(model=model)
    
    return {
        'temporal_drift': analyzer.compute_temporal_drift(reference, student_answers),
        'segment_analysis': analyzer.compute_segment_temporal_drift(reference, student_answers[0] if student_answers else ''),
        'concept_evolution': analyzer.compute_concept_evolution(reference, student_answers),
        'concept_drift_detection': analyzer.detect_concept_drift(reference, student_answers)
    }


if __name__ == '__main__':
    # Example usage
    reference = "Machine learning is a subset of AI that enables systems to learn from data without explicit programming."
    
    student_answers = [
        "AI is about computers",  # Time 1: Poor understanding
        "Machine learning uses data for AI",  # Time 2: Improving
        "Machine learning is a subset of AI where systems learn from data",  # Time 3: Good understanding
    ]
    
    analyzer = TemporalSemanticDrift()
    result = analyze_temporal_drift(reference, student_answers)
    
    print("Temporal Drift Analysis Results:")
    print(f"Improvement Trend: {result['temporal_drift']['drift_trend']}")
    print(f"Improvement Score: {result['temporal_drift']['improvement_score']}")
    print(f"Consistency: {result['temporal_drift']['consistency_score']}")
    print(f"Concept Drift Events: {result['concept_drift_detection']['num_drift_events']}")
