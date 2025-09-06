# JobLens Combined Deployment Guide

This guide provides instructions for deploying both the frontend and backend components of the JobLens application together, ensuring they work seamlessly.

## Prerequisites

- Git installed on your machine
- Node.js and npm installed
- Heroku CLI installed
- Netlify CLI or Vercel CLI installed (depending on your frontend deployment choice)

## Step 1: Deploy the Backend (Flask API)

### Using Heroku

1. **Login to Heroku**
   ```
   heroku login
   ```

2. **Navigate to the backend directory**
   ```
   cd backend
   ```

3. **Create a Heroku app**
   ```
   heroku create joblens-backend
   ```

4. **Set up environment variables**
   ```
   heroku config:set OPENAI_API_KEY=your_openai_api_key
   ```

5. **Deploy the backend**
   ```
   git init
   git add .
   git commit -m "Initial backend deployment"
   git push heroku master
   ```

6. **Note your backend URL**
   ```
   heroku open
   ```
   This will open your backend in a browser. Note the URL (e.g., https://joblens-backend.herokuapp.com)

## Step 2: Configure Frontend to Use Deployed Backend

1. **Update the frontend environment variable**
   
   Edit the `.env.production` file in the frontend directory:
   ```
   VITE_API_URL=https://your-backend-url.herokuapp.com
   ```
   Replace `https://your-backend-url.herokuapp.com` with your actual backend URL from Step 1.

## Step 3: Deploy the Frontend

### Using Netlify

1. **Login to Netlify**
   ```
   netlify login
   ```

2. **Navigate to the frontend directory**
   ```
   cd frontend
   ```

3. **Build the frontend**
   ```
   npm install
   npm run build
   ```

4. **Deploy to Netlify**
   ```
   netlify deploy --prod
   ```

### Using Vercel (Alternative)

1. **Login to Vercel**
   ```
   vercel login
   ```

2. **Navigate to the frontend directory**
   ```
   cd frontend
   ```

3. **Deploy to Vercel**
   ```
   vercel --prod
   ```

## Step 4: Verify the Connection

1. Visit your deployed frontend application
2. Test functionality that requires the backend API
3. Check browser console for any CORS or connection errors

## Troubleshooting

### CORS Issues

If you encounter CORS errors, verify that your backend CORS settings include your frontend domain:

1. In the backend's `app.py`, CORS is configured with:
   ```python
   from flask_cors import CORS
   app = Flask(__name__)
   CORS(app)
   ```

2. For more specific CORS settings, you can modify it to:
   ```python
   CORS(app, origins=["https://your-frontend-domain.netlify.app"])
   ```

### API Connection Issues

1. Verify the `.env.production` file has the correct backend URL
2. Check that the backend is running by visiting the backend URL directly
3. Ensure all API endpoints are correctly formatted in your frontend code

## Updating Your Deployment

### Backend Updates

```
cd backend
git add .
git commit -m "Update message"
git push heroku master
```

### Frontend Updates

```
cd frontend
npm run build
netlify deploy --prod  # or vercel --prod
```

## Monorepo Deployment (Alternative Approach)

If you prefer to deploy both frontend and backend from a single repository:

1. Create a root-level `package.json` with scripts to build and deploy both parts
2. Configure a build system like GitHub Actions to deploy both components
3. Use environment variables to manage the connection between frontend and backend

This approach requires more advanced CI/CD setup but can simplify the deployment process in the long run.