---
layout: post
title: "Anatomy of Hark"
date: 2026-09-30
tags: [Apple, macOS, Hark]
excerpt: "Hark is a menu bar app for the Mac. Press a key and speak: it types what you said at the cursor, opens the app you named, or, through a model server you run beside it, answers what you ask. This article takes it apart, part by part, with the measurements behind each decision."
---

<style>
  /* Diagram-only styles preserved from source — required for the SVG semantic colour coding. */
  figure { margin: 2rem 0; padding: 0; background: none; border: none; }
  figcaption { margin-top: 0.625rem; font-size: 0.85rem; color: #86868b; text-align: center; }
  .diagram { display: block; width: 100%; height: auto; }
  .diagram text { font-family: -apple-system, "SF Pro Text", "Helvetica Neue", Helvetica, Arial, sans-serif; }
  .diagram .t  { font-size: 14px; font-weight: 400; }
  .diagram .th { font-size: 14px; font-weight: 500; }
  .diagram .ts { font-size: 12px; font-weight: 400; }
  .diagram .t-amber  { fill: #633806; } .diagram .t-amber-s { fill: #92611e; }
  .diagram .t-teal   { fill: #085041; } .diagram .t-teal-s  { fill: #0f6e56; }
  .diagram .t-coral  { fill: #712b13; } .diagram .t-coral-s { fill: #993c1d; }
  .diagram .t-gray   { fill: #3a3a38; } .diagram .t-gray-s  { fill: #5f5e5a; }
  .diagram .t-ink    { fill: #2c2c2a; } .diagram .s-mut     { fill: #5f5e5a; }

  /* "to write" callout for Chapter 5 placeholder. */
  .todo {
    background: #f7f6f2; border: 1px dashed #d2cfc4; border-radius: 12px;
    padding: 1rem 1.25rem; margin: 1rem 0; color: #6e6e73; font-size: 0.95rem;
  }
  .todo .tag {
    display: inline-block; font-family: "SF Mono", Menlo, monospace; font-size: 0.7rem;
    letter-spacing: 0.04em; color: #9a7b1e; background: #faeeda; border-radius: 20px;
    padding: 0.1rem 0.5rem; margin-right: 0.5rem; vertical-align: middle;
  }
  .note { color: #6e6e73; font-style: italic; }

  /* Embedded screenshots — match the .ipsw working document styling. */
  figure img {
    display: block;
    width: 100%;
    height: auto;
    border-radius: 12px;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.10);
    border: 1px solid #ececec;
  }

  /* Window-only screenshots with transparent rounded corners: no frame, a shadow that follows the alpha. Width per image through --w. */
  figure img.window { width: auto; max-width: min(100%, var(--w, 620px)); margin: 0 auto; border: 0; border-radius: 0; box-shadow: none; filter: drop-shadow(0 6px 20px rgba(0, 0, 0, 0.22)); }
  /* Stacked screenshots in one figure. */
  figure > img.window + img.window { margin-top: 1rem; }
  /* HUD grid, one column on phones. */
  .hud-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 280px)); gap: 1rem 1.5rem; justify-content: center; }
  .hud-grid img.window { max-width: 280px; margin: 0; }
  /* Project diagrams keep the figure img frame; the link opens them full size. */
  figure a { display: block; }
  figure a img { cursor: zoom-in; }
  /* Captions and notes, readable in both schemes. */
  figcaption { color: #6e6e73; }
  /* Diagrams on a light card when the page is dark, so every label keeps its contrast. */
  @media (prefers-color-scheme: dark) {
    .diagram { background: #faf9f5; border-radius: 12px; }
    figcaption, .note { color: #a1a1a6; }
  }
  /* The drill diagram is framed tight; this keeps it at the same scale as the other diagrams. */
  figure.drill-diagram > svg.diagram { max-width: 497px; margin: 0 auto; }
  /* On phones, diagrams shrink to fit and run edge to edge, past the page margins. */
  @media (max-width: 600px) {
    figure > svg.diagram, figure.drill-diagram > svg.diagram { width: calc(100% + 2.5rem); max-width: none; margin-left: -1.25rem; border-radius: 0; }
  }
  /* Short inline code never breaks at a hyphen. */
  article p code, article li code { white-space: nowrap; }
</style>

<h2>Context</h2>
<p>I've started to design Hark as a menu bar app for the Mac first. Where you can press a key and speak. It types what you said at the cursor, opens the app you named, or, through a model server you run beside it, answers what you ask according to your context. The speech is transcribed on the Mac, by whisper.cpp, a C and C++ implementation of OpenAI's Whisper speech model so far in EU more accurate and also faster than the free DCMA dictation feature on MacOS/iOS. The audio never leaves the Mac, it's the second fundamental point that I wanted to bring here a text to speech that respect privacy. The text lands a little over a tenth of a second after key up, by a sum of parts measured separately, and the app measured about half a gigabyte of memory.</p>
<p>Hark works like a "power tool". The key is the trigger. Hold it and Hark listens. Let go and it does one precise job, then stops. A quick tap locks it on, until the next tap. Its icon is a cordless drill. It is a tool you pick up on purpose, to open one app or write into one text field, then put down. It is not an assistant that is always listening, waiting to be called.</p>
<p></p>
<p>Why the voice? Voice is the most natural way of transferring information, since the beginning of human history, we started to speak, communicate between each other over the most natural way, the language over the voice. And I always wonder to build a product that brings natural human fundamentals and empowering it with technology. There is also an ambition to bring AI close to the human and their work rather than bring them close to AI and adapt their work to technology.</p>
<p>A good product always start by fitting to the current workflow and bring solution rather to adapt yourself to fix your problems.</p>
<figure>
<img class="window" style="--w:128px" src="{{ '/assets/images/anatomy-hark/00-icon.png' | relative_url }}" alt="Hark's app icon, a white cordless drill on a yellow rounded square">
<figcaption>The app icon, unchanged since the first public release, 0.0.2: a white cordless drill on a yellow rounded square, with its grip, battery, chuck and bit. One tool, one job.</figcaption>
</figure>
<p>I always liked Cydia and the jailbreak scene on iOS back in the past. Most of you who is familiar with this culture knows that this drill logo comes from the different tweaks available in Cydia. The drill means many different things, but I always wanted to tweak my way of using my laptop. Despite my technical knowledge is limited (I do not build tweaks...), this animated with curiosity combined with a bit of old school taste, I came to this idea of choosing this logo.</p>
<p>This article takes Hark apart, following one sentence from the key to the cursor. For each part it shows how it is built, why, and what it costs in milliseconds and memory. Five threads run through it:</p>
<ul>
  <li><strong>The architecture choices</strong>. The six parts come first, and chapter 1 shows what holds them together.</li>
  <li><strong>The wait kept short</strong>. The logic behind a sentence adds it up, and chapter 3 makes its largest part small.</li>
  <li><strong>A speech model in little memory</strong>. Chapter 3 keeps Whisper loaded all day, and chapter 6 keeps the language model out of the process.</li>
  <li><strong>A tool each person shapes (by expressing themselve in the most natural way for breaking AI struggles)</strong>. Chapter 4 sets the rules, and chapter 7 hands them over.</li>
  <li><strong>The problems that shaped it</strong>. Each is told where it bites, and Appendix B lists them by date.</li>
</ul>
<p>The running example here is Hark 0.0.4 on a MacBook Pro with an Apple M5 Pro and 64 GB of memory (bought it before mem crisis I feel lucky). Hark is set as a fresh install leaves it: the Small model, the Neural Engine off, the language detected, the live transcript off. The sentence is "The meeting moves to Thursday at ten, same room.", about five seconds on the key, into a Mail draft. Every measurement in this article comes from that one Mac, taken between 18 and 29 September 2026 on the builds that led to 0.0.4, under macOS 27.0 and then 27.2. Each number names its conditions.</p>
<p>The screenshots show a sample log, and no real dictation appears in them. Where one shows something not yet released, the caption says so.</p>
<p>The document is built to grow, as Hark does.</p>
<p class="note">One last detail. The model that does the listening cannot spell the product's name. Whisper writes the nearest word in its vocabulary, and a French voice saying "Hark" comes back as "arc" far more often than as "Hark". So Hark answers to a short list of spellings of its own name, written out, never guessed. The list has a price, and chapter 4 names it: a sentence that really starts with "Arc" goes to the assistant.</p>

<h2>The six parts</h2>
<p>Hark is one process on the Mac, a menu bar app with no Dock icon, for macOS 14 or later on a Mac with Apple silicon, built in Swift. It splits into six parts. What sets them apart first is what each may touch: the speech model, your rules, another app, or something outside the process.</p>

<figure>
<svg class="diagram" viewBox="0 0 680 440" role="img" xmlns="http://www.w3.org/2000/svg">
<title>The six parts of Hark, and what sits beside them</title>
<desc>One Hark process holds six parts: the pipeline, capture, transcription by the whisper.cpp speech model, the decision, delivery and the Ask Hark client. Beside it sit commands.yaml, a model server for Ask in a separate process, and huggingface.co for the model downloads you start.</desc>
<rect x="40" y="44" width="600" height="252" rx="16" fill="none" stroke="#c4c2b8" stroke-width="1" stroke-dasharray="6 4"/>
<text class="th t-ink" x="60" y="70">Hark · one menu bar process</text>
<text class="ts s-mut" x="60" y="88">on this Mac · Apple silicon · macOS 14 or later</text>

<rect x="60" y="104" width="176" height="80" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="148" y="130" text-anchor="middle">Pipeline</text>
<text class="ts t-gray-s" x="148" y="150" text-anchor="middle">one state machine</text>
<text class="ts t-gray-s" x="148" y="168" text-anchor="middle">one log line each</text>

<rect x="252" y="104" width="176" height="80" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="340" y="130" text-anchor="middle">Capture</text>
<text class="ts t-gray-s" x="340" y="150" text-anchor="middle">key · microphone · HUD</text>
<text class="ts t-gray-s" x="340" y="168" text-anchor="middle">mic open while you speak</text>

<rect x="444" y="104" width="176" height="80" rx="10" fill="#faeeda" stroke="#854f0b" stroke-width="1"/>
<text class="th t-amber" x="532" y="130" text-anchor="middle">Transcription</text>
<text class="ts t-amber-s" x="532" y="150" text-anchor="middle">whisper.cpp · Small</text>
<text class="ts t-amber-s" x="532" y="168" text-anchor="middle">Metal GPU · on this Mac</text>

<rect x="60" y="200" width="176" height="80" rx="10" fill="#e1f5ee" stroke="#0f6e56" stroke-width="1"/>
<text class="th t-teal" x="148" y="226" text-anchor="middle">Decision</text>
<text class="ts t-teal-s" x="148" y="246" text-anchor="middle">text, command or ask</text>
<text class="ts t-teal-s" x="148" y="264" text-anchor="middle">reads your rules</text>

<rect x="252" y="200" width="176" height="80" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="340" y="226" text-anchor="middle">Delivery</text>
<text class="ts t-coral-s" x="340" y="246" text-anchor="middle">Accessibility · paste</text>
<text class="ts t-coral-s" x="340" y="264" text-anchor="middle">checked, else clipboard</text>

<rect x="444" y="200" width="176" height="80" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="532" y="226" text-anchor="middle">Ask Hark</text>
<text class="ts t-gray-s" x="532" y="246" text-anchor="middle">one streaming request</text>
<text class="ts t-gray-s" x="532" y="264" text-anchor="middle">only when you ask</text>

<rect x="60" y="316" width="176" height="80" rx="10" fill="#e1f5ee" stroke="#0f6e56" stroke-width="1"/>
<text class="th t-teal" x="148" y="342" text-anchor="middle">commands.yaml</text>
<text class="ts t-teal-s" x="148" y="362" text-anchor="middle">verbs · apps · servers</text>
<text class="ts t-teal-s" x="148" y="380" text-anchor="middle">reloaded when saved</text>

<rect x="252" y="316" width="176" height="80" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1" stroke-dasharray="5 4"/>
<text class="th t-coral" x="340" y="342" text-anchor="middle">Model server</text>
<text class="ts t-coral-s" x="340" y="362" text-anchor="middle">separate process</text>
<text class="ts t-coral-s" x="340" y="380" text-anchor="middle">127.0.0.1 by default</text>

<rect x="444" y="316" width="176" height="80" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1" stroke-dasharray="5 4"/>
<text class="th t-coral" x="532" y="342" text-anchor="middle">huggingface.co</text>
<text class="ts t-coral-s" x="532" y="362" text-anchor="middle">downloads you start</text>
<text class="ts t-coral-s" x="532" y="380" text-anchor="middle">pinned · SHA-256</text>

<rect x="60" y="412" width="16" height="16" rx="3" fill="#faeeda" stroke="#854f0b" stroke-width="1"/>
<text class="ts s-mut" x="84" y="424">Speech model</text>
<rect x="210" y="412" width="16" height="16" rx="3" fill="#e1f5ee" stroke="#0f6e56" stroke-width="1"/>
<text class="ts s-mut" x="234" y="424">Yours to shape</text>
<rect x="360" y="412" width="16" height="16" rx="3" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="ts s-mut" x="384" y="424">Boundary or check</text>
<rect x="510" y="412" width="16" height="16" rx="3" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="ts s-mut" x="534" y="424">Plumbing</text>
</svg>
<figcaption>The six parts of Hark, and what sits beside them.</figcaption>
</figure>

<ul>
  <li><strong>Pipeline</strong> (<code>Pipeline/</code>, <code>Logging/</code>). One state machine. Each utterance, one press of a key from key down to its end, leaves one log line. Chapter 1.</li>
  <li><strong>Capture</strong> (<code>Audio/</code>). The keys, the microphone, and the HUD (heads-up display), the small recording window that never takes the keyboard. Chapter 2.</li>
  <li><strong>Transcription</strong> (<code>Transcription/</code>, <code>Models/</code>). whisper.cpp on the GPU. The Neural Engine, the part of Apple silicon built for machine learning, is an option. Chapter 3.</li>
  <li><strong>Decision</strong> (<code>Commands/</code>). Text, a command, or a question. Chapter 4.</li>
  <li><strong>Delivery</strong> (<code>Focus/</code>, <code>Insertion/</code>). The cursor, or the clipboard with a reason. Chapter 5.</li>
  <li><strong>Ask Hark</strong> (<code>Ask/</code>). A client for a model server that runs beside Hark, not inside it. Chapter 6.</li>
</ul>
<p>Beside them sits one file you edit, <code>commands.yaml</code>, covered in chapter 7.</p>
<p>I always liked to use very simple information to understand complex things. That's why I decided to choose the colors codes. So they keep one meaning each, here and in every diagram that follows. Amber is the speech model at work, the only neural network inside the process. Teal is what is yours to shape. Coral is a boundary or a check: delivery, which writes into another app and verifies it, and anything outside the process. Gray is plumbing. Chapter 1 shows the check that enforces what each part may touch.</p>
<p>Two things cross the edge of the process, and both wait for you. The first is a model download you start, from huggingface.co and its hf.co storage, at a pinned commit, checked against its SHA-256 hash: the app ships with no speech model. The second is the model server for Ask, a separate process, at <code>127.0.0.1</code> by default. A sentence you dictate never waits on either.</p>

<h3>Seeing the "six"</h3>
<p>Click the menu bar icon, and the panel, the window that drops from it, shows all six parts at once, here over a sample log.</p>
<figure>
<img class="window" style="--w:360px" src="{{ '/assets/images/anatomy-hark/01-panel.png' | relative_url }}" alt="Hark's menu bar panel with its status line, the last result and four recent ones">
<figcaption>The panel, over a sample log. Status: <code>Micro MacBook Pro</code>, the built-in microphone's French name, then Small and <code>● Ask</code>, green when the server answers. The last result, a sample 460 ms, then Ask, Text, Text, Command. Six parts, one glance.</figcaption>
</figure>
<p>Every part has a place on it. The status line holds three: the microphone, the model and the green dot for Ask. The last result says where delivery put it, and each row, read back from the log, what the decision made of it.</p>
<p>The panel is the summary. The Log tab is the record.</p>
<figure>
<img class="window" style="--w:520px" src="{{ '/assets/images/anatomy-hark/02-settings-log.png' | relative_url }}" alt="Settings, Log tab, listing six sample utterances with outcome, app, time and model">
<figcaption>Settings › Log, over the same sample log. Each row: when, how it ended, the app, the transcription time, the model. At 11:20, an ask adds the model's time. At 11:05, the running example, in Mail. Sample values.</figcaption>
</figure>
<p>Settings has seven tabs, and they follow the parts: each chapter names the one it uses.</p>
<p>The row at 11:05 is the running example.</p>

<h2>The logic behind a sentence</h2>
<p>The six parts follow the sentence, in seven steps. Each part serves one or more of them.</p>

<figure>
<svg class="diagram" viewBox="0 0 680 640" role="img" xmlns="http://www.w3.org/2000/svg">
<title>The logic behind a sentence</title>
<desc>Seven steps from key down to one log line: key down, the microphone opens, key up, transcribe, resolve, deliver and check, one log line. A focus probe starts at key down beside the capture and is ready for resolve by key up. The time each step takes runs down the right.</desc>
<defs>
<marker id="arr-f04" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#5f5e5a" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
</defs>

<rect x="180" y="40" width="320" height="56" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="340" y="58" text-anchor="middle" dominant-baseline="central">Key down</text>
<text class="ts t-gray-s" x="340" y="76" text-anchor="middle" dominant-baseline="central">⌃⌥V · capture and probe start together</text>
<line x1="340" y1="99" x2="340" y2="122" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f04)"/>

<rect x="180" y="124" width="320" height="56" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="340" y="142" text-anchor="middle" dominant-baseline="central">Microphone opens</text>
<text class="ts t-gray-s" x="340" y="160" text-anchor="middle" dominant-baseline="central">one session · 16 kHz mono · RAM only</text>
<line x1="340" y1="183" x2="340" y2="206" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f04)"/>

<rect x="180" y="208" width="320" height="56" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="340" y="226" text-anchor="middle" dominant-baseline="central">Key up</text>
<text class="ts t-gray-s" x="340" y="244" text-anchor="middle" dominant-baseline="central">the end of speech · the HUD leaves</text>
<line x1="340" y1="267" x2="340" y2="290" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f04)"/>

<rect x="180" y="292" width="320" height="56" rx="10" fill="#faeeda" stroke="#854f0b" stroke-width="1"/>
<text class="th t-amber" x="340" y="310" text-anchor="middle" dominant-baseline="central">Transcribe</text>
<text class="ts t-amber-s" x="340" y="328" text-anchor="middle" dominant-baseline="central">Whisper Small · on the GPU</text>
<line x1="340" y1="351" x2="340" y2="374" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f04)"/>

<rect x="180" y="376" width="320" height="56" rx="10" fill="#e1f5ee" stroke="#0f6e56" stroke-width="1"/>
<text class="th t-teal" x="340" y="394" text-anchor="middle" dominant-baseline="central">Resolve</text>
<text class="ts t-teal-s" x="340" y="412" text-anchor="middle" dominant-baseline="central">your rules · text, command or ask</text>
<line x1="340" y1="435" x2="340" y2="458" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f04)"/>

<rect x="180" y="460" width="320" height="56" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="340" y="478" text-anchor="middle" dominant-baseline="central">Deliver, and check</text>
<text class="ts t-coral-s" x="340" y="496" text-anchor="middle" dominant-baseline="central">Accessibility, else ⌘V, else clipboard</text>
<line x1="340" y1="519" x2="340" y2="542" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f04)"/>

<rect x="180" y="544" width="320" height="56" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="340" y="562" text-anchor="middle" dominant-baseline="central">One log line</text>
<text class="ts t-gray-s" x="340" y="580" text-anchor="middle" dominant-baseline="central">13 keys · then back to idle</text>

<rect x="24" y="124" width="140" height="56" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1" stroke-dasharray="5 4"/>
<text class="th t-gray" x="94" y="142" text-anchor="middle" dominant-baseline="central">Focus probe</text>
<text class="ts t-gray-s" x="94" y="160" text-anchor="middle" dominant-baseline="central">app · field · secure</text>
<path d="M180 68 L94 68 L94 122" stroke="#5f5e5a" stroke-width="1.5" fill="none" stroke-dasharray="5 4" marker-end="url(#arr-f04)"/>
<path d="M94 180 L94 404 L178 404" stroke="#5f5e5a" stroke-width="1.5" fill="none" stroke-dasharray="5 4" marker-end="url(#arr-f04)"/>
<text class="ts t-gray-s" x="86" y="290" text-anchor="end">ready</text>
<text class="ts t-gray-s" x="86" y="306" text-anchor="end">by key up</text>

<text class="ts t-gray-s" x="512" y="68" dominant-baseline="central">t = 0</text>
<text class="ts t-gray-s" x="512" y="152" dominant-baseline="central">76–88 ms to start</text>
<text class="ts t-gray-s" x="512" y="236" dominant-baseline="central">stop 17–24 ms</text>
<text class="ts t-gray-s" x="512" y="320" dominant-baseline="central">76 ms · 5.7 s clip</text>
<text class="ts t-gray-s" x="512" y="404" dominant-baseline="central">in memory</text>
<text class="ts t-gray-s" x="512" y="480" dominant-baseline="central">AX ≤ 0.25 s a call</text>
<text class="ts t-gray-s" x="512" y="496" dominant-baseline="central">paste read ≤ 1 s</text>
<text class="ts t-gray-s" x="512" y="572" dominant-baseline="central">one write(2)</text>

<text class="ts s-mut" x="340" y="628" text-anchor="middle">measured on this Mac, step by step · decode: Small q8_0, Metal, language fixed</text>
</svg>
<figcaption>The logic behind a sentence.</figcaption>
</figure>

<p>The sentence starts with a press of the dictation key, Control-Option-V (⌃⌥V) by default. Two things start at that instant: the capture, and a focus probe that asks macOS which app and which field are in front. Recording does not wait for the probe, so the probe costs the capture nothing. For the running example, the probe has found a Mail draft long before key up.</p>
<p>The microphone opens one session for this press. It delivers 16 kHz mono samples, kept in memory and never written to disk. Key up is the end of speech. No voice detector waits out 300 to 700 ms of trailing silence to guess that you stopped. The release says so, and the HUD leaves.</p>
<p>The amber box is Whisper, transcribing the clip. Resolve, in teal, reads your rules and picks text, a command or an ask. The running example opens with "The", not a verb or the name, so it is text. Deliver, in coral, writes into another app, then checks. For a Mail draft that means a paste, which counts only once Mail reads it. Every path ends in one log line.</p>

