# Factory check and repair (2026-11-11)

KARI tonnestate/Kari release/kari-rc1 60935ed + ed4f5de (build import path) + b0bd918 (Schema.org Service description; 8 stale tests aligned with deliberate commits 29e7b2c, a975881, 429b3b8, repeat-visit). Unit 184/184, e2e 29/29, next build ok. Deployed to /var/www/kari/app (service not installed: systemd creation denied for Claude; deploy/install.sh <domain>).

Fruit-Hub tonnestate/fruit-grid fix/fruit-hub-gemini-final-grounding-20261106 7dcb39b + 601af16 (3 unclosed JSX, artifacts _id typing, consent type). Core 133/133, web 97/97, next build ok. Deployed to /var/www/fruit-hub/app; needs /etc/fruitstack/fruit-hub.env (MongoDB user for fruit_grid) and deploy/install.sh <domain>.

Not merged: KARI improve/kari-quality (5 commits, 76 behind RC; 16 conflicts incl. lib/db.mjs and legal texts).

## KARI quality integration
Local branch cc/kari-quality-integration de7cab3: e6fb028 hardening (as fe40a1e) and 14b4fd5 hashed tickets (as de7cab3) cherry-picked onto the RC, with the ticket migration extended to RC tables visit_stories/paid_visit_credits (absent tables skipped, new test). 77578ad not taken (superseded by the RC legal/report implementation; would add drafted legal texts). Unit 196/196, e2e 30/30, build ok. Deployed to /var/www/kari/app.
