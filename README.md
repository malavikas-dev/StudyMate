# 📚 StudyMate

### 🎓 Plan smarter. Study better.

StudyMate is a modern student study-management web application built with **Python, Flask, SQLite, HTML, CSS, and JavaScript**.

It brings subjects, tasks, study sessions, timers, Pomodoro sessions, analytics, and study planning together in one place — helping students organize their academic workload and build consistent study habits.

---

## ✨ Why StudyMate?

Managing college studies often means switching between different apps for:

- 📚 Subjects
- ✅ Assignments and tasks
- ⏱️ Study timers
- 📅 Exam planning
- 📊 Progress tracking
- 🕐 Study history

**StudyMate brings them together in a single dashboard.**

---

## 🚀 Features

### 📊 Dashboard
Get a quick overview of your study activity.

- Total subjects
- Total tasks
- Completed & pending tasks
- Total study hours
- Task completion progress
- Upcoming tasks
- Upcoming exams

### 📚 Subject Management
Keep all your subjects organized.

- Add subjects
- Set difficulty level
- Set exam dates
- Set target study hours
- Edit subjects
- Delete subjects
- View upcoming exams

### ✅ Task Management
Stay on top of your academic workload.

- Create tasks
- Assign tasks to subjects
- Set due dates
- Add descriptions
- Set estimated study hours
- Mark tasks as completed
- Delete tasks

### ⏱️ Study Timer
Track focused study sessions and automatically save them to your study history.

### 🍅 Pomodoro Timer
Use focused study intervals with Pomodoro-style sessions and save completed sessions.

### 📈 Analytics
Understand your study habits through:

- Total study hours
- Number of study sessions
- Average session duration
- Study hours by subject
- Weekly study activity

### 📅 Study Plan
StudyMate calculates a personalized study overview based on:

- Exam date
- Target study hours
- Hours already studied
- Remaining study hours
- Days remaining
- Required daily study hours
- Subject progress

### 🕐 Study History
View previously recorded study sessions, including:

- Subject
- Duration
- Date

### ⚙️ Settings
Customize your StudyMate experience.

- Student name
- Study mode
- Daily study goal
- Pomodoro duration

---

## 🎨 Interface

StudyMate uses a clean, modern student-focused interface with:

- Responsive layout
- Sidebar navigation
- Dashboard cards
- Progress indicators
- Interactive timers
- Bootstrap Icons
- Google Fonts
- Custom CSS styling

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| 🐍 Python | Backend programming |
| 🌶️ Flask | Web framework |
| 🗄️ SQLite | Database |
| 🌐 HTML5 | Page structure |
| 🎨 CSS3 | Styling & UI |
| ⚡ JavaScript | Client-side interactions |
| 🅱️ Bootstrap 5 | UI components |
| 🔷 Bootstrap Icons | Icons |

---

## 🏗️ Project Architecture

```text
StudyMate/
│
├── app.py
├── database.py
├── requirements.txt
├── .gitignore
│
├── database/
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       └── main.js
│
└── templates/
    ├── base.html
    ├── dashboard.html
    ├── subjects.html
    ├── add_subject.html
    ├── edit_subject.html
    ├── tasks.html
    ├── add_task.html
    ├── timer.html
    ├── pomodoro.html
    ├── analytics.html
    ├── study_plan.html
    ├── sessions.html
    └── settings.html

dashboard
<img width="1920" height="1140" alt="image" src="https://github.com/user-attachments/assets/98a76788-9027-421c-b5b4-cc155939b9e7" />

subjects
<img width="1920" height="1140" alt="image" src="https://github.com/user-attachments/assets/b7bff115-bc77-4ed1-b89b-5e7f18d36c46" />

tasks
<img width="1920" height="1140" alt="image" src="https://github.com/user-attachments/assets/c9d2bba1-b5f8-4b0b-964b-b83ade1a8bd7" />

study timer
<img width="1920" height="1140" alt="image" src="https://github.com/user-attachments/assets/64d9253a-2e7c-45e4-bd7f-1fcd4bcb7ab1" />

study history
<img width="1920" height="1140" alt="image" src="https://github.com/user-attachments/assets/6d5a4f92-d5c4-404f-b812-1728fadd78d4" />

analytics
<img width="1920" height="1140" alt="image" src="https://github.com/user-attachments/assets/c8df8cb5-2867-410e-8fd6-bc33fca4c37b" />

study plan
<img width="1920" height="1140" alt="image" src="https://github.com/user-attachments/assets/c1eadad2-38d0-486f-b5fe-ece9262a131e" />

pomodoro
<img width="1920" height="1140" alt="image" src="https://github.com/user-attachments/assets/a4c6c046-71c6-4b18-85ae-cedbecb417c6" />

settings
<img width="1920" height="1140" alt="image" src="https://github.com/user-attachments/assets/7a09355c-4f7d-4205-ac8b-4692609116df" />
