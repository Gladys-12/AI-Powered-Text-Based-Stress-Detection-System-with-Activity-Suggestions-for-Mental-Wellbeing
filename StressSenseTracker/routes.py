from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from app import app,db
from models import User, EmotionLog
from emotion_model import EmotionPredictor, emotion_predictor
import logging


@app.route("/routes")
def list_routes():
    return "<br>".join(str(rule) for rule in app.url_map.iter_rules())

@app.route('/')
def index():
    """Home page - redirect to dashboard if logged in, otherwise to login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required.', 'error')
            return render_template('register.html')
        
        if len(username) < 3:
            flash('Username must be at least 3 characters long.', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose a different one.', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please use a different email.', 'error')
            return render_template('register.html')
        
        # Create new user
        try:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        
        except Exception as e:
            db.session.rollback()
            logging.error(f"Registration error: {str(e)}")
            flash('An error occurred during registration. Please try again.', 'error')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            flash('Please enter both username and password.', 'error')
            return render_template('login.html')
        
        # Find user by username or email
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()
        
        if user and user.check_password(password):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(next_page if next_page else url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard page"""
    # Get recent emotion logs for the user
    recent_logs = EmotionLog.query.filter_by(user_id=current_user.id)\
                                  .order_by(EmotionLog.timestamp.desc())\
                                  .limit(5)\
                                  .all()
    
    return render_template('dashboard.html', recent_logs=recent_logs)

@app.route('/analyze', methods=['POST'])
@login_required
def analyze_emotion():
    """Analyze emotion from text input"""
    text_input = request.form.get('text_input', '').strip()
    
    if not text_input:
        flash('Please enter some text to analyze.', 'error')
        return redirect(url_for('dashboard'))
    
    if len(text_input) < 10:
        flash('Please enter at least 10 characters for better analysis.', 'warning')
        return redirect(url_for('dashboard'))
    
    try:
        # Predict emotion
        result = emotion_predictor.predict_emotion(text_input)
        
        # Save to database
        emotion_log = EmotionLog(
            user_id=current_user.id,
            text_input=text_input,
            predicted_emotion=result['emotion'],
            confidence_score=result.get('confidence', 0.0)
        )
        db.session.add(emotion_log)
        db.session.commit()
        
        # Get emotion color for display
        emotion_color = emotion_predictor.get_emotion_color(result['emotion'])
        activities = result['activities']  # Correct way

        return render_template('result.html', 
                             result=result, 
                             text_input=text_input,
                             emotion_color=emotion_color,
                             activities=activities)
    
    except Exception as e:
        logging.error(f"Error analyzing emotion: {str(e)}")
        flash('An error occurred while analyzing your text. Please try again.', 'error')
        return redirect(url_for('dashboard'))

@app.route('/history')
@login_required
def history():
    """View emotion analysis history"""
    page = request.args.get('page', 1, type=int)
    logs = EmotionLog.query.filter_by(user_id=current_user.id)\
                          .order_by(EmotionLog.timestamp.desc())\
                          .paginate(page=page, per_page=10, error_out=False)
    
    
    return render_template('history.html', logs=logs)

@app.route('/timeline')
@login_required
def timeline():
    """Interactive timeline visualization of emotion trends"""
    # Get all emotion logs for the user
    logs = EmotionLog.query.filter_by(user_id=current_user.id)\
                          .order_by(EmotionLog.timestamp.asc())\
                          .all()
    
    # Prepare data for timeline visualization
    timeline_data = []
    emotion_counts = {}
    daily_emotions = {}
    
    for log in logs:
        # Format timestamp for JavaScript
        timestamp = log.timestamp.isoformat()
        date_key = log.timestamp.strftime('%Y-%m-%d')
        
        timeline_data.append({
            'timestamp': timestamp,
            'emotion': log.predicted_emotion,
            'confidence': log.confidence_score,
            'text': log.text_input[:100] + '...' if len(log.text_input) > 100 else log.text_input,
            'color': emotion_predictor.get_emotion_color(log.predicted_emotion)
        })
        
        # Count emotions for stats
        emotion_counts[log.predicted_emotion] = emotion_counts.get(log.predicted_emotion, 0) + 1
        
        # Group by day for trend analysis
        if date_key not in daily_emotions:
            daily_emotions[date_key] = []
        daily_emotions[date_key].append(log.predicted_emotion)
    
    # Calculate daily dominant emotions
    daily_trends = []
    for date, emotions in daily_emotions.items():
        dominant_emotion = max(set(emotions), key=emotions.count)
        daily_trends.append({
            'date': date,
            'emotion': dominant_emotion,
            'count': len(emotions),
            'color': emotion_predictor.get_emotion_color(dominant_emotion)
        })
    
    return render_template('timeline.html', 
                         timeline_data=timeline_data,
                         emotion_counts=emotion_counts,
                         daily_trends=daily_trends,
                         total_entries=len(logs))

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('500.html'), 500

# Initialize model when the module loads
# Initialize model when the module loads
def initialize_model():
    """Initialize the emotion prediction model using Huggingface API"""
    try:
        # Assuming emotion_predictor handles API setup or caching internally
        emotion_predictor=EmotionPredictor()
        logging.info("Emotion prediction model initialized successfully.")
    except Exception as e:
        logging.error(f"Failed to initialize emotion prediction model: {str(e)}")

# Call initialization immediately
initialize_model()
