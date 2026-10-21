#!/usr/bin/env python3
"""Builds the static App Review Fixes site into ../app-review-fixes."""
import os, html, datetime

SITE = "https://app-review-fixes.netlify.app"
GUIDE = "https://morningreset4.gumroad.com/l/ship-your-app"
RESCUE = "https://morningreset4.gumroad.com/l/rejection-rescue"
RESCUE_LIVE = False  # flip to True once the Gumroad product exists
GOOGLE_VERIFY = None  # e.g. "google1234abcd.html" from Search Console
APPLE = "https://developer.apple.com/app-store/review/guidelines/"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "app-review-fixes")
TODAY = datetime.date.today().isoformat()

CSS = """
:root{--bg:#fbfaf7;--fg:#1d1d1f;--muted:#5f5f66;--line:#e4e1da;--accent:#0b63ce;--box:#f1efe9;--warn:#fff4d6}
@media (prefers-color-scheme:dark){:root{--bg:#141416;--fg:#ececef;--muted:#a3a3ad;--line:#2c2c31;--accent:#6aa8ff;--box:#1e1e22;--warn:#2d2715}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:17px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
main,header,footer{max-width:720px;margin:0 auto;padding:0 16px}
header{padding-top:20px;font-weight:600}header a{color:var(--fg);text-decoration:none}
h1{font-size:1.9rem;line-height:1.2;margin:28px 0 8px}h2{font-size:1.25rem;margin:32px 0 8px}
p.lede{color:var(--muted);margin-top:0}a{color:var(--accent)}
blockquote{margin:16px 0;padding:12px 16px;background:var(--warn);border-left:4px solid #d9a400;border-radius:6px}
ol li,ul li{margin:6px 0}code{background:var(--box);padding:1px 5px;border-radius:4px;font-size:.92em}
.cta{margin:36px 0;padding:18px 20px;background:var(--box);border:1px solid var(--line);border-radius:10px}
.cta strong{display:block;margin-bottom:4px}.btn{display:inline-block;margin-top:8px;padding:9px 16px;background:var(--accent);color:#fff;border-radius:8px;text-decoration:none;font-weight:600}
.cards a{display:block;padding:14px 16px;margin:10px 0;border:1px solid var(--line);border-radius:10px;text-decoration:none;color:var(--fg)}
.cards a span{display:block;color:var(--muted);font-size:.92rem}
footer{margin-top:48px;padding-bottom:32px;color:var(--muted);font-size:.85rem;border-top:1px solid var(--line);padding-top:16px}
"""

