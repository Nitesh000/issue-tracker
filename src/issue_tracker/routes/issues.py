import uuid

from fastapi import APIRouter, HTTPException, status

from issue_tracker.schema import (
    IssueCreate,
    IssueOut,
    IssueStatus,
    IssueUpdate,
)
from issue_tracker.storage import load_data, save_data

router = APIRouter(prefix="/api/v1/issues", tags=["issues"])


@router.get("/", response_model=list[IssueOut])
async def get_issues():
    """retrive all issues"""
    issues = load_data()
    return issues


@router.post("/", response_model=IssueOut, status_code=status.HTTP_201_CREATED)
async def create_issue(issue: IssueCreate):
    """create issue"""
    issues = load_data()
    new_issue = IssueOut(
        id=str(uuid.uuid4()),
        title=issue.title,
        description=issue.description,
        priority=issue.priority,
        status=IssueStatus.open,
    )
    issues.append(new_issue)
    save_data(issues)
    return new_issue


@router.patch("/{id}", response_model=IssueOut, status_code=status.HTTP_202_ACCEPTED)
async def update_issue(id: str, data: IssueUpdate):
    """update any issue"""
    issues = load_data()
    """check if the issue is there"""
    for issue in issues:
        if issue.id == id:
            updated = issue.model_copy(update=data.model_dump(exclude_unset=True))
            issues[issues.index(issue)] = updated
            save_data(issues)
            return updated
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")
