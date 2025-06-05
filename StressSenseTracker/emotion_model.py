from transformers import pipeline

# Load Hugging Face pre-trained emotion classifier
model_name = "bhadresh-savani/distilbert-base-uncased-emotion"
classifier = pipeline("text-classification", model=model_name, top_k=None)

# Activity recommendations based on emotions
activity_recommendations = {
    'admiration': [
        'Send a message to the person you admire expressing your appreciation',
        'Journal about the qualities you admire and how you can cultivate them',
        'Share an inspiring story or quote on social media',
        'Watch a documentary or talk by someone you admire',
        'Create a vision board with inspiring role models'
    ],
    'amusement': [
        'Watch a funny video or comedy special',
        'Share a joke or meme with a friend',
        'Recall and retell a funny memory',
        'Play a lighthearted game or activity',
        'Enjoy a comic book or humorous podcast'
    ],
    'anger': [
        'Take 10 deep breaths using the 4-7-8 technique',
        'Go for a walk or release tension through exercise',
        'Write about what made you angry and why',
        'Use a punching pillow or stress ball',
        'Distract yourself with calming music or nature sounds'
    ],
    'annoyance': [
        'Step away from the source of irritation',
        'Do a short mindfulness breathing exercise',
        'Listen to calming music',
        'Write down the irritation and tear it up',
        'Talk it out with someone empathetic'
    ],
    'approval': [
        'Celebrate the progress made – big or small',
        'Acknowledge your own accomplishments in a journal',
        'Give someone else a compliment or encouragement',
        'Take a short break as a reward',
        'Make a gratitude list'
    ],
    'caring': [
        'Check in on a loved one or friend',
        'Perform a random act of kindness',
        'Write a letter or card to someone special',
        'Volunteer for a cause you care about',
        'Practice self-care so you can care better for others'
    ],
    'confusion': [
        'Break down the issue and ask “What do I know?”',
        'Take a short walk to reset your mind',
        'Ask someone for clarification or help',
        'Use visual aids like charts to understand better',
        'Watch a quick tutorial on the topic'
    ],
    'curiosity': [
        'Google a question that’s been on your mind',
        'Read an article or watch a video on a new topic',
        'Explore a new hobby or activity',
        'Ask questions to someone knowledgeable',
        'Take an online quiz or mini-course'
    ],
    'desire': [
        'Visualize your goals in a journal or vision board',
        'Make a step-by-step plan toward your desire',
        'Talk about your aspirations with someone supportive',
        'Read success stories in that area',
        'Channel your desire into creative work'
    ],
    'disappointment': [
        'Remind yourself setbacks are part of growth',
        'Write about what you learned from the experience',
        'Do something soothing like a bath or tea',
        'Connect with a supportive friend',
        'Refocus on a new or adjusted goal'
    ],
    'disapproval': [
        'Reflect on whether the criticism is valid or not',
        'Respond with calm, not defensiveness',
        'Set boundaries if needed',
        'Affirm your own values and decisions',
        'Talk to someone who respects your viewpoint'
    ],
    'disgust': [
        'Step away from the trigger and clear your space',
        'Engage in a sensory reset – fresh air, water, fragrance',
        'Talk about the issue with someone to process it',
        'Watch or read something cleansing or uplifting',
        'Clean or declutter your space'
    ],
    'embarrassment': [
        'Remind yourself that everyone feels this sometimes',
        'Laugh it off if possible – humor helps reduce shame',
        'Talk to someone supportive about it',
        'Write down your thoughts to gain perspective',
        'Do something you’re good at to restore confidence'
    ],
    'excitement': [
        'Channel energy into a fun project',
        'Dance to high-energy music',
        'Share your excitement with friends or family',
        'Take a spontaneous walk or drive',
        'Make a creative post or video about it'
    ],
    'fear': [
        'Practice grounding or breathing exercises',
        'Write down fears and rate their realism',
        'Watch a comforting or familiar video',
        'Keep a fear journal and revisit later',
        'Visualize a safe place or outcome'
    ],
    'gratitude': [
        'Write a thank-you note',
        'Make a list of things you’re grateful for',
        'Call or message someone who helped you',
        'Donate or give back to your community',
        'Start a gratitude jar or diary'
    ],
    'grief': [
        'Allow yourself time to feel and cry if needed',
        'Talk about the person or situation you lost',
        'Create a tribute – art, writing, or memory box',
        'Join a support group',
        'Practice gentle self-care activities'
    ],
    'joy': [
        'Capture the moment in a photo or journal',
        'Celebrate with music or a small treat',
        'Express it creatively – drawing, dancing, cooking',
        'Share your joy with a friend',
        'Practice gratitude to amplify the feeling'
    ],
    'love': [
        'Tell someone you love them – friends, family, partner',
        'Do a kind act in their honor',
        'Spend quality time with someone close',
        'Write a love letter or poem',
        'Listen to romantic or heartwarming songs'
    ],
    'nervousness': [
        'Do a quick breathing or body scan exercise',
        'Practice your speech or task to feel prepared',
        'Go for a walk or stretch gently',
        'Listen to calming instrumental music',
        'Visualize a successful outcome'
    ],
    'optimism': [
        'Make a plan for future goals',
        'Motivate someone else with your positive mindset',
        'List the things going well right now',
        'Start a new habit or routine',
        'Visualize your ideal week/month'
    ],
    'pride': [
        'Celebrate your achievement with a small reward',
        'Share your success story',
        'Mentor or help someone just starting out',
        'Document your progress in a journal or portfolio',
        'Acknowledge others who helped you succeed'
    ],
    'realization': [
        'Write down your new insight and how it helps you',
        'Talk it through with a thoughtful friend',
        'Reflect on how it changes your next steps',
        'Make a mind map of your thoughts',
        'Take a quiet walk to process it'
    ],
    'relief': [
        'Take a deep breath and enjoy the calm',
        'Do something purely for fun or relaxation',
        'Reflect on how you overcame the stress',
        'Treat yourself kindly with a reward',
        'Spend time in a peaceful environment'
    ],
    'remorse': [
        'Apologize or make amends if appropriate',
        'Reflect on what led to the mistake and how to avoid it',
        'Write a letter you may or may not send',
        'Give yourself permission to move forward',
        'Talk to someone who offers forgiveness and wisdom'
    ],
    'sadness': [
        'Allow yourself to feel – don’t rush it',
        'Talk to someone who listens without judgment',
        'Cry if you need to, it’s a natural release',
        'Listen to calming music',
        'Try gentle stretching or yoga'
    ],
    'surprise': [
        'Pause and breathe to process it',
        'Share the surprise with someone',
        'Journal how it made you feel',
        'Respond thoughtfully rather than reactively',
        'Turn it into a creative story or sketch'
    ],
    'neutral':[
        'You are perfectly alright!Chill out!',
        'Do whatever you wanna do right now..',
        'Be Happy and Cool like this always',
        'Grab a KitKat, Take a Break'
    ] # type: ignore
}

