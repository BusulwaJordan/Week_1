// Practice page functionality for MathGenius Uganda

class PracticeManager {
    constructor() {
        this.currentMode = null;
        this.currentTopic = null;
        this.currentGrade = 6;
        this.questions = [];
        this.currentQuestionIndex = 0;
        this.userAnswers = [];
        this.startTime = null;
        this.endTime = null;
        this.timer = null;
        this.timeRemaining = 0;
        this.isTimedMode = false;
        this.isPaused = false;
        this.score = 0;
        this.streakCount = 0;
        this.hintsUsed = 0;
        
        this.initializeElements();
        this.bindEvents();
        this.loadUserData();
    }
    
    initializeElements() {
        // Mode selection elements
        this.modeSelection = document.getElementById('modeSelection');
        this.topicSelection = document.getElementById('topicSelection');
        this.practiceInterface = document.getElementById('practiceInterface');
        this.practiceResults = document.getElementById('practiceResults');
        this.pauseModal = document.getElementById('pauseModal');
        
        // Control elements
        this.modeCards = document.querySelectorAll('.mode-card');
        this.gradeTabs = document.querySelectorAll('.grade-tab');
        this.topicItems = document.querySelectorAll('.topic-item');
        
        // Practice interface elements
        this.questionText = document.getElementById('questionText');
        this.questionOptions = document.getElementById('questionOptions');
        this.questionInput = document.getElementById('questionInput');
        this.answerInput = document.getElementById('answerInput');
        this.submitButton = document.getElementById('submitAnswer');
        this.skipButton = document.getElementById('skipQuestion');
        this.hintButton = document.getElementById('hintButton');
        this.nextButton = document.getElementById('nextQuestion');
        
        // Progress elements
        this.currentQuestionSpan = document.getElementById('currentQuestion');
        this.totalQuestionsSpan = document.getElementById('totalQuestions');
        this.questionProgress = document.getElementById('questionProgress');
        this.timeRemaining = document.getElementById('timeRemaining');
        
        // Feedback elements
        this.answerFeedback = document.getElementById('answerFeedback');
        this.feedbackIcon = this.answerFeedback.querySelector('.feedback-icon');
        this.feedbackTitle = this.answerFeedback.querySelector('.feedback-title');
        this.feedbackMessage = this.answerFeedback.querySelector('.feedback-message');
        this.explanationText = document.getElementById('explanationText');
        
        // Header stats
        this.questionsAnsweredStat = document.getElementById('questionsAnswered');
        this.correctAnswersStat = document.getElementById('correctAnswers');
        this.accuracyStat = document.getElementById('accuracy');
        this.timeSpentStat = document.getElementById('timeSpent');
        this.userPointsDisplay = document.getElementById('userPoints');
    }
    
