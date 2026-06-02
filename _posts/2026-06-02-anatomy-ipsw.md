---
layout: post
title: "Anatomy of an .ipsw"
date: 2026-06-02
tags: [Apple, iOS, IPSW]
excerpt: "An .ipsw is the restore archive for an Apple device — a ZIP that holds everything needed to reinstall the system. This document takes the archive apart, family by family, with the tools researchers use."
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
</style>

<h2>Introduction</h2>
<p>An <code>.ipsw</code> is the restore archive for an Apple device. Underneath, it is a ZIP archive. It holds everything needed to reinstall the system.</p>
<p>This document takes the archive apart, family by family. It also covers how to analyze the contents, with the tools researchers use.</p>
<p>The running example is the IPSW of an iPhone 16 Pro Max, on iOS 26.5, build 23F77.</p>
<p>The document is built to grow. The system images chapter is written. The others are waiting for content.</p>
<p class="note">One last detail. Every file carries the same date, 9 January 2007 at 09:41. The build does not record each file's real write time. It sets them all to one fixed value. That keeps the archive reproducible, byte for byte, and leaks no real build dates. The value itself is a nod: 9 January 2007 was the Macworld keynote where the first iPhone was unveiled, and 9:41 is the time its clock showed at the reveal, the time Apple's ads still use. A signature, not the extraction date.</p>

<h2>The five families</h2>
<p>The thirteen items in the archive fall into five families. What sets them apart first is whether they are encrypted.</p>

<figure>
<svg class="diagram" viewBox="0 0 680 392" role="img" xmlns="http://www.w3.org/2000/svg">
<title>The five file families of an .ipsw</title>
<desc>The .ipsw archive groups five families: AEA-encrypted system images, AES-encrypted firmware, plain ramdisks, the kernel, and manifests.</desc>
<rect x="40" y="44" width="600" height="292" rx="16" fill="none" stroke="#c4c2b8" stroke-width="1" stroke-dasharray="6 4"/>
<text class="th t-ink" x="60" y="70">.ipsw file</text>
<text class="ts s-mut" x="60" y="88">ZIP archive, unencrypted</text>

<rect x="60" y="104" width="176" height="96" rx="10" fill="#faeeda" stroke="#854f0b" stroke-width="1"/>
<text class="th t-amber" x="148" y="130" text-anchor="middle">System images</text>
<text class="ts t-amber-s" x="148" y="150" text-anchor="middle">AEA-encrypted</text>
<text class="ts t-amber-s" x="148" y="172" text-anchor="middle">root + cryptex</text>

<rect x="252" y="104" width="176" height="96" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="340" y="130" text-anchor="middle">Firmware</text>
<text class="ts t-coral-s" x="340" y="150" text-anchor="middle">AES-encrypted</text>
<text class="ts t-coral-s" x="340" y="172" text-anchor="middle">iBoot, SEP, baseband</text>

<rect x="444" y="104" width="176" height="96" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="532" y="130" text-anchor="middle">Ramdisks</text>
<text class="ts t-gray-s" x="532" y="150" text-anchor="middle">plain DMG</text>
<text class="ts t-gray-s" x="532" y="172" text-anchor="middle">restore + update</text>

<rect x="60" y="220" width="272" height="96" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="196" y="246" text-anchor="middle">Kernel (kernelcache)</text>
<text class="ts t-gray-s" x="196" y="266" text-anchor="middle">XNU + extensions · 22 MB</text>
<text class="ts t-gray-s" x="196" y="288" text-anchor="middle">loaded during restore</text>

<rect x="348" y="220" width="272" height="96" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="484" y="246" text-anchor="middle">Manifests (.plist)</text>
<text class="ts t-gray-s" x="484" y="266" text-anchor="middle">BuildManifest = driver</text>
<text class="ts t-gray-s" x="484" y="288" text-anchor="middle">+ Restore, SystemVersion…</text>

<rect x="60" y="354" width="16" height="16" rx="3" fill="#faeeda" stroke="#854f0b" stroke-width="1"/>
<text class="ts s-mut" x="84" y="366">AEA-encrypted (system)</text>
<rect x="250" y="354" width="16" height="16" rx="3" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="ts s-mut" x="274" y="366">AES-encrypted (firmware)</text>
<rect x="456" y="354" width="16" height="16" rx="3" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="ts s-mut" x="480" y="366">Plain / unencrypted</text>
</svg>
<figcaption>The five file families of an .ipsw.</figcaption>
</figure>

<ul>
  <li><strong>System images</strong> (<code>.dmg.aea</code>). The system itself, encrypted. Covered in chapter 1.</li>
  <li><strong>Ramdisks</strong> (<code>.dmg</code>). Restore and update RAM disks, in the clear. Chapter 2.</li>
  <li><strong>Kernel</strong> (<code>kernelcache</code>). The XNU kernel and its extensions. Chapter 3.</li>
  <li><strong>Firmware</strong> (folder). The low level: boot chain, SEP, baseband. Chapter 4.</li>
  <li><strong>Manifests</strong> (<code>.plist</code>). The metadata. <code>BuildManifest</code> drives the restore. Chapter 5.</li>
</ul>

<h2>The logic: the restore</h2>
<p>The layout of the archive follows the restore. Each family serves one step.</p>

<figure>
<svg class="diagram" viewBox="0 0 680 516" role="img" xmlns="http://www.w3.org/2000/svg">
<title>The restore sequence of an .ipsw</title>
<desc>DFU mode, loading signed bootloaders, kernel and ramdisk, ASR writing the system, then Apple-signed personalization.</desc>
<defs>
<marker id="arr2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#5f5e5a" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
</defs>

<rect x="160" y="40" width="360" height="56" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="340" y="58" text-anchor="middle" dominant-baseline="central">DFU / Recovery mode</text>
<text class="ts t-gray-s" x="340" y="76" text-anchor="middle" dominant-baseline="central">device waits for restore</text>
<line x1="340" y1="100" x2="340" y2="126" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr2)"/>

<rect x="160" y="136" width="360" height="56" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="340" y="154" text-anchor="middle" dominant-baseline="central">Signed bootloaders</text>
<text class="ts t-gray-s" x="340" y="172" text-anchor="middle" dominant-baseline="central">iBSS then iBEC (Firmware folder)</text>
<line x1="340" y1="196" x2="340" y2="222" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr2)"/>

<rect x="160" y="232" width="360" height="56" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="340" y="250" text-anchor="middle" dominant-baseline="central">Kernel + ramdisk</text>
<text class="ts t-gray-s" x="340" y="268" text-anchor="middle" dominant-baseline="central">minimal restore environment in RAM</text>
<line x1="340" y1="292" x2="340" y2="318" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr2)"/>

<rect x="160" y="328" width="360" height="56" rx="10" fill="#faeeda" stroke="#854f0b" stroke-width="1"/>
<text class="th t-amber" x="340" y="346" text-anchor="middle" dominant-baseline="central">ASR writes the system</text>
<text class="ts t-amber-s" x="340" y="364" text-anchor="middle" dominant-baseline="central">decrypted .aea image &#8594; storage</text>
<line x1="340" y1="388" x2="340" y2="414" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr2)"/>

<rect x="160" y="424" width="360" height="56" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="340" y="442" text-anchor="middle" dominant-baseline="central">Apple personalization</text>
<text class="ts t-coral-s" x="340" y="460" text-anchor="middle" dominant-baseline="central">TSS signs each component · anti-downgrade</text>
</svg>
<figcaption>The restore sequence.</figcaption>
</figure>

<p>The device enters DFU mode. iBoot loads the second-stage bootloaders, iBSS then iBEC. The kernel and the ramdisk then mount a minimal environment in memory. ASR decrypts the system image there and writes it to storage. The firmware components are flashed.</p>
<p>The last lock is the signature. Each component must be signed by Apple's signing server, the TSS. The host sends the device ECID and a nonce. Apple returns an APTicket, valid only while the version is signed. This signing window is what stops you from installing, or rolling back to, a version Apple no longer signs.</p>

<h2>Chapter 1: System images (root + cryptex)</h2>
<p>The four <code>.dmg.aea</code> files, once decrypted, are the operating system. But modern iOS is not a single volume. It is a sealed root volume, with cryptexes grafted on at boot. Understanding this split is knowing where to look for what.</p>

<h3>Architecture</h3>

<figure>
<svg class="diagram" viewBox="0 0 680 272" role="img" xmlns="http://www.w3.org/2000/svg">
<title>The root volume and the cryptexes</title>
<desc>A sealed System volume (root, 8.12 GB) and cryptexes grafted at boot: OS cryptex (dyld shared cache) and App cryptex (Safari, WebKit).</desc>
<rect x="40" y="44" width="600" height="172" rx="16" fill="none" stroke="#c4c2b8" stroke-width="1" stroke-dasharray="6 4"/>
<text class="th t-ink" x="60" y="70">iOS system, assembled at boot</text>
<text class="ts s-mut" x="60" y="88">sealed root + grafted cryptexes</text>

