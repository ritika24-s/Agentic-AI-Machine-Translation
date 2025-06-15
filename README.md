About the project
The Agentic AI Machine Translator can be understood as creating a virtual translation company where different AI specialists collaborate - a CEO agent orchestrates the process, translator agents handle specific language pairs, quality assurance agents review output, and localization specialists ensure cultural appropriateness.

This project is built using LangGraph because it enables intelligent workflows that can loop back, make decisions, and adapt—like a team of translation specialists collaborating on complex documents.

## Langchain Architecture

Graph: Your translation workflow map showing how tasks connect
Nodes: Individual specialists (language detector, translator, quality checker)
Edges: Decision paths between specialists (if quality is poor → retry with different translator)
State: Shared memory containing conversation context, translation history, and current work

```
Text Input → Language Detection → Translation → Quality Check → Output
                                      ↑            ↓
                                      └── Retry Loop ──┘
```

## Setup
Create a virtual environment and install the dependencies.
bash
python -m venv venv
.\venv\Scripts\Activate.ps1 (windows)
source venv/bin/activate (linux|macos)

Optional: Get free API keys
Anthropic: https://console.anthropic.com/
LibreTranslate: No key needed for public API

install dependencies
bash
pip install -r requirements.txt

Set up LibreTranslate locally with following target languages
bash
libretranslate --load-only en,es,fr,de

run the application
bash
python main.py

To only run the translation system, run the following command
bash
python AgentArchitecture/agent_workflow.py

