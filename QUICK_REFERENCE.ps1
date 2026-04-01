#!/usr/bin/pwsh
<#
.SYNOPSIS
    Quick Reference for ExplainGrade Vercel Deployment (PowerShell)

.DESCRIPTION
    Shows quick commands to test locally and deploy to Vercel

.EXAMPLE
    .\QUICK_REFERENCE.ps1
#>

Write-Host ""
Write-Host "═════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  📋 ExplainGrade - Vercel Deployment Quick Guide" -ForegroundColor Green
Write-Host "═════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Write-Host "🚀 STEP 1: TEST LOCALLY (Pick One Method)" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────" -ForegroundColor Gray
Write-Host ""
Write-Host "  Method 1: Python HTTP Server (Simplest)" -ForegroundColor White
Write-Host "  ────────────────────────────────────" -ForegroundColor Gray
Write-Host '    python -m http.server 8000' -ForegroundColor Cyan
Write-Host '    → Open: http://localhost:8000' -ForegroundColor Green
Write-Host ""

Write-Host "  Method 2: Node.js Server (RECOMMENDED)" -ForegroundColor White
Write-Host "  ──────────────────────────────────" -ForegroundColor Gray
Write-Host '    npm install' -ForegroundColor Cyan
Write-Host '    npm start' -ForegroundColor Cyan
Write-Host '    → Open: http://localhost:3000' -ForegroundColor Green
Write-Host ""

Write-Host "  Method 3: npx serve" -ForegroundColor White
Write-Host "  ───────────────────" -ForegroundColor Gray
Write-Host '    npx serve .' -ForegroundColor Cyan
Write-Host '    → Open: http://localhost:3000' -ForegroundColor Green
Write-Host ""

Write-Host "═════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  ✅ VERIFICATION CHECKLIST" -ForegroundColor Green
Write-Host "═════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "  When testing locally, verify these work:" -ForegroundColor White
Write-Host ""
Write-Host "  [ ] Page loads without errors" -ForegroundColor Gray
Write-Host "  [ ] CSS is visible (styled, not plain)" -ForegroundColor Gray
Write-Host "  [ ] Dark/Light theme toggle works" -ForegroundColor Gray
Write-Host "  [ ] Navigation links work" -ForegroundColor Gray
Write-Host "  [ ] File uploads function" -ForegroundColor Gray
Write-Host "  [ ] No errors in browser console (F12)" -ForegroundColor Gray
Write-Host "  [ ] All pages load (index, pipeline, research, chat)" -ForegroundColor Gray
Write-Host ""

Write-Host "═════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  📤 STEP 2: DEPLOY TO VERCEL" -ForegroundColor Green
Write-Host "═════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Write-Host "  OPTION A: Web Dashboard (Easiest)" -ForegroundColor Yellow
Write-Host "  ─────────────────────────────────" -ForegroundColor Gray
Write-Host ""
Write-Host "    1. Commit and push to GitHub:" -ForegroundColor White
Write-Host '       git add .' -ForegroundColor Cyan
Write-Host '       git commit -m "Ready for Vercel"' -ForegroundColor Cyan
Write-Host '       git push origin main' -ForegroundColor Cyan
Write-Host ""
Write-Host "    2. Visit: https://vercel.com/dashboard" -ForegroundColor White
Write-Host "    3. Click: Add New → Project" -ForegroundColor White
Write-Host "    4. Select: Your GitHub Repository" -ForegroundColor White
Write-Host "    5. Framework: Select 'Other'" -ForegroundColor White
Write-Host "    6. Root: Leave as '.'" -ForegroundColor White
Write-Host "    7. Click: Deploy" -ForegroundColor White
Write-Host "    8. Wait for build (2-5 minutes)" -ForegroundColor White
Write-Host "    9. Get your live URL!" -ForegroundColor Green
Write-Host ""

Write-Host "  OPTION B: Vercel CLI" -ForegroundColor Yellow
Write-Host "  ────────────────────" -ForegroundColor Gray
Write-Host ""
Write-Host '    npm install -g vercel' -ForegroundColor Cyan
Write-Host '    vercel --prod' -ForegroundColor Cyan
Write-Host ""

