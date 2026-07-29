#Pydantic schemas for the chains.


from typing import List
from pydantic import BaseModel, Field


class BusinessAnalysis(BaseModel):
    startup_name: str = Field(description="Name of the startup")
    summary: str = Field(description="One paragraph summary of what the startup does")
    industry: str = Field(description="Industry or sector")
    target_customers: str = Field(description="Who the startup serves")
    problem: str = Field(description="The problem being solved")
    solution: str = Field(description="How the startup solves the problem")
    unique_value_proposition: str = Field(description="What makes this startup different")
    business_model: str = Field(description="How the startup operates")
    revenue_model: str = Field(description="How the startup makes money")


class SWOTAnalysis(BaseModel):
    strengths: List[str] = Field(description="Internal strengths of the startup")
    weaknesses: List[str] = Field(description="Internal weaknesses of the startup")
    opportunities: List[str] = Field(description="External opportunities the startup could exploit")
    threats: List[str] = Field(description="External threats the startup faces")


class InvestmentReadiness(BaseModel):
    investment_score: int = Field(description="Overall investment readiness score, 0-100", ge=0, le=100)
    scalability: str = Field(description="Assessment of how scalable the business is")
    innovation: str = Field(description="Assessment of how innovative the product/approach is")
    team_assessment: str = Field(description="Assessment of the team based on available info")
    product_assessment: str = Field(description="Assessment of the product's maturity and fit")
    key_risks: List[str] = Field(description="The most important risks an investor should know about")
    explanation: str = Field(description="Short justification for the investment_score")
