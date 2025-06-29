import subprocess
import os

def get_version():
    """Get the current version from git tags.
    
    Returns:
        str: Version string in format 'X.Y.Z' or 'dev' if no tags found
    """
    try:
        # Try to get the latest tag
        tag = subprocess.check_output(['git', 'describe', '--tags', '--abbrev=0'],
                                   stderr=subprocess.DEVNULL,
                                   universal_newlines=True).strip()
        return tag.lstrip('v')
    except subprocess.CalledProcessError:
        # If no tags found, return development version
        return 'dev'

def get_full_version():
    """Get the full version information including git commit hash.
    
    Returns:
        str: Full version string in format 'X.Y.Z-N-ghash' or 'dev-hash' if no tags found
    """
    try:
        # Try to get the full version description
        version = subprocess.check_output(['git', 'describe', '--tags', '--long'],
                                      stderr=subprocess.DEVNULL,
                                      universal_newlines=True).strip()
        return version.lstrip('v')
    except subprocess.CalledProcessError:
        try:
            # If no tags, return commit hash
            commit = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'],
                                         stderr=subprocess.DEVNULL,
                                         universal_newlines=True).strip()
            return f'dev-{commit}'
        except subprocess.CalledProcessError:
            return 'dev'

# Current version
VERSION = get_version()
FULL_VERSION = get_full_version() 