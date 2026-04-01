@echo off
REM Quick Reference Card for ExplainGrade Vercel Deployment (Windows)
REM Run this file in PowerShell or Command Prompt

echo.
echo ═══════════════════════════════════════════════════════
echo   📋 ExplainGrade Quick Reference (Windows)
echo ═══════════════════════════════════════════════════════
echo.

echo 🚀 QUICK START - Pick ONE method:
echo ───────────────────────────────────────────────────────
echo.
echo 1️⃣  PYTHON HTTP SERVER (Simplest):
echo    python -m http.server 8000
echo    → Open: http://localhost:8000
echo.
echo 2️⃣  NODE.JS SERVER (RECOMMENDED - Simulates Vercel):
echo    npm install
echo    npm start
echo    → Open: http://localhost:3000
echo.
echo 3️⃣  Using npx serve:
echo    npx serve .
echo    → Open: http://localhost:3000
echo.
echo 4️⃣  VS Code Live Server:
echo    Right-click index.html → Open with Live Server
echo.

echo ═══════════════════════════════════════════════════════
echo   ✅ TESTING CHECKLIST
echo ═══════════════════════════════════════════════════════
echo.
echo [ ] Page loads (no blank screen)
echo [ ] CSS styled correctly (dark/light theme visible)
echo [ ] Theme toggle button works
echo [ ] All navigation links work
echo [ ] File upload inputs work
echo [ ] No red errors in console (F12)
echo [ ] Can access all pages (index, pipeline, research, etc)
echo.

echo ═══════════════════════════════════════════════════════
echo   📤 DEPLOY TO VERCEL
echo ═══════════════════════════════════════════════════════
echo.
echo OPTION A: Via Vercel Web Dashboard (Easiest)
echo ───────────────────────────────────────────────────────
echo Step 1: Push to GitHub (PowerShell):
echo   git add .
echo   git commit -m "Ready for Vercel deployment"
echo   git push origin main
echo.
echo Step 2: Go to https://vercel.com/dashboard
echo Step 3: Click "Add New" → "Project"
echo Step 4: Select your GitHub repository
echo Step 5: Framework Preset: Choose "Other"
echo Step 6: Click "Deploy"
echo Step 7: Wait for build to complete
echo Step 8: You get a live URL (yourproject.vercel.app)
echo.
echo OPTION B: Via Vercel CLI
echo ───────────────────────────────────────────────────────
echo   npm install -g vercel
echo   vercel --prod
echo.

echo ═══════════════════════════════════════════════════════
echo   🐛 TROUBLESHOOTING
echo ═══════════════════════════════════════════════════════
echo.
echo Works Locally But Fails on Vercel?
echo ───────────────────────────────────────────────────────
echo.
echo CHECK 1: File Paths
echo   ❌ Wrong:  ^<script src="/app.js"^>
echo   ✅ Correct: ^<script src="app.js"^> or ^<script src="./app.js"^>
echo.
echo CHECK 2: Filenames (Case Sensitive on Vercel!)
echo   ❌ Wrong:  app.JS or App.js
echo   ✅ Correct: app.js (all lowercase)
echo.
echo CHECK 3: Dependencies Installed
echo   In PowerShell:
echo   npm install
echo   npm list
echo.
echo CHECK 4: Check Vercel Build Logs
echo   1. Go: https://vercel.com/dashboard
echo   2. Click your project
echo   3. Click "Deployments" tab
echo   4. Click failed deployment
echo   5. Scroll to "Build Logs"
echo.

echo ═══════════════════════════════════════════════════════
echo   ⚡ MOST COMMON ISSUES & FIXES
echo ═══════════════════════════════════════════════════════
echo.
echo ❌ Cannot GET / (not found)
echo    → Solution: Ensure index.html exists in root
echo.
echo ❌ No CSS (page is unstyled, looks plain)
echo    → Solution: Check link tag: ^<link href="style.css"^>
echo.
echo ❌ Scripts not loading or undefined errors
echo    → Solution: Use relative paths, no leading slash
echo.
echo ❌ "PapaParse is not defined" or "XLSX not defined"
echo    → Solution: Put CDN scripts BEFORE local scripts
echo.
echo ❌ Files work local but not on Vercel
echo    → Solution: Check npm install and file case
echo.

echo ═══════════════════════════════════════════════════════
echo   📚 COMPLETE GUIDES (Read in this order)
echo ═══════════════════════════════════════════════════════
echo.
echo 1. LOCAL_TESTING_GUIDE.md
echo    How to test your site locally before Vercel
echo.
echo 2. VERCEL_DEPLOYMENT_GUIDE.md
echo    Complete deployment instructions
echo.
echo 3. VERCEL_ISSUES_FIXES.md
echo    Detailed troubleshooting for specific issues
echo.

echo ═══════════════════════════════════════════════════════
echo   ✨ QUICK COMMANDS
echo ═══════════════════════════════════════════════════════
echo.
echo Start local server (Node.js):
echo   npm install
echo   npm start
echo.
echo Deploy to Vercel:
echo   vercel --prod
echo.
echo Force rebuild (clear cache):
echo   vercel --prod --force
echo.
echo View git status:
echo   git status
echo.
echo View recent commits:
echo   git log --oneline -5
echo.

echo ═══════════════════════════════════════════════════════
echo   🎯 YOUR NEXT STEPS
echo ═══════════════════════════════════════════════════════
echo.
echo 1. Test locally using ONE method above
echo 2. Open browser to http://localhost:3000
echo 3. Verify everything works (use checklist above)
echo 4. Push to GitHub (if not done yet)
echo 5. Deploy to Vercel (Option A or B)
echo 6. Test your live site at vercel URL
echo.
echo If problems: Read VERCEL_ISSUES_FIXES.md
echo.

echo ═══════════════════════════════════════════════════════
echo.
pause
