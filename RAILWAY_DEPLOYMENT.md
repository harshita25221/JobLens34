# Deploying JobLens on Railway

This guide explains how to deploy the JobLens application on Railway, an alternative platform to Netlify and Heroku.

## What is Railway?

Railway is a modern deployment platform that allows you to deploy both frontend and backend applications. Unlike the separate deployment approach with Netlify and Heroku, Railway can host your entire stack in one place.

## Prerequisites

1. A GitHub account with your JobLens repository pushed to it
2. A Railway account (sign up at [railway.app](https://railway.app) if you don't have one)
3. Your OpenAI API key

## Benefits of Using Railway

- **Unified Deployment**: Deploy both frontend and backend in one platform
- **Automatic HTTPS**: SSL certificates are automatically provisioned
- **Environment Variables**: Easy management across services
- **GitHub Integration**: Automatic deployments from your repository
- **Free Tier**: Includes 500 hours of usage per month

## Step 1: Prepare Your Repository

Ensure your repository is structured properly:

1. Backend directory with proper `package.json` and entry point
2. Frontend directory with build configuration

## Step 2: Deploy on Railway

### Backend Deployment

1. **Log in to Railway**
   - Go to [railway.app](https://railway.app)
   - Sign in with your GitHub account

2. **Create a New Project**
   - Click "New Project" 
   - Select "Deploy from GitHub repo"
   - Choose your JobLens repository

3. **Configure Backend Service**
   - Select "Deploy specific directory"
   - Enter the path to your backend directory (e.g., `backend`)
   - Set the build command: `npm install`
   - Set the start command: `node server.js` (or your entry point)

4. **Add Environment Variables**
   - Go to the "Variables" tab
   - Add `OPENAI_API_KEY` with your OpenAI API key
   - Add any other required environment variables

5. **Deploy the Backend**
   - Railway will automatically build and deploy your backend
   - Note the generated URL (e.g., `https://joblens-backend-production.up.railway.app`)

### Frontend Deployment

1. **Add a New Service to Your Project**
   - In your Railway project, click "New Service"
   - Select "Deploy from GitHub repo"
   - Choose the same repository

2. **Configure Frontend Service**
   - Select "Deploy specific directory"
   - Enter the path to your frontend directory (e.g., `frontend`)
   - Set the build command: `npm install && npm run build`
   - Set the start command: `npx serve -s dist` (for Vite projects)

3. **Add Environment Variables**
   - Go to the "Variables" tab
   - Add `VITE_API_URL` with your backend URL from step 5 above

4. **Deploy the Frontend**
   - Railway will automatically build and deploy your frontend
   - Note the generated URL for your frontend

## Step 3: Configure Custom Domain (Optional)

1. **Add Domain to Your Service**
   - Go to your frontend service
   - Click on the "Settings" tab
   - Scroll to "Custom Domain"
   - Click "Generate Domain" or "Add Custom Domain"
   - Follow the instructions to set up DNS records

## Step 4: Configure API Proxy (If Needed)

If you're using a custom domain and need to proxy API requests:

1. Create a `railway.json` file in your frontend directory:

```json
{
  "services": {
    "frontend": {
      "routes": [
        { "path": "/api/*", "service": "backend" },
        { "path": "/*", "static": "dist" }
      ]
    }
  }
}
```

2. This configuration will route `/api/*` requests to your backend service.

## Troubleshooting

### Build Failures

- Check the deployment logs in the Railway dashboard
- Verify your build and start commands are correct
- Ensure all dependencies are properly listed in `package.json`

### API Connection Issues

- Confirm your environment variables are correctly set
- Check CORS configuration in your backend code
- Verify the API proxy configuration if using custom domains

## Monitoring and Scaling

1. **View Logs**
   - Click on your service in the Railway dashboard
   - Go to the "Logs" tab to view real-time logs

2. **Scaling**
   - In the "Settings" tab, you can adjust resources allocated to your service
   - Upgrade your plan for additional resources if needed

## Continuous Deployment

Railway automatically sets up continuous deployment from your GitHub repository:

1. Every push to your connected branch will trigger a new deployment
2. You can configure which branches trigger deployments in the service settings

## Cost Management

Railway offers a free tier with 500 hours of usage per month. To manage costs:

1. Monitor your usage in the Railway dashboard
2. Consider pausing services when not in use
3. Set up spending limits in your account settings

## Comparing with Netlify/Heroku

| Feature | Railway | Netlify + Heroku |
|---------|---------|------------------|
| Deployment | Single platform | Two separate platforms |
| Configuration | Simpler, unified | More complex, separate configs |
| Free Tier | 500 hours/month | Limited on both platforms |
| Scaling | Built-in | Requires separate scaling on each platform |
| Custom Domains | Supported | Supported on both platforms |