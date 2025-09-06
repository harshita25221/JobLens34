# Deploying JobLens on Netlify Web Interface

This guide explains how to deploy the JobLens frontend on Netlify using their web interface instead of the command line.

## Prerequisites

1. A GitHub, GitLab, or Bitbucket account with your JobLens repository pushed to it
2. A Netlify account (sign up at [netlify.com](https://netlify.com) if you don't have one)
3. Backend already deployed to Heroku or another platform

## Step 1: Prepare Your Repository

Ensure your repository has the following files:

1. The `netlify.toml` file in the frontend directory
2. A `.env.production` file with your backend URL

## Step 2: Deploy on Netlify

1. **Log in to Netlify**
   - Go to [app.netlify.com](https://app.netlify.com/)
   - Sign in with your preferred method (GitHub, GitLab, Bitbucket, or email)

2. **Add a New Site**
   - Click the "Add new site" button
   - Select "Import an existing project"

3. **Connect to Git Provider**
   - Choose your Git provider (GitHub, GitLab, or Bitbucket)
   - Authorize Netlify to access your repositories
   - Select your JobLens repository

4. **Configure Build Settings**
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `dist`
   - Click "Show advanced" to add environment variables

5. **Add Environment Variables**
   - Add `VITE_API_URL` with the value of your backend URL (e.g., `https://joblens-backend.herokuapp.com`)

6. **Deploy the Site**
   - Click "Deploy site"
   - Netlify will start building and deploying your site

7. **Monitor Deployment**
   - Watch the deployment logs for any errors
   - Once complete, Netlify will provide a URL for your deployed site

## Step 3: Configure Custom Domain (Optional)

1. **Add Custom Domain**
   - Go to Site settings > Domain management
   - Click "Add custom domain"
   - Enter your domain name and follow the verification steps

2. **Set Up HTTPS**
   - Netlify automatically provisions SSL certificates through Let's Encrypt
   - Ensure HTTPS is enabled in the HTTPS settings

## Step 4: Configure API Proxy

The `netlify.toml` file should already contain the necessary redirects to proxy API requests to your backend. If not, add the following to your `netlify.toml` file:

```toml
[[redirects]]
  from = "/api/*"
  to = "https://your-backend-url.herokuapp.com/:splat"
  status = 200
  force = true

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

Replace `https://your-backend-url.herokuapp.com` with your actual backend URL.

## Troubleshooting

### Build Failures

- Check the build logs for specific error messages
- Ensure all dependencies are correctly listed in `package.json`
- Verify that the build command and publish directory are correct

### API Connection Issues

- Confirm your backend URL is correct in the environment variables
- Check that CORS is properly configured on your backend
- Verify the redirect rules in `netlify.toml` are correctly set up

### Deployment Updates

When you push changes to your connected repository, Netlify will automatically rebuild and redeploy your site.

## Continuous Deployment

Netlify automatically sets up continuous deployment from your Git repository. Every push to your main branch will trigger a new build and deployment.

To control this behavior:

1. Go to Site settings > Build & deploy > Continuous deployment
2. Configure branch deploy settings and build hooks as needed