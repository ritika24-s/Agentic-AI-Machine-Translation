from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from IPython.display import Image, display
from States.translation_state import TranslationState
from States.conversation_state import ConversationState


class ChatbotGraphBuilder:
    """
    This class is used to build the chatbot graph.
    """
    def __init__(self, memory: bool=False):
        self.translation_state = TranslationState()
        self.graph_builder = StateGraph(TranslationState, ConversationState)
        if memory:
            self.memory = MemorySaver()
        else:
            self.memory = None
        self.graph = None
    
    def add_node(self, node_name:str, node)-> None:
        self.graph_builder.add_node(node_name, node)
    
    def add_edge(self, node_from:str, node_to:str):
        self.graph_builder.add_edge(node_from, node_to)
    
    def add_start_edge(self, node_name:str)-> None:
        self.graph_builder.add_edge(START, node_name)
    
    def add_end_edge(self, node_name:str)-> None:
        self.graph_builder.add_edge(node_name, END)

    def add_condition(self, node_name:str, tool_condition)-> None:
        self.graph_builder.add_conditional_edges(node_name, tool_condition)

    def compile_graph(self):
        self.graph = self.graph_builder.compile(checkpointer=self.memory)
        return self.graph

    def visualize_graph(self):
        try:
            return display(Image(self.graph.get_graph().draw_mermaid_png()))
        except Exception as e:
            print(f"Error visualizing graph: {e}")
            return None
        
    def run_graph(self, data: dict, config: dict=None):
        return self.graph.invoke(data, config=config)

    def get_result(self, result: dict=None, data: dict=None, config: dict=None)-> None:
        if not result and not data:
            raise ValueError("No result or data provided")
        if not result and data:
            result = self.run_graph(data, config=config)
        
        for m in result['messages']:
            m.pretty_print()
        
        return result
        