<h3>Where the milliseconds go</h3>
<p>You feel one wait: from letting go of the key to the text in Mail. The focus probe and the HUD's 120 ms fade, given in chapter 2, run while you speak and add nothing after key up. The microphone is the exception, at the start: its first sample lands 90 to 100 ms after the press, and sound before it is not recorded. Whether that clips a quick first syllable was not measured.</p>
<p>After key up, the wait is a short chain. The microphone stops in 17 to 24 ms. Then Whisper decodes the clip on the GPU, through Metal, Apple's GPU interface. The nearest measurement to the running example is a synthesized 5.7 s sentence on Small <code>q8_0</code>, its 8-bit build: 76 ms, the median of 8 runs after one discarded warm-up, with the language fixed to English. Whisper does the same amount of work for both clips, for a reason chapter 3 explains.</p>
<p>The rest is small, and untimed. Resolve runs in memory, the paste is read in milliseconds by the code's own account, and the log line is one <code>write(2)</code>.</p>

<figure>
<svg class="diagram" viewBox="0 0 680 316" role="img" xmlns="http://www.w3.org/2000/svg">
<title>Key up to text, added up from measured parts</title>
<desc>A timeline from key up, 0 to 160 ms. The microphone stops in 17 to 24 ms, the decode takes 76 ms, then resolve, the paste read and the log line take a few milliseconds each, about 100 to 110 ms in all as a sum of parts measured separately. The HUD's 120 ms fade-out runs beside it. Before key up, the microphone, the focus and the model are already ready.</desc>
<defs>
<marker id="arr-f05" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#993c1d" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
</defs>

<text class="th t-ink" x="40" y="60">While you speak</text>
<text class="ts s-mut" x="40" y="80">audio from 90–100 ms</text>
<text class="ts s-mut" x="40" y="96">focus known</text>
<text class="ts s-mut" x="40" y="112">model warm</text>

<line x1="180" y1="52" x2="180" y2="250" stroke="#c4c2b8" stroke-width="1" stroke-dasharray="6 4"/>


<text class="ts t-gray-s" x="184" y="72">stop · 17–24 ms</text>
<text class="ts t-gray-s" x="452" y="58">resolve, paste read, log</text>
<text class="ts t-gray-s" x="452" y="72">not timed · widths schematic</text>

<rect x="180" y="80" width="66" height="36" rx="4" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<rect x="246" y="80" width="209" height="36" rx="4" fill="#faeeda" stroke="#854f0b" stroke-width="1"/>
<text class="th t-amber" x="350" y="98" text-anchor="middle" dominant-baseline="central">decode · 76 ms</text>
<rect x="455" y="80" width="6" height="36" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<rect x="461" y="80" width="14" height="36" fill="none" stroke="#5f5e5a" stroke-width="1"/>
<rect x="475" y="80" width="3" height="36" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>

<path d="M180 124 L180 130 L478 130 L478 124" stroke="#5f5e5a" stroke-width="1" fill="none"/>
<text class="ts t-gray-s" x="329" y="148" text-anchor="middle">≈ 100–110 ms · a sum of parts measured separately</text>

<rect x="180" y="172" width="330" height="22" rx="4" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="ts t-gray-s" x="345" y="183" text-anchor="middle" dominant-baseline="central">HUD fades out · 120 ms</text>

<text class="ts t-coral-s" x="630" y="216" text-anchor="end">target: p95 under 1.5 s, off this scale</text>
<line x1="636" y1="212" x2="662" y2="212" stroke="#993c1d" stroke-width="1.5" fill="none" marker-end="url(#arr-f05)"/>
<text class="ts t-coral-s" x="660" y="234" text-anchor="end">a model before each sentence: +0.3–0.6 s, an estimate, refused</text>

<line x1="180" y1="250" x2="620" y2="250" stroke="#5f5e5a" stroke-width="1"/>
<line x1="180" y1="250" x2="180" y2="256" stroke="#5f5e5a" stroke-width="1"/>
<line x1="290" y1="250" x2="290" y2="256" stroke="#5f5e5a" stroke-width="1"/>
<line x1="400" y1="250" x2="400" y2="256" stroke="#5f5e5a" stroke-width="1"/>
<line x1="510" y1="250" x2="510" y2="256" stroke="#5f5e5a" stroke-width="1"/>
<line x1="620" y1="250" x2="620" y2="256" stroke="#5f5e5a" stroke-width="1"/>
<text class="ts s-mut" x="180" y="272" text-anchor="middle">key up</text>
<text class="ts s-mut" x="290" y="272" text-anchor="middle">40 ms</text>
<text class="ts s-mut" x="400" y="272" text-anchor="middle">80 ms</text>
<text class="ts s-mut" x="510" y="272" text-anchor="middle">120 ms</text>
<text class="ts s-mut" x="620" y="272" text-anchor="middle">160 ms</text>

<text class="ts s-mut" x="340" y="292" text-anchor="middle">measured on this Mac, M5 Pro · decode: Small q8_0, Metal, 5.7 s sentence, 512 states</text>
<text class="ts s-mut" x="340" y="308" text-anchor="middle">language fixed in the benchmark · no end-to-end measurement exists</text>
</svg>
<figcaption>Key up to text, added up from measured parts.</figcaption>
</figure>

<p>Added up, the chain comes to about 100 to 110 ms from key up to text. That is a sum of parts measured separately. No end-to-end measurement exists: the timer planned for it was never built. The log does not close the gap either. Its <code>transcribe_ms</code> times the whole engine call, queue waits included, not the decode alone.</p>
<p>By the sum of its parts, with the language fixed, the text lands at about the moment the HUD's 120 ms fade-out ends. The running example detects the language, which costs Whisper an extra pass. On short synthesized requests, detection added 24 ms to the median decode in English, which puts the running example near 125 to 135 ms. That is an estimate, and chapter 3 gives the measurements.</p>
<p>For scale, the project's target was under 1.5 s at the 95th percentile, for a five-second sentence. A language model routing every sentence would have added 0.3 to 0.6 s, by the project's own estimate, and needed the model server running before you could type a word. That design was refused, and chapter 7 comes back to it.</p>
<p>The honest summary: most of the wait is one decode, and chapter 3 is about making it small.</p>

<h2>Chapter 1: The pipeline</h2>
<p>The six parts need a conductor. Every utterance, whatever it becomes, runs through one state machine: one stage at a time, one way in, one way out, and one line in a log at the end.</p>

<h3>Presses at the wrong moment</h3>
<p>You press the dictation key again while a sentence is still being transcribed. You cancel, and the transcript lands anyway. Or Whisper finishes before Hark knows which field has focus.</p>
<p>Each case still ends cleanly. A press while busy is its own utterance, logged as <code>busy</code> at once, and the one in progress carries on. A result for an utterance that already ended is rejected.</p>
<p>The mechanism is a reducer, a pure function from a state and an event to the next state. <code>reduce(state, event)</code> reads no clock and does no I/O. It returns the new state and a list of effects: start the microphone, transcribe, insert. The controller, a Swift actor that handles one message at a time, runs each effect in its own task. The result comes back as an event, and the controller never waits, so a second press is handled at once.</p>
<p>So a press can arrive at the wrong moment and still end in exactly one line. That is what the state machine buys.</p>

<h3>One state machine</h3>
<p>The states are the seven steps, now named: <code>idle</code>, <code>capturing</code>, <code>transcribing</code>, <code>resolving</code>. Then one of three endings, <code>acting</code>, <code>inserting</code> or <code>copying</code>, and back to <code>idle</code>.</p>
<p>Version 0.0.3 added <code>asking</code>, with its stages: <code>generating</code>, <code>reviewing</code>, <code>replacing</code> and <code>failed</code>. An ask is known from the start, by the key or menu that began it, and goes to <code>asking</code> straight after its transcript. Only a dictation that opens with "Hark, …" turns into one later, at <code>resolving</code>. Chapter 6 covers it.</p>
<p>Some utterances never reach Whisper: too short or too quiet, they end as <code>too_short</code> or <code>no_speech</code>, at the gates of chapter 2. An insert that fails does not lose the text: the machine falls to <code>copying</code>, with a reason.</p>
<p>One state, <code>confirming</code>, is wired and tested and never entered: no command asks first. Every ending has a name the log can write, one of 27 failure codes or 10 discard reasons. The 62 legal and 28 illegal dictation transitions are tested from tables, and asks have tables of their own, so a change nobody planned fails a test.</p>

<figure>
<svg class="diagram" viewBox="0 0 680 480" role="img" xmlns="http://www.w3.org/2000/svg">
<title>One utterance, one path, one log line</title>
<desc>An utterance moves from idle to capturing at key down, to transcribing at key up, to resolving once the transcript is in, then to acting, inserting or copying; a failed insert falls back to copying. An ask branches to asking, through generating, reviewing and replacing. Every ending writes one log line and returns to idle.</desc>
<defs>
<marker id="arr-f06" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#5f5e5a" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
</defs>

<text class="ts t-gray-s" x="178" y="30" text-anchor="middle">key down</text>
<text class="ts t-gray-s" x="334" y="30" text-anchor="middle">key up</text>
<text class="ts t-gray-s" x="490" y="30" text-anchor="middle">transcript</text>

<rect x="40" y="40" width="120" height="56" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="100" y="59" text-anchor="middle" dominant-baseline="central">idle</text>
<text class="ts t-gray-s" x="100" y="77" text-anchor="middle" dominant-baseline="central">mic closed</text>
<line x1="162" y1="68" x2="192" y2="68" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f06)"/>

<rect x="196" y="40" width="120" height="56" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="256" y="59" text-anchor="middle" dominant-baseline="central">capturing</text>
<text class="ts t-gray-s" x="256" y="77" text-anchor="middle" dominant-baseline="central">mic + focus probe</text>
<line x1="318" y1="68" x2="348" y2="68" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f06)"/>

<rect x="352" y="40" width="120" height="56" rx="10" fill="#faeeda" stroke="#854f0b" stroke-width="1"/>
<text class="th t-amber" x="412" y="59" text-anchor="middle" dominant-baseline="central">transcribing</text>
<text class="ts t-amber-s" x="412" y="77" text-anchor="middle" dominant-baseline="central">one decode</text>
<line x1="474" y1="68" x2="504" y2="68" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f06)"/>

<rect x="508" y="40" width="120" height="56" rx="10" fill="#e1f5ee" stroke="#0f6e56" stroke-width="1"/>
<text class="th t-teal" x="568" y="59" text-anchor="middle" dominant-baseline="central">resolving</text>
<text class="ts t-teal-s" x="568" y="77" text-anchor="middle" dominant-baseline="central">your rules</text>

<line x1="568" y1="100" x2="150" y2="156" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f06)"/>
<line x1="568" y1="100" x2="342" y2="156" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f06)"/>
<line x1="568" y1="100" x2="534" y2="156" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f06)"/>

<rect x="60" y="160" width="176" height="56" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="148" y="179" text-anchor="middle" dominant-baseline="central">acting</text>
<text class="ts t-gray-s" x="148" y="197" text-anchor="middle" dominant-baseline="central">open the app · 15 s max</text>

<rect x="252" y="160" width="176" height="56" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="340" y="179" text-anchor="middle" dominant-baseline="central">inserting</text>
<text class="ts t-gray-s" x="340" y="197" text-anchor="middle" dominant-baseline="central">at the cursor · ch. 5</text>

<rect x="444" y="160" width="176" height="56" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="532" y="179" text-anchor="middle" dominant-baseline="central">copying</text>
<text class="ts t-coral-s" x="532" y="197" text-anchor="middle" dominant-baseline="central">clipboard, with a reason</text>

<path d="M340 220 L340 230 L532 230 L532 222" stroke="#5f5e5a" stroke-width="1.5" fill="none" stroke-dasharray="5 4" marker-end="url(#arr-f06)"/>
<text class="ts t-gray-s" x="436" y="248" text-anchor="middle">a failed insert falls back to copying</text>

<path d="M632 68 L654 68 L654 300 L624 300" stroke="#5f5e5a" stroke-width="1.5" fill="none" stroke-dasharray="5 4" marker-end="url(#arr-f06)"/>
<text class="ts t-coral-s" x="648" y="244" text-anchor="end">an ask</text>

<rect x="60" y="262" width="560" height="116" rx="14" fill="none" stroke="#993c1d" stroke-width="1" stroke-dasharray="6 4"/>
<text class="th t-coral" x="80" y="286">asking</text>
<text class="ts t-coral-s" x="80" y="304">Ask key · Services · "Hark, …" · ch. 6</text>

<rect x="85" y="316" width="150" height="44" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="160" y="330" text-anchor="middle" dominant-baseline="central">generating</text>
<text class="ts t-gray-s" x="160" y="348" text-anchor="middle" dominant-baseline="central">the server streams</text>
<line x1="239" y1="338" x2="259" y2="338" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f06)"/>

<rect x="265" y="316" width="150" height="44" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="340" y="330" text-anchor="middle" dominant-baseline="central">reviewing</text>
<text class="ts t-gray-s" x="340" y="348" text-anchor="middle" dominant-baseline="central">yours to edit</text>
<line x1="419" y1="338" x2="439" y2="338" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f06)"/>

<rect x="445" y="316" width="150" height="44" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="520" y="330" text-anchor="middle" dominant-baseline="central">replacing</text>
<text class="ts t-gray-s" x="520" y="348" text-anchor="middle" dominant-baseline="central">selection checked</text>

<rect x="40" y="394" width="600" height="40" rx="12" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="340" y="414" text-anchor="middle" dominant-baseline="central">Every ending writes one log line, then idle</text>

<text class="ts s-mut" x="340" y="462" text-anchor="middle">early exits: too short (&lt; 250 ms) · no speech (RMS &lt; 0.01) · empty · cancelled · busy</text>
</svg>
<figcaption>One utterance, one path, one log line.</figcaption>
</figure>

<h3>The drill in the menu bar</h3>
<p>The HUD leaves at key up imo. The work goes on, and the menu bar icon shows it. But like in a subtle way. I always liked design that is soft tool where you have to pay attention to the details to see them and this brings a form of expression in your software and products without disturbing the user experience. The key is to find the great balance and for an application that fits in the status bar, Its simplicity is a form of paradox of complexity.The icon is the state machine made visible, one form of the app icon's drill per state. It is a design in progress: the forms are drawn, but the animations are not yet wired into the app, and none of it is released. 0.0.4 still shows a waveform there.</p>
<p>Key down pulls the trigger. The drill is filled while the microphone is open, and kicks up once as the capture starts. A dot beside it means the press has latched, the tap of chapter 2.</p>
<p>So after key up, only the drill's battery stays filled, and the drill dims, while Whisper transcribes and the action runs. If that takes longer than 300 ms, the bit turns too: marks pass above and below it, one turn every 1.2 s. The delay keeps a short dictation from flickering. By the sum of its parts, the running example is done well within those 300 ms, so its bit never turns. An ask shows a sparkle beside the battery until the Ask panel closes, and the bit turns while the answer is written.</p>
<p>An utterance that fails shows a cross for a second, and the drill shakes left and right with it, the way the Mac's login window shakes at a wrong password. One that came to nothing, too short or silent, shows the cross without the shake. A cancel shows nothing, since you did it yourself.</p>
<figure class="drill-diagram">
<svg class="diagram" viewBox="134 22 412 412" role="img" xmlns="http://www.w3.org/2000/svg">
<title>The drill follows the pipeline</title>
<desc>The menu bar drill in four forms: an outline at rest; filled, with one kick at key down, while the microphone is open; dimmed with only the battery filled while Hark works, the bit turning once the work passes 300 ms; and, when an utterance fails, a cross that shakes left and right with the drill.</desc>
<defs><marker id="arr-f06b" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#5f5e5a" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>
<rect x="160" y="40" width="360" height="56" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<g transform="translate(176 44) scale(2.8)" fill="none" stroke="#3a3a38" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"><path d="M5.5 11.5L6.5 7.5L5.5 7.5A2 2 0 0 1 5.5 3.5L12.5 3.5L12.5 7.5L9.5 7.5L8.5 11.5"/><rect x="3.5" y="11.5" width="7" height="3" rx="1"/><path d="M12.5 4L13.8 4L14.4 4.6L14.4 6.4L13.8 7L12.5 7Z" fill="#3a3a38" stroke="none"/><path d="M14.4 5.5L16.2 5.5"/></g>
<text class="th t-gray" x="236" y="60" dominant-baseline="central">At rest</text>
<text class="ts t-gray-s" x="236" y="78" dominant-baseline="central">the drill in outline, between presses</text>
<line x1="340" y1="100" x2="340" y2="126" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f06b)"/>
<text class="ts s-mut" x="352" y="115" dominant-baseline="central">key down</text>
<rect x="160" y="136" width="360" height="56" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<g transform="translate(176 140) scale(2.8) rotate(-9 7 11.5)" fill="none" stroke="#3a3a38" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" opacity="0.28"><path d="M5.5 11.5L6.5 7.5L5.5 7.5A2 2 0 0 1 5.5 3.5L12.5 3.5L12.5 7.5L9.5 7.5L8.5 11.5Z" fill="#3a3a38"/><rect x="3.5" y="11.5" width="7" height="3" rx="1" fill="#3a3a38"/><path d="M12.5 4L13.8 4L14.4 4.6L14.4 6.4L13.8 7L12.5 7Z" fill="#3a3a38" stroke="none"/><path d="M14.4 5.5L16.2 5.5"/></g><g transform="translate(176 140) scale(2.8)" fill="none" stroke="#3a3a38" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"><path d="M5.5 11.5L6.5 7.5L5.5 7.5A2 2 0 0 1 5.5 3.5L12.5 3.5L12.5 7.5L9.5 7.5L8.5 11.5Z" fill="#3a3a38"/><rect x="3.5" y="11.5" width="7" height="3" rx="1" fill="#3a3a38"/><path d="M12.5 4L13.8 4L14.4 4.6L14.4 6.4L13.8 7L12.5 7Z" fill="#3a3a38" stroke="none"/><path d="M14.4 5.5L16.2 5.5"/></g>
<text class="th t-gray" x="236" y="156" dominant-baseline="central">The trigger</text>
<text class="ts t-gray-s" x="236" y="174" dominant-baseline="central">filled, with one kick at key down</text>
<line x1="340" y1="196" x2="340" y2="222" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f06b)"/>
<text class="ts s-mut" x="352" y="211" dominant-baseline="central">key up</text>
<rect x="160" y="232" width="360" height="56" rx="10" fill="#faeeda" stroke="#854f0b" stroke-width="1"/>
<g transform="translate(176 236) scale(2.8)" fill="none" stroke="#3a3a38" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" opacity="0.6"><path d="M5.5 11.5L6.5 7.5L5.5 7.5A2 2 0 0 1 5.5 3.5L12.5 3.5L12.5 7.5L9.5 7.5L8.5 11.5"/><rect x="3.5" y="11.5" width="7" height="3" rx="1" fill="#3a3a38"/><path d="M12.5 4L13.8 4L14.4 4.6L14.4 6.4L13.8 7L12.5 7Z" fill="#3a3a38" stroke="none"/><path d="M14.4 5.5L16.2 5.5"/><path d="M15.3 2.9L16.1 2.1M15.3 8.1L16.1 8.9"/></g>
<text class="th t-amber" x="236" y="252" dominant-baseline="central">Working</text>
<text class="ts t-amber-s" x="236" y="270" dominant-baseline="central">dimmed · the bit turns past 300 ms</text>
<line x1="340" y1="292" x2="340" y2="318" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f06b)"/>
<text class="ts s-mut" x="352" y="307" dominant-baseline="central">if it fails · else back to rest</text>
<rect x="160" y="328" width="360" height="56" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<g transform="translate(173.2 332) scale(2.8)" fill="none" stroke="#3a3a38" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" opacity="0.28"><path d="M5.5 11.5L6.5 7.5L5.5 7.5A2 2 0 0 1 5.5 3.5L12.5 3.5L12.5 7.5L9.5 7.5L8.5 11.5"/><rect x="3.5" y="11.5" width="7" height="3" rx="1"/><path d="M12.5 4L13.8 4L14.4 4.6L14.4 6.4L13.8 7L12.5 7Z" fill="#3a3a38" stroke="none"/><path d="M14.4 5.5L16.2 5.5"/><path d="M13.1 11.8L16.2 14.9M16.2 11.8L13.1 14.9"/></g><g transform="translate(176 332) scale(2.8)" fill="none" stroke="#3a3a38" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"><path d="M5.5 11.5L6.5 7.5L5.5 7.5A2 2 0 0 1 5.5 3.5L12.5 3.5L12.5 7.5L9.5 7.5L8.5 11.5"/><rect x="3.5" y="11.5" width="7" height="3" rx="1"/><path d="M12.5 4L13.8 4L14.4 4.6L14.4 6.4L13.8 7L12.5 7Z" fill="#3a3a38" stroke="none"/><path d="M14.4 5.5L16.2 5.5"/><path d="M13.1 11.8L16.2 14.9M16.2 11.8L13.1 14.9"/></g>
<text class="th t-coral" x="236" y="348" dominant-baseline="central">The shake</text>
<text class="ts t-coral-s" x="236" y="366" dominant-baseline="central">the drill and its cross, left and right</text>
<text class="ts s-mut" x="340" y="414" text-anchor="middle">in progress, not yet released · 0.0.4 shows a waveform in the menu bar</text>
</svg>
<figcaption>The drill follows the pipeline.</figcaption>
</figure>
<p>Each animation lasts under half a second and ends on the state's own form, and only the turning repeats. With Reduce Motion on, nothing moves, and the form alone carries the state. The states differ by shape and opacity, never by color, so the icon stays a template image, a one-color image that macOS tints to match the menu bar.</p>

<h3>The core and the shell</h3>
<p>Hark is one Swift package, cut in three targets, the parts a package builds separately. <strong>HarkCore</strong> holds all the logic, 129 files (yeah...), and imports no UI framework, so everything that decides what happens to a sentence can be tested without a window on screen. <strong>HarkApp</strong> is the shell. Its 39 files of SwiftUI views and AppKit adapters render state and never compute it. The third, HarkObjC, is one function.</p>
<p>The split is enforced. <code>scripts/check.sh</code> runs before every commit. It fails the commit if the core imports SwiftUI or AppKit, if any folder but <code>Transcription/</code> imports whisper.cpp, or if <code>URLSession</code> appears outside its two files. The screen and the speech model each have one door, and the network two.</p>
<p>Where the core touches the system, it defines a seam: a protocol, Swift's word for an interface, that the core owns and something else implements. The app plugs in AppKit adapters, and the tests plug in fakes. Most seams have a default that still ends a press in one log line.</p>

