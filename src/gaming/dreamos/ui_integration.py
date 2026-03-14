"""DreamOS gamification UI integration."""

from __future__ import annotations

from flask import Blueprint, jsonify


gamification_bp = Blueprint("gamification", __name__, url_prefix="/api/gamification")


@gamification_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "service": "gamification"}), 200
