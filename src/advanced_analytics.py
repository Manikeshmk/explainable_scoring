"""
advanced_analytics.py — Advanced Temporal Analytics for ExplainGrade
====================================================================

Implements:
1. Anomaly Detection — detects unusual learning patterns
2. Peer Comparison — compares students to cohort
3. Key Concept Mastery Timeline — tracks individual concept progression
4. Semantic Momentum & Prediction — predicts future performance
5. Semantic Coverage Metrics — multi-dimensional coverage tracking
6. Multidimensional Learning Curves — tracks multiple metrics over time
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict
import re


@dataclass
class StudentMetrics:
    """Container for a student's computed metrics across submissions."""
    student_id: str
    student_name: str
    submissions: List[Dict]
    scores: List[float]
    improvement_scores: List[float]
    consistency_scores: List[float]
    concept_coverage: Dict[str, List[float]]


class AnomalyDetector:
    """
    Detects anomalies in learning patterns:
    - Sudden score jumps (possible cheating/external help)
    - Sudden drops (confusion/error introduction)
    - Non-linear patterns (unusual learning curves)
    """
    
    def __init__(self, z_score_threshold: float = 2.5):
        """
        Args:
            z_score_threshold: Standard deviations to flag as anomaly (default 2.5)
        """
        self.z_threshold = z_score_threshold
        
    def detect_score_anomalies(self, scores: List[float]) -> Dict:
        """
        Detect anomalous score changes between submissions.
        
        Returns:
            Dict with anomaly flags and details
        """
        if len(scores) < 2:
            return {
                'anomalies_detected': False,
                'anomaly_count': 0,
                'anomaly_points': [],
                'anomaly_type': 'none'
            }
        
        # Calculate score differences
        diffs = [scores[i+1] - scores[i] for i in range(len(scores)-1)]
        
        if not diffs or len(diffs) < 2:
            return {
                'anomalies_detected': False,
                'anomaly_count': 0,
                'anomaly_points': [],
                'anomaly_type': 'none'
            }
        
        # Calculate z-scores
        mean_diff = np.mean(diffs)
        std_diff = np.std(diffs)
        
        if std_diff == 0:
            return {
                'anomalies_detected': False,
                'anomaly_count': 0,
                'anomaly_points': [],
                'anomaly_type': 'none'
            }
        
        z_scores = [(d - mean_diff) / std_diff for d in diffs]
        
        # Find anomalies
        anomalies = []
        for i, z in enumerate(z_scores):
            if abs(z) > self.z_threshold:
                anomalies.append({
                    'position': i + 2,  # submission number
                    'from_score': scores[i],
                    'to_score': scores[i+1],
                    'change': diffs[i],
                    'z_score': round(z, 2),
                    'type': 'jump_up' if diffs[i] > 0 else 'jump_down'
                })
        
        # Classify pattern
        pattern = self._classify_anomaly_pattern(diffs)
        
        return {
            'anomalies_detected': len(anomalies) > 0,
            'anomaly_count': len(anomalies),
            'anomaly_points': anomalies,
            'anomaly_type': pattern,
            'mean_change': round(mean_diff, 3),
            'volatility': round(std_diff, 3)
        }
    
    def _classify_anomaly_pattern(self, diffs: List[float]) -> str:
        """Classify the type of anomalous pattern."""
        if not diffs:
            return 'none'
        
        positive_count = sum(1 for d in diffs if d > 0)
        negative_count = sum(1 for d in diffs if d < 0)
        
        # Oscillating pattern (many ups and downs)
        if positive_count > 2 and negative_count > 2:
            return 'oscillating'
        
        # Consistent improvement
        elif positive_count > len(diffs) * 0.7:
            return 'stable_improvement'
        
        # Consistent degradation
        elif negative_count > len(diffs) * 0.7:
            return 'stable_degradation'
        
        # Gradual changes (normal)
        else:
            return 'gradual'
    
    def detect_consistency_anomalies(self, consistency_scores: List[float]) -> Dict:
        """
        Detect when consistency suddenly drops (indicating confusion).
        
        Returns:
            Dict with consistency anomaly information
        """
        if len(consistency_scores) < 2:
            return {
                'consistency_anomalies': False,
                'drop_count': 0,
                'drop_points': []
            }
        
        drops = []
        for i in range(len(consistency_scores) - 1):
            drop = consistency_scores[i] - consistency_scores[i+1]
            # Flag as anomaly if consistency drops by >0.2
            if drop > 0.2:
                drops.append({
                    'position': i + 2,
                    'from': round(consistency_scores[i], 3),
                    'to': round(consistency_scores[i+1], 3),
                    'drop': round(drop, 3)
                })
        
        return {
            'consistency_anomalies': len(drops) > 0,
            'drop_count': len(drops),
            'drop_points': drops
        }


