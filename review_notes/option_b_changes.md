# Changes before the option B live run (not editorial-policy revisions)

These changes respond to a human review question: "Did we stick to the topic I selected?" The v1 output
had drifted toward agents. They are a configuration correction and a collection fix. They are documented
separately from the policy revision (see `policy_v2_comparison.md`), because they change the *inputs*
rather than the editorial rules.

1. **Configuration correction (`config/project.json`):** the run-1 config did not match the approved
   brief. The question wording had been changed, and a fourth theme ("AI in the OS/browser") had been
   added. This restores the student's question ("…changing how people **work and live**…") and the three
   themes: personal context and devices, computer-use agents (now including OS-level assistants), and
   voice and conversational interfaces (the *2001* question). The run-1 version is archived in
   `config/policy_history/project_run1.json`. Policy §1 quotes the question, so its wording was aligned
   too; no rule changed.
2. **Collection fix (collectors and `config/sources.json`):**
   - **Cause:** collectors took the newest N items per source. That missed in-window items on glasses
     and voice, such as the Vergecast's "Meta and Snap battle for your face" (Sep 24), Google's
     "Guided Vision in Gemini Live" (Oct 1), and Simon Willison's "built using my voice" (Oct 9).
   - **Collector change:** the podcast and YouTube collectors now support `include_keywords` (episode or
     video title and description) and `scan_depth`, matching the RSS collector.
   - **Source changes:** three sources were added for the devices and accessibility gap: UploadVR,
     9to5Google, and the Meta Newsroom. Keywords were widened on Google, Road to VR, the Vergecast,
     Sam Witteveen, and Nate B Jones; Simon Willison's `max_items` went from 5 to 8.
   - Discovery filters only decide what is collected. Editorial relevance is still judged in
     `select_items.sh`.
3. **Side effect, expected:** the digest cache key includes the project brief, so all items are
   re-digested under the corrected themes. That costs about $2.
