# Multi-Agent Translation System
This architecture is designed to translate text from one language to another.

## Architecture Philosophy

**Why Multi-Agent?** 
Research shows 49.7% improvement in error detection and +10.6 BLEU score improvements 
through specialized agent collaboration.

## Agent Team Structure
The system is built a system with 5 specialized agents, as follows:

### 1. Intelligence Router Agent
- **Purpose**: Analyze text complexity, 
               makes strategic decisions about how to handle each translation request
               and route to appropriate specialists
- **Expertise**: Complexity detection, domain identification, cultural context
- **Input**: Raw text + language preferences
- **Output**: Processing strategy + routing decisions + context management

### 2. Context Manager Agent  
- **Purpose**: Maintain conversation coherence and translation memory
- **Expertise**: Context management, terminology consistency, conversation threading
- **Input**: Current text + conversation history
- **Output**: Enriched context + consistency requirements

### 3. Translation Specialist Agent
- **Purpose**: Core translation with domain expertise and service optimization
- **Expertise**: Multi-service coordination, domain specialization, quality confidence
- **Input**: Source text + context + routing strategy
- **Output**: Translation candidates with confidence scores

### 4. Quality Guardian Agent
- **Purpose**: Comprehensive quality assurance using professional frameworks
- **Expertise**: MQM evaluation, error detection, cultural validation
- **Input**: Translation candidates + quality requirements
- **Output**: Quality scores + improvement recommendations

### 5. Results Synthesizer Agent
- **Purpose**: Final result coordination and continuous improvement
- **Expertise**: Result optimization, user feedback integration, performance tracking
- **Input**: Quality-assessed translations + user requirements
- **Output**: Final translation + metadata + improvement suggestions



## Agent Communication Patterns
Shared State Pattern: All agents access the same TranslationState, enabling full context visibility
Sequential Handoffs: Router → Context Manager → Translation → QA → Orchestrator
Conditional Loops: QA can send work back to Translation for quality improvements

### How They Work Together: The Magic of Coordination
Example: Translating a German Medical Document

Intelligence Router analyzes: "Medical content, formal register, document translation, high accuracy required"
Context Orchestrator loads: Medical terminology database, German→English formal style preferences
Translation Specialist activates: Medical domain mode, precision pathway, terminology consistency checking
Quality Guardian applies: Medical translation QA framework, terminology verification, cultural localization
Results Synthesizer delivers: Translation + confidence score + medical term glossary + improvement suggestions

The Collaboration Advantage:

Each agent contributes specialized expertise
Collective intelligence exceeds individual capabilities
Built-in error detection and correction
Continuous learning and improvement
Professional-grade quality assurance

## Technology Stack

- **Coordination**: LangGraph for workflow orchestration
- **Translation Services**: LibreTranslate (free) + Google Translate + Hugging Face
- **Memory**: Redis for conversation context and caching
- **API**: Flask for web endpoints
- **Quality**: Custom MQM framework implementation