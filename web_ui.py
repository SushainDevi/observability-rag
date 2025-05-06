import gradio as gr
from rag_core import ObservabilityAssistant
import time

assistant = ObservabilityAssistant()

# Custom CSS for dark theme
dark_theme = """
:root {
    --background-fill-primary: #1a1a1a;
    --background-fill-secondary: #2d2d2d;
    --body-text-color: #ffffff;
    --input-border-color: #4d4d4d;
}
.gr-prose { color: white !important; }
footer { display: none !important; }
"""

def process_query_web(query, history):
    start_time = time.time()
    
    # Process query
    response = assistant.process_query(query)
    
    # Calculate latency
    latency = f"⏱️ Response time: {time.time() - start_time:.2f}s"
    
    # Format as markdown
    return f"""
{response}

{latency}
"""

# Example queries for quick input
examples = [
    "Show servers with >65% CPU in last hour",
    "List hosts with disk usage >90% today",
    "Find memory spikes above 80% in past 6 hours"
]

with gr.Blocks(theme=gr.themes.Soft(), css=dark_theme) as demo:
    gr.Markdown("# 🔭 Observability Assistant")
    gr.Markdown("Ask about server metrics (CPU/Memory/Disk)")
    
    with gr.Row():
        with gr.Column(scale=3):
            input_box = gr.Textbox(
                label="Query",
                placeholder="Enter your observability query...",
                lines=2
            )
            submit_btn = gr.Button("Analyze", variant="primary")
            
        with gr.Column(scale=1):
            gr.Examples(
                examples=examples,
                inputs=input_box,
                label="Quick Examples"
            )
    
    output = gr.Markdown(label="Results")
    
    submit_btn.click(
        fn=process_query_web,
        inputs=input_box,
        outputs=output
    )
    
    input_box.submit(
        fn=process_query_web,
        inputs=input_box,
        outputs=output
    )

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        favicon_path="🖥️",
        share=False
    )