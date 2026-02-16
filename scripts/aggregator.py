name: MAAS Daily OS Upgrade
on:
  schedule:
    - cron: '0 0 * * *' # Runs at midnight every day
  workflow_dispatch: # Allows you to run it manually for testing

jobs:
  upgrade_model:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-status: '3.9'
      - name: Run Aggregator
        run: python scripts/aggregator.py
      - name: Commit Updated Pulse
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add community_pulse.json
          git commit -m "Daily OS Upgrade: Community Pulse Updated"
          git push
