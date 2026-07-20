# Spotless O'Clock - Vercel deployment

This is a framework-free static website. No build command, package installation or environment variables are required.

## Deploy from the Vercel dashboard

1. Create a Git repository containing this folder.
2. In Vercel, choose **Add New > Project** and import the repository.
3. Set **Framework Preset** to **Other**.
4. Leave **Build Command** and **Output Directory** empty.
5. Deploy.

## Deploy with the Vercel CLI

From this folder:

```powershell
npx vercel
```

For a production deployment:

```powershell
npx vercel --prod
```

## After the first deployment

- Add the approved custom domain in **Project Settings > Domains**.
- Add the final domain as a canonical URL and `og:url` in `index.html`.
- Add an absolute `og:image` URL after the production domain is known.
- Confirm service areas, business hours and any insurance or trust claims before launch.

## Project structure

- `index.html` - main website
- `styles.css` - responsive design system
- `script.js` - navigation, animation and WhatsApp quote flow
- `assets/` - versioned, long-cache visual assets
- `404.html` - branded not-found page
- `vercel.json` - URL, security and caching configuration
- `.vercelignore` - files excluded from deployment
