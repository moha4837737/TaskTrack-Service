# Technical Notes

## Biggest Docker problem
My tasks disappeared every time I removed and recreated the container, because SQLite stored its file inside the container's own filesystem. I solved it by saving the database in `/data` and mounting a named volume with `-v tasks-data:/data`. After that, the tasks survived `docker rm -f` and a new `docker run`.

A second issue: Docker image names must be lowercase. I used `tasktrack-api` for the image and container while the GitHub repository is `TaskTrack-Service`, so the README commands work as written.

## Most important Git/GitHub lesson
My first commit was recorded with a placeholder author name because I had not configured `user.name` yet. Since it was not pushed, I fixed it with `git commit --amend --reset-author`. Lesson: configure Git identity before the first commit, and use small commits with clear messages (`docker:`, `docs:`, `ci:`) so the history shows real progress.