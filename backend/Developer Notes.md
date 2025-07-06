# Developer Notes

## Create Project Foundation

#### Create a new project folder
```bash
mkdir Agentic Machine Translator
cd Agentic Machine Translator
```

#### Create a new virtual environment
Why virtual environments matter: Keeps your project dependencies isolated.

```bash
python -m venv venv
# Activate it (choose your OS)

# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

#### Install the necessary packages
```bash
pip install -r requirements.txt
```

#### Create folders for the project
```bash
mkdir -p {agent_architecture,api,config,data,monitoring,terminology,translation_services}
```
Create a "Folder Structure.md" file to keep track of the folder structure.

#### Initialize a git repository
```bash
git init
```
Create .gitignore file.
Create a README.md file.

#### Set up environment variables (.env):
```bash
touch .env
```
Add your environment variables to the .env file.
For reference, see the .env.example file.
Add it to the .gitignore file.

## Create the Agentic Architecture