<figure>
<svg class="diagram" viewBox="0 0 680 372" role="img" xmlns="http://www.w3.org/2000/svg">
<title>Core, seams, adapters</title>
<desc>HarkCore holds the reducer, the transcription folder and the stages. It reaches the system only through seams, protocols it owns, which AppKit adapters implement in the app and fakes implement in tests. HarkObjC, one function that catches exceptions, is called directly by the audio stage.</desc>
<defs>
<marker id="arr-f07" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#5f5e5a" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
</defs>

<rect x="40" y="44" width="220" height="280" rx="16" fill="none" stroke="#c4c2b8" stroke-width="1" stroke-dasharray="6 4"/>
<text class="th t-ink" x="60" y="70">HarkCore</text>
<text class="ts s-mut" x="60" y="88">all logic · no UI</text>

<rect x="60" y="104" width="180" height="56" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="150" y="123" text-anchor="middle" dominant-baseline="central">Reducer</text>
<text class="ts t-gray-s" x="150" y="141" text-anchor="middle" dominant-baseline="central">pure · no clock, no I/O</text>

<rect x="60" y="176" width="180" height="56" rx="10" fill="#faeeda" stroke="#854f0b" stroke-width="1"/>
<text class="th t-amber" x="150" y="195" text-anchor="middle" dominant-baseline="central">Transcription</text>
<text class="ts t-amber-s" x="150" y="213" text-anchor="middle" dominant-baseline="central">only door to whisper.cpp</text>

<rect x="60" y="248" width="180" height="56" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="150" y="267" text-anchor="middle" dominant-baseline="central">Stages</text>
<text class="ts t-gray-s" x="150" y="285" text-anchor="middle" dominant-baseline="central">audio · rules · insertion</text>

<line x1="262" y1="168" x2="286" y2="168" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f07)"/>

<rect x="290" y="104" width="100" height="128" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="340" y="148" text-anchor="middle">Seams</text>
<text class="ts t-coral-s" x="340" y="170" text-anchor="middle">protocols</text>
<text class="ts t-coral-s" x="340" y="188" text-anchor="middle">the core owns</text>

<line x1="392" y1="132" x2="436" y2="132" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f07)"/>
<line x1="392" y1="204" x2="436" y2="204" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f07)"/>

<rect x="420" y="44" width="220" height="280" rx="16" fill="none" stroke="#c4c2b8" stroke-width="1" stroke-dasharray="6 4"/>
<text class="th t-ink" x="440" y="70">Around it</text>
<text class="ts s-mut" x="440" y="88">outside the core</text>

<rect x="440" y="104" width="180" height="56" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="530" y="123" text-anchor="middle" dominant-baseline="central">AppKit adapters</text>
<text class="ts t-gray-s" x="530" y="141" text-anchor="middle" dominant-baseline="central">pasteboard · keys · apps</text>

<rect x="440" y="176" width="180" height="56" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1" stroke-dasharray="5 4"/>
<text class="th t-gray" x="530" y="195" text-anchor="middle" dominant-baseline="central">Test fakes</text>
<text class="ts t-gray-s" x="530" y="213" text-anchor="middle" dominant-baseline="central">no mic · no AX · no network</text>

<rect x="440" y="248" width="180" height="56" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="530" y="267" text-anchor="middle" dominant-baseline="central">HarkObjC</text>
<text class="ts t-coral-s" x="530" y="285" text-anchor="middle" dominant-baseline="central">one function · exceptions</text>

<line x1="242" y1="276" x2="436" y2="276" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f07)"/>
<text class="ts t-gray-s" x="340" y="264" text-anchor="middle">called directly</text>

<text class="ts t-coral-s" x="340" y="354" text-anchor="middle">check.sh fails a commit that imports a UI framework into the core</text>
</svg>
<figcaption>Core, seams, adapters.</figcaption>
</figure>

<p>Three dependencies, no more: whisper.cpp, pinned to its release b5130 as a prebuilt framework, KeyboardShortcuts for the keys, and Yams for the YAML file. HarkObjC exists because AVFoundation, Apple's audio and video framework, raises Objective-C exceptions, which Swift cannot catch. Its one function turns them into errors. Chapter 2 tells the crash that made it necessary.</p>
<p>Until 23 September, every quit crashed. <code>exit()</code> ran the destructors of ggml, whisper.cpp's math library, while GPU memory was still held. Hark now unloads the model first, and past 3 s leaves with <code>_exit</code>, which skips the destructors.</p>

<h3>Keeping the HUD and the keys live</h3>
<p>While you speak, the HUD moves 30 times a second and the keys answer at once. Four rules keep it so:</p>
<ul>
  <li><strong>Strict concurrency.</strong> Swift 6 checks shared state at compile time, and any warning fails the build.</li>
  <li><strong>Private queues.</strong> Three things block: Whisper, the capture session and the Accessibility API (AX), the macOS interface to other apps' controls. Each gets its own serial queue, off the few threads Swift's tasks share.</li>
  <li><strong>A lock for the HUD.</strong> The HUD reads the audio levels behind one small lock, never through an actor, so it cannot queue behind a microphone start.</li>
  <li><strong>A cancel that reaches the decoder.</strong> Whisper checks a stop flag on its own thread. Each flag is numbered, so a cancel that arrives late cannot stop the next sentence. On this Mac, with Small, a cancel 300 ms into decoding the 72 s French clip of chapter 3 returned at 0.30 s, against 0.97 s for the whole decode in that run.</li>
</ul>

<h3>One line per utterance</h3>
<p>Every row in Settings › Log is one line of JSON, one file a day, thirteen keys in a fixed order. It takes one <code>open</code> in append mode and one <code>write(2)</code>, in a folder and a file only your account can read. A failed write goes to the system log, never back into the pipeline.</p>
<p>What a line keeps is decided in code: in a password field, both texts are written as <code>null</code>. An ask writes the instruction you spoke, never the selection or the answer. The last two of the 13 keys, <code>llm_model</code> and <code>llm_ms</code>, came with Ask Hark.</p>
<p>The running example, in the log's format, broken across lines for the page:</p>
<pre><code>{"ts":"2026-09-29T11:05:12.408+02:00","duration_ms":5000,"transcribe_ms":540,
"raw_text":"The meeting moves to Thursday at ten, same room.",
"normalized_text":"the meeting moves to thursday at ten same room",
"resolution":"text_inserted","target_app":"com.apple.mail","action_type":null,
"exit_code":null,"error":null,"model_tier":"small","llm_model":null,"llm_ms":null}</code></pre>
<p>The time and the 540 ms are sample values. In the Log tab, a dot beside each row names its ending.</p>
<figure>
<img class="window" style="--w:520px" src="{{ '/assets/images/anatomy-hark/03-settings-about-dots.png' | relative_url }}" alt="The five dots of Recent and the Log, explained in Settings › About">
<figcaption>Settings › About, the dots in Recent and the Log. Blue, text where it should be. Orange, text only on the clipboard. Green, a command. Gray, discarded. Red, failed. Every ending, named.</figcaption>
</figure>
<p>No line, no utterance. Every press, kept or discarded, can be checked after the fact.</p>

<h2>Chapter 2: Capture (key, microphone, HUD)</h2>
<p>Chapter 1 gave every press one path. Its first state, <code>capturing</code>, starts with a key, not with a microphone.</p>
<p>Three things share the moment: the key that says what you want, the microphone that opens for it, and the HUD that shows you are heard.</p>

<h3>Three keys, two gestures</h3>
<p>Besides the dictation key, Hark has two: the cancel key, Control-Option-Escape (⌃⌥Esc), and the Ask key of chapter 6, Control-Option-A (⌃⌥A). All three can be rebound in Settings › General.</p>

<figure>
<img class="window" style="--w:520px" src="{{ '/assets/images/anatomy-hark/04-settings-keys.png' | relative_url }}" alt="Settings, General tab, with recorders for the dictation, cancel and Ask Hark shortcuts">
<figcaption>Settings › General, rebound on this Mac: dictation <code>⌥⌘V</code>, cancel <code>⌥⌘Q</code>, the tap-or-hold rule, then Ask Hark <code>⌥⌘A</code>. Defaults: <code>⌃⌥V</code>, <code>⌃⌥Esc</code>, <code>⌃⌥A</code>. Yours to change.</figcaption>
</figure>

<p>One key carries two gestures. Recording starts at key down either way. Release within 350 ms and the press <strong>latches</strong>: recording goes on with the key up, until the next tap. Hold longer and it is <strong>push-to-talk</strong>.</p>
<p>The keys are system-wide hot keys from Carbon, an older macOS API, through the KeyboardShortcuts package. Unlike an event tap, they need no Input Monitoring permission. The release marks the end of speech, with no voice detector. Always-on listening, which would need one, was set aside.</p>

<figure>
<svg class="diagram" viewBox="0 0 680 284" role="img" xmlns="http://www.w3.org/2000/svg">
<title>One key, two gestures, split at 350 ms</title>
<desc>Two timelines from key down. Hold: the key stays down past 350 ms, and recording stops at key up. Tap: the key comes up before 350 ms, the capture latches and goes on until a second tap stops it. Recording starts at key down in both.</desc>
<line x1="294" y1="52" x2="294" y2="222" stroke="#993c1d" stroke-width="1" stroke-dasharray="5 4"/>
<text class="ts t-coral-s" x="294" y="44" text-anchor="middle">350 ms</text>

<text class="th t-ink" x="40" y="100">Hold</text>
<text class="ts s-mut" x="40" y="118">push-to-talk</text>
<rect x="160" y="92" width="345" height="20" rx="4" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="ts t-gray-s" x="400" y="106" text-anchor="middle">recording while held</text>
<line x1="160" y1="84" x2="160" y2="120" stroke="#5f5e5a" stroke-width="1.5"/>
<line x1="505" y1="84" x2="505" y2="120" stroke="#5f5e5a" stroke-width="1.5"/>
<text class="ts t-gray-s" x="160" y="76" text-anchor="middle">key down</text>
<text class="ts t-gray-s" x="505" y="76" text-anchor="middle">key up · stops on release</text>

<text class="th t-ink" x="40" y="180">Tap</text>
<text class="ts s-mut" x="40" y="198">hands-free</text>
<rect x="160" y="172" width="440" height="20" rx="4" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="ts t-gray-s" x="447" y="186" text-anchor="middle">latched · recording goes on</text>
<line x1="160" y1="164" x2="160" y2="200" stroke="#5f5e5a" stroke-width="1.5"/>
<line x1="217" y1="164" x2="217" y2="200" stroke="#5f5e5a" stroke-width="1.5"/>
<line x1="600" y1="164" x2="600" y2="200" stroke="#5f5e5a" stroke-width="1.5"/>
<text class="ts t-gray-s" x="160" y="156" text-anchor="middle">key down</text>
<text class="ts t-gray-s" x="221" y="156" text-anchor="start">key up</text>
<text class="ts t-gray-s" x="600" y="156" text-anchor="middle">second tap stops</text>

<line x1="160" y1="230" x2="620" y2="230" stroke="#5f5e5a" stroke-width="1"/>
<line x1="160" y1="230" x2="160" y2="235" stroke="#5f5e5a" stroke-width="1"/>
<line x1="294" y1="230" x2="294" y2="235" stroke="#5f5e5a" stroke-width="1"/>
<line x1="620" y1="230" x2="620" y2="235" stroke="#5f5e5a" stroke-width="1"/>
<text class="ts s-mut" x="160" y="250" text-anchor="middle">0</text>
<text class="ts s-mut" x="294" y="250" text-anchor="middle">350</text>
<text class="ts s-mut" x="620" y="250" text-anchor="middle">1,200 ms</text>
<text class="ts t-gray-s" x="340" y="274" text-anchor="middle">recording starts at key down either way · the release decides which gesture it was</text>
</svg>
<figcaption>One key, two gestures, split at 350 ms.</figcaption>
</figure>

<p class="note">One detail from the first design. Hark was first planned around a hardware button. A two-euro Bluetooth camera shutter was for prototyping only: it sleeps and drops the first press. The pick was a three-key macro pad sending F13, F14 and F15, keys macOS binds to nothing. What shipped is a chord on the keyboard you already have. The button's only job was to emit one keystroke, so nothing after it had to change.</p>

<h3>A window that never takes the keyboard</h3>
<p>While you speak, the HUD at the bottom of the screen shows seven bars and a timer. The caret, the text cursor, stays where it was in Mail. By the project's own specification, this is the most important detail in the app.</p>
<p>Showing a window usually brings its app to the front, and early builds paid for it twice: the Settings window vanished at the first click elsewhere, and a welcome window swallowed the first dictations after each launch.</p>
<p>The HUD is a non-activating panel, a window that shows without bringing its app forward. It never becomes the key window, the one that takes typing, and it ignores the mouse. It is 280 by 64 points, sits 120 points above the Dock, and fades in over 120 ms, instantly under Reduce Motion. A tripwire, <code>HUDFocusGuard</code>, logs a fault if Hark ever becomes active while it shows.</p>

<figure>
<svg class="diagram" viewBox="0 0 680 356" role="img" xmlns="http://www.w3.org/2000/svg">
<title>Why the caret stays where you left it</title>
<desc>Side by side. An ordinary window activates its app, becomes key and takes the caret from Mail, so the insertion target is lost. The HUD is shown without activating, is never key or main, ignores the mouse, and Mail keeps the caret.</desc>
<defs>
<marker id="arr-f11" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#5f5e5a" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
</defs>
<rect x="40" y="44" width="290" height="270" rx="16" fill="none" stroke="#c4c2b8" stroke-width="1" stroke-dasharray="6 4"/>
<text class="th t-ink" x="60" y="70">An ordinary window</text>
<text class="ts s-mut" x="60" y="88">what showing a window usually does</text>

<rect x="60" y="104" width="250" height="50" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="185" y="121" text-anchor="middle" dominant-baseline="central">App activates</text>
<text class="ts t-gray-s" x="185" y="139" text-anchor="middle" dominant-baseline="central">Hark comes to the front</text>
<line x1="185" y1="158" x2="185" y2="174" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f11)"/>

<rect x="60" y="176" width="250" height="50" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="185" y="193" text-anchor="middle" dominant-baseline="central">Window becomes key</text>
<text class="ts t-coral-s" x="185" y="211" text-anchor="middle" dominant-baseline="central">the caret leaves Mail</text>
<line x1="185" y1="230" x2="185" y2="246" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f11)"/>

<rect x="60" y="248" width="250" height="50" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="185" y="265" text-anchor="middle" dominant-baseline="central">Nowhere to type</text>
<text class="ts t-coral-s" x="185" y="283" text-anchor="middle" dominant-baseline="central">the insertion target is lost</text>

<rect x="350" y="44" width="290" height="270" rx="16" fill="none" stroke="#c4c2b8" stroke-width="1" stroke-dasharray="6 4"/>
<text class="th t-ink" x="370" y="70">The HUD</text>
<text class="ts s-mut" x="370" y="88">a non-activating panel</text>

<rect x="370" y="104" width="250" height="50" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="495" y="121" text-anchor="middle" dominant-baseline="central">Shown, not activated</text>
<text class="ts t-gray-s" x="495" y="139" text-anchor="middle" dominant-baseline="central">ordered front regardless</text>
<line x1="495" y1="158" x2="495" y2="174" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f11)"/>

<rect x="370" y="176" width="250" height="50" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="495" y="193" text-anchor="middle" dominant-baseline="central">Never key, never main</text>
<text class="ts t-gray-s" x="495" y="211" text-anchor="middle" dominant-baseline="central">ignores the mouse</text>
<line x1="495" y1="230" x2="495" y2="246" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f11)"/>

<rect x="370" y="248" width="250" height="50" rx="10" fill="#e1f5ee" stroke="#0f6e56" stroke-width="1"/>
<text class="th t-teal" x="495" y="265" text-anchor="middle" dominant-baseline="central">Mail keeps the caret</text>
<text class="ts t-teal-s" x="495" y="283" text-anchor="middle" dominant-baseline="central">your field, untouched</text>

<text class="ts t-gray-s" x="340" y="340" text-anchor="middle">a tripwire logs a fault if Hark ever becomes active while the HUD shows</text>
</svg>
<figcaption>Why the caret stays where you left it.</figcaption>
</figure>

<p>The seven bars are the voice's spectrum, 100 Hz to 6 kHz. They rise at once and fall back over about a third of a second, so a syllable does not blink.</p>

<figure>
<div class="hud-grid">
<img class="window" style="--w:280px" src="{{ '/assets/images/anatomy-hark/05a-hud-listening.png' | relative_url }}" alt="HUD while listening, seven bars and 1:23">
<img class="window" style="--w:280px" src="{{ '/assets/images/anatomy-hark/05b-hud-hands-free.png' | relative_url }}" alt="HUD latched hands-free, with a lock before the time">
<img class="window" style="--w:280px" src="{{ '/assets/images/anatomy-hark/05c-hud-live-transcript.png' | relative_url }}" alt="HUD with a live transcript line under shorter bars">
<img class="window" style="--w:280px" src="{{ '/assets/images/anatomy-hark/05d-hud-length-limit.png' | relative_url }}" alt="HUD at 30:00, length limit reached, transcribing">
</div>
<figcaption>The HUD in four states. Held: seven bars, 1:23. Tapped: a lock. Live transcript, off by default: the newest words. At 30:00, "Length limit reached. Transcribing…". The timers are preview values. None takes the keyboard.</figcaption>
</figure>

<h3>Everything at key down</h3>
<p>Key down waits for nothing. The reducer from chapter 1 moves to <code>capturing</code> and emits its effects at once: start the capture, probe the focus, lower other audio.</p>
<p>On this Mac, the microphone's session starts in 76 to 88 ms, and the first buffer lands about 10 ms later. The probe asks Accessibility which app and field are in front. It answers in 0 to 2 ms warm, 22 to 37 ms on a fresh process's first read. Lowering other audio took 7.9 to 16.8 ms in the installed app, the top of the range on AirPods. That is too long for the main thread, so it runs on its own actor.</p>

<figure>
<svg class="diagram" viewBox="0 0 680 350" role="img" xmlns="http://www.w3.org/2000/svg">
<title>Key down, everything at once</title>
<desc>Lanes on a 0 to 200 ms axis from key down. The reducer moves to capturing at once. The HUD fades in over 120 ms. The microphone session starts in 76 to 88 ms, and its first buffer arrives about 10 ms later, so the first audio lands about 90 to 100 ms after the press. The focus probe answers in 0 to 2 ms warm. Other audio is lowered in 8 to 17 ms.</desc>
<line x1="393" y1="58" x2="393" y2="296" stroke="#993c1d" stroke-width="1" stroke-dasharray="5 4"/>
<text class="ts t-coral-s" x="393" y="50" text-anchor="middle">first audio ≈ 90–100 ms</text>

<text class="th t-ink" x="40" y="83">Reducer</text>
<text class="ts s-mut" x="40" y="99">pure, no I/O</text>
<rect x="179" y="70" width="2" height="18" fill="#5f5e5a"/>
<text class="ts t-gray-s" x="188" y="83">capturing</text>

<text class="th t-ink" x="40" y="129">HUD</text>
<text class="ts s-mut" x="40" y="145">non-activating</text>
<rect x="180" y="116" width="264" height="18" rx="3" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="ts t-gray-s" x="300" y="129" text-anchor="middle">fade in · 120 ms</text>

<text class="th t-ink" x="40" y="175">Microphone</text>
<text class="ts s-mut" x="40" y="191">one session</text>
<rect x="180" y="162" width="194" height="18" rx="3" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="ts t-gray-s" x="277" y="175" text-anchor="middle">start · 76–88 ms</text>
<rect x="374" y="162" width="22" height="18" rx="3" fill="#d3d1c7" stroke="#5f5e5a" stroke-width="1"/>
<text class="ts t-gray-s" x="404" y="175">first buffer</text>

<text class="th t-ink" x="40" y="221">Focus probe</text>
<text class="ts s-mut" x="40" y="237">Accessibility</text>
<rect x="180" y="208" width="5" height="18" rx="1" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="ts t-gray-s" x="192" y="221">0–2 ms warm · 22–37 ms first read</text>

<text class="th t-ink" x="40" y="267">Other audio</text>
<text class="ts s-mut" x="40" y="283">own actor</text>
<rect x="180" y="254" width="37" height="18" rx="3" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="ts t-gray-s" x="224" y="267">lowered to 30% · 8–17 ms</text>

<line x1="180" y1="296" x2="620" y2="296" stroke="#5f5e5a" stroke-width="1"/>
<line x1="180" y1="296" x2="180" y2="301" stroke="#5f5e5a" stroke-width="1"/>
<line x1="290" y1="296" x2="290" y2="301" stroke="#5f5e5a" stroke-width="1"/>
<line x1="400" y1="296" x2="400" y2="301" stroke="#5f5e5a" stroke-width="1"/>
<line x1="510" y1="296" x2="510" y2="301" stroke="#5f5e5a" stroke-width="1"/>
<line x1="620" y1="296" x2="620" y2="301" stroke="#5f5e5a" stroke-width="1"/>
<text class="ts s-mut" x="180" y="316" text-anchor="middle">0</text>
<text class="ts s-mut" x="290" y="316" text-anchor="middle">50</text>
<text class="ts s-mut" x="400" y="316" text-anchor="middle">100</text>
<text class="ts s-mut" x="510" y="316" text-anchor="middle">150</text>
<text class="ts s-mut" x="620" y="316" text-anchor="middle">200 ms</text>
<text class="ts s-mut" x="340" y="340" text-anchor="middle">this Mac · M5 Pro · each lane measured on its own · the fade is set, not measured</text>
</svg>
<figcaption>Key down, everything at once.</figcaption>
</figure>


<h3>Why nothing is open between presses</h3>
<p>You might expect a dictation app to keep its microphone warm. Hark opens nothing while idle.</p>
<p>Until 27 September, capture ran on AVAudioEngine, kept alive as long as the app. With AirPods as the input, it held them in headset mode while idle, and reconfigured itself 48 times in under a minute. Then another app changed the audio setup, and AVFoundation raised an Objective-C exception. Swift cannot catch one, so the process ended.</p>
<p>That crash is why HarkObjC, the one-function target from chapter 1, exists. The same exception now ends one utterance, with a log line, not the process.</p>
<p>The next fix created the engine at each press, and it still had one flaw: it opened the system default input even with another microphone chosen, so AirPods as the default switched to headset mode at every press. That took 2 to 5 s, and short dictations came back silent. Since 28 September, AVCaptureSession opens only the device it is given and delivers 16 kHz mono Float32. No resampler runs.</p>

