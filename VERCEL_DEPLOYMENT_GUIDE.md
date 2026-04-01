# ExplainGrade — Vercel Deployment & Local Testing Guide

## 📋 Project Structure Overview

Your project has:

- ✅ **Frontend:** Browser-based grading system (index.html, app.js, scorer.js)
- ✅ **Optional Python Backend:** Local grading with sentence-transformers (local_grader.py)
- ✅ **Chat Feature:** Assistant chat interface
- ⚠️ **Vercel:** Static site hosting (free tier doesn't support Python)

---

## 🖥️ PART 1: TEST LOCALLY (How Vercel Will See It)

### Option A: Simple HTTP Server (Recommended for Testing)

#### Using Python's Built-in Server

```bash
# Change to project directory
cd c:\Users\deii\Desktop\cloud

# Start local web server
python -m http.server 8000
```

Then open: **http://localhost:8000**

#### Using Node.js Simple Server

```bash
# Install global serve utility
npm install -g serve

# Serve the project
serve .
```

Then open: **http://localhost:3000**

#### Using VS Code Live Server Extension

1. Install "Live Server" extension
2. Right-click `index.html` → "Open with Live Server"
3. Automatically opens in browser

---

### Option B: Simulate Vercel Environment Locally

Create a simple Node.js server that mimics Vercel's behavior:

#### 1. Create `server.js` in your root directory

```javascript
const http = require("http");
const fs = require("fs");
const path = require("path");

const PORT = process.env.PORT || 3000;

const server = http.createServer((req, res) => {
  let filePath = "." + req.url;
  if (filePath === "./") filePath = "./index.html";

  // Add .html extension if missing (simulates Vercel cleanUrls)
  if (!path.extname(filePath)) {
    filePath += ".html";
  }

  const extname = String(path.extname(filePath)).toLowerCase();
  const mimeTypes = {
    ".html": "text/html",
    ".js": "text/javascript",
    ".css": "text/css",
    ".json": "application/json",
    ".png": "image/png",
    ".jpg": "image/jpg",
    ".gif": "image/gif",
    ".svg": "image/svg+xml",
    ".wav": "audio/wav",
    ".mp4": "video/mp4",
    ".woff": "application/font-woff",
    ".ttf": "application/font-ttf",
    ".eot": "application/vnd.ms-fontobject",
    ".otf": "application/font-otf",
    ".wasm": "application/wasm",
  };

  const contentType = mimeTypes[extname] || "application/octet-stream";

  fs.readFile(filePath, (error, content) => {
    if (error) {
      if (error.code === "ENOENT") {
        res.writeHead(404, { "Content-Type": "text/html" });
        res.end("404 - File Not Found");
      } else {
        res.writeHead(500);
        res.end(
          "Sorry, check with the site admin for error: " +
            error.code +
            " ...\n",
        );
      }
    } else {
      res.writeHead(200, { "Content-Type": contentType });
      res.end(content, "utf-8");
    }
  });
});

server.listen(PORT, () => {
  console.log(`🚀 Server running at http://localhost:${PORT}`);
  console.log(`📁 Serving files from: ${process.cwd()}`);
});
```

#### 2. Update `package.json` to include start script

```json
{
  "name": "explaingrade",
  "version": "1.0.0",
  "description": "Explainable Short Answer Grading System",
  "scripts": {
    "start": "node server.js",
    "dev": "node server.js"
  },
  "dependencies": {
    "mammoth": "^1.11.0",
    "xlsx": "^0.18.5"
  }
}
```

#### 3. Install dependencies and run

```bash
npm install
npm start
```

Then open: **http://localhost:3000**

---

### Testing Checklist

When running locally, verify:

- [ ] **Home page loads** → http://localhost:3000
- [ ] **CSS loads correctly** → Check styling (dark/light theme work)
- [ ] **Navigation works** → All links navigate properly
- [ ] **File uploads work** → Try CSV/XLSX/DOCX uploads
- [ ] **Live demo works** → Paste text and click "Compute Score"
- [ ] **Batch upload works** → Upload sample CSV
- [ ] **Chat feature works** → Ask questions about scores
- [ ] **Theme toggle works** → Switch between dark/light
- [ ] **All pages accessible**:
  - index.html
  - pipeline.html
  - research.html
  - usage.html
  - chat.html

---

## 🚀 PART 2: DEPLOY TO VERCEL

### Option 1: Deploy via Vercel Web Interface (Easiest)

#### Step 1: Push Code to GitHub

```bash
cd c:\Users\deii\Desktop\cloud

