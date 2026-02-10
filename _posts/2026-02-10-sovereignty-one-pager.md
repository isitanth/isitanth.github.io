---
layout: standalone
title: "Sovereignty one-pager"
date: 2026-02-10
tags: [Sovereignty, Tech]
excerpt: "Sovereignty is not a binary state. It's a continuum of control across four dimensions — legal, operational, technological, and data — each with its own level of maturity."
---

<link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,500;14..32,600&family=JetBrains+Mono:wght@300;400&display=swap" rel="stylesheet">
<style>
  :root {
    --orange-primary: #ff7900;
    --orange-dark: #f16e00;
    --ob-black: #000000;
    --ob-white: #ffffff;
    --ob-green: #32c832;
    --ob-blue: #527edb;
    --ob-yellow: #ffcc00;
    --ob-red: #cd3c14;
    --ob-blue-light: #4bb4e6;
    --ob-green-light: #50be87;
    --ob-purple: #a885d8;
    --ob-yellow-light: #ffd200;
    --ob-pink: #ffb4e6;
    --grey-900: #333;
    --grey-800: #595959;
    --grey-700: #666;
    --grey-600: #999;
    --grey-500: #ccc;
    --grey-400: #ddd;
    --grey-300: #eee;
    --grey-200: #f6f6f6;
    --grey-100: #fafafa;

    --bg-deep: #000000;
    --bg-card: #0d0d0d;
    --bg-elevated: #1a1a1a;
    --border-subtle: rgba(255,255,255,0.07);
    --border-accent: rgba(255,255,255,0.14);
    --text-primary: #f6f6f6;
    --text-secondary: #999;
    --text-muted: #666;

    --layer-legal: var(--ob-green-light);
    --layer-ops: var(--orange-primary);
    --layer-data: var(--ob-purple);
    --layer-tech: var(--ob-red);

    --layer-legal-bg: rgba(80, 190, 135, 0.07);
    --layer-ops-bg: rgba(255, 121, 0, 0.07);
    --layer-data-bg: rgba(168, 133, 216, 0.07);
    --layer-tech-bg: rgba(205, 60, 20, 0.07);
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    background: var(--bg-deep);
    color: var(--text-primary);
    font-family: 'Inter', sans-serif;
    min-height: 100vh;
    overflow-x: hidden;
  }

  body::after {
    content: '';
    position: fixed;
    inset: 0;
    background: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.03'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 9999;
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 60px 40px 80px;
  }

  .brand-bar {
    height: 4px;
    background: linear-gradient(to right, var(--orange-primary), var(--orange-dark), transparent 80%);
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 10000;
  }

  /* ── Back link ── */
  .back-to-blog {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    letter-spacing: 1px;
    color: var(--text-muted);
    text-decoration: none;
    margin-bottom: 32px;
    transition: color 0.2s ease;
  }
  .back-to-blog:hover { color: var(--orange-primary); }

  /* ── Header ── */
  .header {
    margin-bottom: 64px;
    margin-top: 16px;
    position: relative;
  }

  .header-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 14px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--orange-primary);
    margin-bottom: 24px;
    opacity: 0;
    animation: fadeSlideUp 0.8s ease forwards 0.2s;
  }

  .header h1 {
    font-family: 'Inter', sans-serif;
    font-size: clamp(40px, 5.5vw, 68px);
    font-weight: 400;
    line-height: 1.08;
    letter-spacing: -1.5px;
    color: var(--text-primary);
    max-width: 800px;
    opacity: 0;
    animation: fadeSlideUp 0.8s ease forwards 0.35s;
  }

  .header h1 em {
    font-style: italic;
    color: var(--orange-primary);
  }

  .header-sub {
    font-size: 15px;
    color: var(--text-secondary);
    margin-top: 20px;
    max-width: 560px;
    line-height: 1.7;
    opacity: 0;
    animation: fadeSlideUp 0.8s ease forwards 0.5s;
  }

  .header-line {
    width: 100%;
    height: 1px;
    background: linear-gradient(to right, var(--orange-primary) 0%, rgba(255,121,0,0.3) 30%, transparent 100%);
    margin-top: 40px;
    opacity: 0;
    animation: fadeIn 1s ease forwards 0.7s;
  }

  /* ── Spectrum Bar ── */
  .spectrum-section {
    margin-bottom: 72px;
    opacity: 0;
    animation: fadeSlideUp 0.8s ease forwards 0.9s;
  }

  .section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.78);
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    gap: 14px;
  }

  .section-label::before {
    content: '';
    width: 20px;
    height: 2.5px;
    background: var(--orange-primary);
    border-radius: 1px;
  }

  .spectrum-bar {
    display: flex;
    height: 56px;
    border-radius: 6px;
    overflow: hidden;
    border: 1px solid var(--border-subtle);
  }

  .spectrum-segment {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    gap: 2px;
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    cursor: default;
    position: relative;
    overflow: hidden;
  }

  .spectrum-segment::before {
    content: '';
    position: absolute;
    inset: 0;
    opacity: 0;
    transition: opacity 0.3s ease;
  }

  .spectrum-segment:hover::before { opacity: 1; }
  .spectrum-segment:hover { transform: scaleY(1.04); }

  .seg-legal {
    flex: 3.2;
    background: linear-gradient(135deg, rgba(80,190,135,0.18), rgba(80,190,135,0.06));
    border-right: 1px solid rgba(80,190,135,0.2);
  }
  .seg-legal::before { background: rgba(80,190,135,0.06); }

  .seg-ops {
    flex: 2.8;
    background: linear-gradient(135deg, rgba(255,121,0,0.2), rgba(255,121,0,0.06));
    border-right: 1px solid rgba(255,121,0,0.25);
  }
  .seg-ops::before { background: rgba(255,121,0,0.06); }

  .seg-data {
    flex: 2.4;
    background: linear-gradient(135deg, rgba(168,133,216,0.18), rgba(168,133,216,0.06));
    border-right: 1px solid rgba(168,133,216,0.2);
  }
  .seg-data::before { background: rgba(168,133,216,0.06); }

  .seg-tech {
    flex: 1.6;
    background: linear-gradient(135deg, rgba(205,60,20,0.15), rgba(205,60,20,0.04));
  }
  .seg-tech::before { background: rgba(205,60,20,0.06); }

  .seg-name { font-size: 11px; font-weight: 500; letter-spacing: 0.5px; }
  .seg-legal .seg-name { color: var(--layer-legal); }
  .seg-ops .seg-name { color: var(--layer-ops); }
  .seg-data .seg-name { color: var(--layer-data); }
  .seg-tech .seg-name { color: var(--layer-tech); }

  .seg-score {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    color: var(--text-muted);
  }

  .spectrum-labels {
    display: flex;
    justify-content: space-between;
    margin-top: 10px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    color: var(--text-muted);
    letter-spacing: 1px;
  }

  /* ── Layer Cards ── */
  .layers-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
    margin-bottom: 72px;
  }

  .layer-card {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    padding: 32px 28px;
    position: relative;
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    opacity: 0;
    animation: fadeSlideUp 0.7s ease forwards;
  }

  .layer-card:nth-child(1) { animation-delay: 1.1s; }
  .layer-card:nth-child(2) { animation-delay: 1.25s; }
  .layer-card:nth-child(3) { animation-delay: 1.4s; }
  .layer-card:nth-child(4) { animation-delay: 1.55s; }

  .layer-card:hover {
    border-color: var(--border-accent);
    transform: translateY(-2px);
  }

  .layer-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
  }

  .card-legal::before { background: linear-gradient(to right, var(--layer-legal), transparent 60%); }
  .card-ops::before { background: linear-gradient(to right, var(--layer-ops), transparent 60%); }
  .card-tech::before { background: linear-gradient(to right, var(--layer-tech), transparent 60%); }
  .card-data::before { background: linear-gradient(to right, var(--layer-data), transparent 60%); }

  .card-number {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    letter-spacing: 2px;
    margin-bottom: 14px;
  }

  .card-legal .card-number { color: rgba(80,190,135,0.5); }
  .card-ops .card-number { color: rgba(255,121,0,0.5); }
  .card-tech .card-number { color: rgba(205,60,20,0.5); }
  .card-data .card-number { color: rgba(168,133,216,0.5); }

  .card-title {
    font-family: 'Inter', sans-serif;
    font-size: 24px;
    font-weight: 400;
    margin-bottom: 5px;
    letter-spacing: -0.3px;
  }

  .card-legal .card-title { color: var(--layer-legal); }
  .card-ops .card-title { color: var(--layer-ops); }
  .card-tech .card-title { color: var(--layer-tech); }
  .card-data .card-title { color: var(--layer-data); }

  .card-subtitle {
    font-size: 12px;
    color: var(--text-muted);
    font-style: italic;
    margin-bottom: 16px;
  }

  .card-body {
    font-size: 13px;
    line-height: 1.75;
    color: var(--text-secondary);
  }

  .card-verdict {
    margin-top: 18px;
    padding-top: 14px;
    border-top: 1px solid var(--border-subtle);
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .verdict-icon {
    width: 26px;
    height: 26px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    flex-shrink: 0;
  }

  .verdict-strong .verdict-icon { background: rgba(80,190,135,0.12); }
  .verdict-moderate .verdict-icon { background: rgba(168,133,216,0.12); }
  .verdict-weak .verdict-icon { background: rgba(205,60,20,0.12); }

  .verdict-text {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.3px;
  }

  .verdict-strong .verdict-text { color: var(--layer-legal); }
  .verdict-moderate .verdict-text { color: var(--layer-data); }
  .verdict-weak .verdict-text { color: var(--layer-tech); }

  /* ── Threat Matrix ── */
  .threat-section {
    margin-bottom: 72px;
    opacity: 0;
    animation: fadeSlideUp 0.8s ease forwards 1.8s;
  }

  .threat-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
  }

  .threat-table thead th {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--text-muted);
    text-align: left;
    padding: 12px 16px;
    border-bottom: 1px solid var(--border-accent);
    font-weight: 400;
  }

  .threat-table tbody td {
    padding: 14px 16px;
    border-bottom: 1px solid var(--border-subtle);
    vertical-align: top;
    line-height: 1.6;
  }

  .threat-table tbody tr { transition: background 0.2s ease; }
  .threat-table tbody tr:hover { background: rgba(255,121,0,0.02); }

  .threat-name { color: var(--text-primary); font-weight: 500; white-space: nowrap; }
  .threat-desc { color: var(--text-secondary); font-size: 12.5px; }

  .threat-status {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    padding: 4px 10px;
    border-radius: 4px;
    display: inline-block;
    white-space: nowrap;
  }

  .status-protected {
    color: var(--ob-green-light);
    background: rgba(80,190,135,0.1);
    border: 1px solid rgba(80,190,135,0.15);
  }

  .status-partial {
    color: var(--orange-primary);
    background: rgba(255,121,0,0.1);
    border: 1px solid rgba(255,121,0,0.15);
  }

  .status-exposed {
    color: var(--ob-red);
    background: rgba(205,60,20,0.1);
    border: 1px solid rgba(205,60,20,0.15);
  }

  .threat-percent {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: var(--text-muted);
  }

  /* ── Stack Anatomy ── */
  .stack-section {
    opacity: 0;
    animation: fadeSlideUp 0.8s ease forwards 2s;
    margin-bottom: 72px;
  }

  .stack-visual {
    display: flex;
    flex-direction: column;
    gap: 3px;
  }

  .stack-layer {
    display: grid;
    grid-template-columns: 140px 1fr 180px;
    align-items: center;
    gap: 20px;
    padding: 16px 24px;
    border-radius: 6px;
    border: 1px solid var(--border-subtle);
    transition: all 0.3s ease;
  }

  .stack-layer:hover { border-color: var(--border-accent); }

  .stack-layer-name {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.5px;
    font-weight: 500;
  }

  .stack-layer-detail { font-size: 12.5px; color: var(--text-secondary); }

  .stack-origin {
    text-align: right;
    font-size: 11px;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 8px;
  }

  .origin-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    flex-shrink: 0;
  }

  .origin-eu { background: var(--ob-green-light); }
  .origin-us { background: var(--ob-red); }
  .origin-mixed { background: var(--orange-primary); }

  .origin-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.5px;
  }

  .eu-text { color: var(--ob-green-light); }
  .us-text { color: var(--ob-red); }
  .mixed-text { color: var(--orange-primary); }

  .sl-app { background: var(--layer-legal-bg); }
  .sl-app .stack-layer-name { color: var(--ob-green-light); }

  .sl-platform { background: var(--layer-ops-bg); }
  .sl-platform .stack-layer-name { color: var(--orange-primary); }

  .sl-virt { background: rgba(255,121,0,0.04); }
  .sl-virt .stack-layer-name { color: var(--orange-dark); }

  .sl-os { background: var(--layer-data-bg); }
  .sl-os .stack-layer-name { color: var(--ob-purple); }

  .sl-firmware { background: var(--layer-tech-bg); }
  .sl-firmware .stack-layer-name { color: var(--ob-red); }

  .sl-silicon { background: rgba(205,60,20,0.04); }
  .sl-silicon .stack-layer-name { color: #b83010; }

  .stack-legend {
    display: flex;
    gap: 24px;
    margin-top: 16px;
    justify-content: flex-end;
  }

  .legend-item {
    display: flex;
    align-items: center;
    gap: 6px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: var(--text-muted);
    letter-spacing: 0.5px;
  }

  /* ── Conclusion ── */
  .conclusion {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    padding: 40px 36px;
    position: relative;
    overflow: hidden;
    opacity: 0;
    animation: fadeSlideUp 0.8s ease forwards 2.2s;
  }

  .conclusion::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(to right, var(--orange-primary), var(--ob-green-light), var(--ob-purple), transparent 80%);
  }

  .conclusion-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--orange-primary);
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .conclusion-label::before {
    content: '';
    width: 12px;
    height: 12px;
    background: var(--orange-primary);
    border-radius: 2px;
    flex-shrink: 0;
  }

  .conclusion-text {
    font-family: 'Inter', sans-serif;
    font-size: clamp(21px, 2.8vw, 28px);
    line-height: 1.45;
    color: var(--text-primary);
    max-width: 820px;
    letter-spacing: -0.3px;
  }

  .conclusion-text em {
    font-style: italic;
    color: var(--orange-primary);
  }

  .conclusion-footer {
    margin-top: 24px;
    font-size: 13px;
    color: var(--text-muted);
    line-height: 1.7;
    max-width: 680px;
  }

  .tag {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    padding: 3px 8px;
    border-radius: 3px;
    vertical-align: middle;
    letter-spacing: 0.5px;
  }

  .tag-secnum {
    background: rgba(80,190,135,0.1);
    color: var(--ob-green-light);
    border: 1px solid rgba(80,190,135,0.15);
  }

  /* ── Watermark ── */
  .watermark {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    margin-top: 48px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    letter-spacing: 2px;
    color: var(--text-muted);
    opacity: 0.35;
    padding-top: 20px;
    border-top: 1px solid var(--border-subtle);
  }

  /* ── Animations ── */
  @keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(16px); }
    to { opacity: 1; transform: translateY(0); }
  }

  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }

  /* ── Responsive ── */
  @media (max-width: 768px) {
    .container { padding: 40px 20px 60px; }
    .layers-grid { grid-template-columns: 1fr; }
    .stack-layer { grid-template-columns: 100px 1fr 120px; padding: 12px 14px; }
    .threat-table { font-size: 12px; }
    .threat-table thead th,
    .threat-table tbody td { padding: 10px 8px; }
  }
