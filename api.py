from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from utils import generate_report

app = FastAPI(
    title="Company Sentiment Analysis API",
    description="API for analyzing news sentiment about companies",
    version="1.0.0"
)

class CompanyRequest(BaseModel):
    company_name: str
    days: Optional[int] = 1

@app.post("/analyze", response_model=dict)
async def analyze_company(request: CompanyRequest):
    """
    Generate a sentiment analysis report for a company.
    """
    try:
        # Generate the report from our utils
        report = generate_report(request.company_name, request.days)
        return report
    except Exception as e:
        # If anything goes wrong, return a 400 status with the error message
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify if the server is running.
    """
    return {"status": "healthy"}