<rect x="60" y="104" width="176" height="92" rx="10" fill="#faeeda" stroke="#854f0b" stroke-width="1"/>
<text class="th t-amber" x="148" y="128" text-anchor="middle">System Volume</text>
<text class="ts t-amber-s" x="148" y="150" text-anchor="middle">sealed (SSV) · 8.12 GB</text>
<text class="ts t-amber-s" x="148" y="172" text-anchor="middle">base OS, daemons</text>

<rect x="252" y="104" width="176" height="92" rx="10" fill="#e1f5ee" stroke="#0f6e56" stroke-width="1"/>
<text class="th t-teal" x="340" y="128" text-anchor="middle">OS cryptex</text>
<text class="ts t-teal-s" x="340" y="150" text-anchor="middle">SystemOS · ≈ 2 GB</text>
<text class="ts t-teal-s" x="340" y="172" text-anchor="middle">dyld shared cache</text>

<rect x="444" y="104" width="176" height="92" rx="10" fill="#e1f5ee" stroke="#0f6e56" stroke-width="1"/>
<text class="th t-teal" x="532" y="128" text-anchor="middle">App cryptex</text>
<text class="ts t-teal-s" x="532" y="150" text-anchor="middle">AppOS · ≈ 235 MB</text>
<text class="ts t-teal-s" x="532" y="172" text-anchor="middle">Safari, WebKit</text>

<rect x="60" y="230" width="16" height="16" rx="3" fill="#faeeda" stroke="#854f0b" stroke-width="1"/>
<text class="ts s-mut" x="84" y="242">Sealed volume (SSV)</text>
<rect x="240" y="230" width="16" height="16" rx="3" fill="#e1f5ee" stroke="#0f6e56" stroke-width="1"/>
<text class="ts s-mut" x="264" y="242">Cryptex (grafted, updatable)</text>
</svg>
<figcaption>The root volume and the cryptexes, assembled at boot.</figcaption>
</figure>

<p>The root volume, the ~8.12 GB file, becomes the Signed System Volume (SSV) on the device: a sealed APFS snapshot the system boots from. It is the classic Unix tree: <code>/System</code>, <code>/usr</code>, <code>/bin</code>, the daemons, the <code>dyld</code> loader, the base system apps. The seal is a hash tree anchored in the boot chain. Change one byte and the seal breaks.</p>
<p>A sealed volume is safe, but rigid. You cannot patch it without rebuilding it. Hence the cryptexes. A cryptex is a disk image, itself sealed, grafted on top of the SSV at boot, with its own hash in the chain of trust. The mechanism comes from Apple's Security Research Device, then served the Rapid Security Responses.</p>
<p>Two cryptexes matter here. The OS cryptex holds the dyld shared caches and a few libraries. The App cryptex carries Safari, WebKit, and JavaScriptCore. The point is clear: Apple can patch WebKit by swapping the App cryptex, without touching the SSV or forcing a full update.</p>
<p>On the file side, the four <code>.dmg.aea</code> map to the root (8.12 GB), the OS cryptex (~2.01 GB, most of the dyld cache), and likely the App cryptex with a smaller companion image (155 and 235 MB). Recent versions add cryptexes for Apple Intelligence. The exact mapping is labeled in <code>BuildManifest.plist</code>, under names like <code>Cryptex1,SystemOS</code> and <code>Cryptex1,AppOS</code>.</p>

<h3>The AEA layer</h3>
<p>The <code>.aea</code> extension is an encryption wrapper around the DMG. AEA1 encrypts the images in IPSWs and OTAs. Decryption rests on FCS keys and an HPKE key unwrap.</p>
<p>The important point: this wrapper does not hide the firmware. The keys are publicly retrievable, from Apple's WKMS service or a community database like AppleDB. It exists to control distribution, not to block analysis. Decrypting to study is routine.</p>

<h3>The analysis method</h3>

<figure>
<svg class="diagram" viewBox="0 0 680 612" role="img" xmlns="http://www.w3.org/2000/svg">
<title>From the .aea file to an analyzable system</title>
<desc>Image .dmg.aea extracted from the IPSW, AEA decryption, plain APFS DMG, mounting, exploring and extracting the dyld shared cache, then analyzing the binaries.</desc>
<defs>
<marker id="arr4" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#5f5e5a" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
</defs>

<rect x="160" y="40" width="360" height="56" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="340" y="58" text-anchor="middle" dominant-baseline="central">Image .dmg.aea</text>
<text class="ts t-gray-s" x="340" y="76" text-anchor="middle" dominant-baseline="central">extracted from the .ipsw</text>
<line x1="340" y1="100" x2="340" y2="126" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr4)"/>

<rect x="160" y="136" width="360" height="56" rx="10" fill="#faeeda" stroke="#854f0b" stroke-width="1"/>
<text class="th t-amber" x="340" y="154" text-anchor="middle" dominant-baseline="central">Decrypt the AEA</text>
<text class="ts t-amber-s" x="340" y="172" text-anchor="middle" dominant-baseline="central">FCS key: WKMS or fcs-keys.json</text>
<line x1="340" y1="196" x2="340" y2="222" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr4)"/>

<rect x="160" y="232" width="360" height="56" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="340" y="250" text-anchor="middle" dominant-baseline="central">Plain APFS DMG</text>
<text class="ts t-gray-s" x="340" y="268" text-anchor="middle" dominant-baseline="central">mountable disk image</text>
<line x1="340" y1="292" x2="340" y2="318" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr4)"/>

<rect x="160" y="328" width="360" height="56" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="340" y="346" text-anchor="middle" dominant-baseline="central">Mount the volume</text>
<text class="ts t-gray-s" x="340" y="364" text-anchor="middle" dominant-baseline="central">macOS native · apfs-fuse · ipsw mount</text>
<line x1="340" y1="388" x2="340" y2="414" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr4)"/>

<rect x="160" y="424" width="360" height="56" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="340" y="442" text-anchor="middle" dominant-baseline="central">Explore + extract</text>
<text class="ts t-gray-s" x="340" y="460" text-anchor="middle" dominant-baseline="central">root/, /System, dyld shared cache</text>
<line x1="340" y1="484" x2="340" y2="510" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr4)"/>

<rect x="160" y="520" width="360" height="56" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="340" y="538" text-anchor="middle" dominant-baseline="central">Analyze the binaries</text>
<text class="ts t-gray-s" x="340" y="556" text-anchor="middle" dominant-baseline="central">split dylibs, class-dump, Hopper</text>
</svg>
<figcaption>From the .aea file to an analyzable system.</figcaption>
</figure>

<p>The principle is simple. You extract the image, decrypt it, mount the volume, explore, extract the dyld shared cache, then analyze the binaries.</p>
<p>The real prize is the dyld shared cache, in the OS cryptex (<code>System/Library/Caches/com.apple.dyld/</code> once mounted). It is a single file, actually split into subcaches, that bundles most public and private frameworks, pre-linked. Why it matters: since iOS 8, the SDK no longer ships the extracted frameworks. The only way to get the real library code from the device is to pull it from the cache. To reverse a private framework, you extract it from there first.</p>
<p>macOS and Linux are not equal here. On macOS, a decrypted APFS DMG mounts natively. On Linux, you need <code>apfs-fuse</code>, but since iOS 16 Apple compresses some cryptex files with LZBITMAP, which older versions cannot read. So most research happens on Apple Silicon Macs.</p>
<p>To get started:</p>
<ul>
  <li><code>ipsw mount fs &lt;IPSW&gt;</code>. Mounts the system. AEA decryption is automatic.</li>
  <li><code>ipsw extract --dyld &lt;IPSW&gt;</code>. Pulls out the dyld shared cache.</li>
  <li><code>ipsw extract --dmg fs|sys|app &lt;IPSW&gt;</code>. Pulls out a specific image (root, OS cryptex, App cryptex).</li>
  <li><code>ipsw dyld split</code> and <code>ipsw dyld info</code>. Split the cache into dylibs and inspect it.</li>
  <li><code>ipsw ent &lt;IPSW&gt;</code>. Extracts entitlements. A good starting point for mapping attack surface.</li>
</ul>

<h2>Chapter 2: Ramdisks and ASR</h2>
<p>Before any system is written, the device needs somewhere to run from. The target storage is about to be erased or rewritten, so the restore cannot run from there. It runs from memory instead. That is the ramdisk: a small, complete environment, loaded into RAM, that drives the install.</p>
<p>Two ship in the archive. They look almost identical. What separates them is what they are allowed to touch.</p>

