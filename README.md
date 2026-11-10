# App Hub: setup guide

A simple home page that lists your apps, with each app in its own folder. It's free to host on GitHub Pages.

```
index.html          ← the home page (edit the SITE and APPS lists near the bottom)
404.html            ← shown if someone opens a broken link
apps/
  example/
    index.html      ← one app per folder
```

## 1. Put it online (about 5 minutes)

1. Sign in at github.com, or create a free account. Your username becomes part of the web address, so pick a tidy one.
2. Click **+ → New repository**.
   - For the address `https://USERNAME.github.io`, name the repository exactly `USERNAME.github.io`.
   - For the address `https://USERNAME.github.io/apps`, use any name, such as `apps`.
   - Set it to **Public** (Pages on the free plan needs a public repository), then click **Create repository**.
3. On the new repository page, click **uploading an existing file**. Unzip the starter kit and drag in **everything inside the `app-hub` folder** (index.html, 404.html, README.md and the `apps` folder), not the folder itself. Click **Commit changes**.
4. Go to **Settings → Pages**. Under "Build and deployment", set Source to **Deploy from a branch**, Branch to **main** and folder to **/ (root)**, then click **Save**.
5. Wait a minute or two and refresh. The page shows your live address.

## 2. Add an app

1. Get the app's HTML. In Claude, ask for "the HTML file for this app", or download it from the artifact.
2. In your repository, click **Add file → Upload files**. Drag the file in, and change the path to `apps/my-app-name/index.html`. Use lowercase and hyphens with no spaces, because this becomes the link.
3. Edit `index.html` (click the file, then the pencil icon) and add an entry to the `APPS` list:

```js
{
  title: "Failed Contact Navigator",
  icon: "📞",
  category: "Clinical",
  description: "One line on what it does and who it's for.",
  url: "apps/failed-contact-navigator/",
  status: "live"
},
```

4. Commit. The site updates in about a minute.

## 3. Change the name and wording

At the bottom of `index.html`, edit the `SITE` block (name, headline, intro and footer).

## 4. Use your own domain (optional)

Buy a domain (for example from Cloudflare, Namecheap or 123-reg), then in **Settings → Pages → Custom domain** enter it and follow GitHub's DNS instructions. Tick **Enforce HTTPS** once it's available.

## Before you publish an app, check

- **Everything is public.** Anyone with the link can see the page and its code. Remove patient details, volunteer names, phone numbers, internal links and anything organisation-confidential.
- **Self-contained only.** Apps that use Claude features, connected apps or shared storage won't work here. Keep those on Claude and link to their share link instead (set `url` to the Claude link).
- **Clinical tools.** Add a short note saying what the tool is for, which guidance it's based on (and the date), and that it supports rather than replaces clinical judgement. If a tool is built around your practice's or organisation's processes, check they're happy for it to be public.
- **Saved data stays on the device.** If an app saves data in the browser (localStorage), that data stays on the user's device and isn't shared.
