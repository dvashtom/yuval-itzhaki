"""Matching algorithm for discovery feed."""

from database.db import get_discovery_profiles, get_profile_by_user_id


def get_discovery_feed(current_user_id):
    current_profile = get_profile_by_user_id(current_user_id)
    if not current_profile:
        return []
    gender_filter = current_profile.get('looking_for', 'Everyone')
    profiles = get_discovery_profiles(current_user_id, gender_filter)
    return profiles