<figure>
<svg class="diagram" viewBox="0 0 680 300" role="img" xmlns="http://www.w3.org/2000/svg">
<title>The restore ramdisk and the update ramdisk</title>
<desc>Two small bootable environments in RAM. The restore ramdisk erases and reflashes the whole device. The update ramdisk applies an update in place. Both carry ASR.</desc>
<rect x="40" y="44" width="600" height="200" rx="16" fill="none" stroke="#c4c2b8" stroke-width="1" stroke-dasharray="6 4"/>
<text class="th t-ink" x="60" y="70">Ramdisks · minimal macOS in RAM</text>
<text class="ts s-mut" x="60" y="88">bootable, discarded after restore</text>

<rect x="60" y="104" width="270" height="120" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="195" y="130" text-anchor="middle">Restore ramdisk</text>
<text class="ts t-gray-s" x="195" y="150" text-anchor="middle">arm64eCustomerRamDisk</text>
<text class="ts t-gray-s" x="195" y="174" text-anchor="middle">erase · wipe · full reflash</text>
<text class="ts t-gray-s" x="195" y="194" text-anchor="middle">restored_external · asr · seputil</text>

<rect x="370" y="104" width="270" height="120" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="505" y="130" text-anchor="middle">Update ramdisk</text>
<text class="ts t-gray-s" x="505" y="150" text-anchor="middle">arm64eUpdateRamDisk</text>
<text class="ts t-gray-s" x="505" y="174" text-anchor="middle">update in place · keep data</text>
<text class="ts t-gray-s" x="505" y="194" text-anchor="middle">restored_update · asr</text>
</svg>
<figcaption>The restore ramdisk and the update ramdisk.</figcaption>
</figure>

<p>The <strong>restore ramdisk</strong> is the clean slate. It erases the device, recreates the partitions, and writes a fresh system. User data does not survive. This is the path a full restore takes, the one labeled <code>Erase</code>. The control program on it is <code>restored_external</code>.</p>
<p>The <strong>update ramdisk</strong> is the careful path. It applies a new system without wiping the data volume. The system volume is replaced, the data is left in place. Its control program is <code>restored_update</code>. This is the <code>Update</code> path, the one that runs when a device takes a normal software update.</p>
<p>On a modern arm64e device the two ship as <code>arm64eCustomerRamDisk</code> and <code>arm64eUpdateRamDisk</code>. The <code>BuildManifest</code> points each restore behavior at the right one. Chapter 5 covers how that selection is made.</p>

<h3>What ASR does</h3>
<p>The control program orchestrates. It does not do the copy itself. For the actual writing of the system it hands off to one tool: <code>asr</code>, Apple Software Restore, at <code>/usr/sbin/asr</code> inside the ramdisk. ASR is the part that moves the bytes.</p>
<p>Its job is narrow and it is the heart of the restore. Read the decrypted system image, verify it, write it to the target volume. The verification is not a formality. ASR checksums each block as it goes and refuses anything that does not match. A corrupt or tampered image fails here, not on first boot.</p>

<figure>
<svg class="diagram" viewBox="0 0 680 296" role="img" xmlns="http://www.w3.org/2000/svg">
<title>What ASR does inside the ramdisk</title>
<desc>The control program launches asr. ASR reads the decrypted system image, verifies each block against a checksum, then writes the verified blocks to the target APFS volume on internal storage.</desc>
<defs>
<marker id="arr5" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#5f5e5a" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
</defs>

<rect x="160" y="40" width="360" height="52" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="340" y="60" text-anchor="middle" dominant-baseline="central">restored launches asr</text>
<text class="ts t-gray-s" x="340" y="78" text-anchor="middle" dominant-baseline="central">in the ramdisk</text>
<line x1="340" y1="96" x2="340" y2="120" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr5)"/>

<rect x="160" y="124" width="360" height="52" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="340" y="144" text-anchor="middle" dominant-baseline="central">Read decrypted image</text>
<text class="ts t-gray-s" x="340" y="162" text-anchor="middle" dominant-baseline="central">block by block</text>
<line x1="340" y1="180" x2="340" y2="204" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr5)"/>

<rect x="160" y="208" width="360" height="52" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="340" y="228" text-anchor="middle" dominant-baseline="central">Verify each block</text>
<text class="ts t-coral-s" x="340" y="246" text-anchor="middle" dominant-baseline="central">checksum · reject on mismatch</text>
<line x1="340" y1="264" x2="340" y2="288" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr5)"/>

<text class="ts t-gray-s" x="340" y="282" text-anchor="middle" dominant-baseline="central">writes verified blocks to the target APFS volume</text>
</svg>
<figcaption>What ASR does, inside the ramdisk.</figcaption>
</figure>

<p>This places the ramdisk in the restore sequence from the start of the document. The kernel and ramdisk step is where this environment comes up. The ASR step that follows, the amber box that writes the system, is ASR running inside this ramdisk, reading the decrypted <code>.aea</code> image and writing it to storage. On modern devices the same environment also updates the Secure Enclave through <code>seputil</code>.</p>

<h3>Why they stay in the clear</h3>
<p>The firmware components are AES-encrypted, each with its own key. The ramdisks are not. They are plain disk images, mountable as they are. The reason is structural, and it is worth seeing precisely.</p>

<figure>
<svg class="diagram" viewBox="0 0 680 296" role="img" xmlns="http://www.w3.org/2000/svg">
<title>Why the ramdisk stays in the clear</title>
<desc>Both firmware and ramdisk sit inside the same Image4 signed wrapper. Firmware payloads are AES-encrypted. The ramdisk payload is a plain DMG. The seal is the signature, not the encryption.</desc>
<rect x="40" y="44" width="290" height="208" rx="14" fill="none" stroke="#c4c2b8" stroke-width="1" stroke-dasharray="6 4"/>
<text class="th t-ink" x="60" y="70">Firmware component</text>
<text class="ts s-mut" x="60" y="88">iBoot, SEP, baseband</text>
<rect x="64" y="104" width="242" height="56" rx="9" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="185" y="124" text-anchor="middle" dominant-baseline="central">Image4 wrapper</text>
<text class="ts t-coral-s" x="185" y="142" text-anchor="middle" dominant-baseline="central">signed by Apple</text>
<rect x="64" y="172" width="242" height="56" rx="9" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="185" y="192" text-anchor="middle" dominant-baseline="central">AES-encrypted payload</text>
<text class="ts t-coral-s" x="185" y="210" text-anchor="middle" dominant-baseline="central">needs a key to read</text>

<rect x="350" y="44" width="290" height="208" rx="14" fill="none" stroke="#c4c2b8" stroke-width="1" stroke-dasharray="6 4"/>
<text class="th t-ink" x="370" y="70">Ramdisk</text>
<text class="ts s-mut" x="370" y="88">restore, update</text>
<rect x="374" y="104" width="242" height="56" rx="9" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="495" y="124" text-anchor="middle" dominant-baseline="central">Image4 wrapper</text>
<text class="ts t-coral-s" x="495" y="142" text-anchor="middle" dominant-baseline="central">signed by Apple</text>
<rect x="374" y="172" width="242" height="56" rx="9" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="495" y="192" text-anchor="middle" dominant-baseline="central">Plain DMG payload</text>
<text class="ts t-gray-s" x="495" y="210" text-anchor="middle" dominant-baseline="central">mountable as is</text>
</svg>
<figcaption>The seal is the signature, not the encryption.</figcaption>
</figure>

<p>Both sit inside the same container, the Image4 format covered in chapter 4. Image4 carries a signature. That signature is what the boot chain checks: the device runs this ramdisk only because Apple signed it, and the signature is bound to the device through personalization. Encryption is a separate question.</p>
<p>Firmware payloads add an encryption layer on top of the signature. The ramdisk payload does not. Its DMG is in the clear. The integrity guarantee is identical, it comes from the signature either way, but the contents of the ramdisk are open to read. There is no key to recover. This was not always so. Older iOS encrypted the ramdisks too, and recovering their keys was a step in any analysis. Since roughly iOS 10 they ship decrypted. Today you mount and read them directly.</p>
<p>This matters for analysis. The ramdisk is one of the easiest parts of the archive to study, and one of the most useful. It is a working install environment: <code>asr</code>, <code>restored_external</code>, the personalization helpers, the partition tooling. The logic of the restore is right here, in plain binaries, with nothing to decrypt first.</p>

