import PIL.Image
import gradio as gr
import base64
import time
import os
import google.generativeai as genai

# Set Google API key 
genai.configure(api_key = os.environ['GOOGLE_API_KEY'])

# Create the Model
txt_model = genai.GenerativeModel('gemini-pro')
vis_model = genai.GenerativeModel('gemini-pro-vision')

# Image to Base 64 Converter
def image_to_base64(image_path):
    with open(image_path, 'rb') as img:
        encoded_string = base64.b64encode(img.read())
    return encoded_string.decode('utf-8')

# Function that takes User Inputs and displays it on ChatUI
def query_message(history,txt,img):
    if not img:
        history += [(txt,None)]
        return history
    base64 = image_to_base64(img)
    data_url = f"data:image/jpeg;base64,{base64}"
    history += [(f"{txt} ![]({data_url})", None)]
    return history

# Function that takes User Inputs, generates Response and displays on Chat UI
def llm_response(history,text,img):
    if not img:
        response = txt_model.generate_content(text)
        history += [(None,response.text)]
        return history

    else:
        img = PIL.Image.open(img)
        response = vis_model.generate_content([text,img])
        history += [(None,response.text)]
        return history

# Interface Code
with gr.Blocks() as app:
    # heading = gr.title("Pet Diet Plan Generator", level=1)  # Add a heading
    # heading = gr.Markdown("# Pet Diet Plan Generator")

# Subheading
    # subheading = gr.Markdown("### Answer the following questions to generate a personalized diet plan.")
    gr.HTML(
        """
        <div style="text-align: center; max-width: 1600px; margin: 20px auto;">
        <h2 style="font-weight: 900; font-size: 4rem; margin: 0rem">
           GEMINI PRO CHATBOT
        </h2>
    
        <h2 style="text-align: center; justify-content: center; display:flex; align-items: center; font-weight: 850; font-size: 1.1rem; margin-top: 0.5rem; margin-bottom: 0.5rem">
       
Gemini Pro isn't just a language model; it's a creative powerhouse, a code-wielding wizard , and a tireless knowledge explorer, all rolled into one. It fuels your artistic expression, supercharges your productivity, and bridges the code gap. Dive into scientific mysteries with its help, or imagine AI-powered healthcare. This ever-evolving entity, with its cutting-edge edge, redefines our relationship with technology .
        </h2><br><br>
       <div>
            <h1 > Welcome to the Gemini Pro revolution! 📈</h1>
           
            <h5 style="margin: 0;">If you like our project, please give us a star  on Github to stay updated with the latest developments.</h5><br>
            <div style="display: flex; justify-content: center; align-items: center; text-align: center;>
                <a href="https://github.com/HumanAIGC/OutfitAnyone"><img src="https://img.shields.io/badge/jaskirat-singh-red"></a>
                <a href='https://github.com/Jaskirat-singh04/'><img src='https://img.shields.io/badge/Project-gemini%20pro-green' alt='Project Page'></a>
                <a href='https://www.linkedin.com/in/jaskiratsingh04'><img src='https://img.shields.io/badge/Linked%20In-jaskirat%20-blue'></a>
            </div><br>
        </div>
        <br><br>
       <img src="https://images.tech.co/wp-content/uploads/2023/12/06145436/Google-Gemini-AI-708x400.jpg" alt="textdiffuser-2" style="width: 100%; height: 70%; object-fit: cover;">

        </div><br><br>

        <h2 style="font-weight: 900; display: flex; text-align: left; justify-content: center; font-size: 3rem; align-items:center; margin: 0rem">
          CAPABILITIES
        </h2><br>
        <div style= "display:flex;">
       
        <h2 style="text-align: left; justify-content: center; display:flex; font-weight: 850; font-size: 0.9rem; margin-top: 0.5rem; margin-bottom: 0.5rem; margin-right: 0.3rem; @media (max-width: 600px) {
    font-size: 0.8rem;
  }" >
  <b></b> ✅Writes in any style, from poems to scripts, sparking your imagination and breaking writer's block.Analyzes data, uncovers patterns, and proposes hypotheses.<br>
 </h2>
 <h2 style="text-align: left; justify-content: center; display:flex;  font-weight: 850; font-size: 0.9rem; margin-top: 0.5rem; margin-bottom: 0.5rem; margin-right: 0.3rem">
 <b></b> ✅Translates languages, summarizes documents, and answers questions, freeing you to focus on the big picture.Seamlessly handles text, code, and even images.<br>
 </h2>
 <h2 style="text-align: left; justify-content: center; display:flex;  font-weight: 850; font-size: 0.9rem; margin-top: 0.5rem; margin-bottom: 0.5rem; margin-right: 0.3rem">
 <b></b>✅ Generates and translates code in different languages, speeding up development and democratizing coding.<br>
 </h2>
 
        </div> <br><br>
   
        """)
    
    # subheading = gr.Heading("Answer the following questions to generate a personalized diet plan.", level=3)  # Add a subheading
    with gr.Row():
        image_box = gr.Image(type="filepath")
    
        chatbot = gr.Chatbot(
            scale = 2,
            height=750
        )
    text_box = gr.Textbox(
            placeholder="Enter text and press enter, or upload an image to start",
            container=False,
        )

    btn = gr.Button("Submit")
    clicked = btn.click(query_message,
                        [chatbot,text_box,image_box],
                        chatbot
                        ).then(llm_response,
                                [chatbot,text_box,image_box],
                                chatbot
                                )
    gr.Markdown("## Prompt Examples")
    gr.Examples(
            [
                ["Describe the painting in a poetic way.",'eg1.png'],
                [" Craft a persuasive advertisement for this electric car that highlights its innovative features and eco-friendly benefits, using language that appeals to a tech-savvy audience..",'eg2.png'],
                ["Count no. of people in this image.",'eg3.jpg'],
                ["Tell me some fact about this dog breed.",'eg4.webp'],
            ],
            [
              text_box,
              image_box  
            ],
            examples_per_page=25
        )

    gr.HTML(
        """
        <div style="text-align: justify; max-width: 1100px; margin: 20px auto;">
        <h3 style="font-weight: 450; font-size: 0.8rem; margin: 0rem">
        <b>Disclaimer</b>: 
        Please note that the demo is intended for academic and research purposes <b>ONLY</b>. Any use of the demo for generating inappropriate content is strictly prohibited. The responsibility for any misuse or inappropriate use of the demo lies solely with the users who generated such content, and this demo shall not be held liable for any such use.
        </h3>
        <h3 style="font-weight: 450; font-size: 0.8rem; margin: 0rem">
        <b>All the images and video belongs to their respective owners/organisations. I dont claim any copywrite on any image and video.Big shoutout to hugging face community.</b>
        </h3>
        </div>
          <div style="justify-content: center; display:flex; align-items: center;">
      <iframe width="400px" height="300px" src="https://www.youtube.com/embed/UIZAiXYceBI?si=JaY1OzdXShC5OR_M?autoplay=1" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
        </div>
        """
    )
app.queue()
app.launch(auth=('user','admin'),auth_message="Enter your username and password.If you don't have it please dm me on linkedin @ https://www.linkedin.com/in/jaskiratsingh04 or Email me @singh.kirat.0409@gmail.com Thanks!",debug=True,share=True)