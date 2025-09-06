# JobLens Web Deployment Guide

This guide provides instructions for deploying the JobLens application using web interfaces instead of command-line tools. This approach is ideal for users who prefer graphical interfaces or don't have the necessary CLI tools installed.

## Overview

JobLens consists of two main components that need to be deployed separately:

1. **Backend**: Node.js API server deployed on Heroku or Railway
2. **Frontend**: React application deployed on Netlify or Railway

## Deployment Process

For detailed step-by-step instructions, please refer to the following guides:

1. [Backend Deployment on Heroku](./HEROKU_WEB_DEPLOYMENT.md)
2. [Frontend Deployment on Netlify](./NETLIFY_WEB_DEPLOYMENT.md)
3. [Combined Deployment on Railway](./RAILWAY_DEPLOYMENT.md)

## Deployment Order

### For Heroku and Netlify

For the best experience, deploy in this order:

1. Deploy the backend first on Heroku
2. Note the URL of your deployed backend (e.g., `https://joblens-backend.herokuapp.com`)
3. Deploy the frontend on Netlify, using the backend URL in your environment variables

### For Railway

Railway allows you to deploy both frontend and backend in a single platform:

1. Deploy the backend service first
2. Note the URL of your deployed backend
3. Deploy the frontend service, using the backend URL in your environment variables

## Environment Variables

### Backend (Heroku or Railway)

Required environment variables:
- `OPENAI_API_KEY`: Your OpenAI API key

Optional environment variables:
- `PORT`: Automatically set by Heroku/Railway, but defaults to 5000 locally
- Any database connection strings if applicable

### Frontend (Netlify or Railway)

Required environment variables:
- `VITE_API_URL`: URL of your deployed backend

## Testing Your Deployment

After deploying both components:

1. Visit your Netlify URL (e.g., `https://joblens.netlify.app`)
2. Test the application's functionality
3. Check browser console for any API connection errors
4. Verify that API requests are being correctly proxied to your backend

## Troubleshooting

If you encounter issues:

1. Check the deployment logs on your chosen platforms (Heroku, Netlify, or Railway)
2. Verify that all environment variables are correctly set
3. Ensure CORS is properly configured on your backend
4. Confirm that API proxy configurations are correct

For more specific troubleshooting steps, refer to the individual deployment guides.

## Updating Your Deployment

Heroku, Netlify, and Railway all support continuous deployment from GitHub:

1. Push changes to your connected GitHub repository
2. The platforms will automatically rebuild and redeploy your application
3. Monitor the deployment logs for any errors

## Security Considerations

1. Never commit API keys or sensitive environment variables to your repository
2. Use environment variables for all sensitive information
3. Consider implementing rate limiting on your backend API
4. Regularly rotate your API keys for better security

## Additional Resources

- [Heroku Documentation](https://devcenter.heroku.com/)
- [Netlify Documentation](https://docs.netlify.com/)
- [Railway Documentation](https://docs.railway.app/)
- [Setting up Continuous Deployment](https://docs.netlify.com/site-deploys/create-deploys/)