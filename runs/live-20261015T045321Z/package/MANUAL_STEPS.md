# Manual steps remaining for run live-20261015T045321Z

Preparing this package does not mean anything has been rendered or published.

1. **Google Vids (one video per piece):** open `video_scripts/NN.md`. Paste it into a Google Doc and use
   Vids "docs to video" (or paste it into Vids' script panel). Keep each scene's on-screen source line
   visible and use an AI voiceover. Target 3-5 minutes. Export or publish to YouTube.
2. **YouTube:** upload as public or unlisted. Use the brief title. Paste `youtube/NN_description.txt` as
   the description, replacing {ARTICLE_URL} once the article is live. Mark AI-generated presentation
   where YouTube asks.
3. **Substack:** create a free (not paywalled) post from `articles/NN.md`. Paste the rendered Markdown
   and check that the links survive. Replace {YOUTUBE_URL} with the video link.
4. **Links:** record both URLs in `publication_links.json` and rerun `bash run.sh --package runs/live-20261015T045321Z`.
   Existing links are preserved, and placeholders in the package files are filled in.
5. Verify each link opens in a private browser window.