<figure>
<svg class="diagram" viewBox="0 0 680 300" role="img" xmlns="http://www.w3.org/2000/svg">
<title>The microphone, before and after 28 September</title>
<desc>Two era rows. AVAudioEngine, until 28 September, made per press, still opened the system default input at every press and switched AirPods to headset mode in 2 to 5 s, so short clips came back silent. AVCaptureSession, since 28 September, opens one session per press on the chosen microphone only, starting in 76 to 88 ms. Between presses nothing is open.</desc>
<rect x="40" y="44" width="600" height="96" rx="12" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="60" y="72">AVAudioEngine · until 28 September</text>
<text class="ts t-gray-s" x="60" y="94">made per press, it still opened the system default input</text>
<text class="ts t-gray-s" x="60" y="114">AirPods to headset mode · 2–5 s to switch</text>
<rect x="482" y="64" width="138" height="56" rx="8" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="551" y="86" text-anchor="middle">short clips</text>
<text class="ts t-coral-s" x="551" y="106" text-anchor="middle">came back silent</text>

<rect x="40" y="156" width="600" height="96" rx="12" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="60" y="184">AVCaptureSession · since 28 September</text>
<text class="ts t-gray-s" x="60" y="206">one session per press · only the chosen microphone</text>
<text class="ts t-gray-s" x="60" y="226">start 76–88 ms · 16 kHz mono float delivered</text>
<rect x="482" y="176" width="138" height="56" rx="8" fill="#e1f5ee" stroke="#0f6e56" stroke-width="1"/>
<text class="th t-teal" x="551" y="198" text-anchor="middle">your mic</text>
<text class="ts t-teal-s" x="551" y="218" text-anchor="middle">and nothing else</text>

<text class="ts s-mut" x="340" y="282" text-anchor="middle">between presses, nothing is open</text>
</svg>
<figcaption>The microphone, before and after 28 September.</figcaption>
</figure>

<p>A headset now keeps its music.</p>
<figure>
<img class="window" style="--w:520px" src="{{ '/assets/images/anatomy-hark/06-settings-audio.png' | relative_url }}" alt="Settings, Audio tab: one microphone menu set to the built-in microphone, and a note that Hark opens it only while you dictate">
<figcaption>Settings › Audio. One choice, the microphone: <code>Micro MacBook Pro</code>, the built-in one under its French name. Below it, the promise that Hark opens it only while you dictate. Nothing between presses.</figcaption>
</figure>

<h3>Samples in memory, and two gates</h3>
<p>The samples stay in memory. One minute, 960,000 samples or 3.84 MB, is reserved once and kept between presses. A 30-minute capture grows to 115 MB, then gives the growth back. Raw audio reaches the disk only in a debug build.</p>
<p>Two gates stand before the model, the early exits of chapter 1. A capture under 250 ms is too short. One whose loudest 20 ms stays under 0.01 in root mean square (RMS), a measure of loudness, holds no speech. Either way the model is never called.</p>

<figure>
<svg class="diagram" viewBox="0 0 680 256" role="img" xmlns="http://www.w3.org/2000/svg">
<title>Samples in memory, and two gates</title>
<desc>From the capture session to samples kept in memory, then a check that the capture lasts 250 ms or more, then a check that its peak level reaches 0.01 RMS, then the transcriber. Up to 30 minutes, 115 MB, given back after. Nothing goes to disk outside a debug build.</desc>
<defs>
<marker id="arr-f16" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#5f5e5a" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
</defs>
<rect x="24" y="56" width="112" height="80" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="80" y="84" text-anchor="middle">Session</text>
<text class="ts t-gray-s" x="80" y="104" text-anchor="middle">one per press</text>
<line x1="139" y1="96" x2="151" y2="96" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f16)"/>

<rect x="156" y="56" width="112" height="80" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="212" y="82" text-anchor="middle">Samples</text>
<text class="ts t-gray-s" x="212" y="102" text-anchor="middle">in memory</text>
<text class="ts t-gray-s" x="212" y="120" text-anchor="middle">1 min kept</text>
<line x1="271" y1="96" x2="283" y2="96" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f16)"/>

<rect x="288" y="56" width="112" height="80" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="344" y="82" text-anchor="middle">Long enough</text>
<text class="ts t-coral-s" x="344" y="102" text-anchor="middle">under 250 ms:</text>
<text class="ts t-coral-s" x="344" y="120" text-anchor="middle">too short</text>
<line x1="403" y1="96" x2="415" y2="96" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f16)"/>

<rect x="420" y="56" width="112" height="80" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="476" y="82" text-anchor="middle">Loud enough</text>
<text class="ts t-coral-s" x="476" y="102" text-anchor="middle">under 0.01 RMS:</text>
<text class="ts t-coral-s" x="476" y="120" text-anchor="middle">no speech</text>
<line x1="535" y1="96" x2="547" y2="96" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f16)"/>

<rect x="552" y="56" width="112" height="80" rx="10" fill="#faeeda" stroke="#854f0b" stroke-width="1"/>
<text class="th t-amber" x="608" y="82" text-anchor="middle">Transcriber</text>
<text class="ts t-amber-s" x="608" y="102" text-anchor="middle">whisper.cpp</text>
<text class="ts t-amber-s" x="608" y="120" text-anchor="middle">chapter 3</text>

<line x1="212" y1="136" x2="212" y2="190" stroke="#5f5e5a" stroke-width="1.5" stroke-dasharray="5 4"/>
<text class="ts s-mut" x="222" y="166">in memory: up to 30 min · 115 MB, then given back</text>
<rect x="112" y="190" width="200" height="48" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1" stroke-dasharray="5 4"/>
<text class="th t-coral" x="212" y="206" text-anchor="middle" dominant-baseline="central">Disk</text>
<text class="ts t-coral-s" x="212" y="224" text-anchor="middle" dominant-baseline="central">never, outside a debug build</text>
</svg>
<figcaption>Samples in memory, and two gates.</figcaption>
</figure>

<h3>Lowering other audio, and restoring it</h3>
<p>By default, other audio drops to 30 percent while you speak. Bluetooth headsets broke that: they keep one volume per mode. Hark lowered AirPods to 30 percent of their volume in music mode. At key up it read the headset mode's volume, unchanged, took the mismatch for your own change, and left the music low.</p>
<p>Now Hark lowers nothing when a Bluetooth microphone is the input or the system default, and restores only a volume that still reads what it set. The lowered state is saved first, so a crash is undone at the next launch.</p>
<p>The fastest microphone would be one left open. Hark opens one per press instead, and pays at the start: the first samples arrive about 90 ms after the key goes down. Between presses, nothing listens.</p>

<h2>Chapter 3: Transcription (whisper.cpp on Apple silicon)</h2>
<p>The key comes up. Five seconds of speech are now 80,000 numbers in memory, the samples from chapter 2. This chapter is the amber box, where the Mac does the work a server usually does.</p>
<p>The question is not whether a Mac can run Whisper. It is whether a menu bar app can keep it loaded all day, answer in a tenth of a second, and cost little while it waits.</p>

<h3>Why the model loads at launch</h3>
<p>Hark loads the model at launch, and again when you choose a size in Settings › Model, never inside a sentence. It then runs one warm-up decode: 1.25 s of silence, one token long. That step compiles the GPU code the first press would otherwise compile. A press during warm-up waits behind it, on the serial queue from chapter 1.</p>

<figure>
<svg class="diagram" viewBox="0 0 680 244" role="img" xmlns="http://www.w3.org/2000/svg">
<title>Ready before the first press</title>
<desc>Five steps in a row. You choose a size in Settings. Hark downloads the model pinned to one commit and checks its SHA-256, loads it onto the GPU through Metal, warms it up with one decode of 1.25 s of silence, and keeps it resident, so every press starts warm. Before the warm-up, the first press ever took 16,378 ms for 4.1 s of speech. After it, 242 ms for 15.9 s and 151 ms for 7.8 s, each the whole engine call, language auto. Each new build compiles Metal once, 12.4 to 13.0 s cold, 9 ms warm.</desc>
<defs>
<marker id="arr-f17" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#5f5e5a" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
</defs>

<rect x="40" y="40" width="104" height="84" rx="10" fill="#e1f5ee" stroke="#0f6e56" stroke-width="1"/>
<text class="th t-teal" x="92" y="66" text-anchor="middle">Choose</text>
<text class="ts t-teal-s" x="92" y="86" text-anchor="middle">a size in</text>
<text class="ts t-teal-s" x="92" y="104" text-anchor="middle">Settings</text>
<line x1="146" y1="82" x2="160" y2="82" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f17)"/>

<rect x="164" y="40" width="104" height="84" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="216" y="66" text-anchor="middle">Download</text>
<text class="ts t-coral-s" x="216" y="86" text-anchor="middle">pinned commit</text>
<text class="ts t-coral-s" x="216" y="104" text-anchor="middle">SHA-256 check</text>
<line x1="270" y1="82" x2="284" y2="82" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f17)"/>

<rect x="288" y="40" width="104" height="84" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="340" y="66" text-anchor="middle">Load</text>
<text class="ts t-gray-s" x="340" y="86" text-anchor="middle">onto the GPU</text>
<text class="ts t-gray-s" x="340" y="104" text-anchor="middle">through Metal</text>
<line x1="394" y1="82" x2="408" y2="82" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f17)"/>

<rect x="412" y="40" width="104" height="84" rx="10" fill="#faeeda" stroke="#854f0b" stroke-width="1"/>
<text class="th t-amber" x="464" y="66" text-anchor="middle">Warm up</text>
<text class="ts t-amber-s" x="464" y="86" text-anchor="middle">1.25 s of</text>
<text class="ts t-amber-s" x="464" y="104" text-anchor="middle">silence</text>
<line x1="518" y1="82" x2="532" y2="82" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f17)"/>

<rect x="536" y="40" width="104" height="84" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="588" y="66" text-anchor="middle">Resident</text>
<text class="ts t-gray-s" x="588" y="86" text-anchor="middle">every press</text>
<text class="ts t-gray-s" x="588" y="104" text-anchor="middle">starts warm</text>

<text class="ts t-coral-s" x="340" y="168" text-anchor="middle">before: the first press ever took 16,378 ms for 4.1 s of speech</text>
<text class="ts t-gray-s" x="340" y="192" text-anchor="middle">after: 242 ms for 15.9 s, 151 ms for 7.8 s · Small, language auto, whole engine call</text>
<text class="ts s-mut" x="340" y="216" text-anchor="middle">each new build compiles Metal once: 12.4 to 13.0 s cold, 9 ms warm</text>
</svg>
<figcaption>Ready before the first press.</figcaption>
</figure>

<p>Before the warm-up, the first press ever took 16,378 ms, the model loading and compiling inside the sentence. On Metal, a new build's first start still costs 12.4 to 13.0 s of compilation, now paid at launch.</p>
<p>The price is memory held all day. Hark can unload an idle model, but the option stays off, since a reload pays the warm-up again.</p>

<h3>The price of staying ready</h3>
<p>On 23 September, the installed app with Small and the live transcript off measured a 489 MB footprint, the memory macOS charges to the process, and a 579 MB peak, the Neural Engine state unrecorded, most likely on. On a 16 GB Mac, that is about 3 percent. Before a launch fix it peaked at 1.0 GB: the model had loaded twice.</p>
<p>The weights are what keep it small. On disk, Hark's three models are quantized: their weights are stored in 8 bits (<code>q8_0</code>), or 5 for Large v3 (<code>q5_0</code>), instead of 16. They take 264.5 MB for Small, 823.4 MB for Medium and 1,081.1 MB for Large v3. The 16-bit Large v3, 3.1 GB, was left out as too big to keep loaded in a menu bar app. With the Neural Engine switch on, described below, the Core ML encoders add 163.1 to 1,175.7 MB, hence the 427.5 MB shown for Small.</p>
<p>The live transcript costs more. Whisper does not stream, so the HUD's line is a fresh decode of the last 6 s, on a second copy of Small. In a test process with the Core ML encoder installed, that copy added 427 MB, about its weights plus its 163 MB encoder. It delayed the final decode by 5 ms typically, 18 ms at worst over 40 runs.</p>

<figure>
<svg class="diagram" viewBox="0 0 680 358" role="img" xmlns="http://www.w3.org/2000/svg">
<title>Hark's memory, measured, and what is not</title>
<desc>Bars on a scale from 0 to 1 GB. The whole app with Small and the live transcript off: 489 MB footprint, 579 MB peak. Small loaded once, in a test process: 353 MB. The live transcript's second copy of Small: 427 MB more, off by default. Before a launch fix, with Small loaded twice: a 1.0 GB peak. The model server for Ask is a separate process, not counted in Hark's memory. Medium and Large v3 in memory were not measured. The test-process rows had the Core ML encoder installed, and the app row's Neural Engine state was not recorded.</desc>

<text class="th t-gray" x="40" y="58">Hark, Small</text>
<text class="ts t-gray-s" x="40" y="74">live transcript off</text>
<rect x="220" y="48" width="231.6" height="24" rx="4" fill="none" stroke="#5f5e5a" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="220" y="48" width="195.6" height="24" rx="4" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="ts t-gray-s" x="460" y="64">489 MB · peak 579 MB</text>

<text class="th t-amber" x="40" y="110">Small, loaded once</text>
<text class="ts t-amber-s" x="40" y="126">in a test process</text>
<rect x="220" y="100" width="141.2" height="24" rx="4" fill="#faeeda" stroke="#854f0b" stroke-width="1"/>
<text class="ts t-amber-s" x="369" y="116">+353 MB</text>

<text class="th t-teal" x="40" y="162">Live transcript</text>
<text class="ts t-teal-s" x="40" y="178">Small + its encoder</text>
<rect x="220" y="152" width="170.8" height="24" rx="4" fill="#e1f5ee" stroke="#0f6e56" stroke-width="1" stroke-dasharray="4 3"/>
<text class="ts t-teal-s" x="399" y="168">+427 MB · off by default</text>

<text class="th t-coral" x="40" y="214">Before the fix</text>
<text class="ts t-coral-s" x="40" y="230">Small loaded twice</text>
<rect x="220" y="204" width="400" height="24" rx="4" fill="none" stroke="#993c1d" stroke-width="1"/>
<text class="ts t-coral-s" x="610" y="220" text-anchor="end">peak 1.0 GB</text>

<line x1="220" y1="242" x2="620" y2="242" stroke="#c4c2b8" stroke-width="1"/>
<line x1="220" y1="242" x2="220" y2="248" stroke="#5f5e5a" stroke-width="1"/>
<line x1="420" y1="242" x2="420" y2="248" stroke="#5f5e5a" stroke-width="1"/>
<line x1="620" y1="242" x2="620" y2="248" stroke="#5f5e5a" stroke-width="1"/>
<text class="ts s-mut" x="220" y="264" text-anchor="middle">0</text>
<text class="ts s-mut" x="420" y="264" text-anchor="middle">500 MB</text>
<text class="ts s-mut" x="620" y="264" text-anchor="middle">1 GB</text>

<rect x="40" y="280" width="600" height="32" rx="8" fill="none" stroke="#993c1d" stroke-width="1" stroke-dasharray="6 4"/>
<text class="ts t-coral-s" x="340" y="296" text-anchor="middle" dominant-baseline="central">model server for Ask · a separate process · its memory is not Hark's</text>
<text class="ts s-mut" x="340" y="332" text-anchor="middle">not measured: Medium and Large v3 in memory, the app with the live transcript on</text>
<text class="ts s-mut" x="340" y="350" text-anchor="middle">test-process rows: Core ML encoder installed · app row: Neural Engine state unrecorded</text>
</svg>
<figcaption>Hark's memory, measured, and what is not.</figcaption>
</figure>


<h3>Two halves, two chips</h3>
<p>After key up, two networks run in turn. The <strong>encoder</strong> reads the whole clip once, at a cost set by the window it is given. The <strong>decoder</strong> then writes the text token by token, at a cost that grows with the words.</p>

<figure>
<svg class="diagram" viewBox="0 0 680 360" role="img" xmlns="http://www.w3.org/2000/svg">
<title>Two halves, two chips</title>
<desc>Audio at 16 kHz mono, at least 1.25 s long, becomes a mel spectrogram on the CPU with up to four threads. The encoder reads it once, on the GPU through Metal by default with the window scaled to the clip, or optionally on the Neural Engine through Core ML, always on the full 1,500 states. The decoder writes the text token by token, always on the GPU through Metal. The text then goes to the filter.</desc>
<defs>
<marker id="arr-f18" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#5f5e5a" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
</defs>

<rect x="40" y="56" width="104" height="76" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="92" y="82" text-anchor="middle">Audio</text>
<text class="ts t-gray-s" x="92" y="102" text-anchor="middle">16 kHz mono</text>
<text class="ts t-gray-s" x="92" y="120" text-anchor="middle">1.25 s or more</text>
<line x1="146" y1="94" x2="160" y2="94" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f18)"/>

<rect x="164" y="56" width="104" height="76" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="216" y="82" text-anchor="middle">Mel</text>
<text class="ts t-gray-s" x="216" y="102" text-anchor="middle">on the CPU</text>
<text class="ts t-gray-s" x="216" y="120" text-anchor="middle">up to 4 threads</text>
<line x1="270" y1="94" x2="284" y2="94" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f18)"/>

<rect x="288" y="56" width="104" height="76" rx="10" fill="#faeeda" stroke="#854f0b" stroke-width="1"/>
<text class="th t-amber" x="340" y="82" text-anchor="middle">Encoder</text>
<text class="ts t-amber-s" x="340" y="102" text-anchor="middle">once per clip</text>
<text class="ts t-amber-s" x="340" y="120" text-anchor="middle">cost = window</text>
<line x1="394" y1="94" x2="408" y2="94" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f18)"/>

<rect x="412" y="56" width="104" height="76" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="464" y="82" text-anchor="middle">Decoder</text>
<text class="ts t-gray-s" x="464" y="102" text-anchor="middle">token by token</text>
<text class="ts t-gray-s" x="464" y="120" text-anchor="middle">cost = words</text>
<line x1="518" y1="94" x2="532" y2="94" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f18)"/>

<rect x="536" y="56" width="104" height="76" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="588" y="88" text-anchor="middle">Text</text>
<text class="ts t-gray-s" x="588" y="108" text-anchor="middle">then the filter</text>

<path d="M340 132 V152 H130 V276 H148" stroke="#5f5e5a" stroke-width="1.5" fill="none" stroke-dasharray="5 4"/>
<path d="M130 204 H148" stroke="#5f5e5a" stroke-width="1.5" fill="none" stroke-dasharray="5 4"/>
<path d="M464 132 V174" stroke="#5f5e5a" stroke-width="1.5" fill="none" stroke-dasharray="5 4"/>

<rect x="150" y="176" width="220" height="56" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="260" y="196" text-anchor="middle" dominant-baseline="central">Metal · GPU</text>
<text class="ts t-gray-s" x="260" y="214" text-anchor="middle" dominant-baseline="central">the default · window scaled</text>

<rect x="150" y="248" width="220" height="56" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="260" y="268" text-anchor="middle" dominant-baseline="central">Core ML · Neural Engine</text>
<text class="ts t-coral-s" x="260" y="286" text-anchor="middle" dominant-baseline="central">optional · always 1,500 states</text>

<rect x="410" y="176" width="220" height="56" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="520" y="196" text-anchor="middle" dominant-baseline="central">Metal · GPU</text>
<text class="ts t-gray-s" x="520" y="214" text-anchor="middle" dominant-baseline="central">always</text>

<text class="ts t-gray-s" x="340" y="338" text-anchor="middle">the encoder's cost is set by its window, the decoder's by what you said</text>
</svg>
<figcaption>Two halves, two chips.</figcaption>
</figure>

<p>whisper.cpp runs inside Hark: 3.9 MB of a 14 MB app. Both halves run on the GPU by default, through Metal. The encoder can instead run through Core ML, Apple's framework for compiled models. whisper.cpp lets Core ML pick the chip, and the Neural Engine is the one it is meant for. Which chip ran was not checked. The CPU only builds the mel spectrogram, the clip as frequencies over time.</p>
<p>That second path first failed in silence. whisper.cpp derives the encoder's file name from the weights, and the project had the rule backwards. For the first morning of real use, every decode ran on Metal alone, and only whisper.cpp's log said so. Hark now logs at every load whether the encoder is there.</p>

<h3>What a short sentence costs</h3>
<p>A short sentence should cost less than a long one. Whisper's encoder sees a fixed 30 s window, as 1,500 states, 50 per second. Left alone, a five-second sentence pays for all thirty. <code>audio_ctx</code>, the number of states a decode computes, tells it how much the clip fills.</p>
<p>Hark scales it to the clip: seconds × 50, plus 50, rounded up to a multiple of 256, between 256 and 1,500. The running example, 5 s, needs 300 states, rounded to 512: a third of the window.</p>

<figure>
<svg class="diagram" viewBox="0 0 680 250" role="img" xmlns="http://www.w3.org/2000/svg">
<title>The encoder pays for the seconds you spoke</title>
<desc>A bar for Whisper's 30-second window of 1,500 encoder states, with ticks at 256, 512, 768 and 1,500. A 3 s clip computes 256, the five-second running example 512, a 10 s clip 768, and a 29 s clip all 1,500. The rule: seconds times 50, plus 50, rounded up to a multiple of 256, between 256 and 1,500. With the Core ML encoder the full 1,500 is always computed.</desc>
<text class="th t-ink" x="60" y="44">Whisper's window · 30 s · 1,500 encoder states</text>

<rect x="60" y="68" width="560" height="36" rx="6" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<rect x="60" y="68" width="191.1" height="36" rx="6" fill="#faeeda" stroke="#854f0b" stroke-width="1"/>
<line x1="155.6" y1="64" x2="155.6" y2="108" stroke="#5f5e5a" stroke-width="1"/>
<line x1="251.1" y1="64" x2="251.1" y2="108" stroke="#5f5e5a" stroke-width="1"/>
<line x1="346.7" y1="64" x2="346.7" y2="108" stroke="#5f5e5a" stroke-width="1"/>
<line x1="620" y1="64" x2="620" y2="108" stroke="#5f5e5a" stroke-width="1"/>

