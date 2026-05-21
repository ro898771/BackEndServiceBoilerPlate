"""
ReviewsAPIClient – class-based client with handshake protocol.

Handshake flow for every write operation (POST / PUT / PATCH / DELETE):
  1. Client sends POST /api/dinasour/handshake/
     Server responds { "status": "ready", "token": "<uuid>" }
  2. Only if handshake succeeds, client sends the actual write request
     with header  X-Handshake-Token: <token>
  3. Server validates the token → performs the operation → returns result

Read operations (GET) skip the handshake entirely.

Usage:
    Start server:
        uv run python manage.py runserver 0.0.0.0:8000

    Run this script:
        uv run python trial/test_api.py

    Or import in your own code:
        from trial.test_api import ReviewsAPIClient
        client = ReviewsAPIClient("http://192.168.1.x:8000")
        client.create(5, "Great!")
"""

import json
import requests


class ReviewsAPIClient:
    """Client for the Dinasour Reviews API with built-in handshake support."""

    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url.rstrip("/")
        self.handshake_url = f"{self.base_url}/api/dinasour/handshake/"
        self.endpoint = f"{self.base_url}/api/dinasour/reviews/"

    # ── Internal helpers ──────────────────────────────────────────────────

    def _print(self, label: str, response: requests.Response):
        print(f"\n{'─' * 55}")
        print(f"  {label}")
        print(f"  Status : {response.status_code}")
        try:
            body = json.dumps(response.json(), indent=4)
        except Exception:
            body = response.text or "(empty)"
        print(f"  Body   :\n{body}")
        print("─" * 55)

    def _review_url(self, review_id: int) -> str:
        return f"{self.endpoint}{review_id}/"

    def _handshake(self) -> str | None:
        """
        Phase 1 – request a one-time write token from the server.
        Returns the token string on success, or None if the handshake fails.
        """
        print("\n  [Handshake] Requesting write token...")
        try:
            response = requests.post(self.handshake_url)
        except requests.ConnectionError:
            print("  [Handshake] ERROR – Could not connect to server.")
            return None

        data = response.json()

        if response.status_code == 201 and data.get("status") == "ready":
            token = data["token"]
            print(f"  [Handshake] SUCCESS – Token received (expires in {data['expires_in_seconds']}s)")
            return token

        print(f"  [Handshake] FAILED – Server responded: {data}")
        return None

    def _write(self, method: str, url: str, label: str, payload: dict | None = None) -> dict | None:
        """
        Phase 2 – perform a write request only after a successful handshake.
        Returns the response JSON, or None if handshake or request failed.
        """
        token = self._handshake()
        if token is None:
            print(f"  [Aborted] {label} was NOT sent because handshake failed.")
            return None

        headers = {"X-Handshake-Token": token}
        response = getattr(requests, method)(url, json=payload, headers=headers)
        self._print(label, response)

        if response.status_code in (200, 201, 204):
            print(f"  [Transmit] SUCCESS – Data confirmed received by server.")
        else:
            print(f"  [Transmit] FAILED – Server rejected the request.")

        try:
            return response.json()
        except Exception:
            return {}

    # ── Public CRUD methods ───────────────────────────────────────────────

    def list(self) -> list:
        """GET /api/dinasour/reviews/ — list all reviews (no handshake needed)."""
        response = requests.get(self.endpoint)
        self._print("GET  – List All Reviews", response)
        return response.json()

    def get(self, review_id: int) -> dict:
        """GET /api/dinasour/reviews/<id>/ — retrieve one review (no handshake needed)."""
        response = requests.get(self._review_url(review_id))
        self._print(f"GET  – Get Review #{review_id}", response)
        return response.json()

    def create(self, rating: int, comment: str) -> dict | None:
        """
        POST /api/dinasour/reviews/
        Handshake → if ready → send create request with token.
        """
        return self._write(
            method="post",
            url=self.endpoint,
            label="POST – Create Review",
            payload={"rating": rating, "comment": comment},
        )

    def update(self, review_id: int, rating: int, comment: str) -> dict | None:
        """
        PUT /api/dinasour/reviews/<id>/
        Handshake → if ready → send full update with token.
        """
        return self._write(
            method="put",
            url=self._review_url(review_id),
            label=f"PUT  – Full Update Review #{review_id}",
            payload={"rating": rating, "comment": comment},
        )

    def partial_update(self, review_id: int, **fields) -> dict | None:
        """
        PATCH /api/dinasour/reviews/<id>/
        Handshake → if ready → send partial update with token.
        """
        return self._write(
            method="patch",
            url=self._review_url(review_id),
            label=f"PATCH – Partial Update Review #{review_id}",
            payload=fields,
        )

    def delete(self, review_id: int) -> bool:
        """
        DELETE /api/dinasour/reviews/<id>/
        Handshake → if ready → send delete with token.
        """
        result = self._write(
            method="delete",
            url=self._review_url(review_id),
            label=f"DELETE – Delete Review #{review_id}",
        )
        return result is not None

    def delete_all(self) -> dict | None:
        """
        DELETE /api/dinasour/reviews/delete-all/
        Handshake → if ready → wipe every row in the reviews table.
        """
        return self._write(
            method="delete",
            url=f"{self.endpoint}delete-all/",
            label="DELETE – Delete ALL Reviews",
        )


# ── Demo: full CRUD cycle with handshake ─────────────────────────────────

if __name__ == "__main__":
    # Change to your machine's IP for intranet testing:
    #   client = ReviewsAPIClient("http://192.168.1.50:8000")
    client = ReviewsAPIClient("http://127.0.0.1:8000")

    # print("\n" + "=" * 55)
    # print("   Dinasour Reviews API – Handshake CRUD Demo")
    # print("=" * 55)

    # # 1. Create two reviews (each does its own handshake first)
    review1 = client.create(rating=5, comment="Absolutely amazing experience!")
    # review2 = client.create(rating=2, comment="Could have been much better.")

    # # 2. List all (no handshake — safe read)
    # client.list()

    # # 3. Get one (no handshake — safe read)
    # if review1:
    #     client.get(review1["id"])

    # # 4. Full update (handshake → PUT)
    # if review1:
    #     client.update(review1["id"], rating=4, comment="Actually pretty good on second thought.")

    # # 5. Partial update – only rating (handshake → PATCH)
    # if review2:
    #     client.partial_update(review2["id"], rating=3)

    # # 6. Delete (handshake → DELETE)
    # if review2:
    #     client.delete(review2["id"])

    # # 7. Final list to confirm single deletion
    # client.list()

    # # 8. Delete ALL remaining reviews at once
    # client.delete_all()

    # # 9. Confirm table is empty
    # client.list()
