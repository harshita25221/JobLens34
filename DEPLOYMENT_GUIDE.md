# JobLens Deployment Guide

This guide provides instructions for deploying both the frontend and backend components of the JobLens application.

## Backend Deployment (Python Flask)

### Option 1: Heroku Deployment

1. **Create a Heroku account** if you don't have one at [heroku.com](https://heroku.com)

2. **Install the Heroku CLI** from [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)

3. **Login to Heroku**
   ```
   heroku login
   ```

4. **Navigate to the backend directory**
   ```
   cd backend
   ```

5. **Create a Heroku app**
   ```
   heroku create joblens-backend
   ```

6. **Set up environment variables**
   ```
   heroku config:set OPENAI_API_KEY=your_openai_api_key
   ```

7. **Deploy the backend**
   ```
   git init
   git add .
   git commit -m "Initial backend deployment"
   git push heroku master
   ```

8. **Verify the deployment**
   ```
   heroku open
   ```

### Option 2: Railway Deployment

1. **Create a Railway account** at [railway.app](https://railway.app)

2. **Install the Railway CLI**
   ```
   npm i -g @railway/cli
   ```

3. **Login to Railway**
   ```
   railway login
   ```

4. **Navigate to the backend directory**
   ```
   cd backend
   ```

5. **Create a new Railway project**
   ```
   railway init
   ```

6. **Set up environment variables**
   ```
   railway variables set OPENAI_API_KEY=your_openai_api_key
   ```

7. **Deploy the backend**
   ```
   railway up
   ```

## Frontend Deployment (React/Vite)

### Option 1: Netlify Deployment

1. **Create a Netlify account** if you don't have one at [netlify.com](https://netlify.com)

2. **Install the Netlify CLI**
   ```
   npm install -g netlify-cli
   ```

3. **Login to Netlify**
   ```
   netlify login
   ```

4. **Navigate to the frontend directory**
   ```
   cd frontend
   ```

5. **Build the frontend**
   ```
   npm install
   npm run build
   ```

6. **Deploy to Netlify**
   ```
   netlify deploy --prod
   ```

### Option 2: Vercel Deployment

1. **Create a Vercel account** if you don't have one at [vercel.com](https://vercel.com)

2. **Install the Vercel CLI**
   ```
   npm install -g vercel
   ```

3. **Login to Vercel**
   ```
   vercel login
   ```

4. **Navigate to the frontend directory**
   ```
   cd frontend
   ```

5. **Deploy to Vercel**
   ```
   vercel --prod
   ```

## Connecting Frontend to Backend

After deploying both the frontend and backend, you need to update the frontend environment variables to point to your deployed backend URL:

1. **For Netlify**: Go to Site settings > Build & deploy > Environment variables and add:
   ```
   VITE_API_URL=https://your-backend-url.herokuapp.com
   ```

2. **For Vercel**: Go to Project settings > Environment Variables and add:
   ```
   VITE_API_URL=https://your-backend-url.herokuapp.com
   ```

## Troubleshooting

- **Backend not responding**: Check Heroku/Railway logs for errors
- **CORS issues**: Ensure the backend CORS settings include your frontend domain
- **Environment variables**: Verify all required environment variables are set correctly

## Maintenance

To update your deployed applications after making changes:

1. **Backend (Heroku)**:
   ```
   git add .
   git commit -m "Update message"
   git push heroku master
   ```

2. **Frontend (Netlify/Vercel)**:
   ```
   npm run build
   netlify deploy --prod
   # or
   vercel --prod
   ```