<text class="ts s-mut" x="155.6" y="124" text-anchor="middle">3 s · 256</text>
<text class="ts s-mut" x="346.7" y="124" text-anchor="middle">10 s · 768</text>
<text class="ts s-mut" x="620" y="124" text-anchor="end">29 s · 1,500</text>
<text class="ts t-amber-s" x="251.1" y="144" text-anchor="middle">the running example, 5 s · 512</text>

<text class="ts t-gray-s" x="340" y="176" text-anchor="middle">seconds × 50, plus 50 · rounded up to a multiple of 256 · between 256 and 1,500</text>

<rect x="60" y="192" width="560" height="16" rx="4" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="ts t-coral-s" x="340" y="232" text-anchor="middle">with the Core ML encoder: always the full 1,500</text>
</svg>
<figcaption>The encoder pays for the seconds you spoke.</figcaption>
</figure>

<p>The floor of 256 protects quality. Cut shorter, the encoder's output drifts from what the decoder was trained on. Decoding then starts to repeat itself, which is worse than a slow decode.</p>
<p>On this Mac, with Small, one 5.7 s sentence on Metal took a median 76 ms at 512 states, and 107 ms on the full window. That is 29 percent less. On a warm decode, the code calls it the single biggest latency lever.</p>
<p>Clips under about a second came back empty, so each is padded with silence to 1.25 s. The padding costs nothing, since the encoder is billed by <code>audio_ctx</code>, not by the clip.</p>

<h3>The Neural Engine, measured</h3>
<p>You might expect the Neural Engine to be the fast path. For dictation it is not. The published Core ML encoder is compiled for one shape, the full 1,500 states. Asked for 512, it returns an encoding the decoder cannot read, without an error. The 5.7 s sentence came back as "you", in 9 ms.</p>
<p>One clip, four paths, eight timed decodes each.</p>

<figure>
<svg class="diagram" viewBox="0 0 680 290" role="img" xmlns="http://www.w3.org/2000/svg">
<title>One sentence, four encoder paths</title>
<desc>Median decode time for one 5.7 s sentence on Small q8_0, eight decodes each on an Apple M5 Pro. Metal at 512 states, the default: 76 ms, the sentence. Core ML on the Neural Engine at the full 1,500: 83 ms, the sentence. Metal at the full 1,500: 107 ms, the sentence. Core ML at 512, a shape mismatch: 9 ms, and one word, you.</desc>

<text class="th t-gray" x="40" y="66">Metal · 512</text>
<text class="ts t-gray-s" x="40" y="82">scaled, the default</text>
<rect x="200" y="52" width="212.8" height="32" rx="6" fill="#faeeda" stroke="#854f0b" stroke-width="1"/>
<text class="ts t-amber-s" x="421" y="73">76 ms · the sentence</text>

<text class="th t-gray" x="40" y="122">Core ML · 1,500</text>
<text class="ts t-gray-s" x="40" y="138">Neural Engine, full</text>
<rect x="200" y="108" width="232.4" height="32" rx="6" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="ts t-gray-s" x="441" y="129">83 ms · the sentence</text>

<text class="th t-gray" x="40" y="178">Metal · 1,500</text>
<text class="ts t-gray-s" x="40" y="194">GPU, full window</text>
<rect x="200" y="164" width="299.6" height="32" rx="6" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="ts t-gray-s" x="508" y="185">107 ms · the sentence</text>

<text class="th t-coral" x="40" y="234">Core ML · 512</text>
<text class="ts t-coral-s" x="40" y="250">shape mismatch</text>
<rect x="200" y="220" width="25.2" height="32" rx="6" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="ts t-coral-s" x="233" y="241">9 ms · one word, "you"</text>

<text class="ts s-mut" x="340" y="280" text-anchor="middle">Small q8_0 · one 5.7 s sentence, language fixed · median of 8 decodes · M5 Pro · 21 September</text>
</svg>
<figcaption>One sentence, four encoder paths.</figcaption>
</figure>

<p>Core ML must compute the whole window, and lands at 83 ms: behind Metal at 512 states, ahead of Metal on the full window. Quick, but it cannot skip the silence.</p>
<p>The switch is off for a fresh install, and left on for one that already holds an encoder. On, it should draw less power, which has not been measured, for an extra download per model.</p>

<figure>
<img class="window" style="--w:520px" src="{{ '/assets/images/anatomy-hark/07-settings-model.png' | relative_url }}" alt="Settings, Model tab: three speech models with their sizes, and the Neural Engine switch with its note">
<figcaption>Settings › Model. Small in use at 427.5 MB, Medium at 1.39 GB, Large v3 at 2.26 GB, each with its Core ML encoder: the switch is on here, off on a fresh install. Under it, the trade.</figcaption>
</figure>
<p class="note">A note on the Neural Engine. The power saving is the reason the switch exists, and it has not been measured on this Mac. The switch also has a cost the Model tab does not show. Core ML keeps its compiled encoders in the app's cache folder: 1.9 GB once all three models had been loaded. Turning the switch off, or deleting all models, clears it.</p>

<h3>The decode settings</h3>
<p>Every decode uses the same settings, chosen for one short sentence:</p>
<ul>
  <li><strong>One candidate.</strong> The likeliest token at each step, at temperature 0, the setting that removes randomness, with no fallback. A retry pass would double the worst case.</li>
  <li><strong>No memory of the last sentence.</strong> Past text would leak the previous command into this one. One segment, no timestamps.</li>
  <li><strong>A language, detected or fixed.</strong> Detection costs an extra pass. In the first real use, one take of a one-word French answer came back as an English word, in 422 ms of the log's whole engine call. Another, fixed to French, took 55 ms and was right: one reading each. On a bench of short synthesized requests, a fixed language cut the English median from 75 to 51 ms, over 158 and 150 decodes, encoder setting unrecorded. The default stays automatic, for people who dictate in both languages, with one language per utterance.</li>
  <li><strong>Vocabulary, for the words it gets wrong.</strong> Terms go into the prompt, capped at 800 characters, and Whisper reads 224 prompt tokens at most. On 30 synthesized sentences, with the Neural Engine on, a list labelled "Terms:" raised "Hark" from 28 to 36 right out of 48. It cut a name the model already wrote right from 36 of 42 to 25. A prompt helps a word the model has not learned, and hurts one it already writes.</li>
</ul>
<p>Chapter 4 shows why the product's own name is not left to the vocabulary.</p>

<figure>
<img class="window" style="--w:520px" src="{{ '/assets/images/anatomy-hark/08-settings-language-vocabulary.png' | relative_url }}" alt="Language set to detect automatically, and an empty vocabulary list with its help text">
<figcaption>Lower in the Model tab. Language set to detect, and its cost: an extra pass over every utterance. The vocabulary's help names a word the model gets wrong: Hark, the name from the start of this document, made literal.</figcaption>
</figure>

<h3>Silence, and thirty minutes of speech</h3>
<p>Press the dictation key by accident, and a click or a breath is enough to carry the capture past the gates of chapter 2. Whisper then writes something. Trained on subtitled video, it hallucinates on near-silence: it writes text for audio that holds none. Fed two seconds of digital silence directly, Small writes "you". Its <code>no_speech_prob</code>, Whisper's own estimate that the window holds no speech, reads 0.00000032. The first filter trusted that number, and never fired on the silence it was written for.</p>
<p>Every decode now faces six checks.</p>

<figure>
<svg class="diagram" viewBox="0 0 680 470" role="img" xmlns="http://www.w3.org/2000/svg">
<title>What Whisper writes, and what Hark keeps</title>
<desc>Six checks in order. A match on any of them discards the decode as empty_transcript, and a pass moves on to the next. The checks: blank text once annotations are stripped, no_speech_prob of 0.9 or more, a subtitle credit such as Radio-Canada or Amara.org anywhere, a silence phrase such as thank you or merci as the whole utterance, a loop of one word four times, a short run three times or a clause twice, and a weak filler such as you, oui or okay, only on quiet audio. What passes all six is kept.</desc>
<defs>
<marker id="arr-f23" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#5f5e5a" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
</defs>

<rect x="95" y="28" width="340" height="44" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="265" y="43" text-anchor="middle" dominant-baseline="central">Blank text</text>
<text class="ts t-coral-s" x="265" y="59" text-anchor="middle" dominant-baseline="central">nothing left once annotations are stripped</text>
<line x1="265" y1="74" x2="265" y2="88" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f23)"/>
<text class="ts s-mut" x="275" y="86">pass</text>

<rect x="95" y="92" width="340" height="44" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="265" y="107" text-anchor="middle" dominant-baseline="central">Certain silence</text>
<text class="ts t-coral-s" x="265" y="123" text-anchor="middle" dominant-baseline="central">no_speech_prob 0.9 or more</text>
<line x1="265" y1="138" x2="265" y2="152" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f23)"/>
<text class="ts s-mut" x="275" y="150">pass</text>

<rect x="95" y="156" width="340" height="44" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="265" y="171" text-anchor="middle" dominant-baseline="central">A subtitle credit</text>
<text class="ts t-coral-s" x="265" y="187" text-anchor="middle" dominant-baseline="central">anywhere · Radio-Canada, Amara.org</text>
<line x1="265" y1="202" x2="265" y2="216" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f23)"/>
<text class="ts s-mut" x="275" y="214">pass</text>

<rect x="95" y="220" width="340" height="44" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="265" y="235" text-anchor="middle" dominant-baseline="central">A silence phrase</text>
<text class="ts t-coral-s" x="265" y="251" text-anchor="middle" dominant-baseline="central">the whole utterance · thank you, merci</text>
<line x1="265" y1="266" x2="265" y2="280" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f23)"/>
<text class="ts s-mut" x="275" y="278">pass</text>

<rect x="95" y="284" width="340" height="44" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="265" y="299" text-anchor="middle" dominant-baseline="central">A loop</text>
<text class="ts t-coral-s" x="265" y="315" text-anchor="middle" dominant-baseline="central">one word ×4 · a short run ×3 · a clause ×2</text>
<line x1="265" y1="330" x2="265" y2="344" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f23)"/>
<text class="ts s-mut" x="275" y="342">pass</text>

<rect x="95" y="348" width="340" height="44" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="265" y="363" text-anchor="middle" dominant-baseline="central">A weak filler</text>
<text class="ts t-coral-s" x="265" y="379" text-anchor="middle" dominant-baseline="central">only on quiet audio · you, oui, okay</text>
<line x1="265" y1="394" x2="265" y2="408" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f23)"/>
<text class="ts s-mut" x="275" y="406">pass</text>

<rect x="95" y="412" width="340" height="44" rx="10" fill="#e1f5ee" stroke="#0f6e56" stroke-width="1"/>
<text class="th t-teal" x="265" y="427" text-anchor="middle" dominant-baseline="central">Kept</text>
<text class="ts t-teal-s" x="265" y="443" text-anchor="middle" dominant-baseline="central">your words</text>

<path d="M435 50 H525" stroke="#5f5e5a" stroke-width="1.5" fill="none" stroke-dasharray="5 4"/>
<path d="M435 114 H525" stroke="#5f5e5a" stroke-width="1.5" fill="none" stroke-dasharray="5 4"/>
<path d="M435 178 H525" stroke="#5f5e5a" stroke-width="1.5" fill="none" stroke-dasharray="5 4"/>
<path d="M435 242 H525" stroke="#5f5e5a" stroke-width="1.5" fill="none" stroke-dasharray="5 4"/>
<path d="M435 306 H525" stroke="#5f5e5a" stroke-width="1.5" fill="none" stroke-dasharray="5 4"/>
<path d="M435 370 H525" stroke="#5f5e5a" stroke-width="1.5" fill="none" stroke-dasharray="5 4"/>
<path d="M525 50 V406" stroke="#5f5e5a" stroke-width="1.5" fill="none" stroke-dasharray="5 4" marker-end="url(#arr-f23)"/>
<text class="ts s-mut" x="480" y="42" text-anchor="middle">match</text>

<rect x="455" y="412" width="140" height="44" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="525" y="427" text-anchor="middle" dominant-baseline="central">discarded</text>
<text class="ts t-gray-s" x="525" y="443" text-anchor="middle" dominant-baseline="central">empty_transcript</text>
</svg>
<figcaption>What Whisper writes, and what Hark keeps.</figcaption>
</figure>

<p>A loop counts at four copies of one word, three of a two- or three-word run, and two of a whole clause. "Très très bien" stays speech, since people repeat themselves for emphasis. A weak filler is dropped only on quiet audio, a mean RMS under 0.01, or when <code>no_speech_prob</code> reaches 0.6. The lists are bilingual: 32 silence phrases, 12 credits, 36 fillers. A spoken "oui" survives.</p>
<p>Long speech failed the other way. One call over 72 s of synthesized French returned its first 30 s and two stray words. Clips over 30 s are now cut at the first pause of 2 s or more. Without one, the cut falls at the quietest 20 ms of the last 5 s.</p>

<figure>
<svg class="diagram" viewBox="0 0 680 230" role="img" xmlns="http://www.w3.org/2000/svg">
<title>Seventy-two seconds, cut where the speaker paused</title>
<desc>A schematic 72-second clip, positions not to scale with any real recording. The first chunk ends at a pause of 2 s or more, whose silence is skipped. The second has no pause before its 30 s limit, so it is cut at the quietest 20 ms of its last 5 s. The rest forms the third chunk. Measured: 72 s of French in 1.8 s, 62 s of English in 1.3 s, on Small q8_0 with synthesized speech.</desc>
<text class="th t-ink" x="60" y="46">a 72 s clip, schematic</text>

<rect x="60" y="64" width="210" height="36" rx="6" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<rect x="270" y="64" width="23.3" height="36" fill="#f7f6f2" stroke="#c4c2b8" stroke-width="1" stroke-dasharray="3 3"/>
<rect x="293.3" y="64" width="213.9" height="36" rx="6" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<rect x="507.2" y="64" width="112.8" height="36" rx="6" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<line x1="507.2" y1="58" x2="507.2" y2="106" stroke="#993c1d" stroke-width="2"/>

<text class="ts t-gray-s" x="165" y="86" text-anchor="middle">≤ 30 s</text>
<text class="ts t-gray-s" x="400" y="86" text-anchor="middle">≤ 30 s</text>
<text class="ts t-gray-s" x="563.6" y="86" text-anchor="middle">rest</text>

<text class="ts s-mut" x="281.7" y="122" text-anchor="middle">pause ≥ 2 s · skipped</text>
<text class="ts t-coral-s" x="507.2" y="122" text-anchor="middle">quietest 20 ms</text>

<text class="ts t-coral-s" x="340" y="154" text-anchor="middle">no pause before 30 s: cut at the quietest 20 ms of the last 5 s</text>
<text class="ts t-gray-s" x="340" y="184" text-anchor="middle">measured: 72 s of French in 1.8 s · 62 s of English in 1.3 s</text>
<text class="ts s-mut" x="340" y="206" text-anchor="middle">Small q8_0 · synthesized speech · under auto, the first kept chunk sets the language</text>
</svg>
<figcaption>Seventy-two seconds, cut where the speaker paused.</figcaption>
</figure>

<p>Cut this way, the same 72 s came back whole: in 1.8 s on Small when first measured, 0.97 s in a later run. By the project's estimate, with the Neural Engine on, thirty minutes of speech waits about 35 s.</p>

<p>The fastest model is the one already in memory, computing only the seconds you spoke.</p>


<h2>Chapter 4: The decision (text, command or ask)</h2>
<p>Chapter 3 ends with a transcript, text in memory and nothing more. This chapter decides what it is for.</p>
<p>Say a sentence and it is typed. Say "Open Safari." and Safari opens. Say "Hark," first and you are asking. One key does all three, so every rule here must catch what you meant and leave the rest alone.</p>

<h3>Text unless proven otherwise</h3>
<p>In the running example, the sentence is typed into the Mail draft. Nothing opens, nothing is asked: the common case.</p>
<p>Two checks run, in order. First the name, "Hark": a transcript that starts with it goes to the assistant, Ask Hark with nothing selected, unless a command follows at once. Then the command: a sentence made of an opening verb and an app, with nothing after the app, opens that app. Anything else is text.</p>
<p>A password field changes two things. The name is never looked for there. Its text goes to the clipboard, concealed, with <code>raw_text</code> and <code>normalized_text</code> written as <code>null</code>. A command still runs, and its line still hides the words.</p>

<figure>
<svg class="diagram" viewBox="0 0 680 452" role="img" xmlns="http://www.w3.org/2000/svg">
<title>Text, unless proven otherwise</title>
<desc>A decision column. The transcript is checked for the name first, which goes to Ask unless a command follows; then for a verb and an app with nothing after, which opens the app; then for a password field, which sends the text to the clipboard concealed. Everything else is text, delivered to the cursor. The running example starts with the, so it is text.</desc>
<defs>
<marker id="arr-f26" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#5f5e5a" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
</defs>

<rect x="160" y="40" width="300" height="56" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="310" y="58" text-anchor="middle" dominant-baseline="central">Transcript</text>
<text class="ts t-gray-s" x="310" y="76" text-anchor="middle" dominant-baseline="central">normalized · from chapter 3</text>
<line x1="310" y1="100" x2="310" y2="122" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f26)"/>

<rect x="160" y="124" width="300" height="56" rx="10" fill="#e1f5ee" stroke="#0f6e56" stroke-width="1"/>
<text class="th t-teal" x="310" y="142" text-anchor="middle" dominant-baseline="central">Starts with the name</text>
<text class="ts t-teal-s" x="310" y="160" text-anchor="middle" dominant-baseline="central">hark · arc · ark, a greeting allowed before</text>
<text class="ts s-mut" x="146" y="146" text-anchor="end">never in a</text>
<text class="ts s-mut" x="146" y="162" text-anchor="end">password field</text>
<line x1="464" y1="152" x2="494" y2="152" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f26)"/>
<text class="ts t-gray-s" x="477" y="144" text-anchor="middle">yes</text>
<rect x="496" y="128" width="148" height="48" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="570" y="144" text-anchor="middle" dominant-baseline="central">Ask</text>
<text class="ts t-coral-s" x="570" y="162" text-anchor="middle" dominant-baseline="central">chapter 6</text>
<text class="ts s-mut" x="570" y="194" text-anchor="middle">unless a command follows</text>

<line x1="310" y1="184" x2="310" y2="206" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f26)"/>
<text class="ts t-gray-s" x="320" y="197">no</text>

<rect x="160" y="208" width="300" height="56" rx="10" fill="#e1f5ee" stroke="#0f6e56" stroke-width="1"/>
<text class="th t-teal" x="310" y="226" text-anchor="middle" dominant-baseline="central">Verb, app, nothing after</text>
<text class="ts t-teal-s" x="310" y="244" text-anchor="middle" dominant-baseline="central">your verbs, skipped words, aliases</text>
<line x1="464" y1="236" x2="494" y2="236" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f26)"/>
<text class="ts t-gray-s" x="477" y="228" text-anchor="middle">yes</text>
<rect x="496" y="212" width="148" height="48" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="570" y="228" text-anchor="middle" dominant-baseline="central">Open the app</text>
<text class="ts t-gray-s" x="570" y="246" text-anchor="middle" dominant-baseline="central">within 15 s</text>

<line x1="310" y1="268" x2="310" y2="290" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f26)"/>
<text class="ts t-gray-s" x="320" y="281">no</text>

<rect x="160" y="292" width="300" height="56" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="310" y="310" text-anchor="middle" dominant-baseline="central">Password field</text>
<text class="ts t-coral-s" x="310" y="328" text-anchor="middle" dominant-baseline="central">secure input, or a secure field</text>
<line x1="464" y1="320" x2="494" y2="320" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f26)"/>
<text class="ts t-gray-s" x="477" y="312" text-anchor="middle">yes</text>
<rect x="496" y="296" width="148" height="48" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="570" y="312" text-anchor="middle" dominant-baseline="central">Clipboard</text>
<text class="ts t-coral-s" x="570" y="330" text-anchor="middle" dominant-baseline="central">concealed · text null in log</text>

<line x1="310" y1="352" x2="310" y2="374" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f26)"/>
<text class="ts t-gray-s" x="320" y="365">no</text>

<rect x="160" y="376" width="300" height="56" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="310" y="394" text-anchor="middle" dominant-baseline="central">Text</text>
<text class="ts t-gray-s" x="310" y="412" text-anchor="middle" dominant-baseline="central">to the cursor · chapter 5</text>
<text class="ts t-teal-s" x="40" y="390">running example:</text>
<text class="ts t-teal-s" x="40" y="406">starts with "the"</text>
<text class="ts t-teal-s" x="40" y="422">so, text</text>
</svg>
<figcaption>Text, unless proven otherwise.</figcaption>
</figure>

<p>The column is the teal Resolve step, opened up.</p>
<p>Both checks compare a normalized form: lowercase, accents dropped, "œ" spelled "oe", Whisper's annotations removed, punctuation turned into spaces. "Ouvre le Finder." becomes <code>ouvre le finder</code>. The same string fills <code>normalized_text</code>, so a log line shows what the rules saw.</p>
<p>A code review found one ordering problem. A transcript that beat the focus probe from chapter 2 was resolved with no focus. A password field's text then reached the log and an unconcealed clipboard. The reducer from chapter 1 now waits in <code>resolving</code> until the focus is known. Each message to AX gives up after 0.25 s, so the wait is bounded.</p>

<h3>A grammar, not a guess</h3>
<p>"Ouvre le Finder.", open the Finder, opens Finder. "Finder is slow today." is typed. Both name the same app, and only one is a command.</p>
<p>Whisper misspells app names, so the match has to be approximate. On a whole sentence, approximate matching fires on ordinary speech. The rule first specified was measured before any code relied on it. Jaro-Winkler, a string similarity from 0 to 1 that rewards a common start, scored "Finder is slow today." 0.86 against the alias "finder", and "New note for the meeting." 0.867. Both cleared the 0.85 threshold and would have run. "Please open Finder." scored 0.734 and stayed text.</p>

<figure>
<svg class="diagram" viewBox="0 0 680 350" role="img" xmlns="http://www.w3.org/2000/svg">
<title>Why only the app name is approximate</title>
<desc>Jaro-Winkler scores on a scale from 0.70 to 1.00 with the 0.85 threshold marked. Under the first rule, whole sentences such as Finder is slow today pass the threshold while Please open Finder does not. Under the shipped rule only the app name is compared: Fynder passes, fichier does not, and notre scored 0.953 against note until determiners became skipped words.</desc>
<line x1="440" y1="58" x2="440" y2="236" stroke="#993c1d" stroke-width="1" stroke-dasharray="4 3"/>
<line x1="440" y1="264" x2="440" y2="294" stroke="#993c1d" stroke-width="1" stroke-dasharray="4 3"/>
<text class="ts t-coral-s" x="440" y="52" text-anchor="middle">0.85</text>