# Initialize git if not already done
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Vercel deployment ready"

# Add remote (replace with your GitHub repo)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push to GitHub
git branch -M main
git push -u origin main
```

#### Step 2: Deploy on Vercel Dashboard

1. Go to [vercel.com](https://vercel.com)
2. Sign up/Login with GitHub
3. Click "Add New..." → "Project"
4. Select your repository
5. **Framework Preset:** Select "Other"
6. **Root Directory:** Leave as "."
7. **Build Command:** Leave empty (static files only)
8. **Output Directory:** Leave empty
9. Click "Deploy"

✅ Done! Your site is live on `your-project.vercel.app`

---

### Option 2: Deploy via Vercel CLI

#### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

#### Step 2: Deploy

```bash
cd c:\Users\deii\Desktop\cloud
vercel
```

Follow the prompts:

- Link to existing project? **No** (first deployment)
- Project name? `explaingrade` (or custom)
- Directory? `.` (current)

#### Step 3: Follow the link provided

That's it! ✅

---

### Option 3: GitHub Actions Auto-Deployment

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Vercel

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Deploy to Vercel
        uses: BetaHuhn/deploy-to-vercel-action@v1
        with:
          VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
          VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
          VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}
```

Then set GitHub secrets from Vercel dashboard.

---

## 🔧 COMMON VERCEL DEPLOYMENT ISSUES & FIXES

### Issue 1: "Cannot find module" errors

**Cause:** Missing dependencies in package.json

**Fix:** Ensure package.json has all dependencies with versions

```json
{
  "dependencies": {
    "mammoth": "^1.11.0",
    "xlsx": "^0.18.5"
  }
}
```

### Issue 2: CSS/JS not loading (404 errors)

**Cause:** Incorrect file paths (relative vs absolute)

**Fix:** Use relative paths in HTML

```html
<!-- ❌ Wrong -->
<script src="/app.js"></script>

<!-- ✅ Correct -->
<script src="./app.js"></script>
```

### Issue 3: File uploads failing

**Cause:** Browser security restrictions with local files

**Fix:** This is normal for Vercel. Browser-based uploads work fine.

### Issue 4: Python scripts failing

**Cause:** Vercel free tier doesn't support Python

**Solution:**

- **Option A:** Use browser-only version (no Python backend needed)
- **Option B:** Use Node.js API routes if you need backend processing
- **Option C:** Deploy Python backend separately on Heroku/Railway

---

## 📦 CURRENT vercel.json ANALYSIS

Your current configuration:

```json
{
  "cleanUrls": true,
  "trailingSlash": false,
  "rewrites": [{ "source": "/(.*)", "destination": "/$1.html" }]
}
```

**What it does:**

- Removes `.html` from URLs
- Removes trailing slashes
- Rewrites all routes to try loading `.html` files

**This is correct for static HTML deployment!** ✅

---

## ✅ FINAL DEPLOYMENT CHECKLIST

Before deploying to Vercel:

- [ ] All files committed to Git
- [ ] `package.json` has correct dependencies
- [ ] No absolute paths in HTML/JS (use relative paths)
- [ ] All images/assets are included in repo
- [ ] No Python runtime dependencies in frontend code
- [ ] Local testing passes all checks (see above)
- [ ] `vercel.json` is in root directory
- [ ] GitHub repo is public (or Vercel has access)

---

## 🚭 TO DEBUG DEPLOYMENT ISSUES

### View Vercel Build Logs

1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Select your project
3. Click "Deployments"
4. Click the failed deployment
5. Click "Build Logs" to see errors

### Run Local Build Simulation

```bash
# Install Vercel CLI
npm install -g vercel

# Build locally
vercel --prod --force
```

---

## 📝 NEXT STEPS

1. **Test locally** using Option A or B above
2. **Fix any issues** found in local testing
3. **Push to GitHub** (if not already done)
4. **Deploy to Vercel** using Option 1, 2, or 3
5. **Verify live site** works at your-project.vercel.app

---

**Need Help?**

- Vercel Docs: https://vercel.com/docs
- GitHub Pages Alternative: https://pages.github.com (simpler but less features)
- Your Git Logs: Check `.git` directory for commit history
