/**
 * server.js — Local Development Server
 *
 * Simulates Vercel's static file serving and routing.
 * Use this to test your site locally before Vercel deployment.
 *
 * Usage:
 *   npm install
 *   npm start
 *
 * Then open: http://localhost:3000
 */

const http = require("http");
const fs = require("fs");
const path = require("path");
const url = require("url");

const PORT = process.env.PORT || 3000;

const MIME_TYPES = {
  ".html": "text/html; charset=UTF-8",
  ".js": "application/javascript; charset=UTF-8",
  ".css": "text/css; charset=UTF-8",
  ".json": "application/json",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".gif": "image/gif",
  ".svg": "image/svg+xml",
  ".ico": "image/x-icon",
  ".webp": "image/webp",
  ".wav": "audio/wav",
  ".mp4": "video/mp4",
  ".webm": "video/webm",
  ".woff": "font/woff",
  ".woff2": "font/woff2",
  ".ttf": "font/ttf",
  ".eot": "application/vnd.ms-fontobject",
  ".otf": "font/otf",
  ".wasm": "application/wasm",
  ".csv": "text/csv",
  ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  ".docx":
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  ".pdf": "application/pdf",
  ".txt": "text/plain",
};

/**
 * Resolve file path following Vercel's rules:
 * 1. If it's a directory, serve index.html
 * 2. If no extension, try .html
 * 3. Serve the file as-is
 */
function resolvePath(urlPath) {
  let filePath = path.join(
    process.cwd(),
    urlPath === "/" ? "index.html" : urlPath,
  );

  // Remove trailing slash
  if (filePath.endsWith(path.sep) && filePath !== path.sep) {
    filePath = filePath.slice(0, -1);
  }

  // If no extension, try .html
  if (!path.extname(filePath)) {
    const htmlPath = filePath + ".html";
    if (fs.existsSync(htmlPath)) {
      return htmlPath;
    }
  }

  // If directory, serve index.html
  if (fs.existsSync(filePath) && fs.statSync(filePath).isDirectory()) {
    return path.join(filePath, "index.html");
  }

  return filePath;
}

const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url, true);
  const pathname = parsedUrl.pathname;

  let filePath = resolvePath(pathname);

  const extname = String(path.extname(filePath)).toLowerCase();
  const contentType = MIME_TYPES[extname] || "application/octet-stream";

  // Read and serve the file
  fs.readFile(filePath, (error, content) => {
    if (error) {
      if (error.code === "ENOENT") {
        // Try index.html fallback (for SPA routing)
        const fallbackPath = path.join(process.cwd(), "index.html");
        fs.readFile(fallbackPath, (fallbackError, fallbackContent) => {
          if (!fallbackError) {
            res.writeHead(200, { "Content-Type": MIME_TYPES[".html"] });
            res.end(fallbackContent, "utf-8");
          } else {
            res.writeHead(404, { "Content-Type": "text/html" });
            res.end(`<!DOCTYPE html>
                        <html>
                        <head><title>404 Not Found</title></head>
                        <body>
                            <h1>⚠️ 404 - File Not Found</h1>
                            <p>Requested: <code>${pathname}</code></p>
                            <p>Resolved to: <code>${filePath}</code></p>
                            <p><a href="/">← Back to Home</a></p>
                        </body>
                        </html>`);
          }
        });
      } else {
        res.writeHead(500, { "Content-Type": "text/html" });
        res.end(`<!DOCTYPE html>
                <html>
                <head><title>500 Server Error</title></head>
                <body>
                    <h1>❌ 500 - Server Error</h1>
                    <p>${error.code}: ${error.message}</p>
                </body>
                </html>`);
      }
    } else {
      res.writeHead(200, {
        "Content-Type": contentType,
        "Cache-Control":
          extname === ".html" ? "no-cache" : "public, max-age=3600",
      });
      res.end(content, "utf-8");
    }
  });
});

server.listen(PORT, "0.0.0.0", () => {
  console.log("");
  console.log("╔════════════════════════════════════════════╗");
  console.log("║  🚀 ExplainGrade Development Server       ║");
  console.log("╚════════════════════════════════════════════╝");
  console.log("");
  console.log(`  🌐 Local URL:  http://localhost:${PORT}`);
  console.log(`  📁 Serving:    ${process.cwd()}`);
  console.log("");
  console.log("  This server simulates Vercel's routing.");
  console.log("  Test here before deploying to Vercel.");
  console.log("");
  console.log("  Press Ctrl+C to stop the server");
  console.log("");
});

// Handle graceful shutdown
process.on("SIGINT", () => {
  console.log("\n\n  🛑 Server stopped.\n");
  process.exit(0);
});
