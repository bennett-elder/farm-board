from tests.conftest import LEGACY_KEY, POSTER_KEY, POSTER_ID
from config import settings


class TestAuth:
    async def test_no_key_returns_401(self, client):
        r = await client.post("/post/", json={"blurb": "hello"})
        assert r.status_code == 401

    async def test_invalid_key_returns_401(self, client):
        r = await client.post("/post/", headers={"x-api-key": "bad-key"}, json={"blurb": "hello"})
        assert r.status_code == 401

    async def test_valid_key_via_header(self, client):
        r = await client.post("/post/", headers={"x-api-key": POSTER_KEY}, json={"blurb": "hello"})
        assert r.status_code == 201

    async def test_valid_key_via_query_param(self, client):
        r = await client.post(f"/post/?api-key={LEGACY_KEY}", json={"id": "team-beta", "blurb": "hello"})
        assert r.status_code == 201


class TestPosterIdResolution:
    async def test_legacy_key_with_body_id(self, client):
        r = await client.post("/post/", headers={"x-api-key": LEGACY_KEY}, json={"id": "team-beta", "blurb": "hello"})
        assert r.status_code == 201
        assert r.json()["id"] == "team-beta"

    async def test_legacy_key_no_body_id_returns_400(self, client):
        r = await client.post("/post/", headers={"x-api-key": LEGACY_KEY}, json={"blurb": "hello"})
        assert r.status_code == 400

    async def test_legacy_key_strict_mode_returns_403(self, client, monkeypatch):
        monkeypatch.setattr(settings, "STRICT_API_KEYS", True)
        r = await client.post("/post/", headers={"x-api-key": LEGACY_KEY}, json={"id": "team-beta", "blurb": "hello"})
        assert r.status_code == 403

    async def test_poster_key_uses_key_poster_id(self, client):
        r = await client.post("/post/", headers={"x-api-key": POSTER_KEY}, json={"blurb": "hello"})
        assert r.status_code == 201
        assert r.json()["id"] == POSTER_ID

    async def test_poster_key_ignores_body_id(self, client):
        r = await client.post("/post/", headers={"x-api-key": POSTER_KEY}, json={"id": "wrong-id", "blurb": "hello"})
        assert r.status_code == 201
        assert r.json()["id"] == POSTER_ID

    async def test_poster_key_works_in_strict_mode(self, client, monkeypatch):
        monkeypatch.setattr(settings, "STRICT_API_KEYS", True)
        r = await client.post("/post/", headers={"x-api-key": POSTER_KEY}, json={"blurb": "hello"})
        assert r.status_code == 201
        assert r.json()["id"] == POSTER_ID


class TestPostBehavior:
    async def test_create_returns_expected_fields(self, client):
        r = await client.post("/post/", headers={"x-api-key": POSTER_KEY}, json={"blurb": "first post"})
        assert r.status_code == 201
        data = r.json()
        assert data["id"] == POSTER_ID
        assert data["blurb"] == "first post"
        assert isinstance(data["date"], int)
        assert data["date"] > 1_577_836_800_000  # after 2020-01-01 in ms

    async def test_second_post_updates_blurb(self, client):
        await client.post("/post/", headers={"x-api-key": POSTER_KEY}, json={"blurb": "first"})
        r = await client.post("/post/", headers={"x-api-key": POSTER_KEY}, json={"blurb": "updated"})
        assert r.status_code == 201
        assert r.json()["blurb"] == "updated"

    async def test_each_post_creates_a_comment(self, client, app):
        await client.post("/post/", headers={"x-api-key": POSTER_KEY}, json={"blurb": "first"})
        await client.post("/post/", headers={"x-api-key": POSTER_KEY}, json={"blurb": "second"})
        count = await app.mongodb["comments"].count_documents({"id": POSTER_ID})
        assert count == 2