<text class="th t-ink" x="40" y="44">First rule: the whole sentence against an alias</text>
<text class="ts s-mut" x="40" y="80">Finder is slow today.</text>
<rect x="260" y="67" width="192" height="18" rx="3" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="ts t-coral-s" x="460" y="80">0.86 · would open Finder</text>
<text class="ts s-mut" x="40" y="112">New note for the meeting.</text>
<rect x="260" y="99" width="200" height="18" rx="3" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="ts t-coral-s" x="468" y="112">0.867 · would run "new note"</text>
<text class="ts s-mut" x="40" y="144">Please open Finder.</text>
<rect x="260" y="131" width="41" height="18" rx="3" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="ts t-gray-s" x="309" y="144">0.734 · text</text>

<text class="th t-ink" x="40" y="194">Shipped rule: the app name, after a verb</text>
<text class="ts s-mut" x="40" y="222">Ouvre le Fynder.</text>
<rect x="260" y="209" width="240" height="18" rx="3" fill="#e1f5ee" stroke="#0f6e56" stroke-width="1"/>
<text class="ts t-teal-s" x="508" y="222">0.900 · opens Finder</text>
<text class="ts s-mut" x="40" y="254">Ouvre le fichier.</text>
<rect x="260" y="241" width="116" height="18" rx="3" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="ts t-gray-s" x="384" y="254">0.797 · text</text>
<text class="ts s-mut" x="40" y="286">notre against note: now skipped</text>
<rect x="260" y="273" width="304" height="18" rx="3" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="ts t-coral-s" x="572" y="286">0.953</text>

<text class="ts s-mut" x="260" y="312" text-anchor="middle">0.70</text>
<text class="ts s-mut" x="620" y="312" text-anchor="middle">1.00</text>
<text class="ts s-mut" x="340" y="336" text-anchor="middle">Jaro-Winkler scores, from 0 to 1 · threshold 0.85</text>
</svg>
<figcaption>Why only the app name is approximate.</figcaption>
</figure>

<p>The rule that shipped is a small grammar: an opening verb, skipped words, then an app, then nothing. Verbs and skipped words must be said as written. Only the app name is approximate, compared word by word at 0.85. "Ouvre le Fynder." opens Finder at 0.900. "Ouvre le fichier.", open the file, scores 0.797 and stays text.</p>
<p>The last clause came from a live check on 24 September. "Ouvre le Finder pour demain.", open the Finder for tomorrow, opened Finder. The app must now end the sentence. A polite ending such as "please" may follow it, on main, not yet released.</p>
<p>Each trap found since became a fix. "Notre" scores 0.953 against "note", so determiners became skipped words. Chatty verbs such as "montre", show, left the verb list after "Montre-moi tes notes", show me your notes, opened Notes. The verbs gained their familiar and formal forms, because Whisper hears "affiches-moi" and "ouvrez", then their plural ones, after it heard "Affiche-moi" as "Affichons à".</p>
<p>The specification accepts one cost: a dictation that starts with "ouvre" and an app is a command. That keeps everything else text.</p>
<p>A command does one thing today, open an app. Hark looks for it in six folders and gives it 15 s to come to the front. A miss is named in the log, as <code>app_not_found</code>, <code>app_not_activated</code>, <code>action_timeout</code> and others. Chapter 7 makes every list here yours, and tells why a model does not make this call.</p>

<h3>The name the model cannot spell</h3>
<p>The detail from the start of this document is a design problem. "Hark, …" has to reach the assistant, and the word is not in Whisper's vocabulary.</p>
<p>A bench measured it before any rule: 300 synthesized requests, 1,216 decodes on the Small model. English voices saying "Hark, …" came back as "Hark" 45 times in 100. French voices, once in 100, and as "arc" 27 times. "Hey Hark" in French: 0 of 50. In a live check, a French accent turned "Hark" into "Arc" even in an English sentence.</p>

<figure>
<svg class="diagram" viewBox="0 0 680 256" role="img" xmlns="http://www.w3.org/2000/svg">
<title>The name, as Whisper writes it</title>
<desc>Left: how often Whisper wrote Hark exactly, 45 of 100 English clips, 1 of 100 French clips, 0 of 50 French clips with Hey Hark. Right: Jaro-Winkler against hark with a 0.85 threshold misses arc at 0.72 and catches hard at 0.88 and ark at 0.92. Below: the decision, an exact list of spellings.</desc>
<rect x="40" y="30" width="290" height="150" rx="16" fill="none" stroke="#c4c2b8" stroke-width="1" stroke-dasharray="6 4"/>
<text class="th t-ink" x="60" y="56">Hark written exactly</text>
<text class="ts s-mut" x="60" y="74">synthesized voices · Small</text>
<text class="ts s-mut" x="60" y="104">English, 100 clips</text>
<rect x="190" y="93" width="54" height="14" rx="3" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="ts t-gray-s" x="252" y="104">45</text>
<text class="ts s-mut" x="60" y="130">French, 100 clips</text>
<rect x="190" y="119" width="2" height="14" rx="1" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="ts t-coral-s" x="200" y="130">1</text>
<text class="ts s-mut" x="60" y="156">Hey Hark, French, 50</text>
<text class="ts t-coral-s" x="196" y="156">0</text>

<rect x="350" y="30" width="290" height="150" rx="16" fill="none" stroke="#c4c2b8" stroke-width="1" stroke-dasharray="6 4"/>
<text class="th t-ink" x="370" y="56">Jaro-Winkler, against hark</text>
<text class="ts s-mut" x="370" y="74">threshold 0.85</text>
<line x1="540" y1="84" x2="540" y2="164" stroke="#993c1d" stroke-width="1" stroke-dasharray="4 3"/>
<text class="ts s-mut" x="370" y="104">arc 0.72</text>
<rect x="460" y="93" width="11" height="14" rx="3" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="ts t-coral-s" x="479" y="104">missed</text>
<text class="ts s-mut" x="370" y="130">hard 0.88</text>
<rect x="460" y="119" width="96" height="14" rx="3" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="ts t-coral-s" x="564" y="130">caught, wrongly</text>
<text class="ts s-mut" x="370" y="156">ark 0.92</text>
<rect x="460" y="145" width="117" height="14" rx="3" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="ts t-gray-s" x="585" y="156">caught</text>

<rect x="160" y="196" width="360" height="48" rx="10" fill="#e1f5ee" stroke="#0f6e56" stroke-width="1"/>
<text class="th t-teal" x="340" y="212" text-anchor="middle" dominant-baseline="central">An exact list: hark · arc · ark</text>
<text class="ts t-teal-s" x="340" y="230" text-anchor="middle" dominant-baseline="central">arke on main, not yet released</text>
</svg>
<figcaption>The name, as Whisper writes it.</figcaption>
</figure>

<p>A fuzzy rule fails both ways. Against "hark", "arc" scores 0.72 and is missed, while "hard" (0.88) and "ark" (0.92) pass. Against "arc", "marc" and "parc" score 0.92. The vocabulary prompt from chapter 3 did not rescue it. When the prompt failed, Whisper mostly left the word out, and a missing prefix cannot be matched at all.</p>
<p>So the name is a list, matched exactly after normalization. A greeting may come before the name, but a greeting alone does nothing. The name must end where a word ends, so "Arc-en-ciel", rainbow, and "Hark's" stay dictation. No comma is required: of the 28 French requests where Whisper wrote the name at all, 18 had no comma after it. This is the block 0.0.4 ships:</p>
<pre><code>assistant:
  prefix: [hark, arc, ark]
  greetings: [hey, hello, salut]</code></pre>
<p>"arke" joins the list on main, not yet released, after a live check. A sentence that really starts with "Arc" goes to the assistant, and that cost is accepted.</p>
<p>Text is the default. A command has to prove itself.</p>

<h2>Chapter 5: Delivery</h2>
<p>The running example is text now. It has to land at the caret, in an app Hark does not control.</p>
<p>macOS offers no general way to type into another app's field and know it worked. This chapter is the coral step, the one that delivers and checks.</p>

<h3>Three ways in, tried in order</h3>
<p>The sentence appears at the caret in the Mail draft. Half a second later, your clipboard is as you left it. Three routes stand behind that, and the focus read at key down picks the first:</p>
<ul>
  <li><strong>Accessibility.</strong> Hark sets the field's selected text through AX, then reads the field back. An exact new character count, or the caret exactly past the text, confirms it. Any other change rules out a second try, since a field that rewrote "..." as "…" did take the text. Only a field where nothing moved gets a paste. Safari's web text areas are one: they accept the set and ignore it.</li>
  <li><strong>Paste.</strong> The text goes on the clipboard and Hark posts Command-V, for fields that Accessibility cannot set, or whose answers cannot be trusted.</li>
  <li><strong>Clipboard.</strong> The text stays there for you to paste, with a reason in the log: no field, a password field, or a paste nobody read.</li>
</ul>
<p>A set that timed out is the opposite risk, since the app may still apply it. That text goes to the clipboard as <code>insertion_timeout</code>, never typed twice.</p>

<figure>
<svg class="diagram" viewBox="0 0 680 444" role="img" xmlns="http://www.w3.org/2000/svg">
<title>Field, paste, or clipboard with a reason</title>
<desc>The focus is known at key down. Hark tries an Accessibility insert and reads it back; if nothing moved, it pastes; if no app reads the paste within 1 s, the text goes to the clipboard with a reason. The running example, a Mail draft, goes straight from the focus to the paste. The log line ends as text_inserted or text_clipboard.</desc>
<defs>
<marker id="arr-f29" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#5f5e5a" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
<marker id="arr-f29-teal" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#0f6e56" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
</defs>

<rect x="160" y="40" width="300" height="56" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="310" y="58" text-anchor="middle" dominant-baseline="central">Focus at key down</text>
<text class="ts t-gray-s" x="310" y="76" text-anchor="middle" dominant-baseline="central">Mail · draft body · value settable</text>
<line x1="310" y1="100" x2="310" y2="122" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f29)"/>

<rect x="160" y="128" width="300" height="56" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="310" y="146" text-anchor="middle" dominant-baseline="central">Accessibility insert</text>
<text class="ts t-gray-s" x="310" y="164" text-anchor="middle" dominant-baseline="central">set the selection · read it back</text>
<text class="ts s-mut" x="480" y="160">native text fields</text>
<line x1="310" y1="188" x2="310" y2="210" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f29)"/>
<text class="ts t-gray-s" x="320" y="203">nothing moved</text>

<rect x="160" y="216" width="300" height="56" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="310" y="234" text-anchor="middle" dominant-baseline="central">Paste</text>
<text class="ts t-gray-s" x="310" y="252" text-anchor="middle" dominant-baseline="central">a pasteboard promise · ⌘V</text>
<text class="ts s-mut" x="480" y="232">Mail drafts, terminals,</text>
<text class="ts s-mut" x="480" y="248">Chromium, Electron,</text>
<text class="ts s-mut" x="480" y="264">Firefox, JetBrains</text>
<line x1="310" y1="276" x2="310" y2="298" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f29)"/>
<text class="ts t-gray-s" x="320" y="291">not read in 1 s</text>

<rect x="160" y="304" width="300" height="56" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="310" y="322" text-anchor="middle" dominant-baseline="central">Clipboard</text>
<text class="ts t-coral-s" x="310" y="340" text-anchor="middle" dominant-baseline="central">with a reason · a notification</text>
<text class="ts s-mut" x="480" y="328">no field · password field</text>
<text class="ts s-mut" x="480" y="344">a set that timed out</text>

<path d="M160 68 L120 68 L120 244 L158 244" stroke="#0f6e56" stroke-width="1.5" fill="none" stroke-dasharray="5 4" marker-end="url(#arr-f29-teal)"/>
<text class="ts t-teal-s" x="110" y="150" text-anchor="end">running</text>
<text class="ts t-teal-s" x="110" y="166" text-anchor="end">example</text>

<text class="ts s-mut" x="148" y="406" text-anchor="end">the log line</text>
<rect x="160" y="388" width="140" height="30" rx="8" fill="#e1f5ee" stroke="#0f6e56" stroke-width="1"/>
<text class="ts t-teal-s" x="230" y="403" text-anchor="middle" dominant-baseline="central">text_inserted</text>
<rect x="320" y="388" width="140" height="30" rx="8" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="ts t-coral-s" x="390" y="403" text-anchor="middle" dominant-baseline="central">text_clipboard</text>
</svg>
<figcaption>Field, paste, or clipboard with a reason.</figcaption>
</figure>

<p>Some apps always get a paste: terminals, Chromium browsers, Firefox, JetBrains IDEs, Electron apps such as Slack and VS Code, and any app that embeds Chromium.</p>
<p>In Chromium and Electron apps, an unknown focus most likely means a web field, because their Accessibility tree is off. In a native app it means nothing has focus, and a paste would land nowhere, so the text goes to the clipboard. Chapter 7 shows how to override the choice for any app.</p>
<p>The running example carries a late discovery. Mail's draft body is a web area that answers no selected text. Until 0.0.4, Hark counted it as no field, and every dictation into a Mail draft went to the clipboard as <code>no_text_field</code>. Now a web area whose value can be set counts as a field, and gets a paste.</p>
<p>One guard runs last, right before the text is sent. If the app in front changed since key down, the text goes to the clipboard as <code>focus_changed</code>. The route itself is a menu in Settings:</p>

<figure>
<img class="window" style="--w:520px" src="{{ '/assets/images/anatomy-hark/09-settings-dictation.png' | relative_url }}" alt="Settings, General tab, Dictation section: insertion method, clipboard fallback, live transcript and lower other audio">
<figcaption>Settings › General, Dictation. Automatic insertion, Accessibility then a paste, with the clipboard fallback on. Other audio lowered, and a notification with sound. The live transcript is on here, off by default. The three ways in, one menu.</figcaption>
</figure>

<h3>The paste that counts only when it is read</h3>
<p>You copied a link before you spoke. After the sentence lands in Mail, the link is back on the clipboard. Keeping that promise took a second design.</p>
<p>No API tells an app when another app has consumed a paste. The first version restored the clipboard on a timer. A code review found the flaw: a slow app could paste your old contents, the text was lost, and the log still said <code>text_inserted</code>.</p>
<p>Hark now keeps a copy of your clipboard. It writes the text as a pasteboard promise, clipboard data supplied only when an app reads it. A transient marker makes clipboard managers skip it. Then Hark posts Command-V. The paste counts only when an app reads the promise, which it does as it handles Command-V, in milliseconds. Your contents come back 500 ms after that read, and only if the clipboard still holds Hark's write. Anything newer is yours to keep.</p>

<figure>
<svg class="diagram" viewBox="0 0 680 360" role="img" xmlns="http://www.w3.org/2000/svg">
<title>A paste that counts only when it is read</title>
<desc>Three lifelines: Hark, the pasteboard and Mail. Hark keeps a copy of the clipboard, writes the text as a transient promise, and posts Command-V for the current keyboard layout. Mail reads the promise in milliseconds, which tells Hark the text is inserted. 500 ms later Hark puts the old contents back. With no read within 1 s the line says paste_not_consumed and the text stays on the clipboard.</desc>
<defs>
<marker id="arr-f31" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#5f5e5a" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
<marker id="arr-f31-teal" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#0f6e56" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
</defs>

<rect x="45" y="40" width="150" height="44" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="120" y="54" text-anchor="middle" dominant-baseline="central">Hark</text>
<text class="ts t-gray-s" x="120" y="72" text-anchor="middle" dominant-baseline="central">delivery</text>
<rect x="265" y="40" width="150" height="44" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="340" y="54" text-anchor="middle" dominant-baseline="central">Pasteboard</text>
<text class="ts t-gray-s" x="340" y="72" text-anchor="middle" dominant-baseline="central">your clipboard</text>
<rect x="485" y="40" width="150" height="44" rx="10" fill="#e1f5ee" stroke="#0f6e56" stroke-width="1"/>
<text class="th t-teal" x="560" y="54" text-anchor="middle" dominant-baseline="central">Mail</text>
<text class="ts t-teal-s" x="560" y="72" text-anchor="middle" dominant-baseline="central">your draft</text>

<line x1="120" y1="84" x2="120" y2="320" stroke="#c4c2b8" stroke-width="1" stroke-dasharray="6 4"/>
<line x1="340" y1="84" x2="340" y2="320" stroke="#c4c2b8" stroke-width="1" stroke-dasharray="6 4"/>
<line x1="560" y1="84" x2="560" y2="320" stroke="#c4c2b8" stroke-width="1" stroke-dasharray="6 4"/>

<text class="ts t-gray-s" x="230" y="110" text-anchor="middle">keep a copy of yours</text>
<path d="M122 116 L334 116" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f31)"/>
<text class="ts t-gray-s" x="230" y="148" text-anchor="middle">write a promise · transient</text>
<path d="M122 154 L334 154" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f31)"/>
<text class="ts t-gray-s" x="230" y="186" text-anchor="middle">⌘V · this keyboard layout</text>
<path d="M122 192 L554 192" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f31)"/>
<text class="ts t-teal-s" x="450" y="224" text-anchor="middle">reads it · in milliseconds</text>
<path d="M558 230 L346 230" stroke="#0f6e56" stroke-width="1.5" fill="none" marker-end="url(#arr-f31-teal)"/>
<text class="ts t-gray-s" x="230" y="262" text-anchor="middle">read: text_inserted</text>
<path d="M338 268 L126 268" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f31)"/>
<text class="ts t-gray-s" x="230" y="300" text-anchor="middle">500 ms later: yours back</text>
<path d="M122 306 L334 306" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f31)"/>

<text class="ts t-coral-s" x="340" y="346" text-anchor="middle">no read within 1 s: paste_not_consumed · the text stays on the clipboard</text>
</svg>
<figcaption>A paste that counts only when it is read.</figcaption>
</figure>

<p>Hark treats no read within 1 s as no read at all. The line says <code>paste_not_consumed</code>, and the text stays on the clipboard instead of your old contents. The restore waits while the pipeline is already idle, so it costs the next sentence nothing.</p>
<p>Command-V depends on the keyboard. Hark posts it with the key code that the current layout gives V. The risk is real: during testing, a test script's Command-A, built from the US key code for A, pressed Command-Q under AZERTY and quit TextEdit. Local keyboard events are held back while the keys are posted, so a key you still hold does not mix in.</p>

<h3>Small courtesies</h3>
<p>The rest is detail, and each detail came from a failure:</p>
<ul>
  <li><strong>Spacing.</strong> Two dictations in a row once gave "Hello there.Next sentence." Hark now reads the characters before the caret and adds a space after a letter, a digit or closing punctuation. A Mail draft does not say, so there the text goes in as Whisper wrote it.</li>
  <li><strong>No accidental Return.</strong> Trailing line breaks are removed before the text is sent. They would send a chat message or run a terminal line.</li>
  <li><strong>Nothing silent.</strong> When text goes to the clipboard, a notification shows its first 40 characters, with sound, silent, or off. For a password field it says the text is hidden.</li>
</ul>
<p>Two exits, never ambiguous: the field, or the clipboard with a reason. Unless you turn the fallback off, nothing you said is lost.</p>

<h2>Chapter 6: Ask Hark</h2>
<p>Chapters 2 to 5 never wait on a language model. That rule came before Ask Hark existed, and Ask Hark keeps it: the model runs outside the process.</p>
<p>An ask is one gesture: select text, say what you want done with it, then choose what to keep. A companion example runs through this chapter, in Notes. Select a short paragraph about a meeting, press the Ask key, say "Turn it into a bulleted list.", and press Return.</p>

<h3>Three ways to ask</h3>
<p>An ask starts in one of three places:</p>
<ul>
  <li><strong>Services › Ask Hark</strong>. On text selected in any app, since 0.0.3.</li>
  <li><strong>The Ask key</strong>. Since 0.0.4. On a selection, it asks about that text, with Replace. With nothing selected, it opens Ask Hark as an assistant, with Insert or Copy.</li>
  <li><strong>The name</strong>. "Hark," at the start of a sentence on the dictation key, decided in chapter 4.</li>
</ul>
<p>Services came first. Offered by macOS on selected text in every app, it is the only public route into another app's text menu, and AppKit draws the item itself.</p>
<p>The Ask key reads the selection before the microphone opens. Accessibility answers first, in 0 to 2 ms on this Mac. Where it returns nothing, in web page text, Mail, Chromium and Electron apps, Hark sends Command-C, waits up to 250 ms, then puts your clipboard back. That copy has a cost: in a Chromium-based app with nothing selected, the microphone opened 278 ms after the press, not yet fixed. Never in a password field. Never in editors whose Command-C copies the whole line, such as VS Code, where a question would become an ask about a line of code.</p>
<p>With the Ask key or Services, the words are an instruction from the press, never matched as a command or typed at the caret. The HUD stays hidden, and the Ask panel shows the listening state instead.</p>
<figure>
<img class="window" style="--w:520px" src="{{ '/assets/images/anatomy-hark/10-ask-listening.png' | relative_url }}" alt="Ask Hark panel listening for a spoken instruction about the selected text">
<figcaption>Ask Hark on a selection. A red microphone, the sample paragraph in two lines, Listening… and the hint to say what to do, then press Return. Cancel, or Done. The selection has not left Hark yet.</figcaption>
</figure>

<h3>A model next door</h3>
<p>Whisper lives inside Hark. The language model does not. It runs in a separate server that speaks the OpenAI-compatible chat API, on this Mac by default, at <code>127.0.0.1:8000/v1</code>. Hark never starts or stops it, and its memory is not Hark's. That boundary is the memory decision behind Ask: the largest thing an ask needs lives in a process you start, size and stop. On this Mac, the server runs a 27-billion-parameter model on port 8002.</p>
<p>While you speak, <code>GET /models</code> checks the server, in about 5 ms on this Mac. A closed port refuses in 0.1 ms, so a stopped server says so before your instruction is spent. Then one streaming request goes out. A hand-written parser reads the reply as server-sent events (SSE), text lines over one HTTP response. Each update carries the whole text so far. Only the newest is kept, so a slow screen drops frames instead of queueing them.</p>
<p>Cancel closes the connection, which makes the server stop writing. After a cancel, the next ask's first word came in 799 to 832 ms, against 806 ms on an idle server, so nothing kept running.</p>
<figure>
<svg class="diagram" viewBox="0 0 680 404" role="img" xmlns="http://www.w3.org/2000/svg">
<title>One request out, one stream back</title>
<desc>Hark, one process, holds the Ask panel, a language client with a hand-written SSE parser, and a key read from the Keychain per request. A separate model server on this Mac exposes an OpenAI-compatible API, serves a 27B model and keeps its own log. Between them, a model check while you speak, answered in about 5 ms, one streamed chat request, the first word in 0.7 to 1.0 s, then 25 to 36 tokens a second, and a cancel that closes the stream.</desc>
<defs>
<marker id="arr-f34" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#5f5e5a" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
</defs>

