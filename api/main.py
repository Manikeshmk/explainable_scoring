"""
FastAPI Backend for ExplainGrade AI
Modern async REST API for grading and analytics
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
import json
import os
import sys
from functools import lru_cache

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from local_grader import grade_answer

# Initialize FastAPI app
app = FastAPI(
    title="ExplainGrade API",
    description="AI-Powered Student Assessment Platform",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================= Models =======================

class SubmissionCreate(BaseModel):
    """Model for creating a new submission"""
    student_email: EmailStr
    question: str = Field(..., min_length=5, max_length=1000)
    reference_answer: str = Field(..., min_length=5, max_length=2000)
    student_answer: str = Field(..., min_length=1, max_length=2000)


class GradeResponse(BaseModel):
    """Model for grade response"""
    submission_id: str
    score: float
    explanation: str
    strengths: List[str]
    improvements: List[str]
    timestamp: str


class SubmissionResponse(BaseModel):
    """Model for submission response"""
    submission_id: str
    student_email: str
    question: str
    student_answer: str
    status: str
    created_at: str


class AnalyticsResponse(BaseModel):
    """Model for analytics response"""
    total_submissions: int
    average_score: float
    std_dev: float
    passing_rate: float


# ======================= Storage =======================

class InMemoryStore:
    """Simple in-memory storage for demo purposes"""
    def __init__(self):
        self.submissions = {}
        self.grades = {}
    
    def save_submission(self, submission_id, data):
        self.submissions[submission_id] = data
    
    def get_submission(self, submission_id):
        return self.submissions.get(submission_id)
    
    def save_grade(self, submission_id, grade_data):
        self.grades[submission_id] = grade_data
    
    def get_grade(self, submission_id):
        return self.grades.get(submission_id)
    
    def get_all_grades(self):
        return list(self.grades.values())


store = InMemoryStore()


# ======================= Dependency Injection =======================

def get_store() -> InMemoryStore:
    return store


# ======================= Background Tasks =======================

def grade_submission_background(submission_id: str, reference_answer: str, student_answer: str):
    """Grade submission in the background"""
    try:
        result = grade_answer(reference_answer, student_answer, max_score=10.0)
        result['submission_id'] = submission_id
        result['timestamp'] = datetime.now().isoformat()
        store.save_grade(submission_id, result)
        print(f"✓ Graded submission {submission_id}: {result['score']:.1f}/10")
    except Exception as e:
        print(f"✗ Error grading {submission_id}: {e}")


# ======================= Routes =======================

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for Kubernetes"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "ExplainGrade API"
    }


@app.get("/ready", tags=["Health"])
async def readiness():
    """Readiness check endpoint"""
    return {
        "ready": True,
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/v1/submissions", response_model=SubmissionResponse, tags=["Submissions"])
async def create_submission(
    submission: SubmissionCreate,
    background_tasks: BackgroundTasks,
    store_inst: InMemoryStore = Depends(get_store)
):
    """
    Create a new submission for grading
    
    - **student_email**: Student's email address
    - **question**: The question being asked
    - **reference_answer**: The correct/ideal answer
    - **student_answer**: The student's provided answer
    """
    import uuid
    
    submission_id = str(uuid.uuid4())
    
    submission_data = {
        "submission_id": submission_id,
        "student_email": submission.student_email,
        "question": submission.question,
        "reference_answer": submission.reference_answer,
        "student_answer": submission.student_answer,
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }
    
    # Save submission
    store_inst.save_submission(submission_id, submission_data)
    
    # Grade in background
    background_tasks.add_task(
        grade_submission_background,
        submission_id,
        submission.reference_answer,
        submission.student_answer
    )
    
    return SubmissionResponse(**submission_data)


@app.get("/api/v1/submissions/{submission_id}", response_model=SubmissionResponse, tags=["Submissions"])
async def get_submission(
    submission_id: str,
    store_inst: InMemoryStore = Depends(get_store)
):
    """
    Retrieve a specific submission
    """
    submission = store_inst.get_submission(submission_id)
    
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    return SubmissionResponse(**submission)


@app.get("/api/v1/grades/{submission_id}", response_model=GradeResponse, tags=["Grades"])
async def get_grade(
    submission_id: str,
    store_inst: InMemoryStore = Depends(get_store)
):
    """
    Retrieve grade for a submission
    """
    grade = store_inst.get_grade(submission_id)
    
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not ready or not found")
    
    return GradeResponse(
        submission_id=grade.get('submission_id'),
        score=float(grade.get('score', 0)),
        explanation=grade.get('explanation', ''),
        strengths=grade.get('strengths', []),
        improvements=grade.get('improvements', []),
        timestamp=grade.get('timestamp', '')
    )


@app.get("/api/v1/analytics", response_model=AnalyticsResponse, tags=["Analytics"])
async def get_analytics(store_inst: InMemoryStore = Depends(get_store)):
    """
    Get overall analytics
    """
    grades = store_inst.get_all_grades()
    
    if not grades:
        return AnalyticsResponse(
            total_submissions=0,
            average_score=0.0,
            std_dev=0.0,
            passing_rate=0.0
        )
    
    scores = [g.get('score', 0) for g in grades]
    avg_score = sum(scores) / len(scores) if scores else 0
    
    # Calculate std dev
    variance = sum((x - avg_score) ** 2 for x in scores) / len(scores) if scores else 0
    std_dev = variance ** 0.5
    
    passing = sum(1 for s in scores if s >= 6) / len(scores) if scores else 0
    
    return AnalyticsResponse(
        total_submissions=len(grades),
        average_score=round(avg_score, 2),
        std_dev=round(std_dev, 2),
        passing_rate=round(passing * 100, 1)
    )


@app.post("/api/v1/batch-grade", tags=["Batch Operations"])
async def batch_grade(
    submissions: List[SubmissionCreate],
    background_tasks: BackgroundTasks,
    store_inst: InMemoryStore = Depends(get_store)
):
    """
    Grade multiple submissions at once
    """
    import uuid
    
    results = []
    
    for submission in submissions:
        submission_id = str(uuid.uuid4())
        
        submission_data = {
            "submission_id": submission_id,
            "student_email": submission.student_email,
            "question": submission.question,
            "student_answer": submission.student_answer,
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        
        store_inst.save_submission(submission_id, submission_data)
        
        # Grade in background
        background_tasks.add_task(
            grade_submission_background,
            submission_id,
            submission.reference_answer,
            submission.student_answer
        )
        
        results.append({
            "submission_id": submission_id,
            "status": "queued"
        })
    
    return {
        "total": len(results),
        "queued": len(results),
        "submissions": results
    }


@app.get("/docs", tags=["Documentation"])
async def openapi_schema():
    """Interactive API documentation (Swagger UI)"""
    return app.openapi()


# ======================= Startup =======================

@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    print("🚀 ExplainGrade API starting up...")
    print("📚 API Docs available at /docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("⏹️  ExplainGrade API shutting down...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
