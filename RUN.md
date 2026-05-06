# How to Run the AI Data Assistant (React + Flask)

## Problem: "npm is not recognized"

This error means Node.js is not installed or not in your system PATH.

## Solution - Install Node.js:

1. **Download Node.js** from: https://nodejs.org (LTS version - 18.x or 20.x)
2. **Run the installer** - click next, next, next...
3. **RESTART YOUR TERMINAL** - This is important! Close and reopen your command prompt
4. **Verify installation** - Run: `node --version` and `npm --version`

## After Node.js is Installed:

### Step 1: Create .env File
In the project root folder, create a file named `.env`:
```
OPENAI_API_KEY=your_openai_key_here
```

### Step 2: Open Fresh Terminal (NOT in venv)
Open a NEW command prompt window (don't use the venv terminal for npm)

### Step 3: Install Frontend Dependencies
```bash
cd c:\Users\pedapalli.s.lv\ai_data_project\frontend
npm install
```

### Step 4: Run Backend (Terminal 1)
```bash
cd c:\Users\pedapalli.s.lv\ai_data_project
python api.py
```

### Step 5: Run Frontend (Terminal 2)
```bash
cd c:\Users\pedapalli.s.lv\ai_data_project\frontend
npm run dev
```

### Step 6: Open Browser
Go to: **http://localhost:3000**

---

## IMPORTANT NOTES:

1. **Do NOT run npm inside the venv** - npm should be used in a normal terminal
2. **Restart terminal after installing Node.js** - Path won't update otherwise
3. **Keep both terminals open** while using the app
