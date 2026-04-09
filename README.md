🥗 AI Food Companion

A fully local AI-powered calorie tracking app built with Python, Streamlit, and Ollama — no APIs, no subscriptions, runs entirely on your laptop.

⸻

🚀 Features
	•	💬 Chat-based food logging
	•	🤖 AI understands natural language (e.g., “I ate 2 rotis and paneer”)
	•	🔥 Automatic calorie calculation
	•	📊 Daily tracking with progress visualization
	•	🧠 Local AI using Ollama (100% private)
	•	🗂 Food history and analytics
	•	🎯 Personalized calorie goals

⸻

🧱 Tech Stack
	•	Frontend: Streamlit
	•	Backend: Python
	•	AI Engine: Ollama (LLaMA / Phi)
	•	Database: SQLite
	•	Charts: Plotly

⸻

📂 Project Structure

ai-food-app/

app.py
ai_engine.py
calorie_calc.py
food_database.py
user_profile.py
db.py

utils/
 helpers.py

data/

requirements.txt

⸻

⚙️ Setup (Mac / Linux)
	1.	Clone the repository

git clone https://github.com/devilxdevilx1-web/ai_food_companion.git
cd ai_food_companion

⸻

	2.	Create virtual environment

python3.11 -m venv venv
source venv/bin/activate

⸻

	3.	Install dependencies

pip install -r requirements.txt

⸻

	4.	Install Ollama

brew install ollama

⸻

	5.	Download AI model

ollama pull llama3.2

⸻

	6.	Start Ollama server

ollama serve

⸻

	7.	Run the app

streamlit run app.py

⸻

🌐 Open App

http://localhost:8501

⸻

🧠 How It Works
	1.	User enters profile (age, weight, goal)
	2.	App calculates daily calorie requirement
	3.	User types food in chat
	4.	AI analyzes food and calculates calories
	5.	Data is stored locally in SQLite
	6.	Dashboard updates in real-time

⸻

🔒 Privacy
	•	Runs fully offline
	•	No API calls
	•	No data leaves your device

⸻

🚀 Future Improvements
	•	🎙 Voice input
	•	📱 Mobile app version
	•	🧠 Memory-based AI coach
	•	☁️ Cloud sync

⸻

👨‍💻 Author

Devieswar

⸻

⭐ If you like this project

Give it a star on GitHub ⭐

⸻

📜 License

MIT License
