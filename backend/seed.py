"""
Seed MongoDB with sample data for local development.

Usage:
    cd backend && python seed.py

Reads connection settings from .env (same as the app).
Idempotent: skips posts that already exist by id.
"""
import asyncio
import random
from datetime import datetime, timedelta, timezone
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings
from apps.poster.models import PostModel, CommentModel

TEAMS = [
    "alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta",
    "iota", "kappa", "lambda", "mu", "nu", "xi", "omicron", "pi", "rho",
    "sigma", "tau", "upsilon",
]

BLURBS = [
    "Shipped {} to staging. QA starts Monday.",
    "Completed {} rollout. Monitoring dashboards look clean.",
    "Sprint planning done. {} is the focus this week.",
    "Hotfix for {} deployed to prod. Incident resolved.",
    "Code review for {} finished. Merging tomorrow.",
    "Load testing {} — results within SLA.",
    "Kicked off {} migration. ETA end of week.",
    "Rolled back {}. Root cause under investigation.",
    "Deployed {} to canary. Watching error rates.",
    "Closed out {} tickets. Moving to next milestone.",
    "{} refactor complete. Test coverage up to 87%.",
    "Blocked on {} dependency upgrade. Working with platform team.",
    "{} feature flagged off pending legal review.",
    "Demoed {} to stakeholders. Green light to proceed.",
    "Post-mortem for {} published. Action items assigned.",
]

FEATURES = [
    "onboarding flow", "auth service", "payment gateway", "search index",
    "notification pipeline", "data export", "reporting dashboard", "API v2",
    "cache layer", "webhook system", "audit log", "SSO integration",
    "rate limiter", "dark mode", "bulk import", "email templates",
    "mobile nav", "analytics pipeline", "access control", "billing module",
]

COMMENT_BLURBS = [
    "Two minor issues found, fixes in progress.",
    "All clear after 24h monitoring.",
    "Closing the incident.",
    "Follow-up PR raised for edge case.",
    "Metrics nominal. Signing off.",
    "One regression found — patch coming today.",
    "Stakeholder sign-off received.",
    "Escalating to on-call — latency spike detected.",
    "Back to green. Deploying fix now.",
    "No issues overnight. Marking complete.",
]


def make_posts() -> list[PostModel]:
    posts = []
    now = datetime.now(timezone.utc)
    for i in range(200):
        team = TEAMS[i % len(TEAMS)]
        suffix = i // len(TEAMS)
        post_id = f"team-{team}-{suffix}" if suffix > 0 else f"team-{team}"
        blurb = BLURBS[i % len(BLURBS)].format(FEATURES[i % len(FEATURES)])
        date = now - timedelta(hours=i * 3)
        posts.append(PostModel(id=post_id, blurb=blurb, date=date))
    return posts


def make_comments(posts: list[PostModel]) -> list[CommentModel]:
    comments = []
    for post in posts:
        blurb = random.choice(COMMENT_BLURBS)
        date = post.date + timedelta(hours=random.randint(1, 8))
        comments.append(CommentModel(id=post.id, blurb=blurb, date=date))
    return comments


async def seed():
    client = AsyncIOMotorClient(settings.DB_URL)
    db = client[settings.DB_NAME]

    posts = make_posts()
    comments = make_comments(posts)

    inserted_posts = 0
    for post in posts:
        if await db["posts"].find_one({"id": post.id}) is None:
            await db["posts"].insert_one(post.model_dump())
            inserted_posts += 1
            print(f"  inserted post: {post.id}")
        else:
            print(f"  skipped post (exists): {post.id}")

    inserted_comments = 0
    for comment in comments:
        await db["comments"].insert_one(comment.model_dump())
        inserted_comments += 1
        print(f"  inserted comment for: {comment.id}")

    print(f"\nDone. {inserted_posts} posts, {inserted_comments} comments inserted.")
    client.close()


if __name__ == "__main__":
    asyncio.run(seed())