<h3>Mounting and inspecting them</h3>
<p>There is one catch, and it trips people up. The files named like <code>044-XXXXX-XXX.dmg</code> in the archive are not mountable DMGs. They are Image4 payloads (<code>im4p</code>) with a DMG inside. Double-clicking fails. You extract the payload first, then mount the DMG that comes out.</p>
<p>With <code>ipsw</code>, the whole thing is one command:</p>
<ul>
  <li><code>ipsw mount rdisk &lt;IPSW&gt;</code>. Mounts a restore ramdisk. It extracts the <code>im4p</code> payload and mounts the inner DMG for you.</li>
  <li><code>ipsw mount rdisk &lt;IPSW&gt; --ident Erase</code>. Selects which ramdisk to mount when the archive holds more than one. Without it, the first is used.</li>
</ul>
<p>The manual route shows what is happening underneath, and is worth doing once:</p>
<ul>
  <li><code>ipsw extract --pattern '044-.*\.dmg' &lt;IPSW&gt;</code>. Pulls the ramdisk file out of the archive.</li>
  <li><code>ipsw img4 im4p extract --output ramdisk.dmg 044-XXXXX-XXX.dmg</code>. Unwraps the Image4 payload into a real DMG. On older tooling, <code>img4 -i in -o out</code> does the same.</li>
  <li><code>open ramdisk.dmg</code>, or <code>hdiutil attach ramdisk.dmg</code>. Mounts it on macOS. It appears under <code>/Volumes/</code>.</li>
</ul>
<p>Once mounted, it is a small Unix tree. The parts worth a look:</p>
<ul>
  <li><code>/usr/sbin/asr</code>. The restore engine. The binary to read if you want to understand how the system is written and verified.</li>
  <li><code>/usr/local/bin/restored_external</code> or <code>restored_update</code>. The control program. It speaks to the host over USB and drives the sequence.</li>
  <li><code>/usr/local/share/restore/</code>. Restore options and behavior, including the per-device sizing the install relies on.</li>
  <li>The other helpers. <code>seputil</code> for the Secure Enclave, the APFS and partition tools, the personalization pieces.</li>
</ul>
<p>From there the methods from chapter 1 apply unchanged. Run <code>ipsw macho info</code> on a binary to read its structure, <code>ipsw ent</code> to pull entitlements, then a disassembler for the logic. The ramdisk binaries are small and self-contained, which makes them a clean place to start before the larger system.</p>
<p class="note">A note on platform. The inner DMG here is usually HFS+ or a simple APFS image, lighter than the LZBITMAP-compressed cryptex images from chapter 1, so Linux with <code>apfs-fuse</code> tends to handle it without trouble. Even so, the rest of the pipeline leans on macOS, so an Apple Silicon Mac stays the path of least friction.</p>

<h2>Chapter 3: kernelcache</h2>
<p>The system images from chapter 1 are what the device runs. The kernelcache is what runs them. It is the executable core: the part that schedules processes, manages memory, talks to the hardware, and decides what every other piece is allowed to do. One file in the archive, around 22 MB, and the most concentrated code in the whole image.</p>
<p>The name is precise. It is not just the kernel. It is the kernel and its drivers, compiled and linked ahead of time into one ready-to-run unit, so the device does not assemble them at every boot. Cache, in the sense of precomputed.</p>

<h3>What is inside</h3>
<p>Open a desktop operating system and the kernel is one file, the drivers are many, loaded as needed. iOS does not work that way. The kernel and every built-in driver are fused into a single file, sharing one address space.</p>

<figure>
<svg class="diagram" viewBox="0 0 680 372" role="img" xmlns="http://www.w3.org/2000/svg">
<title>What is fused inside the kernelcache</title>
<desc>The kernelcache is one file holding the XNU kernel proper, hundreds of kexts, prelink metadata, and symbol sets, all linked into a single address space.</desc>
<rect x="40" y="44" width="600" height="288" rx="16" fill="none" stroke="#c4c2b8" stroke-width="1" stroke-dasharray="6 4"/>
<text class="th t-ink" x="60" y="70">kernelcache · one file, one address space</text>
<text class="ts s-mut" x="60" y="88">XNU kernel and all built-in drivers, prelinked</text>

<rect x="60" y="104" width="270" height="92" rx="10" fill="#faeeda" stroke="#854f0b" stroke-width="1"/>
<text class="th t-amber" x="195" y="130" text-anchor="middle">XNU kernel proper</text>
<text class="ts t-amber-s" x="195" y="152" text-anchor="middle">Mach · BSD · IOKit · libkern</text>
<text class="ts t-amber-s" x="195" y="174" text-anchor="middle">scheduler, VM, syscalls</text>

<rect x="350" y="104" width="270" height="92" rx="10" fill="#e1f5ee" stroke="#0f6e56" stroke-width="1"/>
<text class="th t-teal" x="485" y="130" text-anchor="middle">Kexts</text>
<text class="ts t-teal-s" x="485" y="152" text-anchor="middle">hundreds of drivers</text>
<text class="ts t-teal-s" x="485" y="174" text-anchor="middle">AppleMobileFileIntegrity, sandbox, GPU</text>

<rect x="60" y="216" width="270" height="92" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="195" y="242" text-anchor="middle">Prelink metadata</text>
<text class="ts t-gray-s" x="195" y="264" text-anchor="middle">__PRELINK_INFO</text>
<text class="ts t-gray-s" x="195" y="286" text-anchor="middle">bundle IDs, fixed load addresses</text>

<rect x="350" y="216" width="270" height="92" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="485" y="242" text-anchor="middle">Symbol sets · KPI</text>
<text class="ts t-gray-s" x="485" y="264" text-anchor="middle">stable kernel interfaces</text>
<text class="ts t-gray-s" x="485" y="286" text-anchor="middle">what kexts may call</text>
</svg>
<figcaption>What is fused inside the kernelcache.</figcaption>
</figure>

<p>XNU is the kernel itself: the Mach core for scheduling and memory, the BSD layer for the Unix system calls and the file system, IOKit for the driver framework, libkern for the runtime. Around it sit the kexts, the kernel extensions, which are the drivers. There are several hundred. They run the GPU, the storage, the radios, and, more interesting to a researcher, the security machinery: <code>AppleMobileFileIntegrity</code>, the sandbox, the code-signing enforcement.</p>
<p>The other two pieces are metadata, and they matter for analysis. <code>__PRELINK_INFO</code> records every kext's identity and where it loads. The symbol sets, the KPI, define the narrow set of kernel functions a kext is permitted to call. A kext that reaches outside that set will not link. This is the seam an analyst follows to tell one driver from another inside the merged file.</p>

<h3>Three eras of one format</h3>
<p>The kernelcache has not always looked the same. Its format moved through three stages, and the difference is not cosmetic. It decides whether you can pull a single driver out of the file at all. This trips people up, because a guide written for one era gives steps that simply fail on another.</p>

<figure>
<svg class="diagram" viewBox="0 0 680 384" role="img" xmlns="http://www.w3.org/2000/svg">
<title>Three eras of the kernelcache format</title>
<desc>Three stacked rows showing how the kernelcache changed: split kexts before iOS 12, monolithic prelinked kernel, then the MH_FILESET kernel collection from iOS 12 and later. Each row notes whether kexts are separable.</desc>
<defs>
<marker id="arr6" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#5f5e5a" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
</defs>

<rect x="40" y="40" width="600" height="88" rx="12" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="60" y="66">Early · split kexts</text>
<text class="ts t-gray-s" x="60" y="86">kernel and kexts loosely packed, each a separate Mach-O</text>
<text class="ts t-gray-s" x="60" y="106">encrypted through iOS 9 · separable with old tools</text>
<rect x="486" y="56" width="138" height="56" rx="8" fill="#e1f5ee" stroke="#0f6e56" stroke-width="1"/>
<text class="th t-teal" x="555" y="80" text-anchor="middle">kexts</text>
<text class="ts t-teal-s" x="555" y="100" text-anchor="middle">separable</text>
<line x1="340" y1="128" x2="340" y2="148" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr6)"/>

<rect x="40" y="152" width="600" height="88" rx="12" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="60" y="178">Middle · monolithic prelinked</text>
<text class="ts t-gray-s" x="60" y="198">kext code interleaved with the kernel, one Mach-O</text>
<text class="ts t-gray-s" x="60" y="218">plain since iOS 10 · stripped · hard to separate</text>
<rect x="486" y="168" width="138" height="56" rx="8" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="555" y="192" text-anchor="middle">kexts</text>
<text class="ts t-coral-s" x="555" y="212" text-anchor="middle">fused in</text>
<line x1="340" y1="240" x2="340" y2="260" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr6)"/>