    bindEvents() {
        // Mode selection
        this.modeCards.forEach(card => {
            card.addEventListener('click', () => this.selectMode(card.dataset.mode));
        });
        
        // Grade tabs
        this.gradeTabs.forEach(tab => {
            tab.addEventListener('click', () => this.selectGrade(parseInt(tab.dataset.grade)));
        });
        
        // Topic selection
        this.topicItems.forEach(item => {
            const button = item.querySelector('.btn');
            if (button) {
                button.addEventListener('click', () => this.selectTopic(item.dataset.topic));
            }
        });
        
        // Practice controls
        document.getElementById('pausePractice')?.addEventListener('click', () => this.pausePractice());
        document.getElementById('quitPractice')?.addEventListener('click', () => this.quitPractice());
        document.getElementById('backToModes')?.addEventListener('click', () => this.showModeSelection());
        
        // Answer submission
        this.submitButton?.addEventListener('click', () => this.submitAnswer());
        this.skipButton?.addEventListener('click', () => this.skipQuestion());
        this.hintButton?.addEventListener('click', () => this.showHint());
        this.nextButton?.addEventListener('click', () => this.nextQuestion());
        
        // Input events
        this.answerInput?.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.submitAnswer();
            }
        });
        
        // Modal events
        document.getElementById('resumePractice')?.addEventListener('click', () => this.resumePractice());
        document.getElementById('quitFromPause')?.addEventListener('click', () => this.quitPractice());
        document.getElementById('closePauseModal')?.addEventListener('click', () => this.resumePractice());
        
        // Results actions
        document.getElementById('practiceAgain')?.addEventListener('click', () => this.restartPractice());
        document.getElementById('viewProgress')?.addEventListener('click', () => window.location.href = 'progress.html');
        document.getElementById('backToDashboard')?.addEventListener('click', () => window.location.href = 'dashboard.html');
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => this.handleKeyboardShortcuts(e));
    }
    
    loadUserData() {
        const userData = JSON.parse(localStorage.getItem('mathGeniusUser')) || {};
        this.userPointsDisplay.textContent = userData.points || 0;
        
        // Load practice history
        this.practiceHistory = JSON.parse(localStorage.getItem('practiceHistory')) || [];
        this.updateHeaderStats();
    }
    
    selectMode(mode) {
        this.currentMode = mode;
        
        switch (mode) {
            case 'quick':
                this.startQuickPractice();
                break;
            case 'topic':
                this.showTopicSelection();
                break;
            case 'timed':
                this.startTimedChallenge();
                break;
            case 'exam':
                this.startMockExam();
                break;
        }
    }
    
    selectGrade(grade) {
        this.currentGrade = grade;
        
        // Update tab appearance
        this.gradeTabs.forEach(tab => {
            tab.classList.toggle('active', parseInt(tab.dataset.grade) === grade);
        });
        
        // Show corresponding topics
        const grade6Topics = document.getElementById('grade6Topics');
        const grade7Topics = document.getElementById('grade7Topics');
        
        if (grade === 6) {
            grade6Topics.classList.add('active');
            grade7Topics.classList.remove('active');
        } else {
            grade7Topics.classList.add('active');
            grade6Topics.classList.remove('active');
        }
    }
    
    selectTopic(topic) {
        this.currentTopic = topic;
        this.startTopicPractice();
    }
    
    showModeSelection() {
        this.modeSelection.classList.remove('hidden');
        this.topicSelection.classList.add('hidden');
        this.practiceInterface.classList.add('hidden');
        this.practiceResults.classList.add('hidden');
    }
    
    showTopicSelection() {
        this.modeSelection.classList.add('hidden');
        this.topicSelection.classList.remove('hidden');
        this.practiceInterface.classList.add('hidden');
        this.practiceResults.classList.add('hidden');
    }
    
    showPracticeInterface() {
        this.modeSelection.classList.add('hidden');
        this.topicSelection.classList.add('hidden');
        this.practiceInterface.classList.remove('hidden');
        this.practiceResults.classList.add('hidden');
    }
    
    showResults() {
        this.modeSelection.classList.add('hidden');
        this.topicSelection.classList.add('hidden');
        this.practiceInterface.classList.add('hidden');
        this.practiceResults.classList.remove('hidden');
    }
    
    async startQuickPractice() {
        this.questions = await this.generateQuestions('mixed', 10);
        this.timeRemaining = 10 * 60; // 10 minutes
        this.isTimedMode = false;
        this.initializePractice();
    }
    
    async startTopicPractice() {
        const questionCount = this.getTopicQuestionCount();
        this.questions = await this.generateQuestions(this.currentTopic, questionCount);
        this.timeRemaining = questionCount * 90; // 1.5 minutes per question
        this.isTimedMode = false;
        this.initializePractice();
    }
    
    async startTimedChallenge() {
        this.questions = await this.generateQuestions('mixed', 50);
        this.timeRemaining = 10 * 60; // 10 minutes
        this.isTimedMode = true;
        this.initializePractice();
    }
    
    async startMockExam() {
        this.questions = await this.generateQuestions('exam', 50);
        this.timeRemaining = 60 * 60; // 60 minutes
        this.isTimedMode = true;
        this.initializePractice();
    }
    
    getTopicQuestionCount() {
        const topicCounts = {
            'numbers-p6': 30,
            'measurement-p6': 25,
            'geometry-p6': 25,
            'data-p6': 20,
            'problem-solving-p6': 20,
            'ratio-p6': 15,
            'advanced-numbers-p7': 35,
            'algebra-p7': 30,
            '3d-geometry-p7': 30,
            'statistics-p7': 25,
            'financial-p7': 25,
            'advanced-problem-solving-p7': 30
        };
        
        return topicCounts[this.currentTopic] || 20;
    }
    
    async generateQuestions(topic, count) {
        // This would normally fetch from a backend API
        // For demo purposes, we'll generate questions using the question engine
        const questions = [];
        
        for (let i = 0; i < count; i++) {
            const question = this.generateSingleQuestion(topic, i);
            questions.push(question);
        }
        
        return questions;
    }
    
    generateSingleQuestion(topic, index) {
        const questionTypes = this.getQuestionTypesForTopic(topic);
        const randomType = questionTypes[Math.floor(Math.random() * questionTypes.length)];
        
        const question = window.MathGenius.MathUtils.generateProblem(randomType.type, randomType.difficulty);
        
        return {
            id: `q_${Date.now()}_${index}`,
            type: randomType.type,
            difficulty: randomType.difficulty,
            question: question.question,
            correctAnswer: question.answer,
            options: this.generateOptions(question.answer, randomType.type),
            explanation: this.generateExplanation(question),
            hint: this.generateHint(question),
            points: this.getPointsForDifficulty(randomType.difficulty),
            topic: topic,
            isMultipleChoice: randomType.isMultipleChoice !== false
        };
    }
    
    getQuestionTypesForTopic(topic) {
        const typesByTopic = {
            'numbers-p6': [
                { type: 'addition', difficulty: 'easy', isMultipleChoice: true },
                { type: 'subtraction', difficulty: 'easy', isMultipleChoice: true },
                { type: 'multiplication', difficulty: 'easy', isMultipleChoice: true },
                { type: 'division', difficulty: 'easy', isMultipleChoice: true }
            ],
            'measurement-p6': [
                { type: 'measurement', difficulty: 'easy', isMultipleChoice: true },
                { type: 'conversion', difficulty: 'medium', isMultipleChoice: true }
            ],
            'geometry-p6': [
                { type: 'shapes', difficulty: 'easy', isMultipleChoice: true },
                { type: 'angles', difficulty: 'medium', isMultipleChoice: true }
            ],
            'mixed': [
                { type: 'addition', difficulty: 'easy', isMultipleChoice: true },
                { type: 'subtraction', difficulty: 'easy', isMultipleChoice: true },
                { type: 'multiplication', difficulty: 'medium', isMultipleChoice: true },
                { type: 'division', difficulty: 'medium', isMultipleChoice: true }
            ]
        };
        
        return typesByTopic[topic] || typesByTopic['mixed'];
    }
    
    generateOptions(correctAnswer, type) {
        const options = [correctAnswer];
        
        // Generate 3 incorrect options
        for (let i = 0; i < 3; i++) {
            let incorrectAnswer;
            do {
                const variance = Math.floor(Math.random() * 20) - 10;
                incorrectAnswer = correctAnswer + variance;
                if (incorrectAnswer <= 0) incorrectAnswer = correctAnswer + Math.abs(variance);
            } while (options.includes(incorrectAnswer));
            
            options.push(incorrectAnswer);
        }
        
        // Shuffle options
        return window.MathGenius.MathUtils.shuffleArray(options);
    }
    
    generateExplanation(question) {
        return `To solve ${question.question.replace(' = ?', '')}, we calculate step by step and get ${question.answer}.`;
    }
    
    generateHint(question) {
        const hints = [
            "Break down the problem into smaller steps.",
            "Remember the order of operations.",
            "Think about what operation is being asked.",
            "Try working backwards from the answer choices.",
            "Draw a picture or diagram if it helps."
        ];
        
        return hints[Math.floor(Math.random() * hints.length)];
    }
    
    getPointsForDifficulty(difficulty) {
        const pointsByDifficulty = {
            'easy': 10,
            'medium': 15,
            'hard': 25
        };
        
        return pointsByDifficulty[difficulty] || 10;
    }
    
    initializePractice() {
        this.currentQuestionIndex = 0;
        this.userAnswers = [];
        this.startTime = new Date();
        this.endTime = null;
        this.score = 0;
        this.streakCount = 0;
        this.hintsUsed = 0;
        this.isPaused = false;
        
        this.showPracticeInterface();
        this.updatePracticeHeader();
        this.showQuestion();
        
        if (this.isTimedMode) {
            this.startTimer();
        }
    }
    
    updatePracticeHeader() {
        document.getElementById('practiceTitle').textContent = this.getPracticeTitle();
        document.getElementById('practiceDescription').textContent = this.getPracticeDescription();
        this.totalQuestionsSpan.textContent = this.questions.length;
    }
    
    getPracticeTitle() {
        const titles = {
            'quick': 'Quick Practice',
            'topic': `${this.getTopicDisplayName()} Practice`,
            'timed': 'Timed Challenge',
            'exam': 'Mock Exam'
        };
        
        return titles[this.currentMode] || 'Mathematics Practice';
    }
    
    getPracticeDescription() {
        const descriptions = {
            'quick': 'Answer 10 random questions to sharpen your skills',
            'topic': `Master ${this.getTopicDisplayName()} with focused practice`,
            'timed': 'Answer as many questions as possible in 10 minutes',
            'exam': 'Full-length practice test to prepare for exams'
        };
        
        return descriptions[this.currentMode] || 'Choose your practice mode and start learning!';
    }
    
    getTopicDisplayName() {
        const displayNames = {
            'numbers-p6': 'Numbers & Operations',
            'measurement-p6': 'Measurement',
            'geometry-p6': 'Geometry',
            'data-p6': 'Data Handling',
            'problem-solving-p6': 'Problem Solving',
            'ratio-p6': 'Ratio & Proportion',
            'advanced-numbers-p7': 'Advanced Numbers',
            'algebra-p7': 'Algebra Basics',
            '3d-geometry-p7': '3D Geometry',
            'statistics-p7': 'Advanced Statistics',
            'financial-p7': 'Financial Mathematics',
            'advanced-problem-solving-p7': 'Advanced Problem Solving'
        };
        
        return displayNames[this.currentTopic] || 'Mathematics';
    }
    
    showQuestion() {
        if (this.currentQuestionIndex >= this.questions.length) {
            this.endPractice();
            return;
        }
        
        const question = this.questions[this.currentQuestionIndex];
        
        // Update progress
        this.currentQuestionSpan.textContent = this.currentQuestionIndex + 1;
        const progressPercent = ((this.currentQuestionIndex + 1) / this.questions.length) * 100;
        this.questionProgress.style.width = `${progressPercent}%`;
        
        // Update question content
        this.questionText.textContent = question.question;
        document.getElementById('questionType').textContent = this.formatQuestionType(question.type);
        document.getElementById('questionDifficulty').textContent = this.formatDifficulty(question.difficulty);
        
        // Show appropriate input method
        if (question.isMultipleChoice) {
            this.showMultipleChoiceOptions(question.options);
            this.questionInput.style.display = 'none';
        } else {
            this.showTextInput();
            this.questionOptions.style.display = 'none';
        }
        
        // Reset feedback
        this.answerFeedback.classList.add('hidden');
        this.submitButton.disabled = false;
        this.submitButton.innerHTML = '<i class="fas fa-check"></i> Submit Answer';
        
        // Add animation
        document.querySelector('.question-card').classList.add('question-appear');
        setTimeout(() => {
            document.querySelector('.question-card').classList.remove('question-appear');
        }, 500);
    }
    
    showMultipleChoiceOptions(options) {
        this.questionOptions.innerHTML = '';
        this.questionOptions.style.display = 'grid';
        
        options.forEach((option, index) => {
            const button = document.createElement('button');
            button.className = 'option-button';
            button.textContent = option;
            button.dataset.value = option;
            
            button.addEventListener('click', () => {
                // Remove selection from other options
                this.questionOptions.querySelectorAll('.option-button').forEach(btn => {
                    btn.classList.remove('selected');
                });
                
                // Select this option
                button.classList.add('selected');
            });
            
            this.questionOptions.appendChild(button);
        });
    }
    
    showTextInput() {
        this.questionInput.style.display = 'block';
        this.answerInput.value = '';
        this.answerInput.focus();
    }
    
    formatQuestionType(type) {
        const typeNames = {
            'addition': 'Addition',
            'subtraction': 'Subtraction',
            'multiplication': 'Multiplication',
            'division': 'Division',
            'measurement': 'Measurement',
            'geometry': 'Geometry',
            'algebra': 'Algebra'
        };
        
        return typeNames[type] || 'Mathematics';
    }
    
    formatDifficulty(difficulty) {
        return difficulty.charAt(0).toUpperCase() + difficulty.slice(1);
    }
    
    submitAnswer() {
        const question = this.questions[this.currentQuestionIndex];
        let userAnswer = null;
        
        if (question.isMultipleChoice) {
            const selectedOption = this.questionOptions.querySelector('.option-button.selected');
            if (!selectedOption) {
                window.MathGenius.showNotification('Please select an answer', 'error');
                return;
            }
            userAnswer = parseFloat(selectedOption.dataset.value);
        } else {
            userAnswer = parseFloat(this.answerInput.value);
            if (isNaN(userAnswer)) {
                window.MathGenius.showNotification('Please enter a valid number', 'error');
                return;
            }
        }
        
        const isCorrect = userAnswer === question.correctAnswer;
        
        // Record answer
        this.userAnswers.push({
            questionId: question.id,
            userAnswer: userAnswer,
            correctAnswer: question.correctAnswer,
            isCorrect: isCorrect,
            timeSpent: this.getTimeSpent(),
            hintsUsed: this.hintsUsed > 0
        });
        
        // Update score and streak
        if (isCorrect) {
            const points = question.points + (this.streakCount >= 3 ? 5 : 0); // Bonus for streak
            this.score += points;
            this.streakCount++;
            
            // Update user points
            this.updateUserPoints(points);
        } else {
            this.streakCount = 0;
        }
        
        // Show feedback
        this.showAnswerFeedback(isCorrect, question);
        
        // Update stats
        this.updateHeaderStats();
        
        // Disable submit button
        this.submitButton.disabled = true;
    }
    
    showAnswerFeedback(isCorrect, question) {
        this.answerFeedback.classList.remove('hidden');
        this.answerFeedback.classList.add('feedback-appear');
        
        // Update feedback content
        this.feedbackIcon.className = `feedback-icon ${isCorrect ? 'correct' : 'incorrect'}`;
        this.feedbackIcon.innerHTML = `<i class="fas fa-${isCorrect ? 'check' : 'times'}-circle"></i>`;
        
        this.feedbackTitle.className = `feedback-title ${isCorrect ? 'correct' : 'incorrect'}`;
        this.feedbackTitle.textContent = isCorrect ? 'Correct!' : 'Incorrect';
        
        this.feedbackMessage.textContent = isCorrect 
            ? this.getPositiveFeedback() 
            : `The correct answer is ${question.correctAnswer}`;
        
        this.explanationText.textContent = question.explanation;
        
        // Update option styles for multiple choice
        if (question.isMultipleChoice) {
            this.questionOptions.querySelectorAll('.option-button').forEach(btn => {
                const value = parseFloat(btn.dataset.value);
                if (value === question.correctAnswer) {
                    btn.classList.add('correct');
                } else if (btn.classList.contains('selected') && !isCorrect) {
                    btn.classList.add('incorrect');
                }
                btn.style.pointerEvents = 'none';
            });
        }
        
        setTimeout(() => {
            this.answerFeedback.classList.remove('feedback-appear');
        }, 500);
    }
    
    getPositiveFeedback() {
        const messages = [
            'Excellent work!',
            'Great job!',
            'Well done!',
            'Perfect!',
            'Outstanding!',
            'You\'re on fire!',
            'Keep it up!',
            'Brilliant!'
        ];
        
        return messages[Math.floor(Math.random() * messages.length)];
    }
    
    skipQuestion() {
        const question = this.questions[this.currentQuestionIndex];
        
        this.userAnswers.push({
            questionId: question.id,
            userAnswer: null,
            correctAnswer: question.correctAnswer,
            isCorrect: false,
            timeSpent: this.getTimeSpent(),
            skipped: true
        });
        
        this.streakCount = 0;
        this.nextQuestion();
    }
    
    showHint() {
        const question = this.questions[this.currentQuestionIndex];
        this.hintsUsed++;
        
        window.MathGenius.showNotification(question.hint, 'info');
        
        // Reduce points for using hint
        question.points = Math.max(1, question.points - 2);
    }
    
    nextQuestion() {
        this.currentQuestionIndex++;
        this.hintsUsed = 0;
        this.showQuestion();
    }
    
    pausePractice() {
        this.isPaused = true;
        this.pauseModal.classList.remove('hidden');
        
        if (this.timer) {
            clearInterval(this.timer);
        }
        
        // Update pause modal stats
        document.getElementById('pauseQuestionsAnswered').textContent = this.userAnswers.length;
        document.getElementById('pauseAccuracy').textContent = this.calculateAccuracy() + '%';
        document.getElementById('pauseTimeElapsed').textContent = this.formatTime(this.getElapsedTime());
    }
    
    resumePractice() {
        this.isPaused = false;
        this.pauseModal.classList.add('hidden');
        
        if (this.isTimedMode) {
            this.startTimer();
        }
    }
    
    quitPractice() {
        if (confirm('Are you sure you want to quit? Your progress will be lost.')) {
            this.endPractice();
        }
    }
    
    endPractice() {
        this.endTime = new Date();
        
        if (this.timer) {
            clearInterval(this.timer);
        }
        
        // Save practice session
        this.savePracticeSession();
        
        // Show results
        this.displayResults();
        this.showResults();
    }
    
    displayResults() {
        const totalQuestions = this.userAnswers.length;
        const correctAnswers = this.userAnswers.filter(a => a.isCorrect).length;
        const accuracy = totalQuestions > 0 ? Math.round((correctAnswers / totalQuestions) * 100) : 0;
        const timeSpent = this.formatTime(this.getElapsedTime());
        
        // Update result stats
        document.getElementById('finalScore').textContent = this.score;
        document.getElementById('finalAccuracy').textContent = accuracy + '%';
        document.getElementById('finalTime').textContent = timeSpent;
        document.getElementById('pointsEarned').textContent = '+' + this.score;
        
        // Update breakdown
        document.getElementById('correctCount').textContent = correctAnswers;
        document.getElementById('incorrectCount').textContent = this.userAnswers.filter(a => !a.isCorrect && !a.skipped).length;
        document.getElementById('skippedCount').textContent = this.userAnswers.filter(a => a.skipped).length;
        
        // Check for achievements
        this.checkAchievements();
        
        // Add animation
        document.querySelector('.results-card').classList.add('results-appear');
        setTimeout(() => {
            document.querySelector('.results-card').classList.remove('results-appear');
        }, 600);
    }
    
    checkAchievements() {
        const achievements = [];
        const correctAnswers = this.userAnswers.filter(a => a.isCorrect).length;
        const accuracy = this.calculateAccuracy();
        
        // Perfect score achievement
        if (accuracy === 100 && this.userAnswers.length >= 10) {
            achievements.push({ icon: 'trophy', name: 'Perfect Score!' });
        }
        
        // Speed achievement
        if (this.isTimedMode && correctAnswers >= 20) {
            achievements.push({ icon: 'bolt', name: 'Speed Demon!' });
        }
        
        // Streak achievement
        if (this.streakCount >= 10) {
            achievements.push({ icon: 'fire', name: 'Hot Streak!' });
        }
        
        // First practice achievement
        if (this.practiceHistory.length === 0) {
            achievements.push({ icon: 'star', name: 'First Practice!' });
        }
        
        if (achievements.length > 0) {
            this.displayAchievements(achievements);
        }
    }
    
    displayAchievements(achievements) {
        const achievementsEarned = document.getElementById('achievementsEarned');
        const achievementList = document.getElementById('achievementList');
        
        achievementList.innerHTML = '';
        
        achievements.forEach(achievement => {
            const badge = document.createElement('div');
            badge.className = 'achievement-badge';
            badge.innerHTML = `<i class="fas fa-${achievement.icon}"></i>`;
            badge.title = achievement.name;
            
            achievementList.appendChild(badge);
        });
        
        achievementsEarned.style.display = 'block';
    }
    
    restartPractice() {
        // Reset all practice data
        this.currentQuestionIndex = 0;
        this.userAnswers = [];
        this.score = 0;
        this.streakCount = 0;
        this.hintsUsed = 0;
        
        // Generate new questions and restart
        this.selectMode(this.currentMode);
    }
    
    startTimer() {
        this.timer = setInterval(() => {
            if (!this.isPaused) {
                this.timeRemaining--;
                
                if (this.timeRemaining <= 0) {
                    this.endPractice();
                    return;
                }
                
                // Update timer display
                const timerDisplay = document.getElementById('timeRemaining');
                if (timerDisplay) {
                    timerDisplay.textContent = this.formatTime(this.timeRemaining);
                    
                    // Add warning color when time is low
                    if (this.timeRemaining <= 60) {
                        timerDisplay.style.color = '#ef4444';
                    } else if (this.timeRemaining <= 300) {
                        timerDisplay.style.color = '#f59e0b';
                    }
                }
            }
        }, 1000);
    }
    
    updateHeaderStats() {
        const totalAnswered = this.userAnswers.length;
        const correctAnswers = this.userAnswers.filter(a => a.isCorrect).length;
        const accuracy = this.calculateAccuracy();
        const timeSpent = this.formatTime(this.getElapsedTime());
        
        this.questionsAnsweredStat.textContent = totalAnswered;
        this.correctAnswersStat.textContent = correctAnswers;
        this.accuracyStat.textContent = accuracy + '%';
        this.timeSpentStat.textContent = timeSpent;
    }
    
    calculateAccuracy() {
        const totalAnswered = this.userAnswers.filter(a => !a.skipped).length;
        const correctAnswers = this.userAnswers.filter(a => a.isCorrect).length;
        
        return totalAnswered > 0 ? Math.round((correctAnswers / totalAnswered) * 100) : 0;
    }
    
    getElapsedTime() {
        const endTime = this.endTime || new Date();
        return Math.floor((endTime - this.startTime) / 1000);
    }
    
    getTimeSpent() {
        return Math.floor((new Date() - this.startTime) / 1000);
    }
    
    formatTime(seconds) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
    }
    
    updateUserPoints(points) {
        const userData = JSON.parse(localStorage.getItem('mathGeniusUser')) || {};
        userData.points = (userData.points || 0) + points;
        localStorage.setItem('mathGeniusUser', JSON.stringify(userData));
        
        this.userPointsDisplay.textContent = userData.points;
        
        // Animate points increase
        this.userPointsDisplay.classList.add('animate-bounce');
        setTimeout(() => {
            this.userPointsDisplay.classList.remove('animate-bounce');
        }, 1000);
    }
    
    savePracticeSession() {
        const session = {
            id: Date.now(),
            mode: this.currentMode,
            topic: this.currentTopic,
            grade: this.currentGrade,
            startTime: this.startTime,
            endTime: this.endTime,
            questionsAnswered: this.userAnswers.length,
            correctAnswers: this.userAnswers.filter(a => a.isCorrect).length,
            score: this.score,
            accuracy: this.calculateAccuracy(),
            timeSpent: this.getElapsedTime(),
            answers: this.userAnswers
        };
        
        this.practiceHistory.push(session);
        localStorage.setItem('practiceHistory', JSON.stringify(this.practiceHistory));
        
        // Update overall progress
        window.MathGenius.saveUserProgress(this.currentTopic, this.calculateAccuracy());
    }
    
    handleKeyboardShortcuts(e) {
        if (this.practiceInterface.classList.contains('hidden')) return;
        
        // Number keys for multiple choice
        if (e.key >= '1' && e.key <= '4') {
            const optionIndex = parseInt(e.key) - 1;
            const options = this.questionOptions.querySelectorAll('.option-button');
            if (options[optionIndex]) {
                options[optionIndex].click();
            }
        }
        
        // Enter to submit
        if (e.key === 'Enter' && !this.submitButton.disabled) {
            this.submitAnswer();
        }
        
        // Space to continue
        if (e.key === ' ' && !this.answerFeedback.classList.contains('hidden')) {
            e.preventDefault();
            this.nextQuestion();
        }
        
        // S to skip
        if (e.key === 's' || e.key === 'S') {
            this.skipQuestion();
        }
        
        // H for hint
        if (e.key === 'h' || e.key === 'H') {
            this.showHint();
        }
        
        // P to pause
        if (e.key === 'p' || e.key === 'P') {
            this.pausePractice();
        }
    }
}

// Initialize practice manager when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.practiceManager = new PracticeManager();
});

// Handle URL parameters for direct topic access
window.addEventListener('load', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const mode = urlParams.get('mode');
    const topic = urlParams.get('topic');
    const grade = urlParams.get('grade');
    
    if (mode && window.practiceManager) {
        if (grade) {
            window.practiceManager.selectGrade(parseInt(grade));
        }
        
        if (topic) {
            window.practiceManager.currentTopic = topic;
            window.practiceManager.selectMode('topic');
        } else {
            window.practiceManager.selectMode(mode);
        }
    }
});