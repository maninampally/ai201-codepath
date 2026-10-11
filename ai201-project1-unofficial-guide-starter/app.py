import gradio as gr
from query import ask

def handle_query(question):
    if not question.strip():
        return "Please enter a question.", ""
    
    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources

with gr.Blocks(title="FAU Professor Unofficial Guide") as demo:
    gr.Markdown("# 🦉 FAU Professor Unofficial Guide")
    gr.Markdown("Ask questions about FAU CS/EE professors based on real student reviews.")
    
    with gr.Row():
        inp = gr.Textbox(
            label="Your Question",
            placeholder="e.g. Does Alhalabi respond to emails? Is CAP4770 hard?",
            lines=2
        )
    
    btn = gr.Button("Ask", variant="primary")
    
    with gr.Row():
        answer = gr.Textbox(label="Answer", lines=10)
        sources = gr.Textbox(label="Sources", lines=10)
    
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

if __name__ == "__main__":
    demo.launch()