<rect x="40" y="264" width="600" height="100" rx="12" fill="#faeeda" stroke="#854f0b" stroke-width="1"/>
<text class="th t-amber" x="60" y="290">Modern · MH_FILESET (iOS 12+)</text>
<text class="ts t-amber-s" x="60" y="310">a container that bundles many Mach-Os, mapped together</text>
<text class="ts t-amber-s" x="60" y="330">each entry keeps its own segments and identity</text>
<text class="ts t-amber-s" x="60" y="350">this is the iPhone 16 Pro Max case</text>
<rect x="486" y="284" width="138" height="60" rx="8" fill="#e1f5ee" stroke="#0f6e56" stroke-width="1"/>
<text class="th t-teal" x="555" y="308" text-anchor="middle">kexts</text>
<text class="ts t-teal-s" x="555" y="328" text-anchor="middle">separable again</text>
</svg>
<figcaption>Three eras of the kernelcache format.</figcaption>
</figure>

<p>In the early era the kexts were loosely packed beside the kernel, each its own Mach-O. Old tools could lift one out directly. Through iOS 9 the whole thing was also encrypted, so recovering keys came first.</p>
<p>Then came the monolithic era. Kext code was interleaved with the kernel's own and the file was stripped of symbols. There was no clean way to separate a driver anymore. This is the era that earned the kernelcache its reputation for being hard.</p>
<p>The modern era reversed that, and improved on it. Since iOS 12 the kernelcache is an <code>MH_FILESET</code>: a Mach-O container type whose job is to hold many Mach-O binaries and map them into memory together. Each entry, the kernel and every kext, keeps its own segments and its own identity inside the container. The boot loader reads a table of entries to place each one. For an analyst, that table is a gift. The drivers are bundled but no longer blended, so a good tool can hand you a single kext as a clean, standalone binary. The iPhone 16 Pro Max on iOS 26.5 is squarely here.</p>

<h3>Why it is in the clear</h3>
<p>The firmware components in chapter 4 are AES-encrypted, each behind its own key. You might expect the kernel, the most sensitive code on the device, to be the most locked. On a current device it is not. It ships in the clear.</p>

<figure>
<svg class="diagram" viewBox="0 0 680 340" role="img" xmlns="http://www.w3.org/2000/svg">
<title>The kernelcache wrapper, layer by layer</title>
<desc>From outside in: an Image4 wrapper signed by Apple, an im4p payload, LZSS compression, and at the core a plain MH_FILESET Mach-O. No encryption layer. The only obstacle to reading is decompression.</desc>
<defs>
<marker id="arr7" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#5f5e5a" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
</defs>

<rect x="40" y="40" width="430" height="280" rx="14" fill="none" stroke="#993c1d" stroke-width="1" stroke-dasharray="6 4"/>
<text class="th t-coral" x="60" y="66">Image4 wrapper</text>
<text class="ts t-coral-s" x="60" y="84">signed by Apple · integrity only</text>

<rect x="66" y="100" width="378" height="64" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="255" y="124" text-anchor="middle">im4p payload</text>
<text class="ts t-coral-s" x="255" y="146" text-anchor="middle">type krnl · the kernelcache inside</text>

<rect x="92" y="178" width="326" height="58" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="255" y="201" text-anchor="middle">LZSS compression</text>
<text class="ts t-gray-s" x="255" y="221" text-anchor="middle">the only thing in the way</text>

<rect x="118" y="250" width="274" height="58" rx="10" fill="#faeeda" stroke="#854f0b" stroke-width="1"/>
<text class="th t-amber" x="255" y="273" text-anchor="middle">MH_FILESET Mach-O</text>
<text class="ts t-amber-s" x="255" y="293" text-anchor="middle">plain · magic 0xfeedfacf</text>

<rect x="494" y="120" width="146" height="120" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="567" y="150" text-anchor="middle">No AES</text>
<text class="ts t-gray-s" x="567" y="172" text-anchor="middle">no key to</text>
<text class="ts t-gray-s" x="567" y="190" text-anchor="middle">recover</text>
<text class="ts t-gray-s" x="567" y="214" text-anchor="middle">decompress</text>
<text class="ts t-gray-s" x="567" y="232" text-anchor="middle">and read</text>
<line x1="470" y1="180" x2="492" y2="180" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr7)"/>
</svg>
<figcaption>The kernelcache wrapper, layer by layer.</figcaption>
</figure>

<p>The file is wrapped in Image4 and signed, like everything else in chapter 4. The signature is what the boot chain checks. It guarantees the code is Apple's and unmodified. That is integrity, and the device enforces it strictly. Encryption is a different question, and the answer here is no. The payload is type <code>krnl</code>, and inside the wrapper it is only compressed, with LZSS. Decompress it and you have a plain Mach-O, recognizable by its magic bytes, <code>0xfeedfacf</code> for 64-bit. There is no key to recover.</p>
<p>This was not always the case. Through iOS 9 the kernelcache was encrypted as well, and a generation of jailbreak work went into pulling those keys off the hardware. From iOS 10 on, Apple stopped encrypting it. The reasoning is sound: encryption was protecting code that researchers and attackers could read on the device anyway, at the cost of real friction for legitimate study. The signature, not the secrecy, is what actually protects the system. For you, the result is direct. Decompress and read.</p>
<p class="note">Plain at rest does not mean unprotected at runtime. Once the kernel is loaded, the silicon guards it. On the A18 in this device, the Secure Page Table Monitor, with the Trusted Execution Monitor, runs at a higher privilege than the kernel and protects the page tables even against an attacker who already has kernel write. On older chips this role was filled by the Page Protection Layer. The kernelcache you read on disk and the kernel as it runs live under very different rules.</p>

<h3>Extracting and reading it</h3>
<p>The pipeline mirrors chapter 1: get the file out, get past the wrapper, then explore. The wrapper here is simpler, since there is nothing to decrypt.</p>

<figure>
<svg class="diagram" viewBox="0 0 680 520" role="img" xmlns="http://www.w3.org/2000/svg">
<title>From the .ipsw to analyzable kernel code</title>
<desc>A pipeline: extract the kernelcache from the IPSW, decompress LZSS into a Mach-O fileset, list the kexts, extract a target kext with resolved imports, then disassemble. A side note shows the single-command shortcut.</desc>
<defs>
<marker id="arr8" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#5f5e5a" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
</defs>

<rect x="160" y="40" width="360" height="58" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="340" y="62" text-anchor="middle" dominant-baseline="central">Extract from the .ipsw</text>
<text class="ts t-gray-s" x="340" y="82" text-anchor="middle" dominant-baseline="central">ipsw extract --kernel</text>
<line x1="340" y1="102" x2="340" y2="124" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr8)"/>

<rect x="160" y="128" width="360" height="58" rx="10" fill="#faeeda" stroke="#854f0b" stroke-width="1"/>
<text class="th t-amber" x="340" y="150" text-anchor="middle" dominant-baseline="central">Decompress LZSS</text>
<text class="ts t-amber-s" x="340" y="170" text-anchor="middle" dominant-baseline="central">im4p payload to a Mach-O fileset</text>
<line x1="340" y1="190" x2="340" y2="212" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr8)"/>

<rect x="160" y="216" width="360" height="58" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="340" y="238" text-anchor="middle" dominant-baseline="central">List the kexts</text>
<text class="ts t-gray-s" x="340" y="258" text-anchor="middle" dominant-baseline="central">ipsw kernel kexts · find the target</text>
<line x1="340" y1="278" x2="340" y2="300" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr8)"/>

<rect x="160" y="304" width="360" height="58" rx="10" fill="#e1f5ee" stroke="#0f6e56" stroke-width="1"/>
<text class="th t-teal" x="340" y="326" text-anchor="middle" dominant-baseline="central">Extract one kext</text>
<text class="ts t-teal-s" x="340" y="346" text-anchor="middle" dominant-baseline="central">ipsw kernel extract --imports</text>
<line x1="340" y1="366" x2="340" y2="388" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arr8)"/>

<rect x="160" y="392" width="360" height="58" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="340" y="414" text-anchor="middle" dominant-baseline="central">Disassemble</text>
<text class="ts t-gray-s" x="340" y="434" text-anchor="middle" dominant-baseline="central">IDA Pro · Ghidra · ipsw macho disass</text>

<text class="ts t-gray-s" x="340" y="485" text-anchor="middle" dominant-baseline="central">Shortcut: ipsw extract --kernel does the extract and decompress in one step.</text>
</svg>
<figcaption>From the .ipsw to analyzable kernel code.</figcaption>
</figure>