class PeerComparison:
    """
    Compares individual student performance to peer cohort.
    """
    
    def __init__(self):
        self.cohort_metrics = {}
        
    def compute_percentile(self, student_metric: float, all_metrics: List[float]) -> float:
        """Calculate percentile rank for a metric."""
        if not all_metrics:
            return 50.0
        
        rank = sum(1 for m in all_metrics if m <= student_metric)
        return (rank / len(all_metrics)) * 100
    
    def compare_student_to_cohort(
        self,
        student_name: str,
        student_scores: List[float],
        student_improvement: float,
        student_consistency: float,
        cohort_scores_list: List[List[float]],
        cohort_improvements: List[float],
        cohort_consistencies: List[float]
    ) -> Dict:
        """
        Compare a student's performance to the entire cohort.
        
        Returns:
            Dict with percentile ranks and cohort statistics
        """
        # Flatten cohort scores for percentile calculation
        all_scores = [s for scores in cohort_scores_list for s in scores]
        
        final_score = student_scores[-1] if student_scores else 0
        
        return {
            'student_name': student_name,
            'final_score': round(final_score, 3),
            'final_score_percentile': round(self.compute_percentile(final_score, all_scores), 1),
            'improvement_percentile': round(
                self.compute_percentile(student_improvement, cohort_improvements),
                1
            ),
            'consistency_percentile': round(
                self.compute_percentile(student_consistency, cohort_consistencies),
                1
            ),
            'cohort_avg_final_score': round(np.mean(all_scores), 3),
            'cohort_avg_improvement': round(np.mean(cohort_improvements), 3),
            'cohort_avg_consistency': round(np.mean(cohort_consistencies), 3),
            'above_average_score': final_score > np.mean(all_scores),
            'above_average_improvement': student_improvement > np.mean(cohort_improvements),
            'above_average_consistency': student_consistency > np.mean(cohort_consistencies)
        }
    
    def cluster_students(
        self,
        students_data: List[Dict]
    ) -> Dict:
        """
        Cluster students by learning pattern similarity.
        
        Returns:
            Dict with cluster assignments and characteristics
        """
        if not students_data:
            return {'clusters': [], 'cluster_count': 0}
        
        # Features for clustering: [improvement, consistency, volatility]
        features = []
        student_names = []
        
        for student in students_data:
            improvement = student.get('improvement_score', 0)
            consistency = student.get('consistency_score', 0)
            
            if student.get('scores'):
                scores = student['scores']
                volatility = np.std([s for s in scores if isinstance(s, (int, float))]) \
                    if len(scores) > 1 else 0
            else:
                volatility = 0
            
            features.append([improvement, consistency, volatility])
            student_names.append(student.get('student_name', 'Unknown'))
        
        features = np.array(features)
        
        # Simple k-means clustering (k=3 for fast/slow/steady learners)
        clusters = self._kmeans_clustering(features, k=3)
        
        # Label clusters
        cluster_labels = {
            0: 'Rapid Learners',
            1: 'Steady Learners',
            2: 'Struggling Learners'
        }
        
        return {
            'clusters': [
                {
                    'label': cluster_labels.get(c, f'Cluster {c}'),
                    'students': [student_names[i] for i in range(len(student_names)) if clusters[i] == c],
                    'size': sum(1 for c_id in clusters if c_id == c)
                }
                for c in set(clusters)
            ],
            'cluster_count': len(set(clusters))
        }
    
    def _kmeans_clustering(self, X: np.ndarray, k: int, max_iters: int = 10) -> np.ndarray:
        """Simple k-means implementation."""
        n_samples = X.shape[0]
        
        # Initialize random centroids
        indices = np.random.choice(n_samples, k, replace=False)
        centroids = X[indices]
        
        for _ in range(max_iters):
            # Assign to nearest centroid
            distances = np.sqrt(((X - centroids[:, np.newaxis])**2).sum(axis=2))
            labels = np.argmin(distances, axis=0)
            
            # Update centroids
            new_centroids = np.array([
                X[labels == i].mean(axis=0) if (labels == i).any() else centroids[i]
                for i in range(k)
            ])
            
            # Check convergence
            if np.allclose(centroids, new_centroids):
                break
            
            centroids = new_centroids
        
        return np.argmin(distances, axis=0)


