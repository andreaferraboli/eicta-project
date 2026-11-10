# Web task 1: static promotional page

Static page for one festival instance of Euphoric Events (HTML + CSS + a small JavaScript file for DOM manipulation). No server, no build step, no dependency.

**Status: demonstrative.** Festival name, artists, prices and dates are fictional placeholders taken from the demo data. Replace them with the content the group chooses.

## Open it

Double-click `index.html`, or serve the folder (any static server), for example:

```
python -m http.server 8080 --directory delivery-3/web-static
```

## Structure (for the report)

| Part | Content | Styling notes |
|---|---|---|
| Header | brand, anchor navigation | sticky, blurred background, collapses into a menu button under 760px |
| Hero | name, dates, place, countdown, call to action | layered radial gradients, fluid font size with `clamp()` |
| Line-up | acts with day, genre, stage, time; genre filter | CSS grid `auto-fill`, chips toggled by `script.js` |
| Stages | two cards | gradient artwork instead of external images |
| Food & drinks | three stand cards | 3 columns, 1 column on mobile |
| Tickets | day pass / regular / VIP | featured card highlighted |

JavaScript: countdown to the start date, genre filter (`hidden` attribute), mobile menu toggle.

## Evidence to collect

Screenshots of the page in a browser (desktop and mobile width) in `delivery-3/report/figures/`.
