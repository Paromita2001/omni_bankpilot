from app_graph.graph_builder import build_graph

graph = build_graph()

def run_pipeline(user_input):
    result = graph.invoke({
        "input": user_input
    })
    return result["response"]
