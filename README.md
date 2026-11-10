# GP Productivity Tools: Applications

The source for the apps website. **Every HTML file in the [`apps`](apps/) folder automatically appears on the home page.** You don't need to edit any code.

## Add an app

1. Get the app's HTML file. In Claude, ask for "the HTML file for this app", or download it from the artifact.
2. Open the [`apps`](apps/) folder on GitHub and click **Add file → Upload files**.
3. Drag the `.html` file in and click **Commit changes**.
4. About a minute later it's live at `…/apps/<file-name>/` and listed on the home page. Watch progress in the **Actions** tab.

The file name becomes the link, so `Failed Contact Navigator.html` becomes `apps/failed-contact-navigator/`.

Every app automatically gets a slim **"← All apps"** bar across the top.

### Optional: control how the card looks

Add any of these inside the app's `<head>`. If you leave them out, the card uses the page title and sensible defaults.

```html
<title>Failed Contact Navigator</title>
<meta name="description" content="Step-by-step guide for when a patient can't be reached after triage.">
<meta name="app:category" content="Clinical">
<meta name="app:icon" content="📞">
```

| Tag | What it does |
|---|---|
| `app:category` | Groups the app under a filter button. Default categories: Clinical, Practice admin, Volunteering, Utilities. Any new name works. |
| `app:icon` | Any emoji. |
| `app:hidden` set to `true` | Leaves it off the home page but keeps it reachable by direct link, which is handy for testing. |
| `app:backlink` set to `false` | Leaves out the "All apps" bar. |

### Apps with several files

If an app needs images or extra files, upload a folder instead: `apps/my-app/index.html` plus its files.

## Update or remove an app

- **Update:** upload a file with the same name, and GitHub replaces it.
- **Remove:** open the file, click **⋯ → Delete file**, then commit.

## Change the site name or wording

Edit [`site.json`](site.json) (name, headline, intro, footer and category order).

## Before publishing, check

- **It's public.** Anyone can see the page and its code. Remove patient details, staff or volunteer names, phone numbers, internal links and anything confidential.
- **It's self-contained.** Apps that use Claude features, connected apps or shared storage won't work here.
- **Clinical tools.** Say what the tool is for and which guidance it's based on (and the date). If it's built around a specific organisation's processes, check they're happy for it to be public.

## How it works (for reference)

On every change to `main`, [`.github/workflows/pages.yml`](.github/workflows/pages.yml) runs [`scripts/build.py`](scripts/build.py). The script reads each app's title and tags, builds the home page from `scripts/home.template.html` and publishes the result to GitHub Pages. To preview locally, run `python3 scripts/build.py` and open `_site/index.html`.
