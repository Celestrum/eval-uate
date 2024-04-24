# Eval-uate

Eval-uate is a web app that allows users to solve problems set by professors. The application is inspired by PCRS, Exercism, Leetcode, and HackerRank.


### How to run

Set up a supabase project and get the database url and the key that's meant to be private.
Put that into the env file in the backend.
From there run npm install in the frontend and then npm run build.
In the backend make a venv and install the requirements from the requirements.txt file.
Then run the backend with uvicorn main:app --reload

### Task List
- [x] Create a basic structure for the project
- [x] Setup a backend using fastapi
- [x] Setup the database using supabase with a problems table
- [x] Setup a frontend
- [ ] Setup a s3 bucket in supabase to download user submissions to the server
- [ ] Add a problems page letting you see defined problems
- [ ] Add a code editor using CodeMirror or Monaco
- [ ] Add a specific problem page letting you see the problem and submit a solution
- [ ] Add a way to run the code on the server
- [ ] Return the output of the code to the user