# European Tour illustrated strategy guide

Complete v3.3 edition: 41 chapters and 39 real game screenshots. Open dist/index.html locally, or unzip the portable package and open index.html. All assets are included; internet is unnecessary for the local book. Use the chapter search, reader checklists and screenshot enlargement. Print book prepares the complete guide for browser printing or Save as PDF.

Source text is drawn from WALKTHROUGH.md and the Council/expansion guides. scripts/build_strategy_guide.py regenerates chapter data. scripts/capture_strategy_guide.py and capture_strategy_guide_more.py capture earned battery saves on the released ROM; dist/images/provenance.json records those captures. Four battle/ending illustrations are copied from v3.3 evidence.

Content/asset and JavaScript functional checks passed with scripts/test_strategy_guide.cjs. Visual browser QA is unverified: the browser preview could not initialize on this host, and bundled headless Chromium was unavailable. The layout uses responsive and print styles, but has not been visually inspected in a running browser.

The user chose to keep this guide local. No source or screenshot payload has been synchronized or deployed to Sites. An unused private Site was registered earlier; its ID is retained in .openai/hosting.json, but publication is not pending or required.