<rect x="40" y="44" width="200" height="328" rx="16" fill="none" stroke="#c4c2b8" stroke-width="1" stroke-dasharray="6 4"/>
<text class="th t-ink" x="56" y="70">Hark</text>
<text class="ts s-mut" x="56" y="88">one process</text>

<rect x="56" y="104" width="168" height="60" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="140" y="128" text-anchor="middle">Ask panel</text>
<text class="ts t-gray-s" x="140" y="148" text-anchor="middle">listen · wait · review</text>

<rect x="56" y="180" width="168" height="116" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="140" y="206" text-anchor="middle">Language client</text>
<text class="ts t-gray-s" x="140" y="228" text-anchor="middle">URLSession, one stream</text>
<text class="ts t-gray-s" x="140" y="248" text-anchor="middle">hand-written SSE parser</text>
<text class="ts t-gray-s" x="140" y="268" text-anchor="middle">keeps the newest text</text>

<rect x="56" y="312" width="168" height="44" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="140" y="330" text-anchor="middle">Keychain</text>
<text class="ts t-coral-s" x="140" y="348" text-anchor="middle">the key, per request</text>

<rect x="440" y="44" width="200" height="328" rx="16" fill="none" stroke="#993c1d" stroke-width="1" stroke-dasharray="6 4"/>
<text class="th t-coral" x="456" y="70">Model server</text>
<text class="ts t-coral-s" x="456" y="88">separate process</text>
<text class="ts t-coral-s" x="456" y="104">not Hark's memory</text>

<rect x="456" y="120" width="168" height="100" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="540" y="144" text-anchor="middle">OpenAI-compatible</text>
<text class="ts t-gray-s" x="540" y="166" text-anchor="middle">/v1/models</text>
<text class="ts t-gray-s" x="540" y="186" text-anchor="middle">/v1/chat/completions</text>
<text class="ts t-gray-s" x="540" y="206" text-anchor="middle">streamed</text>

<rect x="456" y="236" width="168" height="60" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="540" y="260" text-anchor="middle">A 27B model</text>
<text class="ts t-gray-s" x="540" y="280" text-anchor="middle">on this Mac, port 8002</text>

<rect x="456" y="312" width="168" height="44" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="540" y="330" text-anchor="middle">Its own log</text>
<text class="ts t-gray-s" x="540" y="348" text-anchor="middle">not Hark's file</text>

<text class="ts t-gray-s" x="340" y="122" text-anchor="middle">GET /models, while you speak</text>
<line x1="242" y1="130" x2="437" y2="130" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f34)"/>
<line x1="438" y1="146" x2="243" y2="146" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f34)"/>
<text class="ts t-gray-s" x="340" y="162" text-anchor="middle">about 5 ms</text>

<text class="ts t-gray-s" x="340" y="188" text-anchor="middle">POST chat, one stream</text>
<line x1="242" y1="196" x2="437" y2="196" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f34)"/>
<line x1="438" y1="212" x2="243" y2="212" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f34)"/>
<text class="ts t-gray-s" x="340" y="228" text-anchor="middle">first word in 0.7 to 1.0 s</text>

<line x1="438" y1="262" x2="243" y2="262" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f34)"/>
<text class="ts t-gray-s" x="340" y="278" text-anchor="middle">then 25 to 36 tokens a second</text>

<path d="M242 302 L437 302" stroke="#5f5e5a" stroke-width="1.5" fill="none" stroke-dasharray="5 4" marker-end="url(#arr-f34)"/>
<text class="ts t-coral-s" x="340" y="318" text-anchor="middle">cancel: close the stream</text>

<text class="ts s-mut" x="340" y="394" text-anchor="middle">127.0.0.1 by default · https for any other host · no redirect</text>
</svg>
<figcaption>One request out, one stream back.</figcaption>
</figure>
<p>The rules are flat. Plain http goes only to this Mac, https anywhere else, and no redirect is followed. The key comes from the login Keychain on each request. It is never in <code>commands.yaml</code> or the log. Timeouts: 2 s to connect, 15 s of silence before the first word, 60 s in all. A server off this Mac is possible, and the Ask panel then names its host.</p>
<figure>
<img class="window" style="--w:520px" src="{{ '/assets/images/anatomy-hark/12-settings-ask.png' | relative_url }}" alt="Settings, Ask tab: a server address on this Mac and a key saved in the Keychain">
<figcaption>Settings › Ask, its Server card. The address, <code>http://127.0.0.1:8002/v1</code>, on this Mac, not the default port 8000. The API key, Saved, in the login Keychain and never shown again. The server next door.</figcaption>
</figure>

<h3>Waiting, then writing</h3>
<p>After Return, the Ask panel says Thinking…, then the answer arrives line by line. The first word, the time to first token (TTFT), waits on the server reading the prompt. The rest arrives at the rate the model writes.</p>
<figure>
<img class="window" style="--w:520px" src="{{ '/assets/images/anatomy-hark/13a-ask-thinking.png' | relative_url }}" alt="Ask Hark waiting for the model server at 127.0.0.1:8002">
<img class="window" style="--w:520px" src="{{ '/assets/images/anatomy-hark/13b-ask-streaming.png' | relative_url }}" alt="Ask Hark with a bulleted answer arriving line by line">
<figcaption>Waiting, then writing, under the sample instruction as the title. Above, after 3 s of Thinking…, the Ask panel names the server, <code>127.0.0.1:8002</code>. Below, the answer arrives, its last line cut short. Two latencies, two states.</figcaption>
</figure>
<p>The numbers come from this Mac and its 27-billion-parameter model, 10 asks run 3 times each, with thinking, the model's reasoning pass, off. The server's first chunk came back in a median 1.8 ms. The first word took 0.7 to 1.0 s for a typical ask, 837 ms as the median of all 30 runs.</p>
<p>The model then wrote 25 to 36 tokens a second, and the median ask took 3.59 s in all. The prompt is read at 263 to 355 tokens a second, so a 3,000-token selection waits about 8 to 11 s before its first word.</p>
<figure>
<svg class="diagram" viewBox="0 0 680 244" role="img" xmlns="http://www.w3.org/2000/svg">
<title>The first word, then the rest</title>
<desc>A timeline of an ask with thinking off, medians of 30 runs: the server's first chunk at 1.8 ms, the prompt read until the first word at 837 ms, then writing at 25 to 36 tokens a second until the last word at 3.59 s. With thinking left on, no word came until 7.4 s, off this scale.</desc>
<defs>
<marker id="arr-f37" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#5f5e5a" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
</defs>

<text class="th t-ink" x="40" y="76">An ask</text>
<text class="ts s-mut" x="40" y="92">thinking off, medians</text>

<line x1="160" y1="28" x2="160" y2="98" stroke="#5f5e5a" stroke-width="1"/>
<text class="ts t-gray-s" x="166" y="38">first chunk · 1.8 ms</text>

<rect x="160" y="73" width="86" height="10" rx="3" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="ts t-gray-s" x="166" y="58">reading the prompt</text>

<rect x="246" y="64" width="280" height="28" rx="6" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="ts t-gray-s" x="386" y="82" text-anchor="middle">writing · 25 to 36 tokens a second</text>

<line x1="246" y1="92" x2="246" y2="100" stroke="#5f5e5a" stroke-width="1"/>
<text class="ts t-gray-s" x="246" y="114" text-anchor="middle">first word · 837 ms</text>
<line x1="526" y1="92" x2="526" y2="100" stroke="#5f5e5a" stroke-width="1"/>
<text class="ts t-gray-s" x="526" y="114" text-anchor="middle">last word · 3.59 s</text>

<text class="th t-ink" x="40" y="148">Thinking on</text>
<text class="ts s-mut" x="40" y="164">one case, 3 runs</text>
<rect x="160" y="140" width="444" height="20" rx="4" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="ts t-coral-s" x="382" y="154" text-anchor="middle">no word until 7.4 s</text>
<line x1="606" y1="150" x2="630" y2="150" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f37)"/>

<line x1="160" y1="184" x2="620" y2="184" stroke="#5f5e5a" stroke-width="1"/>
<line x1="160" y1="184" x2="160" y2="190" stroke="#5f5e5a" stroke-width="1"/>
<line x1="262.2" y1="184" x2="262.2" y2="190" stroke="#5f5e5a" stroke-width="1"/>
<line x1="364.4" y1="184" x2="364.4" y2="190" stroke="#5f5e5a" stroke-width="1"/>
<line x1="466.7" y1="184" x2="466.7" y2="190" stroke="#5f5e5a" stroke-width="1"/>
<line x1="568.9" y1="184" x2="568.9" y2="190" stroke="#5f5e5a" stroke-width="1"/>
<text class="ts s-mut" x="160" y="206" text-anchor="middle">0 s</text>
<text class="ts s-mut" x="262.2" y="206" text-anchor="middle">1 s</text>
<text class="ts s-mut" x="364.4" y="206" text-anchor="middle">2 s</text>
<text class="ts s-mut" x="466.7" y="206" text-anchor="middle">3 s</text>
<text class="ts s-mut" x="568.9" y="206" text-anchor="middle">4 s</text>

<text class="ts s-mut" x="340" y="232" text-anchor="middle">10 asks, 3 runs each · at most 1,024 tokens · a 27B model on this Mac</text>
</svg>
<figcaption>The first word, then the rest.</figcaption>
</figure>
<p>The gap between the first chunk and the first word is why Thinking… is a state of its own. For scale, a 5.7 s sentence needs about 100 to 110 ms after key up, a sum of parts never measured end to end.</p>
<p>Two defaults come from the same measurements. Thinking stays off: left on, the first word came at 7.4 s instead of 0.9 s. The temperature is 0.3. At the server's default of 1.0, one politer rewrite invented a request the text never made.</p>

<h3>Nothing changes until you choose</h3>
<p>The answer ends complete and editable. Cancel, Copy, or Replace with Command-Return. Until then, nothing in Notes has changed.</p>
<figure>
<img class="window" style="--w:520px" src="{{ '/assets/images/anatomy-hark/14-ask-reviewing.png' | relative_url }}" alt="Ask Hark panel with a finished bulleted list and Cancel, Copy and Replace buttons">
<figcaption>The answer, complete and editable: three bullets, the last one now whole. Then Cancel, Copy, or Replace, <code>⌘↩</code>, the only button that touches Notes. Nothing changes until you choose.</figcaption>
</figure>
<p>Replace is guarded. Hark brings the caller back and waits up to 600 ms for its focus to settle, since Safari briefly reports none. It reads the selection again and compares words, not white space, which each route reports differently. If the app or the selection changed, the answer goes to the clipboard as <code>selection_changed</code>. Otherwise it goes in as a dictation would, through the same inserter and fallbacks as chapter 5.</p>
<p>The prompts are rules, fixed in code, and the selection is data, never instructions. The answer keeps its language, its tone, and its tu or vous, and adds or removes nothing unless asked. The assistant says in one sentence when a request needs mail, a calendar, files or the web.</p>
<p>In the Mail draft from the start of this document, with nothing selected, press the Ask key and say "Write an email to decline Thursday's meeting." A text field had focus, so Insert is offered. Without one, only Copy.</p>
<figure>
<img class="window" style="--w:520px" src="{{ '/assets/images/anatomy-hark/15a-assistant-insert.png' | relative_url }}" alt="Assistant draft declining Thursday's meeting, with Cancel, Copy and Insert">
<img class="window" style="--w:520px" src="{{ '/assets/images/anatomy-hark/15b-assistant-copy.png' | relative_url }}" alt="The same draft with only Cancel and Copy">
<figcaption>The Ask key with nothing selected, the sample request as the title. Above, with a text field in focus: Cancel, Copy, Insert. Below, with none: Cancel and Copy. One answer, two contexts.</figcaption>
</figure>
<p>A stopped server is one sentence in the Ask panel, with Retry, and Copy Instruction keeps the spoken words.</p>
<figure>
<img class="window" style="--w:520px" src="{{ '/assets/images/anatomy-hark/16-ask-error.png' | relative_url }}" alt="Ask Hark panel saying the model server is not running at 127.0.0.1:8002, with Cancel, Copy Instruction and Retry">
<figcaption>A stopped server, under the sample instruction. One sentence names the address, <code>127.0.0.1:8002</code>, and what to do. Then Cancel, Copy Instruction, or Retry. Dictation never waits on this panel.</figcaption>
</figure>
<p>The model can be slow, wrong or stopped. None of that reaches dictation.</p>
<p class="note">One more detail. The model server on this Mac keeps its own log, and its preview of each request holds the first 23 characters of the message. Hark opens every request with a fixed line longer than that, so the preview never holds a word you said. Hark's own log keeps the spoken instruction, the model's name and its time. It never keeps the selection or the answer.</p>

<h2>Chapter 7: commands.yaml</h2>
<p>Every chapter so far named a default: a key, a model, a verb list, a server. Here each becomes yours.</p>
<p>Each change has a cost. The same key types your words, runs your commands and reaches Ask Hark, so every new option is also a new way to misfire. Three habits keep that in check: a strict grammar where fuzzy matching would catch ordinary speech, a measurement before each rule, and a gesture wherever a guess would be wrong often enough to hurt.</p>

<h3>Where your changes live</h3>
<p>You shape Hark in three places. Gestures say what you want before you speak: three keys, each rebindable, and a tap or a hold. One readable file, <code>commands.yaml</code>, holds your rules: verbs, apps and their nicknames, per-app typing rules, the assistant's name, model servers. A few switches in Settings cover the rest.</p>

<figure>
<svg class="diagram" viewBox="0 0 680 336" role="img" xmlns="http://www.w3.org/2000/svg">
<title>Three surfaces you shape, three stores behind them</title>
<desc>Three teal surfaces: gestures (three keys, tap or hold), a few switches (Settings, seven tabs) and one file (commands.yaml). The keys and the switches are kept in the app's defaults, one key each. The switches also write API keys to the Keychain, a guarded store. The file lives in Application Support and is reloaded when saved, and the Commands and Ask tabs write it too.</desc>
<rect x="40" y="44" width="600" height="272" rx="16" fill="none" stroke="#c4c2b8" stroke-width="1" stroke-dasharray="6 4"/>
<text class="th t-ink" x="60" y="70">Yours to shape</text>
<text class="ts s-mut" x="60" y="88">three surfaces, each with its store</text>

<rect x="60" y="104" width="176" height="96" rx="10" fill="#e1f5ee" stroke="#0f6e56" stroke-width="1"/>
<text class="th t-teal" x="148" y="130" text-anchor="middle">Gestures</text>
<text class="ts t-teal-s" x="148" y="150" text-anchor="middle">three keys</text>
<text class="ts t-teal-s" x="148" y="172" text-anchor="middle">tap or hold</text>

<rect x="252" y="104" width="176" height="96" rx="10" fill="#e1f5ee" stroke="#0f6e56" stroke-width="1"/>
<text class="th t-teal" x="340" y="130" text-anchor="middle">A few switches</text>
<text class="ts t-teal-s" x="340" y="150" text-anchor="middle">Settings, 7 tabs</text>
<text class="ts t-teal-s" x="340" y="172" text-anchor="middle">mic · model · language</text>

<rect x="444" y="104" width="176" height="96" rx="10" fill="#e1f5ee" stroke="#0f6e56" stroke-width="1"/>
<text class="th t-teal" x="532" y="130" text-anchor="middle">One file</text>
<text class="ts t-teal-s" x="532" y="150" text-anchor="middle">commands.yaml</text>
<text class="ts t-teal-s" x="532" y="172" text-anchor="middle">verbs · apps · servers</text>

<line x1="148" y1="200" x2="148" y2="224" stroke="#5f5e5a" stroke-width="1"/>
<path d="M296 200 L296 212 L200 212 L200 224" stroke="#5f5e5a" stroke-width="1" fill="none"/>
<line x1="376" y1="200" x2="376" y2="224" stroke="#5f5e5a" stroke-width="1"/>
<line x1="532" y1="200" x2="532" y2="224" stroke="#5f5e5a" stroke-width="1"/>

<rect x="60" y="224" width="176" height="72" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="148" y="254" text-anchor="middle">The app's defaults</text>
<text class="ts t-gray-s" x="148" y="276" text-anchor="middle">one key each</text>

<rect x="252" y="224" width="176" height="72" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="340" y="254" text-anchor="middle">Keychain</text>
<text class="ts t-coral-s" x="340" y="276" text-anchor="middle">API keys, nothing else</text>

<rect x="444" y="224" width="176" height="72" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="532" y="250" text-anchor="middle">Application Support</text>
<text class="ts t-gray-s" x="532" y="270" text-anchor="middle">reloaded when saved</text>
<text class="ts t-gray-s" x="532" y="286" text-anchor="middle">Settings writes it too</text>
</svg>
<figcaption>Three surfaces you shape, three stores behind them.</figcaption>
</figure>

<p>Behind them sit three stores: the file for rules, the app's defaults for the switches and key chords, one entry each, and the Keychain for API keys alone. For commands and the Ask server, Settings edits the file and does not own the state.</p>

<h3>One file, the source of truth</h3>
<p>Open <code>commands.yaml</code> in any editor, change a line, save. The next sentence uses it. Hark watches the file and its folder, so an editor that saves by renaming a new file into place is still seen. Changes settle for 100 ms, and a save that changes nothing is ignored.</p>
<p>A file edited by hand will hold a typo one day. It never breaks Hark. The parser is strict: no YAML anchors, which let a small file expand without bound, <code>yes</code> read as text rather than as true, no unknown keys, 256 KiB at most. An error names the line and the column, and for a misspelled key, the one you probably meant. The last good version stays in force, and the menu bar icon shows the error.</p>

<figure>
<svg class="diagram" viewBox="0 0 680 488" role="img" xmlns="http://www.w3.org/2000/svg">
<title>A broken edit never breaks Hark</title>
<desc>You save the file from any editor or from Settings. Hark watches the file and its folder, lets changes settle for 100 ms, then parses strictly. A valid file goes into force and is copied as the last good version. An invalid one leaves the last good version in force, and the icon shows the line, the column and a hint. A write from Settings is refused if the file moved meanwhile.</desc>
<defs>
<marker id="arr-f42" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#5f5e5a" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
</defs>

<rect x="220" y="40" width="240" height="56" rx="10" fill="#e1f5ee" stroke="#0f6e56" stroke-width="1"/>
<text class="th t-teal" x="340" y="58" text-anchor="middle" dominant-baseline="central">You save</text>
<text class="ts t-teal-s" x="340" y="76" text-anchor="middle" dominant-baseline="central">any editor, or Settings</text>
<line x1="340" y1="100" x2="340" y2="126" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f42)"/>

<rect x="484" y="40" width="156" height="56" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="562" y="58" text-anchor="middle" dominant-baseline="central">Settings writes</text>
<text class="ts t-coral-s" x="562" y="76" text-anchor="middle" dominant-baseline="central">refused if the file moved</text>
<line x1="482" y1="68" x2="462" y2="68" stroke="#5f5e5a" stroke-width="1.5" fill="none" stroke-dasharray="5 4" marker-end="url(#arr-f42)"/>

<rect x="220" y="128" width="240" height="56" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="340" y="146" text-anchor="middle" dominant-baseline="central">Watched</text>
<text class="ts t-gray-s" x="340" y="164" text-anchor="middle" dominant-baseline="central">the file and its folder</text>
<line x1="340" y1="188" x2="340" y2="214" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f42)"/>

<rect x="220" y="216" width="240" height="56" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="340" y="234" text-anchor="middle" dominant-baseline="central">Settled</text>
<text class="ts t-gray-s" x="340" y="252" text-anchor="middle" dominant-baseline="central">100 ms · same bytes: nothing</text>
<line x1="340" y1="276" x2="340" y2="302" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f42)"/>

<rect x="220" y="304" width="240" height="56" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="340" y="322" text-anchor="middle" dominant-baseline="central">Parsed</text>
<text class="ts t-gray-s" x="340" y="340" text-anchor="middle" dominant-baseline="central">strict · no anchors · no unknown keys</text>

<line x1="340" y1="364" x2="196" y2="398" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f42)"/>
<line x1="340" y1="364" x2="484" y2="398" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr-f42)"/>
<text class="ts t-gray-s" x="256" y="374" text-anchor="end">valid</text>
<text class="ts t-coral-s" x="424" y="374" text-anchor="start">invalid</text>

<rect x="60" y="400" width="260" height="56" rx="10" fill="#e1f5ee" stroke="#0f6e56" stroke-width="1"/>
<text class="th t-teal" x="190" y="418" text-anchor="middle" dominant-baseline="central">In force</text>
<text class="ts t-teal-s" x="190" y="436" text-anchor="middle" dominant-baseline="central">copied as the last good version</text>

<rect x="360" y="400" width="260" height="56" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="490" y="418" text-anchor="middle" dominant-baseline="central">Last good stays in force</text>
<text class="ts t-coral-s" x="490" y="436" text-anchor="middle" dominant-baseline="central">icon warns · line, column, a hint</text>

<text class="ts s-mut" x="340" y="478" text-anchor="middle">cold start with a broken file: the last good copy, else no commands</text>
</svg>
<figcaption>A broken edit never breaks Hark.</figcaption>
</figure>

<p>A cold start with a broken file uses the last good copy. With none, Hark runs with no commands, never the bundled defaults, which could bring back a command you deleted. Settings cannot overwrite a hand edit either. Each write names the version it was based on, and is refused if the file moved meanwhile.</p>
<p>The Commands tab is the same file, shown as a table.</p>

<figure>
<img class="window" style="--w:520px" src="{{ '/assets/images/anatomy-hark/17-settings-commands.png' | relative_url }}" alt="Settings, Commands tab: apps with their aliases, and the lists of opening verbs, skipped words and polite endings">
<figcaption>Settings › Commands, scrolled past its intro: each app and its other names (<code>note</code>, <code>calendrier</code>, <code>musique</code>), then opening verbs, skipped words, polite endings. The endings and <code>app</code>, <code>appli</code>, <code>application</code> are on main, not yet released. Chapter 4's grammar, as a table.</figcaption>
</figure>

