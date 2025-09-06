# JobLens Render Deployment Guide

This guide provides instructions for deploying both the frontend and backend components of JobLens on Render.

## Prerequisites

1. Create a Render account at [render.com](https://render.com)
2. Fork or clone the JobLens repository
3. Have your OpenAI API key ready

## Backend Deployment

1. **Create a New Web Service**
   - Log in to your Render dashboard
   - Click "New +" and select "Web Service"
   - Connect your GitHub repository
   - Select the repository and the branch you want to deploy

2. **Configure the Service**
   - Name: `joblens-backend` (or your preferred name)
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
   - Select the appropriate region

3. **Set Environment Variables**
   - Click on "Environment" tab
   - Add the following variables:
     - `OPENAI_API_KEY`: Your OpenAI API key

4. **Deploy the Service**
   - Click "Create Web Service"
   - Wait for the deployment to complete
   - Note down the service URL (e.g., `https://joblens-backend.onrender.com`)

## Frontend Deployment

1. **Create a Static Site**
   - In your Render dashboard, click "New +"
   - Select "Static Site"
   - Connect your GitHub repository if not already connected
   - Select the repository

2. **Configure the Static Site**
   - Name: `joblens-frontend` (or your preferred name)
   - Build Command: `npm install && npm run build`
   - Publish Directory: `dist`

3. **Set Environment Variables**
   - Add the following environment variable:
     - `VITE_API_URL`: Your backend service URL from step 4 of backend deployment

4. **Deploy the Site**
   - Click "Create Static Site"
   - Wait for the deployment to complete

## Configuration

This project uses a `render.yaml` file for deployment configuration. The file defines both the frontend and backend services:

```yaml
services:
  - type: web
    name: joblens-backend
    env: python
    plan: standard
    buildCommand: ./backend/build.sh
    startCommand: cd backend && gunicorn app:app --workers=1 --threads=2 --timeout=120
    envVars:
      - key: WEB_CONCURRENCY
        value: 1
      - key: MALLOC_ARENA_MAX
        value: 2
      - key: PYTHONHASHSEED
        value: random
      - key: PYTHON_VERSION
        value: 3.10.0
      - key: OPENAI_API_KEY
        sync: false

  - type: web
    name: joblens-frontend
    env: static
    buildCommand: cd frontend && npm install && npm run build
    staticPublishPath: ./frontend/dist
    envVars:
      - key: VITE_API_URL
        value: https://joblens-backend.onrender.com
```

The backend service uses a build script (`build.sh`) to set up the Python environment and dependencies:

```bash
#!/bin/bash
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Set memory optimization environment variables
export MALLOC_ARENA_MAX=2
export PYTHONHASHSEED=random

# Create .profile.d directory for Render environment variables persistence
mkdir -p .profile.d
echo 'export MALLOC_ARENA_MAX=2' > .profile.d/memory_optimization.sh
echo 'export PYTHONHASHSEED=random' >> .profile.d/memory_optimization.sh
chmod +x .profile.d/memory_optimization.sh
```

This script ensures all required dependencies are installed, including the spaCy language model needed for text processing. It also sets memory optimization environment variables to help prevent "Out of memory" errors.

## Verify Deployment

1. Visit your frontend URL to ensure the site loads correctly
2. Test the application functionality:
   - Upload a resume and job description
   - Verify that the analysis works
   - Check for any console errors

## Troubleshooting

### Backend Issues

- Check the deployment logs in your Render dashboard
- Verify environment variables are set correctly
- Ensure all dependencies are listed in `requirements.txt`
- **Issue**: "Out of memory" errors
  - **Solution**: The application has been configured to use the Standard plan with optimized Gunicorn settings (--workers=1 --threads=2) to reduce memory usage. If you still encounter memory issues, consider:
    - Upgrading to a higher plan with more resources
    - Further optimizing memory-intensive operations in the code
    - Adding memory monitoring to identify specific bottlenecks

### Frontend Issues

- Check browser console for errors
- Verify the `VITE_API_URL` is correct
- Ensure the build process completes successfully

## Maintenance

### Updating the Application

1. Push changes to your GitHub repository
2. Render will automatically rebuild and deploy the changes

### Monitoring

- Use Render's dashboard to monitor service health
- Check service logs for any errors
- Monitor resource usage and adjust as needed

## Security Best Practices

1. Keep your OpenAI API key secure and rotate it periodically
2. Use environment variables for all sensitive information
3. Enable HTTPS for all communications
4. Regularly update dependencies to patch security vulnerabilities

## Additional Resources

- [Render Documentation](https://render.com/docs)
- [Python on Render](https://render.com/docs/deploy-python)
- [Static Sites on Render](https://render.com/docs/static-sites)