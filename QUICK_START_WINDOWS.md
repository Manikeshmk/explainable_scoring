# 🚀 ExplainGrade - QUICK START

You're on **Windows**. Here's exactly what to do:

## ⏱️ 2-MINUTE SETUP

### Open PowerShell in your project folder:

```powershell
cd C:\Users\deii\Desktop\cloud

# Install dependencies
npm install

# Start local server (simulates Vercel)
npm start
```

### Open your browser:

```
http://localhost:3000
```

### Test these things:

- [ ] Page loads (not blank)
- [ ] CSS visible (colors, not plain text)
- [ ] Dark/light theme toggle works
- [ ] No errors in console (F12)

---

## 🚢 DEPLOY TO VERCEL

### Method 1: Web Dashboard (EASIER)

```powershell
# Push your code to GitHub
git add .
git commit -m "Deploy to Vercel"
git push origin main
```

Then:

1. Go to https://vercel.com/dashboard
2. Click "Add New" → "Project"
3. Select your GitHub repo
4. Click "Deploy"
5. Wait 2-5 minutes
6. You get a live URL! 🎉

### Method 2: Vercel CLI

```powershell
npm install -g vercel
vercel --prod
```

---

## 🐛 COMMON PROBLEMS & FIXES

**Problem: Works locally but not on Vercel**

Check these in order:

1. File paths - Use `src="app.js"` not `src="/app.js"`
2. Filenames - Must be lowercase: `app.js` not `App.js`
3. npm - Run: `npm install` before deploying
4. View errors - https://vercel.com/dashboard → Your project → Deployments

**Problem: CSS not loading on Vercel**
→ Check HTML has: `<link href="style.css">`

**Problem: Libraries undefined**
→ Put CDN scripts before your local scripts in HTML

---

## 📚 COMPLETE GUIDES

I created detailed guides in your folder:

- **START_HERE.md** ← Read this first!
- **DEPLOYMENT_SUMMARY.md** ← Full overview
- **LOCAL_TESTING_GUIDE.md** ← Testing tips
- **VERCEL_DEPLOYMENT_GUIDE.md** ← Deployment steps
- **VERCEL_ISSUES_FIXES.md** ← Fix errors (9 scenarios)

---

## ⚡ QUICK COMMANDS

```powershell
# Start local server
npm start

# View live logs
npm list

# Deploy to Vercel
vercel --prod

# Force rebuild (clears cache)
vercel --prod --force

# Check git status
git status

# View recent commits
git log --oneline -5
```

---

## 🎯 NEXT STEPS

1. **Run:** `npm install && npm start`
2. **Test:** Open http://localhost:3000
3. **Verify:** Use the checklist above
4. **Deploy:** Choose Method 1 or 2 above
5. **Live:** Visit your vercel URL

---

## ✨ YOUR PROJECT STATUS

✅ **Ready for Vercel deployment!**

- Server.js created for local testing
- package.json updated with scripts
- Comprehensive documentation provided
- All guides ready for troubleshooting

---

## 📖 WHICH FILE TO READ?

- **5 minutes?** → START_HERE.md
- **Want to test locally?** → LOCAL_TESTING_GUIDE.md
- **Want to deploy?** → VERCEL_DEPLOYMENT_GUIDE.md
- **Have an error?** → VERCEL_ISSUES_FIXES.md
- **Full overview?** → DEPLOYMENT_SUMMARY.md

---

## 🎉 That's It!

You're ready to deploy. Start with:

```powershell
npm install && npm start
```

Then test and deploy. All the guides are in your folder!

Questions? Check the detailed guides. 🚀
