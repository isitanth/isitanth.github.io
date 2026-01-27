# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Jekyll-based portfolio and blog for GitHub Pages, deployed at https://isitanth.github.io.

**Tech Stack:** Jekyll 3.9, Ruby 2.6+, kramdown (GitHub-flavored markdown), new.css framework

## Development Commands

```bash
# Install dependencies
bundle install

# Start development server (view at http://127.0.0.1:4000)
bundle exec jekyll serve --host 127.0.0.1 --port 4000

# Clean rebuild if caching issues occur
bundle exec jekyll clean && bundle install && bundle exec jekyll serve --host 127.0.0.1 --port 4000
```

## Architecture

**Layouts hierarchy:**
- `_layouts/default.html` - Base layout with new.css styling, header, footer
- `_layouts/post.html` - Blog post template (extends default, adds Highlight.js)
- `_layouts/blog-list.html` - Blog listing grid (extends default)

**Content structure:**
- `index.md` - Portfolio homepage
- `blog/index.md` - Blog listing page (uses blog-list layout)
- `_posts/YYYY-MM-DD-title.md` - Blog posts (auto-apply post layout)

**URL scheme:** Pretty permalinks configured. Posts appear at `/blog/post-title/`.

## Adding Blog Posts

Create file in `_posts/` with naming format `YYYY-MM-DD-title.md`:

```markdown
---
title: "Post Title"
date: 2025-01-15
tags: [tag1, tag2]
excerpt: "Brief description for listing"
---
Content here...
```

Layout is auto-applied via `_config.yml` defaults.

## Important Notes

- Uses Jekyll 3.9 (not 4.x) for macOS system Ruby compatibility
- Explicit host binding (`--host 127.0.0.1`) required on some configurations
- Deployment: Push to main branch; GitHub Pages auto-builds
