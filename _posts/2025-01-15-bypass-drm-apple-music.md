---
layout: post
title: "Bypass DRM Decryption on streaming platforms: Apple Music case study"
date: 2025-01-15
tags: [Apple Music, DRM, Widevine]
excerpt: "High overview of how Apple Music's DRM protection works, from encrypted HLS segments through Widevine CDM license exchange to final (DRM free) playable audio. Exploring PSSH headers, content decryption modules, and the step-by-step process of transforming locked media into standard audio files. For research and study only."
---

## The problem (that is also the actual state of the art)

Apple Music doesn't give you a single MP3 file.

Instead:

- Audio is split into HLS segments (chunks, typically 10-second pieces)
- Each segment is encrypted with Widevine DRM (AES-128 encryption)
- You need a decryption key to unlock them

### What is HLS segments?

HLS (HTTP Live Streaming) breaks a continuous audio/video stream into many small files called **segments** (typically 2–10s each). The player downloads a playlist (an .m3u8 manifest) that lists segment URLs and switches between bitrates by picking different playlists. Segments can be MPEG-TS or fragmented MP4 (fMP4 / CMAF); each segment contains encoded audio/video frames for a short time slice and is independently addressable over HTTP(S). This chunking gives you adaptive bitrate switching, simple CDN caching, and easy recovery from packet loss.

- Segment = time-contiguous container of compressed frames + timestamps.
- Manifest (.m3u8) maps timeline → segment URLs; player requests segments with normal HTTP GETs.
- fMP4/CMAF segments are preferred now because they unify with DASH and simplify encryption (common boxes like moof/mdat).

### Widevine DRM encryption?