</style>

<div class="brand-bar"></div>

<div class="container">

  <a class="back-to-blog" href="/blog/">&larr; BACK TO BLOG</a>

  <!-- Header -->
  <header class="header">
    <div class="header-label">An overview of sovereignty in 4 dimensions</div>
    <h1>The cloud <em>sovereignty</em> spectrum</h1>
    <p class="header-sub">We have to understand that "Sovereignty" is not a binary state. We can consider it as a continuum of control that can be designed into four dimensions, legal, operational, technological, and data, each with its own level of maturity.</p>
    <div class="header-line"></div>
  </header>

  <!-- Spectrum Bar -->
  <section class="spectrum-section">
    <div class="section-label">Maturity by dimension</div>
    <div class="spectrum-bar">
      <div class="spectrum-segment seg-legal">
        <span class="seg-name">Legal</span>
        <span class="seg-score">██████████ 90%</span>
      </div>
      <div class="spectrum-segment seg-ops">
        <span class="seg-name">Operational</span>
        <span class="seg-score">████████░░ 80%</span>
      </div>
      <div class="spectrum-segment seg-data">
        <span class="seg-name">Data</span>
        <span class="seg-score">███████░░░ 70%</span>
      </div>
      <div class="spectrum-segment seg-tech">
        <span class="seg-name">Technological</span>
        <span class="seg-score">███░░░░░░░ 25%</span>
      </div>
    </div>
    <div class="spectrum-labels">
      <span>&larr; STRONG CONTROL</span>
      <span>MANAGED DEPENDENCY &rarr;</span>
    </div>
  </section>

  <!-- Layer Cards -->
  <div class="layers-grid">

    <div class="layer-card card-legal">
      <div class="card-number">LAYER 01</div>
      <h3 class="card-title">Legal</h3>
      <p class="card-subtitle">Legal indirection as a shield</p>
      <p class="card-body">
        The operating entity is European, subject to GDPR and outside the direct reach of the CLOUD Act. A US court cannot serve a warrant directly to a European operator for data it controls on its own infrastructure. This is a real layer of legal indirection, the data controller remains European.
      </p>
      <div class="card-verdict verdict-strong">
        <div class="verdict-icon">&#10003;</div>
        <span class="verdict-text">Effective protection, SecNumCloud qualified</span>
      </div>
    </div>

    <div class="layer-card card-ops">
      <div class="card-number">LAYER 02</div>
      <h3 class="card-title">Operational</h3>
      <p class="card-subtitle">The keys are in European hands</p>
      <p class="card-body">
        European L1, L2, L3 teams, internal IAM, no SSH access required for Dell or VMware in production. Like a Rafale fighter jet with imported electronics, the French military has exclusive operational control. The component manufacturer has no hand on the missile.
      </p>
      <div class="card-verdict verdict-strong">
        <div class="verdict-icon">&#10003;</div>
        <span class="verdict-text">Real control, sovereign operations</span>
      </div>
    </div>

    <div class="layer-card card-data">
      <div class="card-number">LAYER 03</div>
      <h3 class="card-title">Data</h3>
      <p class="card-subtitle">Encryption and territorial residency</p>
      <p class="card-body">
        Data encrypted at rest and in transit, keys managed by the European operator, territorial residency guaranteed. Exploiting a hardware backdoor would require a state level supply chain attack, a threat model beyond 95% of commercial use cases.
      </p>
      <div class="card-verdict verdict-moderate">
        <div class="verdict-icon">&#9680;</div>
        <span class="verdict-text">Robust, residual hardware risk</span>
      </div>
    </div>

    <div class="layer-card card-tech">
      <div class="card-number">LAYER 04</div>
      <h3 class="card-title">Technological</h3>
      <p class="card-subtitle">Silicon doesn't lie about its origins</p>
      <p class="card-body">
        Intel ME, AMD PSP, iDRAC, BMC firmware, VMware hypervisor, the source code remains opaque. It's the same dilemma as macOS on Apple Silicon: the Secure Enclave relies on an ARM design whose full audit is structurally impossible.
      </p>
      <div class="card-verdict verdict-weak">
        <div class="verdict-icon">&#10007;</div>
        <span class="verdict-text">Unresolved dependency, global gap</span>
      </div>
    </div>

  </div>

  <!-- Threat Matrix -->
  <section class="threat-section">
    <div class="section-label">Threat matrix, European operator model</div>
    <table class="threat-table">
      <thead>
        <tr>
          <th>Threat</th>
          <th>Scenario</th>
          <th>Protection</th>
          <th>Relevance</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="threat-name">CLOUD Act warrant</td>
          <td class="threat-desc">Extraterritorial US legal request for data</td>
          <td><span class="threat-status status-protected">Protected</span></td>
          <td class="threat-percent">~ 95% of clients</td>
        </tr>
        <tr>
          <td class="threat-name">Mass surveillance</td>
          <td class="threat-desc">Passive data collection in transit or at rest</td>
          <td><span class="threat-status status-protected">Protected</span></td>
          <td class="threat-percent">~ 90% of clients</td>
        </tr>
        <tr>
          <td class="threat-name">Vendor lock in</td>
          <td class="threat-desc">Technical dependency, licensing leverage (Broadcom)</td>
          <td><span class="threat-status status-partial">Partial</span></td>
          <td class="threat-percent">~ 70% of clients</td>
        </tr>
        <tr>
          <td class="threat-name">Supply chain attack</td>
          <td class="threat-desc">State level firmware, microcode compromise</td>
          <td><span class="threat-status status-exposed">Exposed</span></td>
          <td class="threat-percent">&lt; 5% of clients</td>
        </tr>
        <tr>
          <td class="threat-name">Silicon backdoor</td>
          <td class="threat-desc">Intel ME, AMD PSP exploitation by a SIGINT agency</td>
          <td><span class="threat-status status-exposed">Exposed</span></td>
          <td class="threat-percent">&lt; 1% of clients</td>
        </tr>
      </tbody>
    </table>
  </section>

  <!-- Stack Anatomy -->
  <section class="stack-section">
    <div class="section-label">Stack anatomy, origin by layer</div>
    <div class="stack-visual">
      <div class="stack-layer sl-app">
        <span class="stack-layer-name">APPLICATION</span>
        <span class="stack-layer-detail">Client workloads, APIs, management portals</span>
        <span class="stack-origin">
          <span class="origin-label eu-text">EU operated</span>
          <span class="origin-dot origin-eu"></span>
        </span>
      </div>
      <div class="stack-layer sl-platform">
        <span class="stack-layer-name">PLATFORM</span>
        <span class="stack-layer-detail">Orchestration, IAM, monitoring, billing</span>
        <span class="stack-origin">
          <span class="origin-label eu-text">EU operated</span>
          <span class="origin-dot origin-eu"></span>
        </span>
      </div>
      <div class="stack-layer sl-virt">
        <span class="stack-layer-name">VIRTUALISATION</span>
        <span class="stack-layer-detail">VMware vSphere, vSAN, NSX (Broadcom)</span>
        <span class="stack-origin">
          <span class="origin-label mixed-text">US code, EU operated</span>
          <span class="origin-dot origin-mixed"></span>
        </span>
      </div>
      <div class="stack-layer sl-os">
        <span class="stack-layer-name">OS, KERNEL</span>
        <span class="stack-layer-detail">Linux (auditable open source), proprietary drivers</span>
        <span class="stack-origin">
          <span class="origin-label mixed-text">mixed, auditable</span>
          <span class="origin-dot origin-mixed"></span>
        </span>
      </div>
      <div class="stack-layer sl-firmware">
        <span class="stack-layer-name">FIRMWARE</span>
        <span class="stack-layer-detail">iDRAC, iLO, BMC, BIOS UEFI (Dell, HPE)</span>
        <span class="stack-origin">
          <span class="origin-label us-text">US origin</span>
          <span class="origin-dot origin-us"></span>
        </span>
      </div>
      <div class="stack-layer sl-silicon">
        <span class="stack-layer-name">SILICON</span>
        <span class="stack-layer-detail">Intel Xeon, AMD EPYC, ME, PSP opaque enclaves</span>
        <span class="stack-origin">
          <span class="origin-label us-text">US origin</span>
          <span class="origin-dot origin-us"></span>
        </span>
      </div>
    </div>
    <div class="stack-legend">
      <div class="legend-item"><span class="origin-dot origin-eu"></span> EU control</div>
      <div class="legend-item"><span class="origin-dot origin-mixed"></span> Mixed</div>
      <div class="legend-item"><span class="origin-dot origin-us"></span> US origin</div>
    </div>
  </section>

  <!-- Conclusion -->
  <div class="conclusion">
    <div class="conclusion-label">The bottom line</div>
    <p class="conclusion-text">
      <em>Operational and legal</em> sovereignty is credible and protects against the real-world threats faced by 95% of clients. <em>Technological</em> sovereignty remains a global gap that no commercial player fills today.
    </p>
    <p class="conclusion-footer">
      This is what the <span class="tag tag-secnum">SecNumCloud 3.2</span> label recognises, it qualifies operations and processes, not the origin of the silicon. The honest positioning: operational sovereignty with a managed technological dependency, governed through risk management.
    </p>
  </div>

  <!-- Watermark -->
  <div class="watermark">
    <span>Designed and crafted with &hearts; using HTML, CSS &amp; Jekyll &mdash; &copy; Anthony Chambet</span>
  </div>

</div>
