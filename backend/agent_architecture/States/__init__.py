"""
This folder contains the states for the translation system.

What is a state?
State: Represents the context or memory that is maintained and updated as the computation progresses.
It ensures that each step in the graph can access relevant information from previous steps, 
allowing for dynamic decision-making based on accumulated data throughout the process.
Reference: https://medium.com/@lorevanoudenhove/how-to-build-ai-agents-with-langgraph-a-step-by-step-guide-5d84d9c7e832

How many states can a langgraph graph have?
It supports multiple states that can be passed between nodes throughout the graph.
Stateful Graphs: LangGraph allows you to create stateful graphs, which can, in fact, maintain multiple states
                 or variables that can be shared and updated between different nodes in your graph. 
                 This flexibility is beneficial for complex workflows where distinct pieces of information
                 need to be tracked simultaneously.
State Definition: States in LangGraph can be implemented using several data structures such as TypedDict, 
                  Pydantic, or dataclasses, allowing you to define various fields and properties. 
                  The functional design allows for adding new fields or modifying existing ones as needed,
                  enabling multiple pieces of state information to coexist.
Using Multiple States: You can utilize multiple states effectively by defining separate channels within a 
                  single overarching state object. Additionally, LangGraph facilitates the merging of
                  states and allows for reducer functions to control how these states interact as they are updated.








"""