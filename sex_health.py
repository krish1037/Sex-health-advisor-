# this is the project on gradio based on the gen AI by python 
import google.generativeai as genai
import gradio as gr
import os

# Configure Gemini API - Use the native Google AI library instead of OpenAI wrapper
api_key = os.getenv("GEMINI_API_KEY", "")
genai.configure(api_key=api_key)

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-flash')

def sexual_health_advisor(age, bedtime, wake_time, exercise_frequency, stress_level, symptoms, duration, lifestyle_factors):
    try:
        # Validate inputs
        if not age or age < 18:
            return "Please provide a valid age (18 or above)."
        
        if not bedtime or not wake_time:
            return "Please provide both bedtime and wake-up time."
        
        # Create a comprehensive prompt based on user inputs
        symptoms_str = ", ".join(symptoms) if symptoms else "No specific symptoms selected"
        lifestyle_str = ", ".join(lifestyle_factors) if lifestyle_factors else "No specific lifestyle factors selected"
        
        prompt = f"""
You are a professional sexual health advisor AI. Provide evidence-based medical advice for sexual health concerns, particularly premature ejaculation and related issues.

IMPORTANT GUIDELINES:
1. Always recommend consulting a healthcare professional for persistent issues
2. Focus on lifestyle improvements, stress management, and healthy habits
3. Provide practical, actionable advice
4. Be professional, supportive, and non-judgmental
5. Avoid explicit content while being medically accurate
6. Include disclaimers about seeking professional medical help

USER PROFILE:
- Age: {age} years old
- Sleep Schedule: Goes to bed at {bedtime}, wakes up at {wake_time}
- Exercise Frequency: {exercise_frequency}
- Current Stress Level: {stress_level}/10
- Reported Symptoms/Concerns: {symptoms_str}
- Duration of Issues: {duration}
- Lifestyle Factors: {lifestyle_str}

Please analyze this user's sexual health profile and provide comprehensive, personalized advice covering:

1. **Analysis of Contributing Factors**
2. **Lifestyle Modifications**
3. **Stress Management Strategies**
4. **Sleep Optimization**
5. **Exercise & Physical Health**
6. **When to Seek Professional Help**

Keep advice practical and actionable. Format your response with clear headers and bullet points.
        """
        
        # Generate response using Gemini
        response = model.generate_content(prompt)
        ai_response = response.text
        
        # Add disclaimer to response
        disclaimer = "\n\n MEDICAL DISCLAIMER: This advice is for educational purposes only. Always consult with a qualified healthcare provider for persistent sexual health concerns. For serious medical issues, please seek professional medical attention immediately."
        
        return ai_response + disclaimer
    
    except Exception as e:
        # Fallback advice when API is unavailable
        return generate_offline_advice(age, exercise_frequency, stress_level, symptoms, lifestyle_factors)

def generate_offline_advice(age, exercise_frequency, stress_level, symptoms, lifestyle_factors):
    """Generate basic advice when API is unavailable"""
    advice = "## Sexual Health Recommendations\n\n"
    
    # Exercise advice
    if exercise_frequency in ["Rarely", "Never"]:
        advice += "**Exercise Recommendations:**\n"
        advice += "- Start with 30 minutes of moderate exercise 3-4 times per week\n"
        advice += "- Kegel exercises can help strengthen pelvic floor muscles\n"
        advice += "- Regular cardio improves blood circulation and stamina\n\n"
    
    # Stress management
    if stress_level >= 7:
        advice += "**Stress Management:**\n"
        advice += "- Practice deep breathing exercises daily\n"
        advice += "- Consider meditation or mindfulness techniques\n"
        advice += "- Ensure adequate sleep (7-9 hours)\n"
        advice += "- Limit caffeine and alcohol intake\n\n"
    
    # Sleep hygiene
    advice += "**Sleep Optimization:**\n"
    advice += "- Maintain consistent sleep schedule\n"
    advice += "- Avoid screens 1 hour before bedtime\n"
    advice += "- Create a cool, dark sleeping environment\n\n"
    
    # General lifestyle
    advice += "**General Lifestyle Tips:**\n"
    advice += "- Maintain a balanced diet rich in zinc, vitamin D, and omega-3\n"
    advice += "- Stay hydrated throughout the day\n"
    advice += "- Limit processed foods and sugar\n"
    advice += "- Consider talking to a healthcare provider about your concerns\n\n"
    
    advice += "**When to Seek Professional Help:**\n"
    advice += "- If symptoms persist for more than 3 months\n"
    advice += "- If the issue is causing significant distress\n"
    advice += "- For personalized treatment options\n"
    
    disclaimer = "\n\n MEDICAL DISCLAIMER: This advice is for educational purposes only. Always consult with a qualified healthcare provider for persistent sexual health concerns."
    
    return advice + disclaimer

# Create the Gradio interface with multiple inputs
with gr.Blocks(title="Sexual Health Advisor", theme="soft") as iface:
    gr.Markdown("#  Sexual Health Advisor")
    gr.Markdown("Get personalized advice for sexual health concerns. All information is confidential and processed securely.")
    
    with gr.Row():
        with gr.Column():
            age = gr.Number(label="Age", value=25, minimum=18, maximum=100)
            bedtime = gr.Textbox(label="Usual Bedtime", placeholder="e.g., 11:00 PM")
            wake_time = gr.Textbox(label="Wake Up Time", placeholder="e.g., 7:00 AM")
            exercise_frequency = gr.Dropdown(
                choices=["Daily", "4-6 times/week", "2-3 times/week", "Once a week", "Rarely", "Never"],
                label="Exercise Frequency",
                value="2-3 times/week"
            )
        
        with gr.Column():
            stress_level = gr.Slider(label="Stress Level (1-10)", minimum=1, maximum=10, value=5)
            symptoms = gr.CheckboxGroup(
                choices=[
                    "Premature ejaculation",
                    "Performance anxiety",
                    "Low libido",
                    "Erectile difficulties",
                    "Sleep issues",
                    "High stress levels"
                ],
                label="Select relevant symptoms/concerns"
            )
            duration = gr.Dropdown(
                choices=["Less than 1 month", "1-3 months", "3-6 months", "6-12 months", "More than 1 year"],
                label="How long have you experienced these issues?",
                value="1-3 months"
            )
    
    lifestyle_factors = gr.CheckboxGroup(
        choices=[
            "Excessive screen time before bed",
            "Irregular sleep schedule",
            "High alcohol consumption",
            "Smoking",
            "Poor diet",
            "Sedentary lifestyle",
            "High work stress",
            "Relationship stress"
        ],
        label="Lifestyle factors (select all that apply)"
    )
    
    submit_btn = gr.Button("Get Health Advice", variant="primary")
    
    output = gr.Textbox(
        label="Personalized Health Advice",
        lines=15,
        max_lines=25
    )
    
    submit_btn.click(
        fn=sexual_health_advisor,
        inputs=[age, bedtime, wake_time, exercise_frequency, stress_level, symptoms, duration, lifestyle_factors],
        outputs=output
    )
    
    gr.Markdown("""
    ### Privacy & Confidentiality
    - Your information is not stored or shared
    - All interactions are processed securely
    - For serious concerns, please consult a healthcare professional
    
    ### Emergency Resources
    - For mental health emergencies: Contact your local crisis hotline
    - For medical emergencies: Contact emergency services
    """)

# Launch the interface
if __name__ == "__main__":
    iface.launch(share=True, server_name="127.0.0.1", server_port=7862)
    
