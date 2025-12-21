#!/usr/bin/env python3
"""
PaperKit Version Manager
Manages version information from .paperkit/_cfg/version.yaml
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Any, Dict

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install 'pyyaml>=5.4'", file=sys.stderr)
    sys.exit(1)


class VersionManager:
    """Manages PaperKit version state stored in .paperkit/_cfg/version.yaml."""
    
    def __init__(self, config_path=None):
        """Initialize the version manager"""
        if config_path is None:
            # Find the .paperkit directory
            script_dir = Path(__file__).parent
            paperkit_root = script_dir.parent.parent
            config_path = paperkit_root / ".paperkit" / "_cfg" / "version.yaml"
        
        self.config_path = Path(config_path)
        self.version_data: Dict[str, Any] = {'version': {}}
        
        if self.config_path.exists():
            self.load()
    
    def load(self):
        """Load version data from YAML file"""
        try:
            with open(self.config_path, 'r') as f:
                loaded = yaml.safe_load(f)
                self.version_data = loaded if isinstance(loaded, dict) else {'version': {}}
        except Exception as e:
            print(f"Error loading version config: {e}", file=sys.stderr)
            sys.exit(1)

        if not isinstance(self.version_data, dict):
            print("Error: version.yaml must be a mapping", file=sys.stderr)
            sys.exit(1)

        if 'version' not in self.version_data or not isinstance(self.version_data['version'], dict):
            print("Error: version.yaml missing required 'version' mapping", file=sys.stderr)
            sys.exit(1)
    
    def save(self):
        """Save version data to YAML file"""
        try:
            with open(self.config_path, 'w') as f:
                # Note: sort_keys=False relies on Python 3.7+ dict insertion ordering.
                # This is acceptable because the project's minPythonVersion is 3.7.
                yaml.dump(self.version_data, f, default_flow_style=False, sort_keys=False)
        except Exception as e:
            print(f"Error saving version config: {e}", file=sys.stderr)
            sys.exit(1)
    
    def _compute_current_from_semver(self):
        """Return derived version string from semver block, honoring prerelease and build."""
        version = self.version_data.get('version', {})
        semver = version.get('semver', {})
        if not all(k in semver for k in ('major', 'minor', 'patch')):
            return None

        prerelease = semver.get('prerelease') or ""
        build = semver.get('build') or ""

        base = f"{semver['major']}.{semver['minor']}.{semver['patch']}"
        current = f"{prerelease}-{base}" if prerelease else base
        if build:
            current = f"{current}+{build}"
        return current

    def get_version(self):
        """Return current version; derive from semver if explicit current is absent."""
        version = self.version_data.get('version', {})
        current = version.get('current')
        if current:
            return current
        computed = self._compute_current_from_semver()
        return computed if computed else "unknown"
    
    def get_full_info(self):
        """Return the full version mapping from the YAML payload."""
        if not self.version_data:
            return {}
        return self.version_data.get('version', {})
    
    def set_version(self, version_string, release_type=None, update_date=True):
        """
        Set a new version and rewrite YAML.

        Args:
            version_string: Accepts <semver> or <prerelease>-<semver>[+build]
            release_type: Optional explicit release type (alpha, beta, rc, stable)
            update_date: When true, stamp release and lastUpdated with today
        """
        version = self.version_data.setdefault('version', {})

        # Parse version string into semver + prerelease (+ optional build)
        prerelease = None
        build = None
        try:
            main_part, build_part = (version_string.split('+', 1) + [None])[:2]
            if build_part is not None:
                build = build_part

            parts = main_part.split('-')
            if len(parts) == 2:
                prerelease, semver = parts
            elif len(parts) == 1:
                semver = main_part
            else:
                raise ValueError(f"Invalid version format: {version_string}")

            semver_parts = semver.split('.')
            if len(semver_parts) != 3:
                raise ValueError(f"Invalid semantic version format: {semver}")

            major, minor, patch = semver_parts
            semver_block = version.setdefault('semver', {})
            semver_block['major'] = int(major)
            semver_block['minor'] = int(minor)
            semver_block['patch'] = int(patch)
            semver_block['prerelease'] = prerelease or ""
            semver_block['build'] = build or ""
        except (ValueError, IndexError) as e:
            print(
                f"Error: Failed to parse version '{version_string}': {e}.",
                file=sys.stderr,
            )
            sys.exit(1)

        # Derived current (generated, do not edit manually)
        computed = self._compute_current_from_semver()
        version['current'] = computed if computed else version_string

        # Release metadata
        release = version.setdefault('release', {})
        if release_type:
            release['type'] = release_type
        elif prerelease:
            release.setdefault('type', prerelease)
        else:
            release.setdefault('type', 'stable')

        if update_date:
            today = datetime.now().strftime("%Y-%m-%d")
            release['date'] = today
            version.setdefault('metadata', {})['lastUpdated'] = today

        self.save()
    
    def bump_version(self, part='patch'):
        """Increment semver component (major/minor/patch) and clear build metadata."""
        version = self.version_data.get('version', {})
        semver = version.get('semver', {})

        if not all(k in semver for k in ('major', 'minor', 'patch')):
            print("Error: semver block is missing required fields", file=sys.stderr)
            sys.exit(1)

        major = semver.get('major', 1)
        minor = semver.get('minor', 0)
        patch = semver.get('patch', 0)
        prerelease = semver.get('prerelease', '')
        # Build numbers are per-build metadata; reset on bump
        semver['build'] = ''

        if part == 'major':
            major += 1
            minor = 0
            patch = 0
        elif part == 'minor':
            minor += 1
            patch = 0
        elif part == 'patch':
            patch += 1
        else:
            print(f"Error: Invalid part '{part}'. Use 'major', 'minor', or 'patch'", file=sys.stderr)
            sys.exit(1)

        new_base = f"{major}.{minor}.{patch}"
        new_version = f"{prerelease}-{new_base}" if prerelease else new_base

        self.set_version(new_version)
        return new_version


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='PaperKit Version Manager',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s get                    # Get current version
  %(prog)s info                   # Get full version info
  %(prog)s set alpha-1.3.0        # Set new version
  %(prog)s bump patch             # Bump patch version
  %(prog)s bump minor             # Bump minor version
  %(prog)s bump major             # Bump major version
        """
    )
    
    parser.add_argument('command', 
                       choices=['get', 'info', 'set', 'bump'],
                       help='Command to execute')
    parser.add_argument('value', nargs='?',
                       help='Value for set/bump command')
    parser.add_argument('--config', 
                       help='Path to version.yaml config file')
    parser.add_argument('--no-date-update', action='store_true',
                       help='Do not update release date when setting version')
    
    args = parser.parse_args()
    
    # Initialize version manager
    vm = VersionManager(args.config)
    
    # Execute command
    if args.command == 'get':
        print(vm.get_version())
    
    elif args.command == 'info':
        info = vm.get_full_info()
        print(json.dumps(info, indent=2))
    
    elif args.command == 'set':
        if not args.value:
            print("Error: Version string required for 'set' command", file=sys.stderr)
            sys.exit(1)
        vm.set_version(args.value, update_date=not args.no_date_update)
        print(f"Version updated to: {args.value}")
    
    elif args.command == 'bump':
        if not args.value:
            print("Error: Part required for 'bump' command (major, minor, or patch)", file=sys.stderr)
            sys.exit(1)
        new_version = vm.bump_version(args.value)
        print(f"Version bumped to: {new_version}")


if __name__ == '__main__':
    main()
