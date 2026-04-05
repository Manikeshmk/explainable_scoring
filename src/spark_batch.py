"""
Apache Spark Batch Processing for ExplainGrade AI
Process large batches of submissions for analytics
"""

import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, avg, stddev, min as spark_min, max as spark_max,
    count, when, round as spark_round, desc, window,
    from_json, schema_of_json
)
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.evaluation import RegressionEvaluator
from datetime import datetime


class SparkBatchGrader:
    def __init__(self, app_name="ExplainGrade Analytics"):
        """Initialize Spark session"""
        self.spark = SparkSession.builder \
            .appName(app_name) \
            .master("local[*]") \
            .getOrCreate()
        
        self.spark.sparkContext.setLogLevel("WARN")
    
    def load_submissions(self, filepath):
        """
        Load submissions from JSON file
        
        Args:
            filepath: Path to JSON file with submissions
        
        Returns:
            Spark DataFrame
        """
        print(f"📂 Loading submissions from {filepath}...")
        
        try:
            df = self.spark.read.json(filepath)
            print(f"✓ Loaded {df.count()} submissions")
            return df
        except Exception as e:
            print(f"✗ Error loading file: {e}")
            return None
    
    def add_grades(self, df):
        """
        Add grade scores to submissions
        This would integrate with your grading logic
        
        Args:
            df: DataFrame with submissions
        
        Returns:
            DataFrame with grades added
        """
        from local_grader import grade_answer
        
        print("⚙️  Computing grades in parallel...")
        
        # Create a UDF for grading (simplified)
        from pyspark.sql.types import DoubleType
        
        def compute_grade(reference, student_answer):
            try:
                result = grade_answer(reference, student_answer, max_score=10.0)
                return float(result['score'])
            except:
                return 0.0
        
        grade_udf = self.spark.udf.register("grade_udf", compute_grade, DoubleType())
        
        df_with_grades = df.withColumn(
            "score",
            grade_udf(col("reference_answer"), col("student_answer"))
        )
        
        print(f"✓ Grades computed for {df_with_grades.count()} submissions")
        return df_with_grades
    
    def compute_analytics(self, df_grades):
        """
        Compute 6D analytics on all submissions
        
        Args:
            df_grades: DataFrame with grades
        
        Returns:
            Analytics dictionary
        """
        print("📊 Computing analytics...")
        
        # Basic statistics
        stats = df_grades.select(
            avg("score").alias("mean_score"),
            stddev("score").alias("std_dev"),
            spark_min("score").alias("min_score"),
            spark_max("score").alias("max_score"),
            count("*").alias("total_submissions")
        ).collect()[0]
        
        analytics = {
            "total_submissions": stats.total_submissions,
            "mean_score": float(stats.mean_score or 0),
            "std_dev": float(stats.std_dev or 0),
            "min_score": float(stats.min_score or 0),
            "max_score": float(stats.max_score or 0),
            "timestamp": datetime.now().isoformat()
        }
        
        # Distribution
        distribution = df_grades.select(
            when(col("score") >= 9, "A").otherwise(
            when(col("score") >= 8, "B").otherwise(
            when(col("score") >= 7, "C").otherwise(
            when(col("score") >= 6, "D").otherwise("F")
            ))).alias("grade")
        ).groupBy("grade").count().collect()
        
        analytics["grade_distribution"] = {
            row["grade"]: row["count"] for row in distribution
        }
        
        print(f"✓ Analytics computed:")
        print(f"   Mean: {analytics['mean_score']:.2f}")
        print(f"   Std Dev: {analytics['std_dev']:.2f}")
        
        return analytics
    
    def per_student_performance(self, df_grades):
        """
        Compute per-student performance metrics
        
        Args:
            df_grades: DataFrame with grades
        
        Returns:
            DataFrame with student performance
        """
        print("👥 Computing per-student performance...")
        
        student_stats = df_grades.groupBy("student_email").agg(
            avg("score").alias("avg_score"),
            count("*").alias("submission_count"),
            spark_max("score").alias("best_score"),
            spark_min("score").alias("worst_score")
        ).orderBy(desc("avg_score"))
        
        student_stats.show(10)
        return student_stats
    
    def concept_coverage_analysis(self, df_grades):
        """
        Analyze concept coverage and mastery
        
        Args:
            df_grades: DataFrame with grades
        
        Returns:
            Coverage analysis
        """
        print("🎯 Analyzing concept coverage...")
        
        # This would be integrated with your semantic analysis
        coverage = {
            "total_students": df_grades.select("student_email").distinct().count(),
            "questions_asked": df_grades.select("question").distinct().count(),
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"✓ Coverage: {coverage['questions_asked']} questions across {coverage['total_students']} students")
        return coverage
    
    def identify_struggling_students(self, df_grades, percentile=25):
        """
        Identify students in bottom percentile
        
        Args:
            df_grades: DataFrame with grades
            percentile: Percentile threshold (default bottom 25%)
        
        Returns:
            DataFrame of struggling students
        """
        print(f"🚨 Identifying struggling students (bottom {percentile}%)...")
        
        threshold = df_grades.selectExpr(f"percentile_approx(score, {percentile/100})").collect()[0][0]
        
        struggling = df_grades.filter(col("score") <= threshold).select(
            "student_email",
            "question",
            "score",
            "student_answer"
        ).orderBy("score")
        
        count = struggling.count()
        print(f"✓ Found {count} student-question pairs needing attention")
        
        return struggling
    
    def save_results(self, analytics, output_path="analytics_batch.json"):
        """
        Save analytics results to file
        
        Args:
            analytics: Analytics dictionary
            output_path: Output file path
        """
        with open(output_path, 'w') as f:
            json.dump(analytics, f, indent=2)
        
        print(f"💾 Results saved to {output_path}")
    
    def stop(self):
        """Stop Spark session"""
        self.spark.stop()


def main():
    """Example usage"""
    grader = SparkBatchGrader()
    
    # For real usage, load actual submissions:
    # df = grader.load_submissions("submissions.json")
    
    # For testing, create sample data
    sample_data = [
        {
            "student_email": "student1@example.com",
            "question": "What is ML?",
            "reference_answer": "Machine learning is a subset of artificial intelligence",
            "student_answer": "ML is when computers learn from data"
        },
        {
            "student_email": "student2@example.com",
            "question": "What is ML?",
            "reference_answer": "Machine learning is a subset of artificial intelligence",
            "student_answer": "Machine learning enables systems to learn and improve without programming"
        }
    ]
    
    import json
    temp_file = "temp_submissions.json"
    with open(temp_file, 'w') as f:
        for item in sample_data:
            f.write(json.dumps(item) + "\n")
    
    # Load data
    df = grader.spark.read.json(temp_file)
    
    # Compute analytics
    analytics = grader.compute_analytics(df)
    coverage = grader.concept_coverage_analysis(df)
    
    # Combine results
    results = {
        "statistics": analytics,
        "coverage": coverage,
        "generated_at": datetime.now().isoformat()
    }
    
    grader.save_results(results)
    grader.stop()
    
    print("\n✓ Batch processing complete!")


if __name__ == "__main__":
    main()
