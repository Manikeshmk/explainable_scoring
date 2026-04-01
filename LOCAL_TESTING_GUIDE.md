# Local Testing & Vercel Troubleshooting Guide

## 🚀 Quick Start (2 Minutes)

### Test Locally Like Vercel Will

```bash
# Method 1: Using built-in server (EASIEST)
python -m http.server 8000
# Then open: http://localhost:8000

# Method 2: Using Node.js server (RECOMMENDED)
npm install
npm start
# Then open: http://localhost:3000

# Method 3: Using npx serve
npm install -g serve
serve .
# Then open: http://localhost:3000
```

---

## 🔍 Debugging Checklist

### When local test works but Vercel fails:

**1. Check File Names Case Sensitivity**

```
❌ <script src="app.JS"></script>     (Windows works, Vercel fails)
✅ <script src="app.js"></script>     (Both work)
```

**2. Check Relative Paths**

```
❌ <script src="/app.js"></script>    (Might fail)
✅ <script src="./app.js"></script>   (Always works)
✅ <script src="app.js"></script>     (Also works)
```

**3. Check External Dependencies**

```bash
# Make sure all npm packages are in package.json
npm list
```

**4. Check Vercel Logs**

- Go to: https://vercel.com/dashboard
- Select your project → Deployments → Failed deployment
- Click "Build Logs" to see the error

**5. Clear Cache & Redeploy**

```bash
# Via Vercel CLI
vercel --prod --force --yes
```

---

## 🚨 Common Issues & Solutions

### Issue: "Cannot GET /"

**Cause:** index.html not found or wrong path

**Debug:**

```bash
# Check if index.html exists in root
ls -la index.html  # Mac/Linux
dir index.html     # Windows (PowerShell)
```

**Solution:**

- Ensure `index.html` is in the root directory
- Check filename case: must be lowercase `.html`

---

### Issue: CSS/Images not loading (404 errors in console)

**Cause:** Wrong file paths

**Check in browser console (F12):**

- Look for failed requests
- Note the path it tried to load

**Solution:**

```html
<!-- In your HTML, use relative paths ONLY -->
<link rel="stylesheet" href="./style.css" />
<script src="./app.js"></script>
<img src="./images/logo.png" />
```

---

### Issue: JavaScript files not loading

**Cause:** Missing or incorrect script tags

**Solution:**

1. Open browser console (F12)
2. Look for "Failed to load" errors
3. Verify file exists: `ls -la app.js`
4. Check script src attribute uses correct path

---

### Issue: Mammoth/XLSX not recognized

**Cause:** Missing node_modules or dependencies not installed

**Solution:**

```bash
# Install all dependencies
npm install

# Verify they are installed
npm list

# Your package.json should have:
{
  "dependencies": {
    "mammoth": "^1.11.0",
    "xlsx": "^0.18.5"
  }
}
```

---

### Issue: Upload/File Processing not working

**Cause:** Normal in browser - security restrictions

**Solution:** This is expected behavior. Browser cannot access local files directly. Only works with:

- File input elements (users select files)
- Drag & drop
- Copy-paste (for text files)

---

## 🧪 Test Before Deploying

Create a testing checklist:

```
VISUAL TESTING:
[ ] Homepage loads and displays correctly
[ ] Dark/light theme toggle works
[ ] Navigation links work
[ ] All text is readable
[ ] Images load properly
[ ] CSS is styled correctly

FUNCTIONALITY TESTING:
[ ] Live demo form works (paste text + submit)
[ ] Batch upload accepts CSV file
[ ] DOCX upload works
[ ] XLSX upload works
[ ] Chat feature loads
[ ] All buttons are clickable
[ ] Forms validate inputs
[ ] No console errors (F12)

RESPONSIVE TESTING:
[ ] Mobile view looks good (F12 → Toggle Device Toolbar)
[ ] Tablet view works
[ ] Desktop view looks correct

BROWSER TESTING:
[ ] Chrome (test on latest)
[ ] Firefox (optional)
[ ] Safari (optional Mac)
```

---

## 📊 Vercel Deployment Flowchart

```
START
  ↓
Push to GitHub
  ↓
Go to vercel.com
  ↓
Connect GitHub account
  ↓
Import your repository
  ↓
Framework: Select "Other" (for static)
  ↓
Root: Keep as "."
  ↓
Build: Leave empty
  ↓
Environment: Leave empty (unless needed)
  ↓
Click "Deploy"
  ↓
Wait for build to complete
  ↓
✅ Get your live URL (usually yourname-projectname.vercel.app)
  ↓
Test the live site
  ↓
If issues → Check Vercel build logs
  ↓
END
```

---

## 🎯 Commands Reference

### Local Testing Commands

```bash
# Option 1: Python HTTP Server
python -m http.server 8000
# Open: http://localhost:8000

# Option 2: Node.js custom server (simulates Vercel)
npm install
npm start
# Open: http://localhost:3000

# Option 3: Using npx serve
npx serve .
# Open: http://localhost:3000

# Option 4: VS Code Live Server
# Install extension, right-click index.html → "Open with Live Server"
```

### Vercel CLI Commands

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy to preview (testing)
vercel

# Deploy to production
vercel --prod

# Force redeploy (clear cache)
vercel --prod --force

# View logs locally
vercel logs

# Preview latest deployment
vercel --prod --preview
```

### Git Commands

```bash
# Add all changes
git add .

# Commit changes
git commit -m "Your message"

# Push to GitHub
git push origin main

# View status
git status

# View recent commits
git log --oneline -5
```

---

## 🔗 Useful Links

| Resource                     | Link                                                                        |
| ---------------------------- | --------------------------------------------------------------------------- |
| Vercel Dashboard             | https://vercel.com/dashboard                                                |
| Vercel Docs                  | https://vercel.com/docs                                                     |
| GitHub Repo Settings         | https://github.com/YOUR_USERNAME/YOUR_REPO/settings                         |
| Vercel Environment Variables | https://vercel.com/docs/environment-variables                               |
| HTML Validator               | https://validator.w3.org                                                    |
| Check MIME Types             | https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types |

---

## 💡 Pro Tips

1. **Always test locally first** before pushing to Vercel
2. **Use relative paths** for all assets (CSS, JS, images)
3. **Keep vercel.json simple** for static sites
4. **Monitor build logs** for warnings/errors
5. **Cache-bust on updates**: Add version query: `app.js?v=1.0.0`
6. **Use .gitignore** to exclude large files
7. **Test in incognito mode** to clear browser cache

---

## ❓ Still Having Issues?

### Step-by-step debugging:

1. **Test locally** - Does it work on localhost?
2. **Check Git** - Are files committed and pushed?
3. **Check console** - Are there JS errors? (F12)
4. **Check Build Logs** - What does Vercel say? (Dashboard → Deployments)
5. **Check paths** - Are all file references relative?
6. **Check MIME types** - Are assets loading with correct types?
7. **Hard refresh** - Press Ctrl+Shift+R to clear cache on Vercel site

### Still stuck?

Share these details:

- Your GitHub repo URL
- Screenshot of Vercel build logs
- Screenshot of browser console errors (F12)
- Local test results (what works/doesn't work)
