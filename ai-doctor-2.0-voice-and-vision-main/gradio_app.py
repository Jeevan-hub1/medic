# if you dont use pipenv uncomment the following:
from dotenv import load_dotenv
load_dotenv()

#VoiceBot UI with Gradio
import os
import gradio as gr

from brain_of_the_doctor import encode_image, analyze_image_with_query, analyze_text_with_query
from voice_of_the_patient import record_audio, transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_gtts, text_to_speech_with_elevenlabs

load_dotenv()

system_prompt="""You have to act as a professional doctor, i know you are not but this is for learning purpose. 
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Donot say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please.
            Your primary language is English, but you MUST respond in the same language the user uses."""


def process_inputs(audio_filepath, image_filepath):
    speech_to_text_output = transcribe_with_groq(GROQ_API_KEY=os.environ.get("GROQ_API_KEY"), 
                                                 audio_filepath=audio_filepath,
                                                 stt_model="whisper-large-v3")

    # Handle the image input
    if image_filepath:
        doctor_response = analyze_image_with_query(query=system_prompt+speech_to_text_output, encoded_image=encode_image(image_filepath), model="llama-3.2-11b-vision-preview")
    else:
        doctor_response = "No image provided for me to analyze"

    voice_of_doctor = text_to_speech_with_elevenlabs(input_text=doctor_response, output_filepath="final.mp3") 

    return speech_to_text_output, doctor_response, voice_of_doctor


medicine_system_prompt = """You are a professional pharmacist. The user is asking about a medicine. 
They have provided the name of the medicine and optionally an image of it.
Please explain what this medicine is used for, its benefits, potential side effects, and general usage instructions.
Keep your response clear, concise, and easy to understand for a patient.
Do not provide a medical diagnosis, but rather pharmaceutical information.
Your primary language is English, but you MUST respond in the same language the user uses.
"""

def process_medicine(medicine_name, image_filepath):
    if not medicine_name and not image_filepath:
        return "Please provide a medicine name or an image."
    
    query = medicine_system_prompt
    if medicine_name:
        query += f"\n\nMedicine Name provided by user: {medicine_name}"
        
    if image_filepath:
        response = analyze_image_with_query(query=query, encoded_image=encode_image(image_filepath), model="llama-3.2-11b-vision-preview")
    else:
        response = analyze_text_with_query(query=query)
        
    return response

# Create the interfaces
ai_doctor_iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath"),
        gr.Image(type="filepath")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio("Temp.mp3")
    ],
    title="AI Doctor with Vision and Voice"
)

medicine_iface = gr.Interface(
    fn=process_medicine,
    inputs=[
        gr.Textbox(label="Medicine Name", placeholder="e.g. Paracetamol, Amoxicillin..."),
        gr.Image(type="filepath", label="Medicine Image (Optional)")
    ],
    outputs=[
        gr.Textbox(label="Medicine Information", lines=10)
    ],
    title="Medicine Analyzer"
)

app = gr.TabbedInterface([ai_doctor_iface, medicine_iface], ["AI Doctor", "Medicine Analyzer"])

app.launch(debug=True)

#http://127.0.0.1:7860