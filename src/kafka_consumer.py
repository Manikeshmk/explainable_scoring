"""
Kafka Consumer for ExplainGrade AI
Processes student submissions in real-time from Kafka
"""

import json
import time
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from datetime import datetime
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from local_grader import grade_answer


class GradingConsumer:
    def __init__(self, bootstrap_servers='localhost:9092', group_id='grading-workers'):
        """Initialize Kafka consumer"""
        self.consumer = KafkaConsumer(
            'submissions',
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            max_poll_records=100
        )
        self.output_topic = 'grades'
        self.grades_processed = 0
    
    def process_submission(self, submission):
        """
        Process a single submission
        
        Args:
            submission: Dict with submission data
        
        Returns:
            Grade result dict
        """
        try:
            # Grade the answer
            grade_result = grade_answer(
                submission['reference_answer'],
                submission['student_answer'],
                max_score=10.0
            )
            
            # Add metadata
            grade_result['submission_id'] = submission['submission_id']
            grade_result['student_email'] = submission['student_email']
            grade_result['processed_at'] = datetime.now().isoformat()
            grade_result['status'] = 'completed'
            
            return grade_result
        except Exception as e:
            return {
                'submission_id': submission['submission_id'],
                'student_email': submission['student_email'],
                'status': 'error',
                'error': str(e),
                'processed_at': datetime.now().isoformat()
            }
    
    def start_consuming(self, batch_size=10):
        """
        Start consuming messages from Kafka
        
        Args:
            batch_size: Number of messages to process before committing
        """
        print(f"🔵 Consumer started. Listening on 'submissions' topic...")
        print(f"   Consumer group: grading-workers")
        print(f"   Batch size: {batch_size}")
        print("   (Press Ctrl+C to stop)\n")
        
        batch = []
        
        try:
            for message in self.consumer:
                submission = message.value
                
                print(f"📨 Received submission: {submission['submission_id']}")
                
                # Process submission
                grade = self.process_submission(submission)
                batch.append(grade)
                
                # Print grade result
                print(f"   ✓ Grade: {grade['score']:.1f}/10")
                
                self.grades_processed += 1
                
                # Process batch when it reaches desired size
                if len(batch) >= batch_size:
                    self.save_batch(batch)
                    batch = []
        
        except KeyboardInterrupt:
            print("\n\n⏹️  Consumer stopped by user")
            if batch:
                self.save_batch(batch)
        
        finally:
            self.consumer.close()
            print(f"\n📊 Total grades processed: {self.grades_processed}")
    
    def save_batch(self, batch):
        """
        Save a batch of grades (to file/database)
        
        Args:
            batch: List of grade results
        """
        filename = f"grades_batch_{int(time.time())}.json"
        with open(filename, 'w') as f:
            json.dump(batch, f, indent=2)
        print(f"   💾 Saved batch of {len(batch)} grades to {filename}")
    
    def get_consumer_lag(self):
        """Get consumer lag statistics"""
        partitions = self.consumer.partitions_for_topic('submissions')
        if not partitions:
            return None
        
        lag_info = {}
        for partition in partitions:
            tp = self.consumer.position(partition)
            committed = self.consumer.committed(partition)
            lag = tp - (committed or 0) if committed else 0
            lag_info[f'partition_{partition}'] = lag
        
        return lag_info


def main():
    """Start the consumer"""
    try:
        consumer = GradingConsumer(bootstrap_servers='localhost:9092')
        consumer.start_consuming(batch_size=5)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