<p>The fast path is one command. <code>ipsw extract --kernel &lt;IPSW&gt;</code> pulls the kernelcache out and decompresses it in the same step, leaving a Mach-O fileset ready to read. If you ever have a raw <code>im4p</code> in hand, <code>ipsw kernel dec</code> decompresses it on its own.</p>
<p>From there the useful commands:</p>
<ul>
  <li><code>ipsw kernel version &lt;kernelcache&gt;</code>. Reads the build string. It tells you the XNU version, the build date, and the target chip, for example <code>RELEASE_ARM64_T8140</code> on this device. A quick way to confirm you have the right file.</li>
  <li><code>ipsw kernel kexts &lt;kernelcache&gt;</code>. Lists every kext in the fileset with its bundle ID and version. This is your index into the file.</li>
  <li><code>ipsw kernel extract &lt;kernelcache&gt; &lt;bundle-id&gt; --imports</code>. Pulls one kext out as a standalone Mach-O. The <code>--imports</code> flag is the important part: it scans the other entries and writes the resolved names back into the symbol table, so calls into the kernel show as names rather than bare addresses. The result loads cleanly in IDA Pro or Ghidra.</li>
  <li><code>ipsw kernel kexts --diff &lt;old&gt; &lt;new&gt;</code>. Lists which kexts changed between two builds. Paired with the version diffing from the appendix, this is how you find what a security update actually touched, without reading the whole kernel.</li>
</ul>
<p>A concrete path makes it real. To study how the sandbox is enforced, list the kexts, find <code>com.apple.security.sandbox</code>, extract it with <code>--imports</code>, and open it in a disassembler. You are now reading the policy engine that decides what every app on the device may do, as a single clean binary, with nothing decrypted along the way.</p>
<p>One platform note carries over from chapter 1. The disassembly itself is portable, but the surrounding workflow, the symbol resolution and the version diffing, leans on macOS. An Apple Silicon Mac stays the smoother path.</p>

<h2>Chapter 4: Firmware</h2>
<p>So far the archive has opened up. The system images mounted. The ramdisks mounted. The kernel decompressed and read. This chapter is the part that mostly does not open. The firmware is the lowest layer, the code that runs before the kernel and beside it, and on a modern device it is the one family you cannot read.</p>
<p>It is also where the format the whole document keeps naming finally gets explained. Every component here, and in truth every signed component in the archive, is wrapped in Image4. Start there.</p>

<h3>The Image4 container</h3>
<p>Image4 is the wrapper. It replaced the older IMG3 on every 64-bit Apple device, and unlike IMG3's custom layout, it is a standard ASN.1 structure in DER encoding. The same container holds the bootloaders, the kernel from chapter 3, the ramdisks from chapter 2, and the firmware here. Learn it once and the whole archive reads the same way.</p>

<figure>
<svg class="diagram" viewBox="0 0 680 360" role="img" xmlns="http://www.w3.org/2000/svg">
<title>The Image4 container, taken apart</title>
<desc>An Image4 file is a DER-encoded ASN.1 container holding three parts: the IM4P payload, the IM4M manifest that signs it, and the optional IM4R restore info carrying the boot nonce.</desc>
<rect x="40" y="44" width="600" height="300" rx="16" fill="none" stroke="#993c1d" stroke-width="1" stroke-dasharray="6 4"/>
<text class="th t-coral" x="60" y="70">IMG4 file</text>
<text class="ts t-coral-s" x="60" y="88">DER-encoded ASN.1 · replaces the old IMG3</text>

<rect x="60" y="104" width="560" height="68" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="80" y="130">IM4P · payload</text>
<text class="ts t-coral-s" x="80" y="152">the data · a 4-char type tag (ibot, krnl, sepi) · optional KBAG</text>

<rect x="60" y="184" width="560" height="68" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="80" y="210">IM4M · manifest</text>
<text class="ts t-coral-s" x="80" y="232">the signature · component hashes · the certificate chain</text>

<rect x="60" y="264" width="560" height="60" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="80" y="288">IM4R · restore info (optional)</text>
<text class="ts t-gray-s" x="80" y="310">the boot nonce · set per restore · ties one signature to one boot</text>
</svg>
<figcaption>The Image4 container, taken apart.</figcaption>
</figure>

<p>Three parts. The IM4P is the payload, the actual thing being shipped, tagged with a four-character type so the device knows what it is: <code>ibot</code> for iBoot, <code>krnl</code> for the kernel, <code>sepi</code> for the Secure Enclave, and so on. If the payload is encrypted, the IM4P also carries a KBAG, a keybag holding the key, itself wrapped so only the right chip can open it. This is the <code>im4p</code> you met in chapter 2, when a ramdisk DMG would not mount and you had to extract the payload first.</p>
<p>The IM4M is the manifest, and it is the only signed part. It holds hashes of the components it vouches for and the certificate chain back to Apple. This is what the boot chain actually checks. It is the modern form of the APTicket from the glossary, the device-bound ticket the TSS produces. The IM4R is the smallest piece and usually the only optional one. It carries the boot nonce, a fresh value per restore, which ties a given signature to a single boot and stops an old signed image from being replayed later.</p>

<h3>The chain of trust</h3>
<p>The firmware components are not a pile of files. They are an ordered chain, and the order is the security. Each stage verifies the next, by its Image4 signature, before it hands over control. Break any link and the next stage refuses to run.</p>

<figure>
<svg class="diagram" viewBox="0 0 680 470" role="img" xmlns="http://www.w3.org/2000/svg">
<title>The boot chain as a relay of trust</title>
<desc>BootROM verifies and runs iBoot, which verifies the kernelcache. A side branch shows the DFU and restore path through iBSS and iBEC. The Secure Enclave boots its own signed sepOS in parallel.</desc>
<defs>
<marker id="arrB" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#5f5e5a" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
</defs>

<rect x="180" y="40" width="320" height="56" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="340" y="60" text-anchor="middle" dominant-baseline="central">BootROM</text>
<text class="ts t-coral-s" x="340" y="78" text-anchor="middle" dominant-baseline="central">burned into silicon · the root of trust</text>
<line x1="340" y1="96" x2="340" y2="120" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arrB)"/>

<rect x="180" y="124" width="320" height="56" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="340" y="144" text-anchor="middle" dominant-baseline="central">iBoot</text>
<text class="ts t-coral-s" x="340" y="162" text-anchor="middle" dominant-baseline="central">the bootloader · one image, all phases</text>
<line x1="340" y1="180" x2="340" y2="204" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arrB)"/>

<rect x="180" y="208" width="320" height="56" rx="10" fill="#faeeda" stroke="#854f0b" stroke-width="1"/>
<text class="th t-amber" x="340" y="228" text-anchor="middle" dominant-baseline="central">kernelcache</text>
<text class="ts t-amber-s" x="340" y="246" text-anchor="middle" dominant-baseline="central">verified, then run · chapter 3</text>

<rect x="180" y="300" width="320" height="56" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="340" y="320" text-anchor="middle" dominant-baseline="central">Restore path · iBSS then iBEC</text>
<text class="ts t-gray-s" x="340" y="338" text-anchor="middle" dominant-baseline="central">the DFU twins of iBoot · chapter 2</text>

<rect x="180" y="384" width="320" height="56" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="340" y="404" text-anchor="middle" dominant-baseline="central">Secure Enclave · sepOS</text>
<text class="ts t-coral-s" x="340" y="422" text-anchor="middle" dominant-baseline="central">own boot ROM, own signed OS, in parallel</text>

<path d="M180 232 L96 232 L96 328 L178 328" stroke="#5f5e5a" stroke-width="1.5" fill="none" stroke-dasharray="5 4" marker-end="url(#arrB)"/>
<text class="ts t-gray-s" x="96" y="214" text-anchor="middle">DFU</text>

<path d="M500 152 L584 152 L584 412 L502 412" stroke="#5f5e5a" stroke-width="1.5" fill="none" stroke-dasharray="5 4" marker-end="url(#arrB)"/>
<text class="ts t-coral-s" x="584" y="134" text-anchor="middle">starts SEP</text>
</svg>
<figcaption>The boot chain as a relay of trust.</figcaption>
</figure>

<p>It begins in the BootROM, code burned into the silicon at manufacture. It cannot be changed, so it is the root: whatever it trusts, the chain trusts. On a modern device the BootROM loads iBoot directly. Older devices had a separate first stage, the LLB, the Low Level Bootloader, but on recent silicon one iBoot image handles every phase, so the LLB no longer ships as its own file. iBoot initializes the hardware, then verifies and runs the kernelcache. That is the link back to chapter 3: the kernel runs only because iBoot checked its signature first. Alongside the bootloaders sits <code>iBootData</code>, a small data blob iBoot consumes, not code of its own.</p>
<p>The restore path is a branch off the same trunk. When the device is in DFU, the BootROM loads iBSS, the single-stage iBoot, which loads iBEC, the restore-mode iBoot. These are the signed bootloaders the restore sequence named at the start of the document, and the ones that bring up the environment chapter 2's ramdisk runs in. Off to the side, the Secure Enclave boots in parallel. It has its own boot ROM and its own signed operating system, sepOS, and the main processor never sees inside it.</p>