Widevine is a pretty cool Google's DRM stack for protecting premium media. At a high level it's a **system** composed of an encrypted media file (or also called as encrypted HLS/DASH segments), a client-side **CDM (Content Decryption Module)** embedded in the OS/browser running chromium engines for example, and a **license server** that issues decryption keys and policy (it's called playback rights).

The protected stream is usually encrypted with standard block ciphers (an algorithm that transforms plaintext into ciphertext, with AES) under keys identified by a Key ID (KID); the player sends a license request (including a PSSH) to the license server, the server responds with a license (key material + policy), and the CDM (often in a TEE or hardware-backed OEM module) performs the actual decryption and enforces policy.

- **CDM / OEMCrypto**: proprietary binary that performs crypto inside a protected environment so keys never land in app memory.
- **CENC / PSSH / KID**: Common Encryption metadata (CENC) carries the KID and PSSH payload so any conformant DRM can find/ask for the right key.
- **Security levels**: Widevine supports security levels (L1 / L2 / L3) where L1 uses full hardware/TEE protection and L3 is software-based with weaker guarantees.

### How do you decrypt songs?

Important: Apple Music uses Apple's **FairPlay** DRM for playback within Apple's ecosystem (not Widevine). The safe, correct flow for a licensed user is the following:

1. **Client requests content** (stream or download) and receives an HLS manifest pointing at encrypted segments (fMP4/CMAF or CBCS blocks).
2. **Player asks the Playback/License server**: the app (authenticated with your subscription token) requests a license for the content. That request includes identifiers (content KID / playback context).
3. **License server returns license**: the server issues a license blob (key material + policy), encrypted for the device. Apple's FairPlay server ties that license to Apple's hardware/secure APIs so the key can't be extracted.
4. **CDM / Secure Enclave decrypts**: the platform's CDM (or secure media pipeline / Secure Enclave on Apple devices) receives the license and performs decryption inside the trusted environment. Decrypted audio frames are handed to the secure audio path or media pipeline for playback — the application process never gets raw persistent keys.
5. **Offline playback**: downloaded files remain encrypted on disk; the license may contain a persistent key bound to the device so the app can decrypt offline but only under the same entitlement and on the same device ecosystem.

Crucial security guarantees (why you can't just copy & decrypt): keys are delivered only after authenticated entitlement checks, keys are consumed inside a hardware/OS-protected CDM (TEE / Secure Enclave / OEMCrypto), and the decrypted path is protected so apps/processes can't simply capture raw PCM reliably.

#### So grosso-modo here's the breakdown:

**Apple Music decryption** = So you start from a FairPlay license exchange + device-bound keys + secure playback inside what we can call the "Apple's protected media pipeline"; as a subscriber you get keys only through authenticated licenses and playback happens inside a CDM/TEE — and you don't get raw keys or unprotected files at all.

#### Why Widevine and not FairPlay?

While Apple Music officially uses FairPlay DRM for its native apps (macOS Music app, iOS), this tool targets the **web browser API** which uses Widevine DRM instead. When accessing Apple Music via web browsers (Chrome, Firefox, Edge), Apple serves Widevine-encrypted streams for cross-platform compatibility since FairPlay only works in Apple's ecosystem.

The key difference: FairPlay uses device-bound keys + Secure Enclave/TEE where decryption happens inside Apple's protected media pipeline with no access to raw keys. Widevine, however, follows a standard CDM protocol that can be implemented via `pywidevine`, making it accessible for this tool. By authenticating as a web browser (via cookies and user-agent), the tool receives Widevine-protected HLS streams instead of FairPlay ones, allowing extraction of decryption keys through the Widevine license exchange protocol.

## How to step-by-step make a DRM removal process

### Step 1: Get the PSSH (Protection System Specific Header)

When you fetch song metadata, the HLS item (playlist, song, video) contains a special header python speaking, by defining the **m3u8** **object** according to Glomatico's project analysis:

```python
# interface_song.py:get_stream_info_legacy (line 387-388)
m3u8_obj = m3u8.loads(await get_response_text(stream_url))
stream_info.widevine_pssh = m3u8_obj.keys[0].uri
```

```python
# Example PSSH from playlist:
EXT-X-KEY:METHOD=SAMPLE-AES,URI="data:text/plain;base64,AAAANHBzc2gAAAAA...",KEYFORMAT="urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed"
```

This **base64** string contains:

1. Key ID (KID): Identifies which key you need
2. Algorithm: How it's encrypted (AES-128, AES-CTR, etc.)

### Step 2: CDM (Content Decryption Module) License Exchange

Now comes the Widevine handshake:

```python
# interface_song.py:get_decryption_key_legacy (line 407-433)
async def get_decryption_key_legacy(stream_info, cdm):
    # Open a CDM session
    cdm_session = cdm.open()
    
    # Parse the PSSH to extract key ID
    widevine_pssh_data = WidevinePsshData()
    widevine_pssh_data.algorithm = 1  # AES-CTR
    widevine_pssh_data.key_ids.append(
        base64.b64decode(stream_info.widevine_pssh.split(",")[1])
    )
    pssh_obj = PSSH(widevine_pssh_data.SerializeToString())
    
    # Generate a license challenge (encrypted request)
    challenge = base64.b64encode(
        cdm.get_license_challenge(cdm_session, pssh_obj)
    ).decode()
    
    # Send challenge to Apple's license server
    license_response = await apple_music_api.get_license_exchange(
        song_id,
        widevine_pssh,
        challenge,
    )
    # Apple verifies you have subscription via cookies file!
    
    # Parse the license response (contains the key!)
    cdm.parse_license(cdm_session, license_response["license"])
    
    # Extract the content decryption key
    decryption_key = next(
        i for i in cdm.get_keys(cdm_session) if i.type == "CONTENT"
    )
    
    return decryption_key.key.hex()  # The actual AES key!
```

So we open a CDM session to initialize a secure context for key exchange and license parsing: `cdm_session = cdm.open()`

Next, parse the PSSH to extract the Key ID(s) this defines which content keys the license must deliver. The PSSH is serialized into a proper Widevine object: (WidevinePsshData, PSSH()).

Generate a license challenge from the CDM using this last PSSH. This challenge encapsulates device identity and session data, encrypted by the CDM.

Send this challenge to the license server. The server validates entitlement and returns a **signed license blob** bound to your session and of course, your device.

Parse the returned license in the CDM as it installs the content decryption key internally.

Finally, extract the active content key from the CDM (`cdm.get_keys`) for decryption, or use the CDM handle to decrypt segments directly. Cool tho?

**You open a secure CDM session, send it the PSSH so it knows which key to ask for, then generate a license challenge that's verified by the server — once approved, the CDM gets the decryption key and can unlock the encrypted song segments for playback.**

**_It's like borrowing a movie from a digital library:_**

**Your player (CDM) shows its ID card and asks the library (license server) for the key to open the movie box (encrypted song).**

**If your subscription is valid, the library gives a unique key that only your player can use — it opens the box, watches the movie, but never keeps or reveals the key. It's actually more easy to get the idea like this.**

---

#### Why Apple gives you the key:

- Your cookies prove you have an active Apple Music subscription
- The media-user-token cookie authenticates you
- Apple's server checks: "Is this user allowed to stream this song?"
- If yes → our dear server returns encrypted license containing the AES decryption key

---

### Step 3: Download Encrypted HLS Segments

Now we have two important items at this stage.

The first one is the **stream URL**, also called the **HLS playlist**.

The second is the **decryption key** in hexadecimal form (an AES-128 key).

Don't get confused — a _playlist_ here isn't a list of songs. It's more like a **table of contents** for an encrypted track: it doesn't contain the audio itself, only the list of locked fragments and the instructions on how to reassemble them in the correct order.

From an engineering standpoint, the .m3u8 file is an **HLS manifest**, a small text file that lists URLs for all the media segments (.m4s, .ts, etc.) that make up the stream. It defines playback order, segment duration, and sometimes the encryption key location or codec information. It's basically the **map** the player (or yt-dlp) uses to fetch and reconstruct the actual data.

The action here is to make a download stream in the python tool with proper execution using a path for the encrypted stream (chunks by the way):

```python
# downloader_song.py:download (line 274-283)
encrypted_path = "/tmp/gamdl_abc123/song_encrypted.m4a"
await download_stream(stream_url, encrypted_path)
```

```python
# downloader_base.py:_download_ytdlp (line 293-306)
with YoutubeDL({
    "quiet": True,
    "outtmpl": encrypted_path,
    "allow_unplayable_formats": True,  # Keep encrypted segments!
    "fixup": "never",  # Don't try to fix/decrypt
}) as ydl:
    ydl.download(stream_url)
```

Well ok but YoutubeDL it's out of context? No, It's a **generic media extraction framework** that supports **hundreds of streaming platforms**, not just "YouTube". It parses each site's player page, extracts the streaming manifest (like HLS/DASH URLs), and can download raw media segments or merge them into playable files.

In this snippet, it's being used in a low-level way to fetch **encrypted HLS segments** without trying to decrypt them (`allow_unplayable_formats=True`, `fixup="never"`), meaning it's acting as a **segment fetcher**, not a player, don't get confused!

yt-dlp retrieves the HLS **.m3u8 manifest**, enumerates each segment URL, downloads all encrypted chunks (typically .m4s fragments) — often in parallel (async) — and concatenates them sequentially into a single container file like **foo_song_encrypted.m4a**, preserving the original encryption for later decryption by the CDM.

**It's like collecting all the locked pieces of a music CD one by one, putting them back in order into a single disc, but the music is still locked until your player later uses the proper key to unlock it, no worries we're on that way.**

**Our stage right now is the following: in our encrypted path we got a brand fresh and clean (almost) single .m4a file with encrypted audio data.**

### Step 4: Decrypt the audio

Now the crucial part! Two paths depending on codec* you guys are choosing:

_**\*codec** (short for coder–decoder) is the algorithm that compresses and decompresses audio or video data._

- Path A: Legacy codecs (AAC-256, AAC-HE) -> FFmpeg direct decryption (we go further with this)
- Path B: Experimental codecs (ALAC, Atmos) -> mp4decrypt

#### Using FFmpeg (path A)

```python
# downloader_song.py:remux_ffmpeg (line 158-186)
await remux_ffmpeg(
    encrypted_path,
    staged_path,
    decryption_key="a1b2c3d4e5f6..."  # The hex key from CDM
)

# Internally runs:
ffmpeg -loglevel error -y \
    -decryption_key a1b2c3d4e5f6... \  # ← FFmpeg decrypts on-the-fly!
    -i /tmp/song_encrypted.m4a \
    -c copy \                            # Copy streams (no re-encoding)
    -movflags +faststart \               # Optimize for streaming
    /tmp/song_staged.m4a
```

What FFmpeg does here:

1. Reads encrypted .m4a file
2. Decrypts audio stream using the AES key previously collected (built-in AES-128 decryption)
3. Copies decrypted audio to new container (but no re-encoding!)
4. Adds faststart flag (moves metadata to front for allowing you to do web playback)

#### Using more modern codecs

```python
# downloader_song.py:decrypt_mp4decrypt (line 188-215)
await decrypt_mp4decrypt(
    encrypted_path,
    decrypted_path,
    decryption_key,
    legacy=False
)

# Internally runs:
mp4decrypt \
    --key 00000000000000000000000000000001:a1b2c3d4... \
    --key 00000000000000000000000000000000:b2c3d4e5... \
    /tmp/song_encrypted.m4a \
    /tmp/song_decrypted.m4a
```

#### Why two damn keys in there?

Theses experimental codecs usually have multiple encryption tracks like below:

- Key ID 00...01 = main audio track
- Key ID 00...00 = default/fallback key

**And then you have to do the remux process again with FFmpeg:**

```python
await remux_ffmpeg(decrypted_path, staged_path)
# Now FFmpeg just repackages (no decryption needed, you just did in the step before)
```

It's important here to understand **what remuxing does**, you are doing it everytime without knowing it on whatever kind of media formats you can consume everyday and it's kind of black magic still at this stage.

**"Remuxing" = Re-multiplex = Repackage streams into a clean container (forget Docker here please...).**

Because your raw received file is just a garbage of junk metadato from a DRM system, the atom structure is messy here. **MP4 atoms = chunks of data it's not physics here...** You also need the faststart flag (a metadata that is at the end of the file).

```
Before remux:
[Encrypted atoms][Audio stream][DRM atoms][Metadata at end]

After remux:
[Metadata at start][Clean audio stream][EOF]
     ↑
   faststart: Metadata first = instant playback, Mickael Jackson is happy (RIP)
```

And no re-encoding! The audio data itself is just copied byte-for-byte. Only the container structure changes.

### Step 5: Apply metadata tags

Metadata matters on a fresh clean decrypted audio file. It allows you to have the artist name, credits, song cover, order in a EP/album and more.

```python
# downloader_base.py:apply_tags (line 330-356)
mp4 = MP4(staged_path)  # Open with mutagen library
mp4.clear()             # Remove all existing tags

# Add text metadata
mp4["©nam"] = [tags.title]           # ©nam = Title
mp4["©ART"] = [tags.artist]          # ©ART = Artist
mp4["©alb"] = [tags.album]           # ©alb = Album
mp4["trkn"] = [(tags.track, tags.track_total)]  # Track 1/12

# Embed cover art
cover_bytes = await get_cover_bytes(cover_url)
mp4["covr"] = [MP4Cover(cover_bytes, imageformat=MP4Cover.FORMAT_JPEG)]

mp4.save()  # Write back to file
```

Then, fully tagged, DRM-free .m4a file is ready!

### Here's my key takeaways

1. Key source: NOT from cookies! From Widevine license server after proving subscription
2. Encryption: AES-128 encryption on each HLS segment
3. Decryption: FFmpeg (legacy) or mp4decrypt (experimental) removes DRM
4. Remuxing: Repackages into clean MP4 container, no re-encoding
5. Result: Standard .m4a file that works anywhere, DRM-free

The cookies are only used to authenticate with Apple's license server. The actual decryption key is dynamically generated per-song and delivered via the Widevine CDM protocol.

## Conclusion

The workflow above reveals something crucial about modern streaming. The only real barrier between a legal playback and a fully usable local file is the key. Once your device obtains that key, DRM becomes just a thin cryptographic wrapper. A 10-second encrypted segment and a standard .m4a file are separated by a single decision: does the user get access to the key or not.

When the pipeline runs inside Apple's Secure Enclave with FairPlay, that separation is enforced through hardware and strict policy. As soon as the same content falls back to browser-based Widevine L3 for cross-platform compatibility, those walls weaken. The exact same design that enables offline playback, switching devices, and smooth user experience also unintentionally enables extraction: keys can be obtained, segments decrypted, containers remuxed.

This is the real paradox of streaming DRM.  
To let you listen, the system must give you the key.  
Once you have the key, you technically have the file.

My goal here is not to promote piracy. Understanding how DRM works is not an invitation to steal music. It is a way to see how fragile our digital "ownership" truly is. I write this kind of breakdown because I enjoy diving deep into the technologies that shape our everyday media. I like to explore, question, and sometimes dismantle the systems in front of us so I can rebuild my own understanding.

If this article sparked your curiosity or taught you something new, I am glad. Feel free to reach out. These explorations keep me sharp as an engineer and inspire me to improve the tools and ideas we rely on.

Special thanks to **Glomatico** for the incredible work on [gamdl (Glomatico's Apple Music Downloader)](https://github.com/glomatico/gamdl). It is a great example of how curiosity and technical skill can reveal the inner workings of complex systems.
