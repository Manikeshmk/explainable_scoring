"""
Kafka Producer for ExplainGrade AI
Submits student answers to Kafka for real-time processing
"""

import json
import time
import uuid
from datetime import datetime
from kafka import KafkaProducer
from kafka.errors import KafkaError


class GradingProducer:
    def __init__(self, bootstrap_servers='localhost:9092'):
        """Initialize Kafka producer"""
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            acks='all',  # Wait for all replicas to acknowledge
            retries=3
        )
        self.topic = 'submissions'
    
    def submit_answer(self, student_email, question, reference_answer, student_answer):
        """
        Submit a student answer for grading
        
        Args:
            student_email: Student's email
            question: Question asked
            reference_answer: Reference/ideal answer
            student_answer: Student's provided answer
        
        Returns:
            submission_id: Unique ID for this submission
        """
        submission_id = str(uuid.uuid4())
        
        submission = {
            "submission_id": submission_id,
            "timestamp": datetime.now().isoformat(),
            "student_email": student_email,
            "question": question,
            "reference_answer": reference_answer,
            "student_answer": student_answer,
            "status": "pending"
        }
        
        # Send to Kafka
        future = self.producer.send(self.topic, value=submission)
        
        try:
            record_metadata = future.get(timeout=10)
            print(f"✓ Submission {submission_id}")
            print(f"  Topic: {record_metadata.topic}")
            print(f"  Partition: {record_metadata.partition}")
            print(f"  Offset: {record_metadata.offset}")
            return submission_id
        except KafkaError as e:
            print(f"✗ Failed to send submission: {e}")
            return None
    
    def batch_submit(self, submissions_list):
        """
        Submit multiple answers
        
        Args:
            submissions_list: List of dicts with keys:
                - student_email
                - question
                - reference_answer
                - student_answer
        
        Returns:
            List of submission IDs
        """
        submission_ids = []
        for submission in submissions_list:
            submission_id = self.submit_answer(
                submission['student_email'],
                submission['question'],
                submission['reference_answer'],
                submission['student_answer']
            )
            submission_ids.append(submission_id)
            time.sleep(0.1)  # Small delay between submissions
        
        self.producer.flush()  # Ensure all messages are sent
        return submission_ids
    
    def close(self):
        """Close the producer"""
        self.producer.close()


def main():
    """Example usage"""
    producer = GradingProducer()
    
    # Example submissions
    test_submissions = [
        {
            "student_email": "student1@example.com",
            "question": "What is machine learning?",
            "reference_answer": "Machine learning is a subset of AI where systems learn from data without explicit programming",
            "student_answer": "Machine learning is when computers learn from data"
        },
        {
            "student_email": "student2@example.com",
            "question": "Explain neural networks",
            "reference_answer": "Neural networks are computing systems inspired by biological neural networks that constitute animal brains",
            "student_answer": "Neural networks are inspired by brains and learn patterns"
        }
    ]
    
    print("📤 Submitting answers to Kafka...")
    submission_ids = producer.batch_submit(test_submissions)
    print(f"✓ Submitted {len(submission_ids)} answers")
    
    producer.close()


if __name__ == "__main__":
    main()