<h3>Why you cannot read it</h3>
<p>Here the firmware breaks from everything before it. The kernel was wrapped and signed but not encrypted, so you decompressed it and read it. The firmware is wrapped, signed, and encrypted, each component behind its own key. And on this device, those keys are out of reach.</p>

<figure>
<svg class="diagram" viewBox="0 0 680 392" role="img" xmlns="http://www.w3.org/2000/svg">
<title>Per-component encryption and the A12 boundary</title>
<desc>Each firmware component carries its own AES key in a keybag, unwrapped by the chip's GID key. On A11 and earlier a bootrom exploit exposed those keys. On A12 and later, including this device, they cannot be reached.</desc>
<defs>
<marker id="arrC" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#5f5e5a" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
</defs>

<rect x="40" y="44" width="600" height="132" rx="14" fill="none" stroke="#993c1d" stroke-width="1" stroke-dasharray="6 4"/>
<text class="th t-coral" x="60" y="70">One component, locked</text>
<text class="ts t-coral-s" x="60" y="88">iBoot, SEP, baseband, each its own key</text>

<rect x="60" y="104" width="270" height="56" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="195" y="126" text-anchor="middle">AES-encrypted payload</text>
<text class="ts t-coral-s" x="195" y="146" text-anchor="middle">unreadable without the key</text>

<rect x="350" y="104" width="270" height="56" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="485" y="126" text-anchor="middle">KBAG · the keybag</text>
<text class="ts t-coral-s" x="485" y="146" text-anchor="middle">key, wrapped to the GID key</text>
<line x1="350" y1="132" x2="332" y2="132" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arrC)"/>

<rect x="40" y="200" width="290" height="172" rx="14" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="185" y="228" text-anchor="middle">A11 and earlier</text>
<text class="ts t-gray-s" x="185" y="254" text-anchor="middle">checkm8, a bootrom exploit</text>
<text class="ts t-gray-s" x="185" y="274" text-anchor="middle">runs the GID key on demand</text>
<text class="th t-teal" x="185" y="300" text-anchor="middle">keys recoverable</text>
<text class="ts t-gray-s" x="185" y="326" text-anchor="middle">old firmware decrypted</text>
<text class="ts t-gray-s" x="185" y="346" text-anchor="middle">and published in key databases</text>

<rect x="350" y="200" width="290" height="172" rx="14" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="495" y="228" text-anchor="middle">A12 and later</text>
<text class="ts t-coral-s" x="495" y="254" text-anchor="middle">no public bootrom exploit</text>
<text class="ts t-coral-s" x="495" y="274" text-anchor="middle">the GID key stays sealed</text>
<text class="th t-coral" x="495" y="300" text-anchor="middle">keys out of reach</text>
<text class="ts t-coral-s" x="495" y="326" text-anchor="middle">this device, an A18</text>
<text class="ts t-coral-s" x="495" y="346" text-anchor="middle">firmware stays opaque</text>
</svg>
<figcaption>Per-component encryption and the A12 boundary.</figcaption>
</figure>

<p>The mechanism is the KBAG in the IM4P. The key for the payload sits there, but wrapped, encrypted to the chip's GID key, a key fused into the silicon that never leaves it. To unwrap it you must run the GID key, and the GID key only runs inside the hardware AES engine. So decryption is not a matter of finding a file. It needs code execution on the chip itself, in the narrow window before the kernel loads and the GID engine is switched off. The boot-chain components are keyed to the application processor's GID key. The SEP firmware has its own, keyed to the Secure Enclave's GID, a separate lock again.</p>
<p>That window is exactly what a bootrom exploit opened. On A11 and earlier, checkm8 gave researchers code execution in the BootROM, which let them run the GID key and recover the firmware keys. That is why old firmware can be decrypted and why community key databases exist. But checkm8 does not reach A12 and later. This device is an A18. There is no public BootROM exploit for it, the GID key stays sealed, and the firmware keys cannot be pulled. The diagrams in this document call the firmware family AES-encrypted, and on this hardware that is the end of the story for the public side. It stays opaque.</p>
<p>This is the exact mirror of chapter 3. The kernel is the most sensitive code, shipped in the clear, because the signature is what protects it. The firmware is lower still, shipped encrypted, with keys you cannot reach. Same archive, opposite postures, and worth holding both in mind: signing is about integrity, encryption is about secrecy, and Apple applies them independently. The history is a steady retreat of secrecy. Early devices encrypted nearly everything and the keys leaked. Then the kernel was left in the clear. The firmware kept its encryption, and from A12 on the keys finally became unreachable rather than merely undiscovered.</p>

<h3>Signing and personalization</h3>
<p>The signature is checked at every step, but a plain signature would be replayable: capture one signed image, install it forever. Apple closes that with personalization. The signature is bound to one specific device, and granted only while Apple still signs that version. This is the personalization step the restore sequence named at the very start of the document.</p>

<figure>
<svg class="diagram" viewBox="0 0 680 384" role="img" xmlns="http://www.w3.org/2000/svg">
<title>Personalization, the TSS handshake</title>
<desc>The host reads the device ECID and a fresh nonce, sends them with the build manifest to Apple's TSS signing server, and receives a signed manifest, the APTicket, valid only for this device while the version is signed.</desc>
<defs>
<marker id="arrP" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#5f5e5a" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
</defs>

<rect x="60" y="44" width="232" height="84" rx="11" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="176" y="72" text-anchor="middle">Device</text>
<text class="ts t-gray-s" x="176" y="94" text-anchor="middle">ECID, a unique chip ID</text>
<text class="ts t-gray-s" x="176" y="112" text-anchor="middle">plus a fresh nonce</text>

<rect x="388" y="44" width="232" height="84" rx="11" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="504" y="72" text-anchor="middle">Apple TSS</text>
<text class="ts t-coral-s" x="504" y="94" text-anchor="middle">the signing server</text>
<text class="ts t-coral-s" x="504" y="112" text-anchor="middle">signs only what it still signs</text>

<text class="ts t-gray-s" x="340" y="62" text-anchor="middle">ECID + nonce</text>
<path d="M296 74 L384 74" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arrP)"/>
<path d="M384 100 L298 100" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arrP)"/>
<text class="ts t-coral-s" x="340" y="120" text-anchor="middle">signed manifest</text>

<line x1="176" y1="128" x2="176" y2="170" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arrP)"/>

<rect x="60" y="174" width="560" height="64" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="340" y="200" text-anchor="middle">APTicket · the personalized manifest (IM4M)</text>
<text class="ts t-coral-s" x="340" y="222" text-anchor="middle">valid for this ECID only · this nonce only · while the version is signed</text>

<line x1="340" y1="238" x2="340" y2="280" stroke="#5f5e5a" stroke-width="1.5" fill="none" marker-end="url(#arrP)"/>

<rect x="60" y="284" width="270" height="76" rx="10" fill="#faeeda" stroke="#854f0b" stroke-width="1"/>
<text class="th t-amber" x="195" y="310" text-anchor="middle">Boot checks the ticket</text>
<text class="ts t-amber-s" x="195" y="330" text-anchor="middle">matches hashes and ECID</text>
<text class="ts t-amber-s" x="195" y="348" text-anchor="middle">refuses if either is off</text>

<rect x="350" y="284" width="270" height="76" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="485" y="310" text-anchor="middle">No downgrade</text>
<text class="ts t-gray-s" x="485" y="330" text-anchor="middle">once the window closes,</text>
<text class="ts t-gray-s" x="485" y="348" text-anchor="middle">that version will not sign</text>
</svg>
<figcaption>Personalization, the TSS handshake.</figcaption>
</figure>

<p>The host reads two things off the device: the ECID, a unique chip identifier, and a fresh nonce. It sends them to Apple's signing server, the TSS, with the build manifest from chapter 5. The TSS signs, but only for components it still signs at that moment, and returns a manifest, the APTicket, valid for that ECID and that nonce alone. At boot, each stage checks the ticket: the component hashes must match, the ECID must match, and the nonce must be current. If any is off, it refuses.</p>
<p>Two consequences fall out of this. The image is not portable: a manifest signed for one phone is useless on another, because the ECID will not match. And there is no downgrade: once Apple stops signing a version, the signing window closes, the TSS will not produce a ticket for it, and you cannot install it even with every file in hand. The personalization box in the restore sequence is this handshake. The IM4M from the first section of this chapter is the APTicket that comes out of it.</p>

