# JobLens Combined Deployment

This document provides instructions for deploying both the frontend and backend components of JobLens together.

## Prerequisites

Before deployment, ensure you have all required tools installed:

1. **Check the prerequisites document**:
   ```
   DEPLOYMENT_PREREQUISITES.md
   ```

2. Install all required tools:
   - Node.js and npm
   - Heroku CLI
   - Netlify CLI (or Vercel CLI)
   - Git

## Deployment Options

You have three main options for deploying the JobLens application:

### Option 1: Automated Deployment Script

Use the provided PowerShell script to deploy both components with minimal effort:

1. Open PowerShell
2. Navigate to the project root directory
3. Run the deployment script:
   ```
   .\deploy.ps1
   ```

4. Follow the prompts to complete the deployment

**Note**: The script now checks for required tools and will provide helpful error messages if any prerequisites are missing.

The script will:
- Deploy the backend to Heroku
- Update the frontend configuration to use the deployed backend URL
- Build and deploy the frontend to Netlify or Vercel (based on configuration)

### Option 2: Manual Deployment

Follow the steps in the `COMBINED_DEPLOYMENT_GUIDE.md` file for detailed instructions on manually deploying each component.

### Option 3: Railway Deployment

Deploy both frontend and backend on Railway using a single platform:

1. Create a Railway account at [railway.app](https://railway.app)
2. Follow the steps in the `RAILWAY_DEPLOYMENT.md` file for detailed instructions

This option simplifies deployment by hosting both components on the same platform.

## Platform Configurations

### Netlify Configuration

A `netlify.toml` file has been added to the root directory that:

1. Builds the frontend from the `frontend` directory
2. Sets up API proxying to redirect API requests to your Heroku backend
3. Configures proper routing for the single-page application

This configuration allows you to deploy both frontend and backend from a single repository.

### Railway Configuration

Railway allows you to deploy both frontend and backend services from the same repository without additional configuration files. The platform automatically detects your project structure and provides:

1. Unified environment variable management
2. Automatic HTTPS and custom domain support
3. Built-in service communication

## Environment Variables

Make sure to set the following environment variables:

- Backend (Heroku or Railway):
  - `OPENAI_API_KEY`: Your OpenAI API key

- Frontend (Netlify/Vercel/Railway):
  - `VITE_API_URL`: URL of your deployed backend (set automatically by the deployment script or manually in Railway)

## Troubleshooting

If you encounter issues during deployment:

1. Check the logs of your backend app:
   - For Heroku:
     ```
     heroku logs --tail -a your-app-name
     ```
   - For Railway: View logs in the Railway dashboard

2. Verify your frontend environment variables are correctly set

3. Test the backend API directly using a tool like Postman

4. Check for CORS issues in your browser's developer console

For more detailed troubleshooting, refer to the deployment guide for your chosen platform:
- `COMBINED_DEPLOYMENT_GUIDE.md` for Heroku/Netlify/Vercel
- `RAILWAY_DEPLOYMENT.md` for Railway
- `RENDER_DEPLOYMENT.md` for Render