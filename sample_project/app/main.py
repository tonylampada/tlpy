"""
FastAPI Sample Application
Demonstrates a simple TODO API with in-memory storage
"""

from datetime import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="TODO API", description="A simple TODO list API built with FastAPI", version="1.0.0"
)


class TodoItem(BaseModel):
    """Model for a TODO item"""

    id: int | None = Field(None, description="Unique identifier")
    title: str = Field(..., min_length=1, max_length=100, description="TODO title")
    description: str | None = Field(None, max_length=500, description="TODO description")
    completed: bool = Field(False, description="Completion status")
    created_at: datetime | None = Field(None, description="Creation timestamp")
    updated_at: datetime | None = Field(None, description="Last update timestamp")


class TodoCreate(BaseModel):
    """Model for creating a TODO item"""

    title: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)


class TodoUpdate(BaseModel):
    """Model for updating a TODO item"""

    title: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)
    completed: bool | None = None


# In-memory storage
todos_db: dict[int, TodoItem] = {}
next_id = 1


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to TODO API", "docs": "/docs", "health": "/health"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/todos", response_model=list[TodoItem])
async def get_todos(completed: bool | None = None):
    """Get all TODO items, optionally filtered by completion status"""
    todos = list(todos_db.values())

    if completed is not None:
        todos = [t for t in todos if t.completed == completed]

    return todos


@app.get("/todos/{todo_id}", response_model=TodoItem)
async def get_todo(todo_id: int):
    """Get a specific TODO item by ID"""
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail=f"TODO with id {todo_id} not found")

    return todos_db[todo_id]


@app.post("/todos", response_model=TodoItem, status_code=201)
async def create_todo(todo: TodoCreate):
    """Create a new TODO item"""
    global next_id

    now = datetime.now()
    new_todo = TodoItem(
        id=next_id,
        title=todo.title,
        description=todo.description,
        completed=False,
        created_at=now,
        updated_at=now,
    )

    todos_db[next_id] = new_todo
    next_id += 1

    return new_todo


@app.put("/todos/{todo_id}", response_model=TodoItem)
async def update_todo(todo_id: int, todo_update: TodoUpdate):
    """Update a TODO item"""
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail=f"TODO with id {todo_id} not found")

    existing_todo = todos_db[todo_id]
    update_data = todo_update.dict(exclude_unset=True)

    if update_data:
        for field, value in update_data.items():
            setattr(existing_todo, field, value)
        existing_todo.updated_at = datetime.now()

    return existing_todo


@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    """Delete a TODO item"""
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail=f"TODO with id {todo_id} not found")

    del todos_db[todo_id]
    return {"message": f"TODO {todo_id} deleted successfully"}


@app.get("/stats")
async def get_stats():
    """Get statistics about TODO items"""
    todos = list(todos_db.values())
    completed = [t for t in todos if t.completed]

    return {
        "total": len(todos),
        "completed": len(completed),
        "pending": len(todos) - len(completed),
        "completion_rate": f"{(len(completed) / len(todos) * 100):.1f}%" if todos else "0%",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