<h3>What is in the folder</h3>
<p>Even where you cannot decrypt it, it is worth knowing what the <code>Firmware</code> folder holds, because the shape of it tells you how the device is built.</p>

<figure>
<svg class="diagram" viewBox="0 0 680 300" role="img" xmlns="http://www.w3.org/2000/svg">
<title>What is in the Firmware folder</title>
<desc>The Firmware folder groups the boot chain components, the coprocessor firmware like SEP and the always-on processor, the baseband for cellular, and the device trees that describe the hardware to the kernel.</desc>
<rect x="40" y="44" width="600" height="240" rx="16" fill="none" stroke="#993c1d" stroke-width="1" stroke-dasharray="6 4"/>
<text class="th t-coral" x="60" y="70">Firmware/ · the low level</text>
<text class="ts t-coral-s" x="60" y="88">each piece an Image4, signed, mostly encrypted</text>

<rect x="60" y="104" width="270" height="76" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="195" y="130" text-anchor="middle">Boot chain</text>
<text class="ts t-coral-s" x="195" y="150" text-anchor="middle">LLB, iBoot, iBSS, iBEC, iBootData</text>
<text class="ts t-coral-s" x="195" y="168" text-anchor="middle">dfu/ and all_flash/</text>

<rect x="350" y="104" width="270" height="76" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="485" y="130" text-anchor="middle">Coprocessors</text>
<text class="ts t-coral-s" x="485" y="150" text-anchor="middle">SEP (sepi), always-on processor</text>
<text class="ts t-coral-s" x="485" y="168" text-anchor="middle">GPU, Neural Engine firmware</text>

<rect x="60" y="192" width="270" height="76" rx="10" fill="#faece7" stroke="#993c1d" stroke-width="1"/>
<text class="th t-coral" x="195" y="218" text-anchor="middle">Baseband</text>
<text class="ts t-coral-s" x="195" y="238" text-anchor="middle">cellular modem firmware</text>
<text class="ts t-coral-s" x="195" y="256" text-anchor="middle">own processor, signed apart</text>

<rect x="350" y="192" width="270" height="76" rx="10" fill="#f1efe8" stroke="#5f5e5a" stroke-width="1"/>
<text class="th t-gray" x="485" y="218" text-anchor="middle">Device trees</text>
<text class="ts t-gray-s" x="485" y="238" text-anchor="middle">the hardware map for the kernel</text>
<text class="ts t-gray-s" x="485" y="256" text-anchor="middle">readable, not encrypted</text>
</svg>
<figcaption>What is in the Firmware folder.</figcaption>
</figure>

<p>The boot chain lives in <code>dfu/</code> and <code>all_flash/</code>: LLB where present, iBoot, iBSS, iBEC, iBootData, and the small images shown at boot. The coprocessor firmware is the Secure Enclave (<code>sepi</code>), the always-on processor that listens for "Hey Siri" while the device sleeps, and the firmware for the GPU and Neural Engine. The baseband is the cellular modem's own software, running on its own processor and signed on its own track, which is why a baseband update is a separate event. Each of these is an Image4, signed, and on this device mostly encrypted.</p>
<p>The device trees are the exception, and the one part here you can actually read. A device tree is the hardware map handed to the kernel at boot: which chips exist, at which addresses, on which buses. It is not encrypted, because it is configuration rather than code. <code>ipsw fw devicetree</code> parses it, and reading it is a quiet way to see what hardware the system expects.</p>

<h3>What you can still do</h3>
<p>The firmware resists analysis on this hardware, but not completely, and knowing where the edges are saves wasted effort.</p>
<ul>
  <li><strong>Inspect the wrappers.</strong> <code>ipsw img4 im4p info &lt;file&gt;</code> reads the Image4 metadata: the type tag, the description, whether a KBAG is present. You learn what a component is, and whether it is encrypted, without decrypting anything.</li>
  <li><strong>Read the manifest.</strong> The IM4M is not encrypted. <code>ipsw img4 im4m info &lt;file&gt;</code> shows what a build vouches for. Paired with the version diffing from the appendix, it tells you which firmware components changed between builds, even when you cannot read inside them.</li>
  <li><strong>Read the device trees.</strong> Unencrypted, and a clean view of the hardware. <code>ipsw fw devicetree &lt;file&gt;</code>.</li>
  <li><strong>Decrypt only old, exposed firmware.</strong> For A11 and earlier, keys exist. <code>ipsw img4 im4p extract --iv &lt;iv&gt; --key &lt;key&gt; &lt;file&gt;</code> decrypts with a known key, and the <code>--lookup</code> flag will fetch one from the community database. Useful for studying how the boot chain worked, on hardware where it is open. Not this device. Other parsers do the same: <code>pyimg4</code> and <code>img4tool</code>.</li>
</ul>
<p>The honest summary: on a current iPhone the firmware is the wall at the bottom of the archive. You can map it, name its parts, read the manifests and the device trees, and watch it change between versions. You cannot, for the most part, read what it does. That boundary is not a gap in tooling. It is the security model holding.</p>

<h2>Chapter 5: Manifests</h2>
<div class="todo"><span class="tag">to write</span><code>BuildManifest.plist</code> as the conductor. Update and Erase behaviors. The link to personalization and the chain of trust. Reading the other <code>.plist</code> files.</div>

<hr>

<h2>Appendix A: Methodology and tooling</h2>
<p>Main tool: <code>ipsw</code> (blacktop). It consolidates the whole pipeline and handles AEA decryption automatically.</p>
<ul>
  <li>Install (macOS): <code>brew install blacktop/tap/ipsw</code>.</li>
  <li>Decryption keys: <code>ipsw dl appledb</code> builds and updates <code>fcs-keys.json</code>, reusable offline.</li>
  <li>Ecosystem: <code>apfs-fuse</code> (Linux), <code>hdiutil</code> or <code>open</code> (macOS), DyldExtractor, class-dump, then Hopper, Ghidra, IDA, or radare2 for disassembly.</li>
</ul>
<p>One practice that changes everything: version diffing. <code>ipsw</code> compares two IPSWs and lists what changed, binaries added, removed, modified. That is how you target what a security fix touched, without guessing.</p>
<p>Discipline: work read-only, keep the originals, keep <code>fcs-keys.json</code> up to date, go from broad to specific.</p>

<h2>Glossary</h2>
<ul>
  <li><strong>SSV</strong> (Signed System Volume). Sealed snapshot of the system volume, verified at boot.</li>
  <li><strong>Cryptex</strong>. Sealed disk image, grafted onto the system at boot, updatable on its own.</li>
  <li><strong>AEA</strong> (Apple Encrypted Archive). Encryption wrapper for DMGs, in IPSWs and OTAs.</li>
  <li><strong>FCS</strong>. Keys used to decrypt AEA, retrieved from Apple (WKMS).</li>
  <li><strong>dyld shared cache</strong>. Large file bundling the system frameworks, pre-linked.</li>
  <li><strong>ASR</strong> (Apple Software Restore). Tool that writes the system image to storage.</li>
  <li><strong>APTicket / SHSH</strong>. Device-bound signing ticket, produced by the TSS.</li>
  <li><strong>ECID</strong>. Unique identifier of the device chip.</li>
  <li><strong>kernelcache</strong>. XNU kernel and its extensions, precompiled.</li>
  <li><strong>BuildManifest</strong>. Manifest listing the components and driving personalization.</li>
</ul>

<h2>References</h2>
<ul class="ref">
  <li>The Apple Wiki: <a href="https://theapplewiki.com/wiki/Apple_Encrypted_Archive">Apple Encrypted Archive</a></li>
  <li>blacktop/ipsw: <a href="https://blacktop.github.io/ipsw/">documentation</a> and <a href="https://deepwiki.com/blacktop/ipsw">DeepWiki</a></li>
  <li>The Eclectic Light Company: <a href="https://eclecticlight.co/2022/11/16/cryptex-how-a-custom-iphone-is-changing-macos-updates/">cryptexes</a></li>
  <li>The Apple Wiki: <a href="https://theapplewiki.com/wiki/Dev:Dyld_shared_cache">dyld shared cache</a></li>
  <li>sgan81/apfs-fuse: <a href="https://github.com/sgan81/apfs-fuse/issues/168">LZBITMAP compression</a></li>
  <li>Wikipedia: <a href="https://en.wikipedia.org/wiki/IPSW">IPSW</a></li>
  <li>EveryMac: <a href="https://everymac.com/systems/apple/iphone/specs/apple-iphone-16-pro-max-global-a3296-specs.html">iPhone 16 Pro Max (iPhone17,2)</a></li>
</ul>
