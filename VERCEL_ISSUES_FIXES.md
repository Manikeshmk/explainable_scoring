# ExplainGrade — Issues Found & How to Fix Them for Vercel

## ✅ What's Working Well

Your project has **good structure** for Vercel deployment:

- ✅ HTML files use relative paths for CSS/JS (e.g., `href="style.css"`)
- ✅ External libraries use CDN links (won't have missing module issues)
- ✅ Proper `vercel.json` configuration for static site routing
- ✅ `package.json` has dependencies listed

---

## 🔴 Potential Issues & Fixes

### Issue 1: Missing NPM Dependencies on Vercel

**Symptom:** Mammoth/XLSX says "not found" on Vercel (but works locally)

**Root Cause:** npm install might not run during Vercel build

**Fix:**

```bash
# Local testing
npm install

# Ensure package.json has these (MUST have exact versions):
{
  "dependencies": {
    "mammoth": "^1.11.0",
    "xlsx": "^0.18.5"
  }
}

# Git commit and push
git add package.json package-lock.json
git commit -m "Update dependencies for Vercel"
git push origin main
```

---

### Issue 2: Script Not Loading on Vercel (But Works Locally)

**Symptom:**

- Local: Works fine
- Vercel: "scorer.js not found" or blank page

**Root Cause:** Case sensitivity or wrong paths

**Check & Fix:**

```bash
# 1. Verify all files exist (case-sensitive)
ls -la scorer.js      # Should show the file (Linux/Mac)
dir scorer.js         # Should show the file (Windows PowerShell)

# 2. Check HTML has correct paths
# In index.html:
<script src="scorer.js"></script>     ✅ Works on Vercel
<script src="./scorer.js"></script>   ✅ Also works
<script src="/scorer.js"></script>    ⚠️ Might fail on Vercel

# 3. Windows users: Check filename case
# ❌ scorer.JS or Scorer.js       (Fails on Vercel)
# ✅ scorer.js or SCORER.js       (Works everywhere)
```

---

### Issue 3: CSS Not Loading (Styling Broken on Vercel)

**Symptom:**

- Local: Beautiful styling with dark/light theme
- Vercel: No CSS, looks like plain HTML

**Root Cause:** `style.css` path error

**Fix:**

In every HTML file, verify:

```html
<!-- ✅ Correct for root-level style.css -->
<link rel="stylesheet" href="style.css" />

<!-- Also works but not necessary -->
<link rel="stylesheet" href="./style.css" />

<!-- ❌ WRONG - Don't use this -->
<link rel="stylesheet" href="/style.css" />
```

---

### Issue 4: CDN Libraries Failing

**Symptom:** "PapaParse is not defined" or similar on Vercel

**Root Cause:** CDN not loading before scripts run

**Check in index.html (Line ~241-246):**

```html
<!-- These should be BEFORE app.js, scorer.js, chat.js -->
<script src="https://cdn.jsdelivr.net/npm/papaparse@5.4.1/papaparse.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/mammoth@1.8.0/mammoth.browser.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>

<!-- These should be AFTER the CDN libraries -->
<script src="scorer.js"></script>
<script src="chat.js"></script>
<script src="app.js"></script>
```

**Fix if needed:**

1. Make sure CDN scripts come **before** your local scripts
2. Check browser console (F12) for "is not defined" errors

---

### Issue 5: Fonts Not Loading

**Symptom:** Using default font instead of "Inter"

**Root Cause:** Google Fonts CDN issue

**Current setup (looks good):**

```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link
  href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap"
  rel="stylesheet"
/>
```

This should work fine on Vercel. If not loading:

1. Check browser Network tab (F12) for failed requests
2. Hard refresh (Ctrl+Shift+R)
3. Check CSS uses `font-family: 'Inter', sans-serif;`

---

### Issue 6: Images/Assets Not Loading

**Symptom:** Some images show broken icon

**Root Cause:** Case sensitivity or wrong relative path

**Debug:**

1. Open DevTools (F12) → Network tab
2. Reload page
3. Look for red `404` errors
4. Check the filename case matches exactly

**Common fixes:**

```html
<!-- ❌ WRONG -->
<img src="/images/logo.PNG" />
<!-- Case mismatch -->
<img src="images/logo.png" />
<!-- Works if in images/ -->

<!-- ✅ CORRECT for assets in root -->
<img src="./images/logo.png" />

<!-- ✅ CORRECT for assets in same directory -->
<img src="logo.png" />
```

---

### Issue 7: File Upload Not Working on Vercel

**Symptom:** Upload buttons don't work

**This is NORMAL** - Browser security. File uploads are local client-side operations and should work. If not:

1. Check browser console for errors
2. Verify file input element has correct attributes:
   ```html
   <input type="file" id="some-id" accept=".csv,.xlsx,.docx" />
   ```
3. Check `app.js` handles file input events

---

### Issue 8: Theme Toggle Not Working

**Symptom:** Dark/light theme button doesn't do anything

**Root Cause:** Check `app.js` is loading properly

**Debug:**

1. Open console (F12)
2. Type: `typeof Papa !== "undefined"` (should be true)
3. Type: `document.getElementById("theme-toggle")` (should show element)

If failing:

- Check `app.js` loaded (Network tab in DevTools)
- Check for console errors
- Verify script tag in HTML

---

### Issue 9: Chat Feature Not Working

**Symptom:** Chat assistant displays but can't ask questions

**Root Cause:** `chat.js` not loading or CSV data issue

**Fix:**

1. Verify `chat.js` in root directory
2. Check it loads: Open DevTools → Network → look for chat.js
3. Check HTML loads chat.js: `<script src="chat.js"></script>`
4. Look for console errors (F12)

---

## 🧪 Pre-Deployment Checklist

### File & Path Check

```bash
# Verify all key files exist in root:
ls -la index.html     # Main page
ls -la app.js        # UI controller
ls -la scorer.js     # Scoring engine
ls -la chat.js       # Chat assistant
ls -la style.css     # Styles
```

### HTML Validation

```bash
# Check HTML is valid
# Go to: https://validator.w3.org
# Upload your index.html
# Look for errors/warnings
```

### Verify Local Works

```bash
# Test on localhost first
npm install
npm start

# Open browser to http://localhost:3000

# Checklist:
[ ] Page loads without errors
[ ] CSS is styled correctly
[ ] Dark/light toggle works
[ ] All navigation links work
[ ] File uploads accept files
[ ] No console errors (F12)
[ ] All pages accessible
```

### Git Commit Everything

```bash
# Make sure everything is committed
git status                    # Should show no changes
git log --oneline -5         # Should show your commits

# If you changed files:
git add .
git commit -m "Description of changes"
git push origin main
```

---

## 🚀 Step-by-Step Deployment

### Step 1: Test Locally

```bash
npm install
npm start
# Test at http://localhost:3000
# Verify everything works
```

### Step 2: Commit to GitHub

```bash
git add .
git commit -m "Ready for Vercel deployment"
git push origin main
```

### Step 3: Deploy to Vercel

```bash
# Option A: Via Vercel Dashboard
# Go to: https://vercel.com/dashboard
# Click: Add New → Project
# Select: Your GitHub Repo
# Click: Deploy

# Option B: Via Vercel CLI
npm install -g vercel
vercel --prod
```

### Step 4: View Build Logs

```bash
# If deployment failed:
# 1. Go to: https://vercel.com/dashboard
# 2. Click your project
# 3. Click "Deployments" tab
# 4. Click failed deployment
# 5. Scroll to "Build Logs"
# 6. Look for error messages
```

### Step 5: Debug if Needed

```bash
# Force clear cache and rebuild
vercel --prod --force
```

---

## 📋 Common Error Messages & Solutions

| Error                    | Cause                            | Solution                           |
| ------------------------ | -------------------------------- | ---------------------------------- |
| Cannot GET /             | index.html missing               | Ensure `index.html` in root        |
| 404 style.css            | Path error                       | Check `href="style.css"` in HTML   |
| PapaParse is not defined | Library loading order            | CDN scripts before local scripts   |
| Module not found         | Missing npm dependency           | Check `package.json` has it        |
| Port already in use      | Another app on port 3000         | Kill process or use different port |
| Case mismatch error      | Windows ↔ Vercel case difference | Use lowercase filenames            |

---

## 🆘 Getting Help

### Share These Details:

1. Screenshot of Vercel build logs
2. Your GitHub repo URL
3. Screenshot of browser console errors (F12)
4. What works locally vs what fails on Vercel

### Useful Commands for Debugging:

```bash
# View recent commits
git log --oneline -10

# Check unstaged changes
git status

# See what will be deployed
git ls-files

# Check file size (Vercel has 100MB limit for free)
du -sh .

# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

---

## ✨ You're Ready!

Your project is well-structured. Following this guide should get it deployed to Vercel without issues.

**Good luck! 🚀**
