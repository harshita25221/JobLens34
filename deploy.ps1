# JobLens Deployment Script for Windows PowerShell

# Configuration
$BACKEND_APP_NAME = "joblens-backend" # Change this to your Heroku app name
$FRONTEND_DEPLOYMENT = "netlify" # Options: "netlify" or "vercel"

Write-Host "=== JobLens Combined Deployment Script ==="
Write-Host "This script will deploy both backend and frontend components."

# Check prerequisites
Write-Host "`nChecking prerequisites..."

# Check for Node.js and npm
$npmExists = $null -ne (Get-Command npm -ErrorAction SilentlyContinue)
if (-not $npmExists) {
    Write-Host "ERROR: npm is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Node.js and npm from https://nodejs.org/" -ForegroundColor Yellow
    Write-Host "After installation, restart your terminal and run this script again." -ForegroundColor Yellow
    exit 1
}

# Check for Heroku CLI
$herokuExists = $null -ne (Get-Command heroku -ErrorAction SilentlyContinue)
if (-not $herokuExists) {
    Write-Host "ERROR: Heroku CLI is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Heroku CLI from https://devcenter.heroku.com/articles/heroku-cli" -ForegroundColor Yellow
    Write-Host "After installation, restart your terminal and run this script again." -ForegroundColor Yellow
    exit 1
}

# Check for Netlify CLI if using Netlify
if ($FRONTEND_DEPLOYMENT -eq "netlify") {
    $netlifyExists = $null -ne (Get-Command netlify -ErrorAction SilentlyContinue)
    if (-not $netlifyExists) {
        Write-Host "ERROR: Netlify CLI is not installed or not in PATH" -ForegroundColor Red
        Write-Host "Please install Netlify CLI using: npm install -g netlify-cli" -ForegroundColor Yellow
        Write-Host "After installation, restart your terminal and run this script again." -ForegroundColor Yellow
        exit 1
    }
}

# Check for Vercel CLI if using Vercel
if ($FRONTEND_DEPLOYMENT -eq "vercel") {
    $vercelExists = $null -ne (Get-Command vercel -ErrorAction SilentlyContinue)
    if (-not $vercelExists) {
        Write-Host "ERROR: Vercel CLI is not installed or not in PATH" -ForegroundColor Red
        Write-Host "Please install Vercel CLI using: npm install -g vercel" -ForegroundColor Yellow
        Write-Host "After installation, restart your terminal and run this script again." -ForegroundColor Yellow
        exit 1
    }
}

Write-Host "All prerequisites are installed." -ForegroundColor Green

# Deploy Backend to Heroku
Write-Host "`n=== Deploying Backend to Heroku ==="
Set-Location -Path "$PSScriptRoot\backend"

# Check if logged in to Heroku
Write-Host "Checking Heroku login status..."
$herokuAuthStatus = heroku auth:whoami
if ($LASTEXITCODE -ne 0) {
    Write-Host "Not logged in to Heroku. Please login:"
    heroku login
}

# Check if app exists
$appExists = heroku apps:info $BACKEND_APP_NAME
if ($LASTEXITCODE -ne 0) {
    Write-Host "Creating Heroku app $BACKEND_APP_NAME..."
    heroku create $BACKEND_APP_NAME
} else {
    Write-Host "Using existing Heroku app $BACKEND_APP_NAME"
}

# Check for OpenAI API key
$openaiKeySet = heroku config:get OPENAI_API_KEY -a $BACKEND_APP_NAME
if ([string]::IsNullOrEmpty($openaiKeySet)) {
    $OPENAI_API_KEY = Read-Host -Prompt "Enter your OpenAI API key"
    heroku config:set OPENAI_API_KEY=$OPENAI_API_KEY -a $BACKEND_APP_NAME
}

# Deploy to Heroku
Write-Host "Deploying backend to Heroku..."

# Check if git is initialized
if (-not (Test-Path -Path ".git")) {
    git init
}

