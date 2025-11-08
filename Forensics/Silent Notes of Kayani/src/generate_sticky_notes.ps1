# create_30_stickies.ps1
# Minimal, robust script to create 30 Sticky Notes (note #16 contains Base32 flag)
# Run with: powershell -ExecutionPolicy Bypass -File .\create_30_stickies.ps1

Add-Type -AssemblyName System.Windows.Forms

# Base32-encoded flag (RFC4648) for: c0ngr4ts_y0u_f0und_my-n0t3s
$flagBase32 = "MMYG4Z3SGR2HGX3ZGB2V6ZRQOVXGIX3NPFPW4MDUGNZQ===="

# 30 multi-line English notes (each >= 4 lines). Customize text if you want.
$notes = @(
@"
Meeting notes - Project A
Discuss milestones for sprint two.
Assign tasks to team leads by Friday.
Review risks and dependencies.
"@,
@"
Shopping list and errands
Buy printer paper, pens, and staples.
Pick up groceries Friday evening.
Call to schedule appliance repair.
"@,
@"
Ideas for blog posts
1) How we optimized CI pipelines.
2) Troubleshooting memory leaks.
3) Case study: caching improvements.
"@,
@"
Daily goals
Finish report draft.
Send metrics to the analytics team.
Prepare slides for Monday.
Reflect and plan tomorrow.
"@,
@"
Onboarding checklist
Create accounts for new hires.
Share project guidelines and repos.
Schedule introductory walkthrough.
Collect access approvals.
"@,
@"
Personal reminders
Renew car insurance next month.
Book dentist appointment.
Backup photos and documents.
Plan a weekend getaway.
"@,
@"
Server maintenance notes
Patch schedule: Saturday 02:00.
Notify users of planned downtime.
Verify backups post-patch.
Document any post-update issues.
"@,
@"
Research notes
Read the 2024 caching paper.
Summarize key takeaways in a paragraph.
List experiments to reproduce results.
Share findings at team meeting.
"@,
@"
Customer feedback summary
Collect recent tickets and comments.
Prioritize recurring complaints.
Draft response templates for support.
Escalate product issues where needed.
"@,
@"
Quick reference
SSH to staging: ssh dev@staging.example.com
DB read-only: use replica endpoint.
Keep credentials in vault.
"@,
@"
Sprint retrospective notes
What went well: faster builds.
What to improve: flaky tests.
Action items: stabilize test suite.
Follow up in two weeks.
"@,
@"
Training ideas
Hands-on workshop: secure coding basics.
Pair programming rotations for juniors.
Weekly lightning talks on tooling.
Collect volunteer presenters.
"@,
@"
Expense notes
Submit receipts by end of month.
Tag costs to correct cost centers.
Verify travel reimbursements.
Keep soft copies of receipts.
"@,
@"
Marketing tasks
Prepare copy for landing page.
Coordinate launch tweet thread.
Schedule newsletter for next Tuesday.
Measure sign-ups after campaign.
"@,
@"
QA checklist
Reproduce bug on latest build.
Capture steps and screenshots.
Assign bug to owner with priority.
Verify fix on staging before release.
"@,
@"
Secret memo - read carefully
We keep small logs of support inquiries here.
Some lines look like codes but are not secrets.
If needed, contact the operations lead.
$flagBase32
"@,
@"
Architecture sketch notes
Consider event-driven processing.
Evaluate message queue backpressure.
Document tradeoffs for consistency vs latency.
Diagram in the shared drive.
"@,
@"
Deployment notes
Blue/green deploy recommended.
Health checks must return 200.
Rollback plan ready in case of failure.
Notify channel on completion.
"@,
@"
Conference ideas
Submit CFP for developer conference.
Prepare a 20-minute talk about observability.
Gather demo assets and slides.
Seek co-speaker to cover case studies.
"@,
@"
Compliance reminders
Rotate keys quarterly.
Complete required training modules.
Confirm audit evidence is stored properly.
Escalate missing items.
"@,
@"
Team goals
Improve code review turnaround.
Increase test coverage by 10%.
Automate repetitive tasks where possible.
Celebrate small wins weekly.
"@,
@"
User research snippets
Interview findings: onboarding confusion.
Hypothesis: simplify first-time flow.
Next step: prototype simplified UI.
Test with five users.
"@,
@"
Backup notes
Full backup runs nightly at 01:00.
Store offsite copies monthly.
Test restore process quarterly.
Document any failures.
"@,
@"
Design tasks
Finalize icon set for app.
Ensure accessibility contrast ratios.
Create component library documentation.
Publish to designers' repo.
"@,
@"
Legal reminders
Review third-party license updates.
Confirm data retention policies.
Coordinate with legal for new contracts.
Log signed agreements centrally.
"@,
@"
Performance notes
Identify slow endpoints with APM.
Cache heavy read queries intelligently.
Measure tail latencies and optimize.
Schedule profiling session.
"@,
@"
Customer onboarding
Prepare step-by-step setup guide.
Create checklist for success manager.
Collect customer goals and KPIs.
Set up follow-up calls.
"@,
@"
Release notes template
Summary: What changed and why.
Breaking changes: list and mitigation.
Upgrade steps: pre/post actions.
Contact: team for support.
"@,
@"
Personal project log
Work on side project evenings.
Track progress in short bullet points.
Set small weekly milestones.
Keep code in feature branches.
"@
)

# Ensure we have exactly 30 entries
if ($notes.Count -lt 30) {
    while ($notes.Count -lt 30) { $notes += "Placeholder note.`nLine two.`nLine three.`nLine four." }
} elseif ($notes.Count -gt 30) {
    $notes = $notes[0..29]
}

# Place the flag into note #16 (index 15). Overwrite that entry with a 4+ line English note including the flag.
$notes[15] = @"
Hidden memo - internal
Please review the note below carefully.
This line contains an encoded identifier that looks like a token.
Encoded snippet: $flagBase32
"@

# Launch Sticky Notes app (opens the app)
Start-Process "explorer.exe" "shell:AppsFolder\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe!App"
Start-Sleep -Seconds 4

# Create notes: Ctrl+N then paste clipboard (Set-Clipboard & Ctrl+V). Small sleeps for reliability.
for ($i = 0; $i -lt 30; $i++) {
    # New note
    [System.Windows.Forms.SendKeys]::SendWait('^n')
    Start-Sleep -Milliseconds 400

    # Put current note text to clipboard and paste
    Set-Clipboard -Value $notes[$i]
    Start-Sleep -Milliseconds 120
    [System.Windows.Forms.SendKeys]::SendWait('^v')
    Start-Sleep -Milliseconds 300

    # Give an extra newline so content appears stable, then small pause
    [System.Windows.Forms.SendKeys]::SendWait('{ENTER}')
    Start-Sleep -Milliseconds 350
}

Write-Host "`n✅ Done: 30 Sticky Notes created. Note #16 contains the Base32 flag."
Write-Host "Open Sticky Notes to verify. The data is saved automatically to plum.sqlite (LocalState)."