class ConceptMasteryTimeline:
    """
    Tracks how student understanding of specific concepts evolves.
    """
    
    def __init__(self):
        self.concept_mentions = defaultdict(list)
        
    def extract_concepts(self, text: str) -> List[str]:
        """
        Extract key concepts from text.
        Simple implementation: noun phrases and technical terms.
        """
        # Convert to lowercase and split
        words = text.lower().split()
        
        # Extract multi-word phrases and single important words
        concepts = []
        
        # Technical term detection (capitalized in original text, usually)
        original_words = text.split()
        for i, word in enumerate(original_words):
            clean_word = re.sub(r'[^\w]', '', word).lower()
            
            # Prefer longer words (likely to be technical terms)
            if len(clean_word) > 4 and clean_word.isalpha():
                concepts.append(clean_word)
        
        # Extract bigrams (two-word concepts)
        for i in range(len(words) - 1):
            bigram = f"{words[i]} {words[i+1]}"
            if len(words[i]) > 3 and len(words[i+1]) > 3:
                concepts.append(bigram)
        
        # Remove duplicates and return
        return list(set(concepts))[:10]  # Top 10 concepts
    
    def track_concept_mastery(
        self,
        reference: str,
        student_answers: List[str],
        time_points: Optional[List[int]] = None
    ) -> Dict:
        """
        Track how concept coverage evolves across submissions.
        
        Returns:
            Dict with concept mastery timeline
        """
        if not student_answers:
            return {
                'concepts_tracked': [],
                'mastery_timeline': {},
                'concepts_gained': [],
                'concepts_lost': [],
                'concept_stability': 0.0
            }
        
        # Extract reference concepts
        ref_concepts = set(self.extract_concepts(reference))
        
        if not ref_concepts:
            return {
                'concepts_tracked': [],
                'mastery_timeline': {},
                'concepts_gained': [],
                'concepts_lost': [],
                'concept_stability': 0.0
            }
        
        if time_points is None:
            time_points = list(range(1, len(student_answers) + 1))
        
        # Track coverage for each concept
        mastery_timeline = {}
        for concept in list(ref_concepts)[:5]:  # Top 5 concepts
            coverage = []
            for answer in student_answers:
                answer_concepts = set(self.extract_concepts(answer))
                is_present = 1.0 if concept.lower() in [c.lower() for c in answer_concepts] else 0.0
                coverage.append(is_present)
            
            mastery_timeline[concept] = {
                'timeline': coverage,
                'first_mention': next((i for i, c in enumerate(coverage) if c > 0), None),
                'last_mention': next((len(coverage)-1-i for i in range(len(coverage)) if coverage[len(coverage)-1-i] > 0), None),
                'total_mentions': sum(coverage),
                'mastery_trend': coverage[-1] - coverage[0] if coverage else 0
            }
        
        # Concepts gained in latest vs first
        first_answer_concepts = set(self.extract_concepts(student_answers[0]))
        last_answer_concepts = set(self.extract_concepts(student_answers[-1]))
        
        gained = last_answer_concepts - first_answer_concepts
        lost = first_answer_concepts - last_answer_concepts
        
        stability = self._compute_concept_stability(mastery_timeline)
        
        return {
            'concepts_tracked': list(ref_concepts)[:5],
            'mastery_timeline': {
                k: {
                    'timeline': v['timeline'],
                    'first_mention': v['first_mention'],
                    'mastery_trend': round(v['mastery_trend'], 2)
                }
                for k, v in mastery_timeline.items()
            },
            'concepts_gained': list(gained)[:3],
            'concepts_lost': list(lost)[:3],
            'concept_stability': round(stability, 3)
        }
    
    def _compute_concept_stability(self, timeline_dict: Dict) -> float:
        """Compute overall concept stability (lower = more changes)."""
        if not timeline_dict:
            return 0.0
        
        stabilities = []
        for concept_data in timeline_dict.values():
            timeline = concept_data.get('timeline', [])
            if len(timeline) > 1:
                # Measure how consistent the mentions are
                changes = sum(1 for i in range(len(timeline)-1) if timeline[i] != timeline[i+1])
                stability = 1.0 - (changes / (len(timeline) - 1))
                stabilities.append(stability)
        
        return np.mean(stabilities) if stabilities else 0.5