def page(slug, title, desc, body):
    canon = SITE + ("/" if slug == "" else f"/{slug}")
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">
<style>{CSS}</style></head>
<body><header><a href="/">App Review Fixes</a></header>
<main>{body}</main>
<footer>Written by Ryan, an indie iOS developer in Toronto, from his own App Review rejections. Not affiliated with Apple. Always check Apple's current <a href="{APPLE}">App Review Guidelines</a>. Updated {TODAY}.</footer>
</body></html>"""

CTA = f"""<div class="cta"><strong>Shipping a subscription app with Expo, EAS or RevenueCat?</strong>
I turned the fixes from my own 10 rejections into a pre-submit checklist plus 17 copy-paste AI prompts, so you can check everything before you submit.
<br><a class="btn" href="{GUIDE}">Get the guide</a></div>
"""
RESCUE_CTA = f"""<div class="cta"><strong>Already rejected and stuck?</strong>
Send me your rejection message. Within 2 business days you get the likely cause, the exact fix steps, an AI prompt to make the fix, and a reply to send Apple. No logins or code access needed. $49.
<br><a class="btn" href="{RESCUE}">Get my rejection reviewed</a></div>"""
if RESCUE_LIVE:
    CTA = CTA + RESCUE_CTA
_X = """"""

PAGES = []

PAGES.append(("guideline-2-1-b-in-app-purchase-rejection",
"Guideline 2.1(b) Rejection: In-App Purchases Not Submitted (How to Fix)",
"Rejected under App Store guideline 2.1(b) because your subscription or in-app purchase wasn't submitted or showed no plans? Here's why it happens and the exact fix steps.",
f"""<h1>Guideline 2.1(b): "in-app purchase products have not been submitted"</h1>
<p class="lede">This is the most common rejection for first-time subscription apps, and the fix is mostly in App Store Connect, not your code.</p>
<p>Apple's guideline 2.1(b) says in-app purchases must be "complete, up-to-date, visible to the reviewer and functional." Developers report rejection messages like these:</p>
<blockquote>One or more of the In-App Purchase products referenced in your app have not been submitted for review.<br><br>The subscription screen did not display any available plans for purchase.</blockquote>
<h2>Why it happens</h2>
<ul>
<li><strong>Your first subscription must ship with an app version.</strong> Apple reviews your first-ever in-app purchase only together with a binary. Submitting the build alone isn't enough.</li>
<li><strong>The product isn't "Ready to Submit."</strong> The "In-App Purchases and Subscriptions" section only appears on the version page once at least one product reaches that status.</li>
<li><strong>The link drops off after a rejection.</strong> After a rejection, check that your subscriptions are still attached to the version before you resubmit. I had to re-attach mine more than once.</li>
<li><strong>Agreements aren't active.</strong> Until the Paid Apps Agreement, tax and banking are active, products may not load, so the reviewer sees an empty paywall.</li>
</ul>
<h2>Fix, step by step</h2>
<ol>
<li>In App Store Connect, open each subscription and fill everything until it reads <code>Ready to Submit</code>: display name and description, price, availability, subscription group localization, the App Review screenshot of your paywall, and a review note.</li>
<li>Check Business → Agreements: the Paid Apps Agreement must be active.</li>
<li>Go to your app version page and refresh. In <em>In-App Purchases and Subscriptions</em>, click Edit and select every product.</li>
<li>If the build is stuck in review, remove it from review, upload a new build if needed, re-link the products, and submit everything together.</li>
<li>In the Resolution Center, write a short note, for example: "The subscriptions are now attached to this version and the Paid Apps Agreement is active."</li>
<li>Using RevenueCat? Confirm the product IDs in App Store Connect match your RevenueCat products and the offering your app loads.</li>
</ol>
<h2>If a product is stuck in "Rejected" or "Developer Action Needed"</h2>
<p>A rejected localization often can't be edited. Developers report it's sometimes faster to create a new product with a new product ID (deleted IDs can't be reused), update the ID in your code or RevenueCat, build again, and submit.</p>
{CTA}
<p><a href="/ipad-rejection-guideline-2-1-a">Also rejected on iPad? Read the iPad guide →</a></p>"""))

PAGES.append(("ipad-rejection-guideline-2-1-a",
"Rejected on iPad Under Guideline 2.1(a)? Why iPhone Apps Get Tested on iPad",
"App Review tested your iPhone app on an iPad and found a crash, a stuck screen or a failed purchase? Here's why it happens and what to check before you resubmit.",
f"""<h1>Rejected on iPad (2.1(a)) even though you built an iPhone app</h1>
<p class="lede">Reviewers often test on iPad. If your app gets stuck, crashes or can't complete a purchase on iPad, it's rejected.</p>
<p>Guideline 2.1(a) covers apps that "crash or exhibit obvious technical problems." Guideline 2.4.1 says iPhone apps should run on iPad whenever possible. Apple has told developers that "all apps designed for use on iPhone must still be formatted correctly and behave properly when running on iPad."</p>
<p>This happened to me. One of my rejections came from a reviewer on an iPad Air: the app got stuck on the welcome screen, and the same review flagged that the in-app purchase wasn't submitted.</p>
<h2>What to check before resubmitting</h2>
<ol>
<li><strong>Run the app on an iPad simulator or device</strong> with the latest iPadOS, from a fresh install. Go through onboarding, login and the paywall.</li>
<li><strong>Check your device setting.</strong> In Expo, <code>ios.supportsTablet</code> in your app config controls whether the app runs as a native iPad app. Whichever you choose, test the iPad experience. If you support iPad, App Store Connect will also ask for iPad screenshots.</li>
<li><strong>Test a sandbox purchase on iPad.</strong> Developers have reported purchase failures that only happen on iPad, for example a Flutter StoreKit 2 issue on iPadOS 27 (<a href="https://github.com/flutter/flutter/issues/194373">flutter#194373</a>).</li>
<li><strong>Look for layouts that assume a phone screen:</strong> fixed heights, buttons pushed off screen, and keyboard covering inputs.</li>
<li>In the Resolution Center, state the device and OS version you tested on and what you fixed.</li>
</ol>
{CTA}
<p><a href="/guideline-2-1-b-in-app-purchase-rejection">Also got 2.1(b) for your subscription? Fix it here →</a></p>"""))

PAGES.append(("subscription-paywall-rejection-guideline-3-1-2",
"Subscription Paywall Rejected (Guideline 3.1.2): Required Terms, Privacy and Price Info",
"Subscription app rejected under 3.1.2 or for missing Terms of Use? The checklist of what Apple requires on your paywall and in your App Store listing.",
f"""<h1>Subscription paywall rejected: what 3.1.2 requires</h1>
<p class="lede">Most paywall rejections come from a missing link or a price that isn't clear. Check these before you submit.</p>
<h2>On the paywall (in the app)</h2>
<ul>
<li>The subscription title, the length (for example, monthly or yearly), and the price per period.</li>
<li>The billed amount is the most prominent price on screen. A "per week" price can't be bigger than the real yearly charge.</li>
<li>Working links to your <strong>Terms of Use (EULA)</strong> and <strong>Privacy Policy</strong>.</li>
<li>A visible <strong>Restore Purchases</strong> button. Guideline 3.1.1 rejections often cite a missing restore option.</li>
</ul>
<h2>In App Store Connect</h2>
<ul>
<li>Privacy Policy URL filled in.</li>
<li>If you use Apple's standard EULA, add a Terms of Use link to your App Description. Apps without one get a template rejection.</li>
<li>Each subscription has an App Review screenshot of the paywall.</li>
</ul>
<h2>Value</h2>
<p>Guideline 3.1.2(a) says a subscription "must provide ongoing value to the customer." In your review notes, say briefly what subscribers get over time.</p>
{CTA}"""))

PAGES.append(("waiting-for-review-subscriptions",
"App Stuck in \"Waiting for Review\" With Subscriptions? What to Check and What Not to Do",
"New app with subscriptions stuck in Waiting for Review for days or weeks? What to check in App Store Connect, how to request an expedited review, and what not to do.",
f"""<h1>Stuck in "Waiting for Review" with a subscription app</h1>
<p class="lede">Lots of new subscription apps sit in "Waiting for Review" for a long time. Usually you can only wait, but some setup problems are worth ruling out first.</p>
<p>The Apple Developer Forums have many threads from developers with new apps stuck for one to several weeks, often after a first rejection and resubmission. Apple doesn't publish review times for each app, so nobody outside Apple can tell you exactly when yours will move.</p>
<h2>Check these first</h2>
<ol>
<li><strong>Agreements:</strong> under Business in App Store Connect, the Paid Apps Agreement, tax and banking should all be active. Reviewers can't test subscriptions without them.</li>
<li><strong>Subscriptions attached:</strong> on the version page, the subscriptions should be listed under "In-App Purchases and Subscriptions" and show as submitted with the version. A first subscription has to be reviewed together with an app version. See <a href="/guideline-2-1-b-in-app-purchase-rejection">the 2.1(b) guide</a>.</li>
<li><strong>Review notes and demo account:</strong> if your app has login, App Review Information needs a demo account that works and doesn't expire.</li>
<li><strong>Unanswered messages:</strong> check the App Review section and your email for a question from Apple that's waiting on you. An unanswered information request can hold things up.</li>
</ol>
<h2>Request an expedited review (if you have a real reason)</h2>
<p>Apple has a Contact App Review form where you can request an expedited review, for example for a critical bug fix or a time-sensitive launch. Give a short, specific reason. Developers on the forums report mixed results, and some say an accepted expedite still took days.</p>
<h2>What not to do</h2>
<ul>
<li>Don't keep removing the build and resubmitting just to "bump" it. Developers report it doesn't help and can make things worse.</li>
<li>Don't open several duplicate support requests. Send one clear message and follow up after a few days.</li>
</ul>
<p>When it does move, a common next step for subscription apps is a 2.1(b) or iPad issue. It's worth testing for those while you wait: <a href="/ipad-rejection-guideline-2-1-a">iPad testing checklist</a>.</p>
{CTA}"""))

PAGES.append(("ipad-screenshots-2-3",
"iPad Screenshot Sizes for App Store Connect (and Avoiding 2.3 Rejections)",
"Which iPad screenshot sizes App Store Connect requires (13-inch: 2064 x 2752 or 2048 x 2732), when iPad screenshots are required, and how to avoid guideline 2.3 metadata rejections.",
f"""<h1>iPad screenshots: required sizes and avoiding 2.3 rejections</h1>
<p class="lede">If your app runs on iPad, App Store Connect needs at least one 13-inch iPad screenshot. And they have to actually show iPad.</p>
<h2>Sizes Apple accepts (from Apple's screenshot specifications)</h2>
<ul>
<li><strong>iPad 13-inch, required if your app runs on iPad:</strong> 2064 x 2752 or 2048 x 2732 pixels (portrait), or the landscape versions 2752 x 2064 and 2732 x 2048.</li>
<li><strong>iPhone, required:</strong> at least one set for the "iPhone with Dynamic Island" sizes, for example 1179 x 2556 or 1206 x 2622 portrait. Larger sets like 1320 x 2868 are optional.</li>
<li>1 to 10 screenshots per size, in .png or .jpg/.jpeg, with no transparency.</li>
</ul>
<p>Check Apple's current <a href="https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications">screenshot specifications</a> before uploading, because sizes change with new devices.</p>
<h2>Does my Expo app "run on iPad"?</h2>
<p>If <code>ios.supportsTablet</code> is true in your Expo config, your app is a native iPad app and needs iPad screenshots. That's how mine ended up needing them. Either way, test it on an iPad, because reviewers often use one.</p>
<h2>Avoiding guideline 2.3 (accurate metadata)</h2>
<ul>
<li>Your iPad screenshots must show the app running on iPad. A stretched iPhone screenshot isn't enough.</li>
<li>Show real screens from the current build, not mockups of features that don't exist yet.</li>
<li>Keep text overlays honest: no prices or claims that don't match the app.</li>
</ul>
<h2>Quick way to capture them</h2>
<p>Run the app in the Xcode Simulator on an "iPad Pro 13-inch" device and press Cmd+S to save a screenshot. Check the pixel size before uploading.</p>
{CTA}"""))

def index():
    cards = "".join(f'<a href="/{s}">{html.escape(t)}<span>{html.escape(d)}</span></a>' for s, t, d, _ in PAGES)
    body = f"""<h1>App Store rejection fixes for subscription apps</h1>
<p class="lede">Plain-English fixes for the App Review rejections that block indie and AI-built apps, from a solo developer whose first app was rejected 10 times. The next update was rejected once, and the one after that was approved on the first try.</p>
<div class="cards">{cards}</div>{CTA}"""
    return page("", "App Store Rejection Fixes for Subscription Apps", "Step-by-step fixes for App Store rejections: 2.1(b) in-app purchases, iPad 2.1(a), 3.1.2 subscription paywalls. Written for Expo, React Native and AI-built apps.", body)

def main():
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, "index.html"), "w").write(index())
    for s, t, d, b in PAGES:
        open(os.path.join(OUT, f"{s}.html"), "w").write(page(s, t, d, b))
    urls = [SITE + "/"] + [f"{SITE}/{s}" for s, *_ in PAGES]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n"
    open(os.path.join(OUT, "sitemap.xml"), "w").write(sm)
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    open(os.path.join(OUT, "vercel.json"), "w").write('{\n  "cleanUrls": true,\n  "trailingSlash": false\n}\n')
    if GOOGLE_VERIFY:
        open(os.path.join(OUT, GOOGLE_VERIFY), "w").write(f"google-site-verification: {GOOGLE_VERIFY}")
    print("built", len(PAGES) + 1, "pages")

main()