Write-Host "═════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  🐛 TROUBLESHOOTING" -ForegroundColor Green
Write-Host "═════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Write-Host "  ❌ Problem: Works locally but not on Vercel" -ForegroundColor Red
Write-Host "  ✅ Solutions:" -ForegroundColor Green
Write-Host "     • Check file paths are relative (no leading /)" -ForegroundColor Gray
Write-Host "     • Check filenames match case (app.js not app.JS)" -ForegroundColor Gray
Write-Host "     • Run: npm install && npm list" -ForegroundColor Gray
Write-Host "     • Check Vercel build logs (see below)" -ForegroundColor Gray
Write-Host ""

Write-Host "  ❌ Problem: CSS not loading (unstyled page)" -ForegroundColor Red
Write-Host "  ✅ Solution:" -ForegroundColor Green
Write-Host '     Check HTML has: <link href="style.css">' -ForegroundColor Gray
Write-Host ""

Write-Host "  ❌ Problem: Libraries undefined (Papa, XLSX, etc)" -ForegroundColor Red
Write-Host "  ✅ Solution:" -ForegroundColor Green
Write-Host "     Put CDN library scripts BEFORE your local scripts" -ForegroundColor Gray
Write-Host ""

Write-Host "  📊 VIEW VERCEL BUILD LOGS:" -ForegroundColor Yellow
Write-Host "     1. Go to: https://vercel.com/dashboard" -ForegroundColor Gray
Write-Host "     2. Click your project" -ForegroundColor Gray
Write-Host "     3. Click 'Deployments' tab" -ForegroundColor Gray
Write-Host "     4. Click failed deployment" -ForegroundColor Gray
Write-Host "     5. Look at 'Build Logs'" -ForegroundColor Gray
Write-Host ""

Write-Host "═════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  📚 COMPLETE DOCUMENTATION" -ForegroundColor Green
Write-Host "═════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "  These files have detailed information:" -ForegroundColor White
Write-Host ""
Write-Host "  📖 LOCAL_TESTING_GUIDE.md" -ForegroundColor Magenta
Write-Host "     How to test locally before Vercel" -ForegroundColor Gray
Write-Host ""
Write-Host "  📖 VERCEL_DEPLOYMENT_GUIDE.md" -ForegroundColor Magenta
Write-Host "     Complete deployment instructions" -ForegroundColor Gray
Write-Host ""
Write-Host "  📖 VERCEL_ISSUES_FIXES.md" -ForegroundColor Magenta
Write-Host "     Detailed troubleshooting guide" -ForegroundColor Gray
Write-Host ""

Write-Host "═════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  ⚡ USEFUL COMMANDS" -ForegroundColor Green
Write-Host "═════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Test locally:" -ForegroundColor Yellow
Write-Host '    npm install && npm start' -ForegroundColor Cyan
Write-Host ""
Write-Host "  Install Vercel CLI:" -ForegroundColor Yellow
Write-Host '    npm install -g vercel' -ForegroundColor Cyan
Write-Host ""
Write-Host "  Deploy to Vercel:" -ForegroundColor Yellow
Write-Host '    vercel --prod' -ForegroundColor Cyan
Write-Host ""
Write-Host "  Force rebuild:" -ForegroundColor Yellow
Write-Host '    vercel --prod --force' -ForegroundColor Cyan
Write-Host ""
Write-Host "  Check git status:" -ForegroundColor Yellow
Write-Host '    git status' -ForegroundColor Cyan
Write-Host ""

Write-Host "═════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  🎯 WHAT TO DO NOW" -ForegroundColor Green
Write-Host "═════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "  1. Open PowerShell in your project folder" -ForegroundColor White
Write-Host "     (or use Windows Terminal)" -ForegroundColor Gray
Write-Host ""
Write-Host "  2. Test locally (choose one method above)" -ForegroundColor White
Write-Host ""
Write-Host "  3. Open http://localhost:3000 in browser" -ForegroundColor White
Write-Host ""
Write-Host "  4. Verify everything works (use checklist above)" -ForegroundColor White
Write-Host ""
Write-Host "  5. Deploy to Vercel (Option A or B)" -ForegroundColor White
Write-Host ""
Write-Host "  6. Test your live site" -ForegroundColor White
Write-Host ""
Write-Host "  If issues → Read VERCEL_ISSUES_FIXES.md" -ForegroundColor Yellow
Write-Host ""

Write-Host "═════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Good luck! 🚀" -ForegroundColor Green
Write-Host ""
