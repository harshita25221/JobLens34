# JobLens Deployment Prerequisites

Before running the deployment script, please ensure you have the following tools installed and configured on your system:

## Required Tools

### 1. Node.js and npm

**Installation:**
1. Download and install Node.js from [nodejs.org](https://nodejs.org/)
2. Verify installation by running:
   ```
   node --version
   npm --version
   ```

### 2. Heroku CLI

**Installation:**
1. Download and install the Heroku CLI from [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
2. Verify installation by running:
   ```
   heroku --version
   ```
3. Login to your Heroku account:
   ```
   heroku login
   ```

### 3. Netlify CLI

**Installation:**
1. Install the Netlify CLI using npm:
   ```
   npm install -g netlify-cli
   ```
2. Verify installation by running:
   ```
   netlify --version
   ```
3. Login to your Netlify account:
   ```
   netlify login
   ```

### 4. Git

**Installation:**
1. Download and install Git from [git-scm.com](https://git-scm.com/downloads)
2. Verify installation by running:
   ```
   git --version
   ```

## Environment Setup

### OpenAI API Key

You'll need an OpenAI API key for the backend functionality:

1. Create an account at [platform.openai.com](https://platform.openai.com/)
2. Generate an API key from your account dashboard
3. Keep this key secure - do not commit it to version control

## Running the Deployment Script

After installing all prerequisites:

1. Open PowerShell
2. Navigate to the project root directory
3. Run the deployment script:
   ```
   .\deploy.ps1
   ```

## Manual Installation Alternative

If you prefer to manually deploy without using the script, follow the detailed instructions in the `COMBINED_DEPLOYMENT_GUIDE.md` file.

## Troubleshooting

### Common Issues

1. **Command not found errors**:
   - Ensure all tools are properly installed
   - Check that installation directories are added to your system PATH
   - Try restarting your terminal/PowerShell after installation

2. **Authentication issues**:
   - Make sure you're logged in to Heroku and Netlify before deployment
   - Check that your API keys and credentials are valid

3. **Build failures**:
   - Ensure all dependencies are installed (`npm install` in the frontend directory)
   - Check for any syntax errors in your code