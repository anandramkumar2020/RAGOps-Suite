# RAGOps Environment Setup

## Backend Setup

### 1. Create and Activate Conda Environment
```bash
conda create --name ragstack-env python=3.11 --yes
conda activate ragstack-env
```

### 2. Install Backend Dependencies
The following packages were installed using pip:
```bash
pip install llama-index
pip install fastapi
pip install uvicorn
pip install python-dotenv
```

### 3. Environment Configuration
Create a `.env` file in the `ragstack/backend` directory with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

### 4. Running the Backend
```bash
# Start the backend server
cd ragstack/backend
python main.py

# The server will be available at http://localhost:8000
# You can access the API documentation at http://localhost:8000/docs
```

### 5. Stopping the Backend
```bash
# Press Ctrl+C in the terminal where the backend is running
# This will gracefully shut down the FastAPI server
```

## Frontend Setup

### 1. Create React Project using Vite
```bash
npm create vite@latest ragstack/frontend -- --template react
```

### 2. Install Frontend Dependencies
```bash
cd ragstack/frontend
npm install
```

### 3. Running the Frontend
```bash
npm run dev

# The development server will be available at http://localhost:5173
# The terminal will show any compilation errors or warnings
```

### 4. Stopping the Frontend
```bash
# Press Ctrl+C in the terminal where the frontend is running
# This will stop the Vite development server
```

## Project Structure
```
RAGOps-Suite/
├── ragstack/
│   ├── backend/
│   │   ├── data/           # Document storage
│   │   ├── main.py        # FastAPI server
│   │   └── .env          # Environment variables
│   └── frontend/
│       ├── src/
│       │   ├── App.jsx   # Main React component
│       │   └── App.css   # Styles
│       └── package.json
└── environment/
    └── setup_instructions.md
```

## Development Tips

1. Always start the backend server before the frontend to ensure the API endpoints are available.
2. Keep the terminal windows for both servers visible to monitor for any errors or warnings.
3. The backend server must be restarted to pick up any changes to Python files.
4. The frontend development server automatically reloads when you make changes to the source files.
5. Make sure to properly stop both servers before making any major changes to the environment or dependencies.