class SemanticMomentum:
    """
    Tracks semantic momentum and predicts future performance.
    """
    
    def __init__(self):
        pass
    
    def compute_momentum(self, scores: List[float]) -> Dict:
        """
        Compute semantic momentum (rate of improvement).
        
        Returns:
            Dict with momentum metrics and predictions
        """
        if len(scores) < 2:
            return {
                'momentum': 0.0,
                'acceleration': 0.0,
                'confidence': 'low',
                'predicted_next_score': scores[0] if scores else 0,
                'prediction_confidence': 0.0
            }
        
        # Momentum = average change per submission
        diffs = [scores[i+1] - scores[i] for i in range(len(scores)-1)]
        momentum = np.mean(diffs)
        
        # Acceleration = change in momentum
        if len(diffs) > 1:
            second_diffs = [diffs[i+1] - diffs[i] for i in range(len(diffs)-1)]
            acceleration = np.mean(second_diffs)
        else:
            acceleration = 0.0
        
        # Predict next score
        if momentum > 0:
            predicted_score = scores[-1] + momentum + (acceleration * 0.5)
            confidence = 'high' if len(scores) >= 4 else 'medium'
        else:
            predicted_score = max(0, scores[-1] + momentum)
            confidence = 'medium'
        
        # Confidence decreases with low momentum variance or few samples
        prediction_confidence = min(1.0, len(scores) / 5.0 * 0.7) if momentum != 0 else 0.3
        
        return {
            'momentum': round(momentum, 3),
            'acceleration': round(acceleration, 3),
            'confidence': confidence,
            'predicted_next_score': round(predicted_score, 3),
            'prediction_confidence': round(prediction_confidence, 2),
            'momentum_direction': 'improving' if momentum > 0.1 else 'declining' if momentum < -0.1 else 'stagnant'
        }
    
    def predict_mastery_timeline(
        self,
        scores: List[float],
        target_score: float = None,
        max_predictions: int = 5
    ) -> Dict:
        """
        Predict when student will reach mastery (target score).
        
        Args:
            scores: Historical scores
            target_score: Target to reach (default: max score)
            max_predictions: Max future predictions to generate
        """
        if len(scores) < 2:
            return {
                'mastery_predicted': False,
                'submissions_to_mastery': None,
                'predicted_timeline': []
            }
        
        # Calculate momentum
        momentum_data = self.compute_momentum(scores)
        momentum = momentum_data['momentum']
        
        if target_score is None:
            target_score = max(scores) * 1.1  # 10% above current max
        
        current_score = scores[-1]
        
        # If not improving, mastery unlikely
        if momentum <= 0:
            return {
                'mastery_predicted': False,
                'submissions_to_mastery': None,
                'predicted_timeline': [],
                'reason': 'No improvement momentum detected'
            }
        
        # Calculate submission count to mastery
        gap = target_score - current_score
        submissions_needed = gap / momentum
        
        # Generate predictions
        predictions = []
        for i in range(1, min(int(submissions_needed) + 2, max_predictions + 1)):
            pred_score = current_score + (momentum * i)
            predictions.append({
                'submission_number': len(scores) + i,
                'predicted_score': round(pred_score, 3),
                'confidence': round(1.0 / (1.0 + (i / 3.0)), 2)  # Decreases with distance
            })
        
        return {
            'mastery_predicted': submissions_needed < max_predictions,
            'submissions_to_mastery': int(np.ceil(submissions_needed)) if submissions_needed > 0 else None,
            'predicted_timeline': predictions,
            'momentum': momentum
        }


