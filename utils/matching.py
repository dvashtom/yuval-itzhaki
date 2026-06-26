"""Matching algorithm for discovery feed."""

from database.db import get_discovery_profiles, get_profile_by_user_id


def get_discovery_feed(current_user_id):
    """Get profiles for discovery. Shows all available profiles."""
    current_profile = get_profile_by_user_id(current_user_id)
    if not current_profile:
        return []
    # For MVP, show all profiles (don't filter by gender preference too aggressively)
    # This ensures the user always sees profiles
    looking_for = current_profile.get('looking_for', 'Everyone')
    profiles = get_discovery_profiles(current_user_id, looking_for)
    # If no results with filter, try without filter
    if not profiles:
        profiles = get_discovery_profiles(current_user_id, None)
    return profiles
