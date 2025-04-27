# Asha_chatbot
# HerKey Asha - AI Career Assistant for Women

## Project Overview
HerKey Asha is an AI-powered career assistant specifically designed to help women navigate their professional journeys with confidence and clarity. The chatbot provides personalized career guidance, mentorship recommendations, and job opportunities tailored to women's career development needs.

## Key Features
- **Personalized Career Guidance**: Get advice on career paths, skill development, and professional growth
- **Industry-Specific Recommendations**: Access information relevant to your field of interest
- **Mentorship Connections**: Discover mentorship programs and networking opportunities
- **Job Opportunity Alerts**: Learn about positions suitable for your skillset and career goals
- **Bias-Free Conversations**: Ensures positive and empowering interactions

## Technical Implementation
- Built with Streamlit for the frontend interface
- Uses LangChain and FAISS for efficient knowledge retrieval
- Powered by Mistral-7B-Instruct LLM for natural conversational ability
- Vector database for storing and retrieving career-related information
- Analytics tracking for continuous improvement

## Installation Instructions

### Prerequisites
- Python 3.8+ installed
- Hugging Face API token (for LLM access)

### Setup Steps
1. Clone the repository:
   ```
   git clone https://github.com/Tanisha2212/Asha_chatbot.git
   cd ASHA_Chatbot_hackathon
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your environment variables:
   ```
   export HF_TOKEN=your_huggingface_token
   ```
   On Windows:
   ```
   set HF_TOKEN=your_huggingface_token
   ```

5. Run the application:
   ```
   streamlit run main.py
   ```

6. The application should now be running at `http://localhost:8501`

## For Hackathon Judges

### Demo Access
To quickly experience the application without setup:
- Visit our hosted demo at: [https://ashachatbot-kpajhfrmal7ou9ymhrrtes.streamlit.app/]
- Use the test credentials provided in the hackathon submission email

### Evaluation Guide
To best evaluate our solution:

1. **Try these sample queries**:
   - "What career paths are good for women in tech with 5 years of experience?"
   - "Are there any mentorship programs for women in leadership roles?"
     

3. **Features to test**:
   - Check how the assistant responds to career-specific questions
   - Observe the encouraging tone and empowerment-focused responses
   - Test the feedback mechanism (thumbs up/down)
   - Notice the analytics panel tracking questions and feedback

4. **Technical aspects to evaluate**:
   - Response quality and relevance
   - Speed of knowledge retrieval
   - UI/UX design and accessibility
   - Bias detection functionality

### Project Impact
HerKey Asha addresses several critical challenges:
- Gender bias in career guidance and job searching
- Limited access to mentorship for women professionals
- Need for tailored career development resources
- Building confidence in professional settings

Our goal is to create an accessible tool that empowers women throughout their career journeys, from entry-level positions to leadership roles.

## Contact Information
For any questions or technical support during evaluation:
- Email: team@herkey-asha.com
- Project Lead: [Your Name] - [your contact information]

Thank you for considering our project!
