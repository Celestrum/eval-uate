"""
The main backend for eval-uate
"""
# command to run the server
# uvicorn main:app --reload

from decouple import config  # type: ignore
from fastapi import FastAPI, status, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from supabase import create_client, Client
from pydantic import BaseModel

DEBUG = config("DEBUG", default=False, cast=bool)


DB_URL: str = config("SUPABASE_URL")  # type: ignore
DB_KEY: str = config("SUPABASE_KEY")  # type: ignore


app = FastAPI()
supabase: Client = create_client(DB_URL, DB_KEY)

app.mount("/assets", StaticFiles(directory="templates/assets"), name="assets")
templates = Jinja2Templates(directory="templates")


"""
example row of problem table
{
    "id": 1,
    "title": "FizzBuzz",
    "created_at": "2021-10-10T20:00:00Z",
    "updated_at": "2021-10-10T20:00:00Z"
    "problem_data": {
        "description": "Write a program that prints the numbers from 1 to 100.
        But for multiples of three print “Fizz” instead of the number and for the multiples of five print “Buzz”.
        For numbers which are multiples of both three and five print “FizzBuzz”.",
        "input": "The input will be a single integer N",
        "output": "Print N lines, each containing the number or the word as described above",
        "starter_code": "function fizzBuzz(n) {\n    // your code here\n}"
    }
}

{
    "id": 2,
    "title": "Sum of Two Numbers",
    "created_at": "2021-10-10T20:00:00Z",
    "updated_at": "2021-10-10T20:00:00Z"
    "problem_data": {
        "description": "Write a program that takes two numbers as input and prints their sum",
        "input": "The input will be two integers A and B",
        "output": "Print a single integer, the sum of A and B",
        "starter_code": "function sum(a, b) {\n    // your code here\n}"
    }
}
"""


@app.get("/")
async def serve_spa(request: Request):
    """Serves the Vue frontend from the same server as the api to avoid CORS"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/healthcheck")
def healthcheck():
    """Ping test to see if the server is running"""
    return {"msg": "Server running for eval-uate"}


@app.get("/problems")
def get_problems():
    """Get all problems"""
    problems = supabase.table("problems").select("*").execute()
    return problems


@app.get("/problems/{problem_id}")
def get_problem(problem_id: str):
    """Get a specific problem"""
    problem = supabase.table("problems").select("*").eq("id", problem_id).execute()
    return problem


class ProblemDataSchema(BaseModel):
    """The JSON schema for the problem_data field in the problems table"""

    description: str
    input: str
    output: str
    starter_code: str


class ProblemSchema(BaseModel):
    """A row in the problems table"""

    title: str
    problem_data: ProblemDataSchema


@app.post("/problems", status_code=status.HTTP_201_CREATED)
def create_problem(problem_data: ProblemSchema):
    """Create a new problem"""
    problem = supabase.table("problems").insert(problem_data.model_dump()).execute()
    return problem