emotion_colors = {
    'joy': '#FFD700',
    'sadness': '#1E90FF',
    'anger': '#FF4500',
    'fear': '#8A2BE2',
    'love': '#FF69B4',
    'surprise': '#00FA9A',
    'neutral': '#B0BEC5',
    # add more as needed
}

class EmotionPredictor:
    def __init__(self):
        self.classifier = classifier

    def predict_emotion(self, text):
        if not text:
            return {
                'emotion': 'neutral',
                'confidence': 0.0,
                'activities': activity_recommendations['neutral']
            }

        try:
            result = self.classifier(text)
            top_result = result[0][0]
            emotion = top_result['label'].lower()
            confidence = top_result['score']
            activities = activity_recommendations.get(emotion, activity_recommendations['neutral'])

            return {
                'emotion': emotion,
                'confidence': confidence,
                'activities': activities
            }

        except Exception as e:
            return {
                'emotion': 'neutral',
                'confidence': 0.0,
                'activities': activity_recommendations['neutral'],
                'error': str(e)
            }

    def get_emotion_color(self, emotion):
        colors = {
            'joy': '#FFD700',          # Gold
            'sadness': '#2196F3',      # Blue
            'anger': '#F44336',        # Red
            'fear': '#8A2BE2',         # BlueViolet
            'love': '#FF69B4',         # HotPink
            'surprise': '#00FA9A',     # MediumSpringGreen
            'neutral': '#607D8B',      # Blue Grey
            'disgust': '#4CAF50',      # Green
            # You can add more if your model supports
        }
        return colors.get(emotion, '#607D8B')



# Instantiate predictor
emotion_predictor = EmotionPredictor()