class SemanticCoverageMetrics:
    """
    Tracks multidimensional semantic coverage.
    """
    
    def compute_coverage_dimensions(
        self,
        reference: str,
        student_answer: str
    ) -> Dict:
        """
        Compute multiple coverage metrics.
        
        Returns multi-dimensional coverage profile
        """
        ref_words = set(reference.lower().split())
        stu_words = set(student_answer.lower().split())
        
        # Lexical coverage (vocabulary overlap)
        lexical_overlap = len(ref_words & stu_words) / len(ref_words) if ref_words else 0
        
        # Concept coverage (key terms, likely longer words)
        ref_concepts = {w for w in ref_words if len(w) > 4}
        stu_concepts = {w for w in stu_words if len(w) > 4}
        concept_coverage = len(ref_concepts & stu_concepts) / len(ref_concepts) if ref_concepts else 0
        
        # Length coverage (answer completeness)
        ref_len = len(reference.split())
        stu_len = len(student_answer.split())
        length_coverage = min(stu_len / ref_len, 1.0) if ref_len > 0 else 0
        
        # Semantic diversity (unique concept count)
        semantic_diversity = len(stu_concepts) / max(len(ref_concepts), 1)
        
        # Precision (no unnecessary concepts)
        precision = len(stu_concepts & ref_concepts) / len(stu_concepts) if stu_concepts else 0
        
        return {
            'lexical_coverage': round(lexical_overlap * 100, 1),
            'concept_coverage': round(concept_coverage * 100, 1),
            'length_coverage': round(length_coverage * 100, 1),
            'semantic_diversity': round(min(semantic_diversity, 1.0) * 100, 1),
            'precision': round(precision * 100, 1),
            'overall_coverage': round(np.mean([
                lexical_overlap,
                concept_coverage,
                length_coverage,
                min(semantic_diversity, 1.0),
                precision
            ]) * 100, 1)
        }


class MultidimensionalLearningCurves:
    """
    Tracks multiple learning metrics simultaneously.
    """
    
    def compute_learning_curves(
        self,
        scores: List[float],
        drift_scores: List[float],
        consistency_scores: List[float],
        coverage_metrics: List[Dict]
    ) -> Dict:
        """
        Create multidimensional learning curves.
        
        Returns curves for multiple metrics
        """
        n_submissions = len(scores)
        
        return {
            'accuracy_curve': {
                'values': [round(s, 3) for s in scores],
                'trend': self._compute_trend(scores),
                'average': round(np.mean(scores), 3),
                'volatility': round(np.std(scores), 3)
            },
            'semantic_drift_curve': {
                'values': [round(1.0 - d, 3) for d in drift_scores],
                'trend': self._compute_trend([1.0 - d for d in drift_scores]),
                'average': round(np.mean([1.0 - d for d in drift_scores]), 3),
                'volatility': round(np.std([1.0 - d for d in drift_scores]), 3)
            },
            'consistency_curve': {
                'values': [round(c, 3) for c in consistency_scores],
                'trend': self._compute_trend(consistency_scores),
                'average': round(np.mean(consistency_scores), 3),
                'volatility': round(np.std(consistency_scores), 3)
            },
            'coverage_curves': {
                'concept_coverage': {
                    'values': [round(m.get('concept_coverage', 0) / 100, 3) for m in coverage_metrics],
                    'trend': self._compute_trend([m.get('concept_coverage', 0) / 100 for m in coverage_metrics]),
                    'average': round(np.mean([m.get('concept_coverage', 0) / 100 for m in coverage_metrics]), 3)
                },
                'lexical_coverage': {
                    'values': [round(m.get('lexical_coverage', 0) / 100, 3) for m in coverage_metrics],
                    'trend': self._compute_trend([m.get('lexical_coverage', 0) / 100 for m in coverage_metrics]),
                    'average': round(np.mean([m.get('lexical_coverage', 0) / 100 for m in coverage_metrics]), 3)
                }
            },
            'submission_count': n_submissions
        }
    
    def _compute_trend(self, values: List[float]) -> str:
        """Compute trend direction."""
        if len(values) < 2:
            return 'insufficient_data'
        
        first_half_avg = np.mean(values[:len(values)//2])
        second_half_avg = np.mean(values[len(values)//2:])
        
        diff = second_half_avg - first_half_avg
        
        if diff > 0.1:
            return 'improving'
        elif diff < -0.1:
            return 'degrading'
        else:
            return 'stable'
