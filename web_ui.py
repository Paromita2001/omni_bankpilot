import gradio as gr
from app import run_pipeline
from services.stt import speech_to_text
from services.tts import text_to_speech

def handle_text(user_text, history):
    if history is None:
        history = []

    if not user_text.strip():
        return history, None

    response = run_pipeline(user_text)

    history.append({"role": "user", "content": user_text})
    history.append({"role": "assistant", "content": response})

    audio = text_to_speech(response)
    return history, audio


def handle_voice(audio, history):
    if history is None:
        history = []

    user_text = speech_to_text(audio)

    if not user_text:
        history.append({
            "role": "assistant",
            "content": "I couldn’t understand your voice clearly. Please type your question."
        })
        return history, None

    return handle_text(user_text, history)


with gr.Blocks(title="Omni BankPilot – AI Banking Assistant") as demo:
    gr.Markdown("## 🏦 Omni BankPilot – AI Banking Assistant")

    chatbot = gr.Chatbot(label="Chat")
    state = gr.State([])

    gr.Markdown("### 💬 Type your query (Recommended)")
    text_input = gr.Textbox(placeholder="Type here…")
    text_btn = gr.Button("Send")

    gr.Markdown("### 🎤 Or speak (Optional)")
    audio_input = gr.Audio()
    voice_btn = gr.Button("Process Voice")

    audio_out = gr.Audio(label="Bot speaks 🔊")

    text_btn.click(
        handle_text,
        inputs=[text_input, state],
        outputs=[chatbot, audio_out]
    )

    voice_btn.click(
        handle_voice,
        inputs=[audio_input, state],
        outputs=[chatbot, audio_out]
    )

demo.launch()
