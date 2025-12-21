#!/usr/bin/env python3
"""
Quote Generator for Twitch Chat
================================

Provides random quotes from FreeRideInvestor blog posts and other sources.
Can be triggered via !quote command in Twitch chat.

V2 Compliance: <400 lines, single responsibility
Author: Agent-7 (Web Development Specialist)
License: MIT
"""

import random
import logging
from typing import Optional

logger = logging.getLogger(__name__)


# Quotes from FreeRideInvestor blog posts
FREERIDEINVESTOR_QUOTES = [
    # Deployment & Infrastructure
    "Slow is smooth… smooth is fast.",
    "Infrastructure you built but don't use… isn't infrastructure. It's technical debt with a bow on it.",
    "That's the swarm effect. One agent's question unlocks another agent's execution.",
    "No more friction between idea and live.",
    "I'll do it quick' is how drift sneaks in. Those little tasks stack into hours.",
    "Infrastructure you don't use is just debt with a pretty label.",
    "30-second deploys instead of 5-minute sessions. No context switching.",
    "One command deploys. No more manual uploads.",
    "The infrastructure was there. Just… dormant. Sitting in the repo. Waiting.",
    "ROI: 16x faster. Zero errors. Full focus retained.",
    "Lower friction = more iterations. More iterations = faster improvement.",
    "This is what 'infrastructure as force multiplier' actually means.",
    "If I do it twice… I script it. If I script it… I trust it.",
    "I had the tool. Didn't use it. Agent asked one question… surfaced the whole capability.",
    "Real talk… how long was I uploading files one by one when I could've scripted this once?",
    "I've been clicking through WordPress admin like it's 2015.",
    "No more 'let me just quickly fix it.'",
    "That's energy I need for real work.",
    "Next deploy… automated. Next file change… one command. No more friction between idea and live.",
    "Faster improvement = better UX = more conversions.",

    # Trading & Mindset
    "We're not defined by past numbers but by how we move forward.",
    "Small, consistent actions win the race.",
    "This year is about turning lessons into action and strategies into results.",
    "Consistency over perfection. Small, consistent actions win the race.",
    "Every great trader has faced setbacks...it's part of the journey.",
    "This is the year of persistence, growth, and better decisions.",
    "Instead of focusing on yesterday's results, let's build the discipline and habits that drive long-term success.",
    "Fail early, fail often, but always fail forward.",

    # Building & Creation
    "You don't get stuck in ideas... you turn them into tangible outcomes with grounded action.",
    "You take pride in understanding and refining your craft, focusing on the journey rather than applause.",
    "When things get messy, you find clarity and growth through the chaos.",
    "You're not here to play; you're here to build.",
    "You thrive in the balance between structure and chaos, dreaming and doing.",
    "You map things out with precision, ensuring each step serves the bigger picture.",
    "Your persistence is quiet and deliberate. You don't seek to outshine others...you're here to prove something to yourself.",
    "You don't shy away from complexity... you thrive in it, finding clarity and growth through the chaos.",
    "Understanding your process isn't just self-indulgence...it's a way to refine how you tackle challenges.",
    "When the going gets tough, this mindset becomes your superpower.",
    "Your approach blends creativity with practicality, balancing vision and execution seamlessly.",
    "Persistence is your quiet strength, keeping you moving when others might falter.",

    # Life & Growth
    "Perfection is a polished lie. The world doesn't need us to be flawless... it needs us to be honest.",
    "A shattered mirror doesn't stop reflecting light. Instead, it catches it in unexpected ways.",
    "Every wrong turn, every stumble, is just another step closer to where we're meant to be.",
    "The journey isn't about the destination. It's about who we become along the way.",
    "Even when the darkness seems overwhelming, remember: the stars are always there. You just have to look up.",
    "Every struggle is a lesson, and every lesson brings us closer to who we're meant to be.",
    "The cracks are where the light gets in. And that light? It's you, shining brighter than you ever thought possible.",
    "Do you ever wonder why we hold onto our mistakes like they define us?",
    "Life isn't a straight path. It's a labyrinth, twisting and turning, looping back on itself.",
    "When you're standing in front of a wall too high to climb...don't ask yourself why you're not strong enough. Ask yourself what the wall is here to teach you.",
    "Sometimes, the most profound insights come in the quiet moments, when the world slows down, and you let your thoughts wander.",
    "This isn't just about what you create... it's about how you create.",
]


def get_random_quote() -> str:
    """
    Get a random quote from the collection.

    Returns:
        Random quote string
    """
    if not FREERIDEINVESTOR_QUOTES:
        return "No quotes available."

    return random.choice(FREERIDEINVESTOR_QUOTES)


def get_quote_by_index(index: int) -> Optional[str]:
    """
    Get a specific quote by index.

    Args:
        index: Quote index (0-based)

    Returns:
        Quote string or None if index out of range
    """
    if 0 <= index < len(FREERIDEINVESTOR_QUOTES):
        return FREERIDEINVESTOR_QUOTES[index]
    return None


def get_all_quotes() -> list[str]:
    """
    Get all available quotes.

    Returns:
        List of all quotes
    """
    return FREERIDEINVESTOR_QUOTES.copy()


def get_quote_count() -> int:
    """
    Get total number of quotes available.

    Returns:
        Number of quotes
    """
    return len(FREERIDEINVESTOR_QUOTES)


def format_quote_for_chat(quote: str, source: str = "FreeRideInvestor") -> str:
    """
    Format a quote for Twitch chat display.

    Args:
        quote: Quote text
        source: Source of the quote

    Returns:
        Formatted quote string for chat
    """
    return f'💬 "{quote}"... {source}'


__all__ = [
    "get_random_quote",
    "get_quote_by_index",
    "get_all_quotes",
    "get_quote_count",
    "format_quote_for_chat",
    "FREERIDEINVESTOR_QUOTES",
]

