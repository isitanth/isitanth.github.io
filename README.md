# Jekyll Portfolio & Blog

Static site converted to Jekyll for GitHub Pages, preserving original design and CSS.

## Structure

```
jekyllWebsite/
├── _config.yml              # Jekyll configuration
├── _layouts/
│   ├── default.html         # Base layout with shared CSS
│   ├── blog-list.html       # Blog listing page
│   └── post.html            # Individual blog post
├── _posts/
│   └── 2025-01-15-bypass-drm-apple-music.md
├── index.md                 # Portfolio homepage
├── blog.md                  # Blog listing page
├── Gemfile                  # Ruby dependencies
└── README.md                # This file
```

## Key Features

- **Preserved Design**: All original CSS maintained in layouts
- **Automatic Blog Listing**: Posts automatically appear on `/blog/`
- **Markdown Posts**: Write posts in `_posts/` directory
- **Clean URLs**: `yourusername.github.io/blog/post-title/`

## Local Development

### Quick Start

1. **Install dependencies** (first time only):
   ```bash
   bundle install
   ```

2. **Start the server**:
   ```bash
   bundle exec jekyll serve --host 127.0.0.1 --port 4000
   ```

3. **View site**: Open `http://127.0.0.1:4000`

4. **Stop server**: Press `Ctrl+C`

### Important Notes

- Using **Jekyll 3.9** (not 4.x) for compatibility with macOS system Ruby 2.6
- URLs are clean (no `.html` extension) thanks to `permalink: pretty`
- Server must bind to `127.0.0.1` explicitly on some macOS configurations

## Deploy to GitHub Pages

### Method 1: GitHub Repository (Recommended)

1. **Create repository** named `yourusername.github.io`

2. **Update `_config.yml`**:
   ```yaml
   url: "https://yourusername.github.io"
   ```

3. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial Jekyll site"
   git branch -M main
   git remote add origin https://github.com/yourusername/yourusername.github.io.git
   git push -u origin main
   ```

4. **Enable GitHub Pages**:
   - Go to repository Settings → Pages
   - Source: Deploy from branch `main`
   - Folder: `/ (root)`
   - Save

5. **Wait 1-2 minutes**, then visit `https://yourusername.github.io`

### Method 2: GitHub Actions (Alternative)

Create `.github/workflows/pages.yml`:

```yaml
name: Deploy Jekyll to GitHub Pages

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.1'
          bundler-cache: true
      - name: Build with Jekyll
        run: bundle exec jekyll build
      - uses: actions/upload-pages-artifact@v3

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - uses: actions/deploy-pages@v4
        id: deployment
```

Then in Settings → Pages → Source: select "GitHub Actions"

## Adding New Blog Posts

Create file in `_posts/` with format: `YYYY-MM-DD-title.md`

```markdown
---
title: "Your Post Title"
date: 2025-01-15
tags: [tag1, tag2]
excerpt: "Brief description for the listing page"
---

Your content here in **Markdown**...
```

**Note**: You don't need to specify `layout: post` anymore! The `_config.yml` defaults automatically apply the `post` layout to all files in `_posts/`.

Post will automatically appear on blog listing page.

## Customization

- **Colors/Styles**: Edit `_layouts/default.html` `<style>` section
- **Site info**: Edit `_config.yml`
- **Navigation**: Edit `index.md` and layout files

## Troubleshooting

### Common Issues

**"cannot load such file -- google/protobuf_c" error**
- **Cause**: Jekyll 4.x incompatibility with macOS system Ruby 2.6
- **Solution**: Use Jekyll 3.9 (already configured in `Gemfile`)
- If you upgraded to Jekyll 4.x by mistake:
  ```bash
  rm -f Gemfile.lock
  bundle install
  ```

**URLs showing `.html` extensions**
- **Cause**: `permalink` setting not configured
- **Solution**: Verify `_config.yml` has `permalink: pretty`
- Restart Jekyll server after changing config

**Permission errors during `bundle install`**
- **Solution**: Install to local vendor directory:
  ```bash
  bundle config set --local path 'vendor/bundle'
  bundle install
  ```

**Site not updating after changes?**
- Stop server (`Ctrl+C`) and restart:
  ```bash
  bundle exec jekyll serve --host 127.0.0.1 --port 4000
  ```
- Config file (`_config.yml`) changes **always** require restart
- Content/layout changes should auto-regenerate

**Clean rebuild if things break:**
```bash
bundle exec jekyll clean
bundle install
bundle exec jekyll serve --host 127.0.0.1 --port 4000
```

**Port 4000 already in use?**
```bash
# Use different port
bundle exec jekyll serve --host 127.0.0.1 --port 4001

# Or kill existing Jekyll process
lsof -ti:4000 | xargs kill -9
```

## Technical Details

### Jekyll Version & Compatibility

- **Jekyll**: 3.9.x (not 4.x)
- **Ruby**: System Ruby 2.6.10 (macOS default)
- **Why Jekyll 3.9?**: Jekyll 4.x has protobuf/sass-embedded dependencies incompatible with Ruby 2.6

### Key Configuration

**`_config.yml`**:
- `permalink: pretty` — Removes `.html` extensions from URLs
- `markdown: kramdown` — Markdown processor
- Posts automatically collected from `_posts/` directory
- **Front matter defaults** — Auto-applies `layout: post` to all posts and `layout: default` to all pages
  - No need to specify layout in individual post front matter

**`Gemfile`**:
```ruby
gem "jekyll", "~> 3.9"  # NOT 4.x
gem "kramdown-parser-gfm"  # GitHub-flavored markdown
```

### File Structure Changes

**Before (static HTML)**:
```
index.html
blog.html
blog1.html
```

**After (Jekyll)**:
```
index.md                              # Portfolio
blog/index.md                         # Blog listing
_posts/2025-01-15-bypass-drm-apple-music.md  # Blog post
_layouts/
  ├── default.html                    # Shared wrapper
  ├── blog-list.html                  # Auto-lists posts
  └── post.html                       # Article template
```

**URL Mapping**:
- `index.html` → `http://127.0.0.1:4000/`
- `blog.html` → `http://127.0.0.1:4000/blog/`
- `blog1.html` → `http://127.0.0.1:4000/blog/bypass-drm-apple-music/`

## Original Files (Reference Only)

Keep these for reference, but they're no longer used by Jekyll:
- `index.html` → migrated to `index.md`
- `blog.html` → migrated to `blog/index.md` + `_layouts/blog-list.html`
- `blog1.html` → migrated to `_posts/2025-01-15-bypass-drm-apple-music.md`