try {
    git add .
    
    # Check if there are changes to commit
    $status = git status --porcelain
    if ($status) {
        git commit -m "Backend deployment"
    } else {
        Write-Host "No changes to commit for backend" -ForegroundColor Yellow
    }
    
    git push heroku master --force
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to push to Heroku" -ForegroundColor Red
        Write-Host "Check the error messages above for details." -ForegroundColor Yellow
        Write-Host "You may need to run 'heroku login' first." -ForegroundColor Yellow
        exit 1
    }
} catch {
    Write-Host "ERROR: An error occurred during Heroku deployment" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}

# Get the backend URL
$BACKEND_URL = "https://$BACKEND_APP_NAME.herokuapp.com"
Write-Host "Backend deployed to: $BACKEND_URL"

# Update frontend environment with backend URL
Write-Host "`n=== Updating Frontend Configuration ==="
Set-Location -Path "$PSScriptRoot\frontend"

# Update .env.production with backend URL
$envContent = "VITE_API_URL=$BACKEND_URL"
Set-Content -Path ".env.production" -Value $envContent
Write-Host "Updated .env.production with backend URL"

# Deploy Frontend
Write-Host "`n=== Deploying Frontend ==="

# Install dependencies and build
Write-Host "Installing dependencies and building frontend..."
try {
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: npm install failed" -ForegroundColor Red
        Write-Host "Check the error messages above for details." -ForegroundColor Yellow
        exit 1
    }
    
    npm run build
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: npm run build failed" -ForegroundColor Red
        Write-Host "Check the error messages above for details." -ForegroundColor Yellow
        exit 1
    }
} catch {
    Write-Host "ERROR: An error occurred during frontend build" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}

# Deploy based on selected platform
if ($FRONTEND_DEPLOYMENT -eq "netlify") {
    # Check if logged in to Netlify
    Write-Host "Checking Netlify login status..."
    try {
        $netlifyStatus = netlify status
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Not logged in to Netlify. Please login:" -ForegroundColor Yellow
            netlify login
            if ($LASTEXITCODE -ne 0) {
                Write-Host "ERROR: Failed to login to Netlify" -ForegroundColor Red
                Write-Host "Please try logging in manually with 'netlify login' and run this script again." -ForegroundColor Yellow
                exit 1
            }
        }
        
        Write-Host "Deploying to Netlify..."
        netlify deploy --prod
        if ($LASTEXITCODE -ne 0) {
            Write-Host "ERROR: Failed to deploy to Netlify" -ForegroundColor Red
            Write-Host "Check the error messages above for details." -ForegroundColor Yellow
            exit 1
        }
    } catch {
        Write-Host "ERROR: An error occurred during Netlify deployment" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
        exit 1
    }
} elseif ($FRONTEND_DEPLOYMENT -eq "vercel") {
    # Check if logged in to Vercel
    Write-Host "Checking Vercel login status..."
    try {
        $vercelStatus = vercel whoami
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Not logged in to Vercel. Please login:" -ForegroundColor Yellow
            vercel login
            if ($LASTEXITCODE -ne 0) {
                Write-Host "ERROR: Failed to login to Vercel" -ForegroundColor Red
                Write-Host "Please try logging in manually with 'vercel login' and run this script again." -ForegroundColor Yellow
                exit 1
            }
        }
        
        Write-Host "Deploying to Vercel..."
        vercel --prod
        if ($LASTEXITCODE -ne 0) {
            Write-Host "ERROR: Failed to deploy to Vercel" -ForegroundColor Red
            Write-Host "Check the error messages above for details." -ForegroundColor Yellow
            exit 1
        }
    } catch {
        Write-Host "ERROR: An error occurred during Vercel deployment" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
        exit 1
    }
}

Write-Host "`n=== Deployment Complete ==="
Write-Host "Backend URL: $BACKEND_URL"
Write-Host "Frontend has been deployed to $FRONTEND_DEPLOYMENT"
Write-Host "Check the deployment logs above for the frontend URL"