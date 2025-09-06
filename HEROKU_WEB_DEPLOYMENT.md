# Deploying JobLens Backend on Heroku Web Interface

This guide explains how to deploy the JobLens backend on Heroku using their web interface instead of the command line.

## Prerequisites

1. A GitHub account with your JobLens repository pushed to it
2. A Heroku account (sign up at [heroku.com](https://heroku.com) if you don't have one)
3. Your OpenAI API key

## Step 1: Prepare Your Repository

Ensure your backend code is ready for deployment:

1. Make sure you have a `Procfile` in the backend directory with the content:
   ```
   web: node server.js
   ```
   (Replace `server.js` with your actual entry point file if different)

2. Verify your `package.json` includes all necessary dependencies and has a proper start script

3. Ensure your server listens on the port provided by Heroku:
   ```javascript
   const PORT = process.env.PORT || 5000;
   app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
   ```

## Step 2: Deploy on Heroku

1. **Log in to Heroku**
   - Go to [dashboard.heroku.com](https://dashboard.heroku.com/)
   - Sign in with your Heroku account

2. **Create a New App**
   - Click the "New" button in the top right corner
   - Select "Create new app"
   - Enter a unique app name (e.g., "joblens-backend")
   - Choose your region
   - Click "Create app"

3. **Connect to GitHub**
   - In the Deploy tab, select "GitHub" as the deployment method
   - Connect your GitHub account if not already connected
   - Search for your repository and click "Connect"

4. **Configure Environment Variables**
   - Go to the Settings tab
   - Click "Reveal Config Vars"
   - Add the following variables:
     - `OPENAI_API_KEY`: Your OpenAI API key
     - Any other environment variables your backend requires

5. **Choose Deployment Method**
   - Return to the Deploy tab
   - Choose either:
     - **Manual Deploy**: Select a branch and click "Deploy Branch"
     - **Automatic Deploys**: Enable automatic deploys from a specific branch

6. **Monitor Deployment**
   - Watch the build logs for any errors
   - Once complete, click "View" to see your deployed backend

## Step 3: Configure CORS

Ensure your backend has CORS configured to allow requests from your frontend domain:

```javascript
const cors = require('cors');

// For development, allowing all origins
app.use(cors());

// For production, specify allowed origins
app.use(cors({
  origin: ['https://your-frontend-domain.netlify.app', 'http://localhost:3000']
}));
```

Replace `https://your-frontend-domain.netlify.app` with your actual frontend URL.

## Step 4: Connect Frontend to Backend

Update your frontend environment variables to point to your new Heroku backend URL:

1. In Netlify, go to Site settings > Build & deploy > Environment
2. Add or update the `VITE_API_URL` variable with your Heroku app URL (e.g., `https://joblens-backend.herokuapp.com`)

## Troubleshooting

### Build Failures

- Check the build logs for specific error messages
- Ensure all dependencies are correctly listed in `package.json`
- Verify that the Procfile is correctly configured

### Application Errors

- Check the Heroku logs by clicking "More" > "View logs" in your app dashboard
- Ensure all environment variables are correctly set
- Verify your database connection strings if using a database

### API Connection Issues

- Confirm CORS is properly configured on your backend
- Check that your frontend is using the correct backend URL

## Scaling Your App

By default, Heroku deploys your app to a single web dyno. To scale:

1. Go to the Resources tab in your Heroku dashboard
2. Adjust the number of dynos as needed

Note: Free tier Heroku apps will sleep after 30 minutes of inactivity. For production use, consider upgrading to a paid plan.

## Continuous Deployment

If you enabled automatic deploys, Heroku will automatically rebuild and redeploy your app when you push changes to the connected branch.

To view deployment history:
1. Go to the Activity tab in your Heroku dashboard
2. Review recent build and release activities