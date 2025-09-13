from typing import Optional, List
from pydantic import BaseModel, Field


# Define the state for the lead calling subgraph
class Lead(BaseModel):
    id: str  # The lead being processed
    first_name: str
    last_name: str
    address: str
    email: str
    phone: str

class CallAnalysisResponse(BaseModel):
    """Response model for the Sales Call Analysis Specialist."""
    
    summary: str = Field(
        ..., description="A concise summary highlighting the key talking points and interactions during the call."
    )
    interested: str = Field(
        ..., description="Determination of the lead's interest level: 'Interested', 'Not Interested', or 'Undecided'."
    )
    justification: Optional[str] = Field(
        default=None, description="Justification for the interest evaluation, providing context from the call transcript."
    )

class RunPayload(BaseModel):
    lead_ids: List[str]
