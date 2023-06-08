# steel-eye-task

## How to run
- Clone the repository.
- Open the repo in a terminal and create a virtual environment by following this [guide](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/).
- After virtualenv creation and activation, run <code>pip install - r requirements.txt</code> in the terminal.
- Create a supabase project and create tables.
- Once all packages are installed, create a dotenv file and put the following content in it:
```bash
SUPABASE_URL = "<YOUR_SUPABASE_URL>"
SUPABASE_KEY = "<YOUR_SUPABASE_KEY>"
```
- Run <code>uvicorn main:app --reload</code> in the terminal.
- Open [app](http://127.0.0.1:8000/docs) in browser to access the API.