<p>The tab shows the verb and word lists but does not edit them. They, and the rest, are edited in the file, as in this excerpt:</p>
<pre><code>version: 3
defaults:
  threshold: 0.85
apps:
  com.sublimetext.4: { insert: paste }
# on main, not yet released
endings:
  en: [please]
  fr: ["s'il te plaît", "s'il vous plaît"]</code></pre>
<p>The <code>apps:</code> line sends one editor to paste. Upgrades respect your edits too: only a default file nobody touched, recognized by its hash, is replaced at launch, and a fix on main extends this to the files of 0.0.3 and 0.0.4.</p>

<h3>What each option costs</h3>
<p>Earlier chapters measured these costs. Vocabulary helps a word the model has not learned and hurts one it already writes, as chapter 3 showed. Each spelling added to the assistant's name is a word that can no longer start a dictation, as chapter 4 showed. The <code>apps:</code> list overrides chapter 5's built-in routes both ways: to a paste, to Accessibility, or to the clipboard. Someone who will not grant Accessibility can choose Clipboard only, and the missing grant becomes a warning, not an error.</p>

<h3>What stays fixed, on purpose</h3>
<p>Some freedoms were weighed and turned down:</p>
<ul>
  <li><strong>The prompts</strong>. They live in the code, out of the file's reach, so their rules hold for everyone.</li>
  <li><strong>Commands open apps</strong>. Nothing else, since 23 September 2026. URL, Shortcuts, shell and AppleScript actions are set aside.</li>
  <li><strong>Every installed app as a command</strong>. Declined on 23 September. Hark opens the apps <code>commands.yaml</code> names.</li>
  <li><strong>A catalog of writing tools</strong>. Replaced on 28 September by one entry. The spoken instruction is the tool.</li>
</ul>

<h3>Why a model does not decide</h3>
<p>The idea was one key for everything, with a model on the Mac deciding whether a sentence is text, a command or a request. It was probed on 29 September 2026 on this Mac: a small on-device classifier, through Core ML.</p>
<p>Speed was never the problem. It answered in milliseconds, and it was right on most of a set of test sentences, half English and half French.</p>
<p>The replay changed the plan. Over 128 logged dictations into text fields, from two days on this Mac, it would have sent 28 away from typing with a confidence of 0.7 or more, 22 percent. The labels came from what happened, so they are approximate. From the words alone, the same sentence is dictation in one app and a task in another.</p>

<figure>
<svg class="diagram" viewBox="0 0 680 330" role="img" xmlns="http://www.w3.org/2000/svg">
<title>A guess from the words, or a gesture</title>
<desc>Left, a classifier probed on this Mac: milliseconds per answer and right on most test sentences, yet 22 percent of 128 logged dictations into text fields sent away from typing. Right, what ships: the dictation key, the Ask key and the spoken name, each saying what you want.</desc>
<rect x="40" y="44" width="290" height="236" rx="16" fill="none" stroke="#c4c2b8" stroke-width="1" stroke-dasharray="6 4"/>
<text class="th t-ink" x="60" y="70">A model guesses from the words</text>
<text class="ts s-mut" x="60" y="88">probed, then set aside</text>

<rect x="60" y="104" width="250" height="48" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="185" y="124" text-anchor="middle">Milliseconds per answer</text>
<text class="ts t-gray-s" x="185" y="142" text-anchor="middle">on this Mac, through Core ML</text>

<rect x="60" y="160" width="250" height="48" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="185" y="180" text-anchor="middle">Right on most test sentences</text>
<text class="ts t-gray-s" x="185" y="198" text-anchor="middle">English and French</text>

<rect x="60" y="216" width="250" height="48" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="185" y="236" text-anchor="middle">22 percent sent away</text>
<text class="ts t-coral-s" x="185" y="254" text-anchor="middle">28 of 128 logged dictations</text>

<rect x="350" y="44" width="290" height="236" rx="16" fill="none" stroke="#c4c2b8" stroke-width="1" stroke-dasharray="6 4"/>
<text class="th t-ink" x="370" y="70">The gesture says it</text>
<text class="ts s-mut" x="370" y="88">what ships</text>

<rect x="370" y="104" width="250" height="48" rx="10" fill="#e1f5ee" stroke="#0f6e56" stroke-width="1"/>
<text class="th t-teal" x="495" y="124" text-anchor="middle">Dictation key</text>
<text class="ts t-teal-s" x="495" y="142" text-anchor="middle">text, or a verb and an app</text>

<rect x="370" y="160" width="250" height="48" rx="10" fill="#e1f5ee" stroke="#0f6e56" stroke-width="1"/>
<text class="th t-teal" x="495" y="180" text-anchor="middle">Ask key</text>
<text class="ts t-teal-s" x="495" y="198" text-anchor="middle">a selection, or nothing</text>

<rect x="370" y="216" width="250" height="48" rx="10" fill="#e1f5ee" stroke="#0f6e56" stroke-width="1"/>
<text class="th t-teal" x="495" y="236" text-anchor="middle">"Hark, …"</text>
<text class="ts t-teal-s" x="495" y="254" text-anchor="middle">an exact list of spellings</text>

<text class="ts s-mut" x="340" y="312" text-anchor="middle">a small classifier · Core ML · this Mac, M5 Pro, 64 GB · confidence 0.7 or more</text>
</svg>
<figcaption>A guess from the words, or a gesture.</figcaption>
</figure>

<p>The design was set aside the same day. Routing stays an open question, to be rethought from a signal other than the words. A language model in front of every sentence had already been refused, for the 0.3 to 0.6 s it would add to each. Today the gestures route.</p>
<p>Fast is not the same as right. Like the drill from the start of this document, Hark does the job you picked it up for, never one it guessed.</p>

<hr>

<h2>Appendix A: Methodology and measurements</h2>
<p>Main tool: one Swift package, in Swift 6 language mode, with strict concurrency and warnings as errors. <code>scripts/bundle.sh</code> builds and signs the app, runs its self-test, and with <code>--install</code> installs it.</p>
<ul>
  <li><strong>The rig.</strong> One MacBook Pro, Apple M5 Pro, 64 GB, on macOS 27.0 for the transcription measurements of 21 September, 27.2 from 24 September. Small <code>q8_0</code> unless stated, the Neural Engine on or off as each number says. No other chip was measured.</li>
  <li><strong>The clocks.</strong> Whisper's own clock for a decode. <code>transcribe_ms</code> for the whole engine call, queue waits included. The physical footprint for memory, the figure Activity Monitor shows.</li>
  <li><strong>The speech.</strong> Synthesized with <code>say</code>, in several voices, so runs repeat. Synthesized speech is not a real voice, and the records say so.</li>
  <li><strong>Not measured.</strong> Key up to text, end to end. Medium and Large v3, in memory or in time. The Neural Engine's power draw. The whole app with the live transcript on.</li>
  <li><strong>Reproduce.</strong> Transcription benchmarks run only with <code>HARK_TEST_MODEL</code> and <code>HARK_TEST_BENCH</code> set, the name bench with <code>HARK_TEST_PREFIX_BENCH</code>. The model-server and classifier measurements are in the project's records, not the repository. <code>Hark --self-test</code> checks the signed app at every build, Whisper with Metal included, and ends one synthetic press in one 13-key line.</li>
  <li><strong>Tests.</strong> 800 in 122 suites at build 69, written as plain tables, with no network, no microphone and no real Accessibility.</li>
  <li><strong>Signing.</strong> Releases are signed ad hoc, so macOS treats each update as a new app. The README says how to allow Accessibility again.</li>
</ul>
<p>The screenshots come from build 70, five commits after 0.0.4, over a sample log:</p>
<pre><code>open -n -a Hark --args -HarkDebugPreview panel -HarkDebugLogs &lt;folder&gt;</code></pre>
<p>The <code>-n</code> starts a preview process beside the running Hark, whose real log is left as it is. Other screens use other names after <code>-HarkDebugPreview</code>.</p>
<p>One practice runs through the project: premises measured before tests assert them. Each defect of the transcription milestone was a premise nobody had checked, not a mistake in the code. When a regression test passed before its fix, it was deleted: it proved nothing.</p>
<p>Work began on 18 September 2026. The public history starts with 0.0.2 on 28 September, 0.0.3 the same day, 0.0.4 on 29 September. The tests went from 23 to 800. The README closes with one line: "Designed and engineered by isitanth, powered by Claude Code, built for you."</p>

<h2>Appendix B: The problems, by date</h2>
<p>Between 21 and 29 September, fifteen problems shaped Hark. Here they are in the order they were met:</p>
<ul>
  <li><strong>21 September. A filter that never fired.</strong> Silence came back as "you". The clip's level now decides. Chapter 3.</li>
  <li><strong>21 September. A first press of 16 seconds.</strong> A cold first decode, now paid at launch. Chapter 3.</li>
  <li><strong>21 September. The encoder that never loaded.</strong> A file name derived backwards. Every load now logs whether the encoder is there. Chapter 3.</li>
  <li><strong>21 September. A 5.7 s sentence read as "you".</strong> Core ML's fixed shape. Metal by default. Chapter 3.</li>
  <li><strong>22 September. A transcript faster than the focus.</strong> A password field's text reached the log. <code>resolving</code> now waits. Chapter 4.</li>
  <li><strong>22 September. A paste on a timer.</strong> Lost text, logged as inserted. A paste counts once read. Chapter 5.</li>
  <li><strong>23 September. Sentences read as commands.</strong> Fuzzy matching rewards a common start. A verb-first grammar. Chapter 4.</li>
  <li><strong>23 September. Every quit a crash.</strong> ggml's destructors met live GPU memory. Unload first, then <code>_exit</code>. Chapter 1.</li>
  <li><strong>24 September. Seventy-two seconds in one pass.</strong> Whisper's 30 s window. Long clips cut at pauses. Chapter 3.</li>
  <li><strong>27 September. The exception Swift cannot catch.</strong> An audio change under the engine. HarkObjC, then a capture session per press. Chapter 2.</li>
  <li><strong>28 September. AirPods left low.</strong> Two volumes per headset. No lowering over Bluetooth. Chapter 2.</li>
  <li><strong>28 September. The name Whisper cannot spell.</strong> Fuzzy matching failed both ways. An exact list. Chapter 4.</li>
  <li><strong>28 September. The Mail draft on the clipboard.</strong> No selection in the draft. A paste since 0.0.4. Chapter 5.</li>
  <li><strong>29 September. Editors that copy a line.</strong> Command-C copied the whole line. No Command-C there. Chapter 6.</li>
  <li><strong>29 September. Routing from the words alone.</strong> Fast, but 22 percent of dictations into text fields sent away from typing. Set aside. Chapter 7.</li>
</ul>

<h2>Appendix C: The project's diagrams</h2>
<p>These diagrams come from the project's documentation and open full size from their link. The first two and the last are older than the figures above; their captions give their date and what has changed since. The five in between are redrawn from the code of Hark 0.0.4.</p>

<figure>
<a href="{{ '/assets/images/anatomy-hark/11-data-flow-level0.svg' | relative_url }}"><img src="{{ '/assets/images/anatomy-hark/11-data-flow-level0.svg' | relative_url }}" alt="Data-flow diagram: Hark as one process inside the Mac, with the microphone, the user, the app in front and notifications, and huggingface.co outside"></a>
<figcaption>The data-flow diagram, level 0, drawn on 28 September 2026, before Ask Hark. The dashed line is the Mac, and only the model download crosses. The model server of chapter 6 adds a second flow, on this Mac by default.</figcaption>
</figure>

<figure>
<a href="{{ '/assets/images/anatomy-hark/18-architecture-overview.svg' | relative_url }}"><img src="{{ '/assets/images/anatomy-hark/18-architecture-overview.svg' | relative_url }}" alt="Layered architecture of Hark, from the SwiftUI app down to Metal, Core ML and the Neural Engine"></a>
<figcaption>Hark layer by layer, drawn on 28 September 2026, before Ask Hark: SwiftUI on top, chapter 1's seams, Metal below. Its Neural Engine encoder is off by default. Since then: an asking state, a seventh tab, a second network peer.</figcaption>
</figure>

<figure>
<a href="{{ '/assets/images/anatomy-hark/19a-key-to-samples.svg' | relative_url }}"><picture><source media="(max-width: 600px)" srcset="{{ '/assets/images/anatomy-hark/19a-key-to-samples-phone.svg' | relative_url }}"><img src="{{ '/assets/images/anatomy-hark/19a-key-to-samples.svg' | relative_url }}" alt="Diagram: the talk and Ask keys reach PipelineController, which probes focus, starts AudioCapture and drops captures too short or too quiet."></picture></a>
<figcaption>From the key to the samples, redrawn from the code of Hark 0.0.4. Both keys reach one controller, the Ask key after reading the selection. Dictation probes the focus at key down, and the microphone is open only from start to stop. Raw audio reaches disk only in debug builds.</figcaption>
</figure>

<figure>
<a href="{{ '/assets/images/anatomy-hark/19b-samples-to-transcript.svg' | relative_url }}"><picture><source media="(max-width: 600px)" srcset="{{ '/assets/images/anatomy-hark/19b-samples-to-transcript-phone.svg' | relative_url }}"><img src="{{ '/assets/images/anatomy-hark/19b-samples-to-transcript.svg' | relative_url }}" alt="Diagram: the samples pass through SwappableTranscriptionEngine into the Transcriber's four steps; PipelineReducer then picks idle, asking or the resolver."></picture></a>
<figcaption>From the samples to the transcript, redrawn from the code of Hark 0.0.4. The samples reach the engine without entering the reducer's state. whisper.cpp runs on Metal by default: a 5.7 s clip on Small, 76 ms, against 83 ms with the Core ML switch on.</figcaption>
</figure>

<figure>
<a href="{{ '/assets/images/anatomy-hark/20a-commands-yaml.svg' | relative_url }}"><picture><source media="(max-width: 600px)" srcset="{{ '/assets/images/anatomy-hark/20a-commands-yaml-phone.svg' | relative_url }}"><img src="{{ '/assets/images/anatomy-hark/20a-commands-yaml.svg' | relative_url }}" alt="Diagram: commands.yaml is watched by DispatchFileWatcher and parsed by ConfigStore, which feeds ResolutionSettings, AskSettings and HealthStatus."></picture></a>
<figcaption>commands.yaml, the file you write, redrawn from the code of Hark 0.0.4. One actor re-reads it after each save, and the app hands each part to the code that uses it. A broken file never replaces the last good one, and Settings never writes over a newer edit.</figcaption>
</figure>

<figure>
<a href="{{ '/assets/images/anatomy-hark/20b-models.svg' | relative_url }}"><picture><source media="(max-width: 600px)" srcset="{{ '/assets/images/anatomy-hark/20b-models-phone.svg' | relative_url }}"><img src="{{ '/assets/images/anatomy-hark/20b-models.svg' | relative_url }}" alt="Diagram: Settings › Model drives DownloadCoordinator and ModelStore; URLSessionDownloader fetches pinned files from huggingface.co for the Transcriber."></picture></a>
<figcaption>The models you choose, redrawn from the code of Hark 0.0.4. Nothing downloads until you click, every file is checked against a pinned SHA-256, and the Core ML encoder comes only with its switch on. This downloader is one of two network clients; Ask's is the other.</figcaption>
</figure>

<figure>
<a href="{{ '/assets/images/anatomy-hark/20c-log.svg' | relative_url }}"><picture><source media="(max-width: 600px)" srcset="{{ '/assets/images/anatomy-hark/20c-log-phone.svg' | relative_url }}"><img src="{{ '/assets/images/anatomy-hark/20c-log.svg' | relative_url }}" alt="Diagram: PipelineController appends one line per utterance through UtteranceLog; LogReader feeds the panel and Settings › Log; LogHistory deletes them."></picture></a>
<figcaption>The log Hark keeps, redrawn from the code of Hark 0.0.4: one line per utterance, 13 keys, a folder at 0700 and files at 0600. The panel and Settings › Log read it back, and Clear History, offered in both, deletes it.</figcaption>
</figure>

<figure>
<a href="{{ '/assets/images/anatomy-hark/21-deployment.svg' | relative_url }}"><img src="{{ '/assets/images/anatomy-hark/21-deployment.svg' | relative_url }}" alt="Deployment view of the Mac: SSD files, macOS services, the Hark process and the CPU, GPU and Neural Engine"></a>
<figcaption>One process on one Mac, drawn on 28 September 2026: files on the SSD, daemons in macOS, work split across CPU, GPU and Neural Engine. Drawn before Ask Hark, so the model server and its Keychain item are missing.</figcaption>
</figure>

<h2>Glossary</h2>
<ul>
  <li><strong>whisper.cpp</strong>. C and C++ implementation of OpenAI's Whisper speech model, run inside Hark.</li>
  <li><strong>Utterance</strong>. One press of a key, from key down to its log line.</li>
  <li><strong>HUD</strong> (heads-up display). The small recording window that never takes the keyboard.</li>
  <li><strong>Neural Engine</strong>. The part of Apple silicon built for machine learning.</li>
  <li><strong>Metal</strong>. Apple's GPU interface, which runs both halves of Whisper by default.</li>
  <li><strong>Quantization</strong> (<code>q8_0</code>, <code>q5_0</code>). Weights stored in 8 or 5 bits instead of 16.</li>
  <li><strong>Token</strong>. The unit a model reads and writes, a word or part of one.</li>
  <li><strong>Encoder / decoder</strong>. Whisper's two halves: audio read once, then text written token by token.</li>
  <li><strong>Reducer</strong>. Pure function from a state and an event to the next state and its effects.</li>
  <li><strong>Actor</strong>. A Swift type that handles one message at a time.</li>
  <li><strong>RMS</strong> (root mean square). A measure of loudness, used by the gate for silent clips.</li>
  <li><strong>Seam</strong>. A protocol the core owns, implemented by the app or a test fake.</li>
  <li><strong>Accessibility API</strong> (AX). The macOS interface to other apps' interface elements.</li>
  <li><strong>Latch</strong>. A tap under 350 ms that keeps recording until the next tap.</li>
  <li><strong>Non-activating panel</strong>. A window that shows without bringing its app forward.</li>
  <li><strong>Core ML</strong>. Apple's framework for compiled models on the CPU, GPU or Neural Engine.</li>
  <li><strong><code>audio_ctx</code></strong>. How many of the encoder's 1,500 window states a decode computes.</li>
  <li><strong>Temperature</strong>. How much randomness a model allows in picking the next token.</li>
  <li><strong>Hallucination</strong>. Text a speech model writes for audio that holds no speech.</li>
  <li><strong><code>no_speech_prob</code></strong>. Whisper's own estimate that a window holds no speech.</li>
  <li><strong>Footprint</strong>. The memory macOS charges to a process, as Activity Monitor shows.</li>
  <li><strong>Jaro-Winkler</strong>. String similarity from 0 to 1 that rewards a common start.</li>
  <li><strong>Assistant</strong>. Ask Hark with nothing selected, reached by the Ask key or by starting a sentence with the name.</li>
  <li><strong>Pasteboard promise</strong>. Clipboard data supplied only when another app reads it.</li>
  <li><strong>SSE</strong> (server-sent events). A stream of text events over one open HTTP response.</li>
  <li><strong>TTFT</strong> (time to first token). The wait before a language model writes its first word.</li>
</ul>

<h2>References</h2>
<ul class="ref">
  <li>isitanth/hark: <a href="https://github.com/isitanth/hark">repository</a>, <a href="https://github.com/isitanth/hark/blob/main/CHANGELOG.md">changelog</a> and <a href="https://github.com/isitanth/hark/releases">releases</a></li>
  <li>ggml-org/whisper.cpp: <a href="https://github.com/ggml-org/whisper.cpp">repository</a></li>
  <li>Hugging Face: <a href="https://huggingface.co/ggerganov/whisper.cpp">whisper.cpp models</a></li>
  <li>arXiv: <a href="https://arxiv.org/abs/2212.04356">the Whisper paper</a></li>
  <li>Apple Developer: <a href="https://developer.apple.com/documentation/coreml">Core ML</a></li>
  <li>Apple Developer: <a href="https://developer.apple.com/documentation/metal">Metal</a></li>
  <li>Apple Developer: <a href="https://developer.apple.com/documentation/avfoundation/avcapturesession">AVCaptureSession</a></li>
  <li>Apple Developer: <a href="https://developer.apple.com/documentation/appkit/nspanel">NSPanel</a></li>
  <li>Apple Developer: <a href="https://developer.apple.com/documentation/applicationservices/axuielement_h">AXUIElement</a></li>
  <li>Apple Developer: <a href="https://developer.apple.com/documentation/appkit/nspasteboarditemdataprovider">pasteboard promises</a></li>
  <li>Apple Developer: <a href="https://developer.apple.com/documentation/security/keychain-services">Keychain services</a></li>
  <li>Apple Developer Archive: <a href="https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/SysServices/introduction.html">Services</a></li>
  <li>Apple Human Interface Guidelines: <a href="https://developer.apple.com/design/human-interface-guidelines/the-menu-bar">the menu bar</a></li>
  <li>Apple Human Interface Guidelines: <a href="https://developer.apple.com/design/human-interface-guidelines/settings">settings</a></li>
  <li>Apple Human Interface Guidelines: <a href="https://developer.apple.com/design/human-interface-guidelines/privacy">privacy</a></li>
  <li>Apple Machine Learning Research: <a href="https://machinelearning.apple.com/research/hey-siri">Hey Siri</a></li>
  <li>Apple Machine Learning Research: <a href="https://machinelearning.apple.com/research/neural-engine-transformers">Transformers on the Neural Engine</a></li>
  <li>Apple Machine Learning Research: <a href="https://machinelearning.apple.com/research/core-ml-on-device-llama">Llama with Core ML</a></li>
  <li>Apple Machine Learning Research: <a href="https://machinelearning.apple.com/research/exploring-llms-mlx-m5">LLMs with MLX on M5</a></li>
  <li>The Swift Programming Language: <a href="https://docs.swift.org/swift-book/documentation/the-swift-programming-language/concurrency/">concurrency</a></li>
  <li>sindresorhus/KeyboardShortcuts: <a href="https://github.com/sindresorhus/KeyboardShortcuts">repository</a></li>
  <li>jpsim/Yams: <a href="https://github.com/jpsim/Yams">repository</a></li>
  <li>WHATWG: <a href="https://html.spec.whatwg.org/multipage/server-sent-events.html">server-sent events</a></li>
  <li>Wikipedia: <a href="https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance">Jaro-Winkler distance</a></li>
</ul>
