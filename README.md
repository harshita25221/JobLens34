# JobLens

JobLens is a job search application that helps users find relevant job opportunities and analyze required skills.

## Project Structure

The project consists of two main components:

- **Frontend**: React application built with Vite, TypeScript, and Tailwind CSS
- **Backend**: Node.js API server that interfaces with the OpenAI API

## Deployment Options

JobLens can be deployed using several methods:

### 1. Automated Deployment Script

Use the provided PowerShell script to deploy both components with minimal effort:

```powershell
.\deploy.ps1
```

The script will:
- Deploy the backend to Heroku
- Update the frontend configuration to use the deployed backend URL
- Build and deploy the frontend to Netlify or Vercel (based on configuration)

### 2. Manual Deployment

Follow the steps in the `COMBINED_DEPLOYMENT_GUIDE.md` file for detailed instructions on manually deploying each component.

### 3. Web Interface Deployment

If you prefer using web interfaces instead of command-line tools:

- For Heroku and Netlify: See `WEB_DEPLOYMENT_GUIDE.md`
- For Railway (unified deployment): See `RAILWAY_DEPLOYMENT.md`

## Prerequisites

Before deployment, ensure you have all required tools installed. See `DEPLOYMENT_PREREQUISITES.md` for details.

## Documentation

- `DEPLOYMENT_README.md`: Quick reference for deployment options
- `COMBINED_DEPLOYMENT_GUIDE.md`: Detailed manual deployment steps
- `DEPLOYMENT_PREREQUISITES.md`: Required tools and setup
- `WEB_DEPLOYMENT_GUIDE.md`: Web interface deployment overview
- `HEROKU_WEB_DEPLOYMENT.md`: Heroku web interface deployment
- `NETLIFY_WEB_DEPLOYMENT.md`: Netlify web interface deployment
- `RAILWAY_DEPLOYMENT.md`: Railway unified deployment
- `RENDER_DEPLOYMENT.md`: Render unified deployment

## Environment Variables

### Backend

- `OPENAI_API_KEY`: Your OpenAI API key

### Frontend

- `VITE_API_URL`: URL of your deployed backend

## Development

### Backend

```bash
cd backend
npm install
npm start
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```