#!/usr/bin/env python3
"""
PaperKit Version Manager
Manages version information from .paperkit/_cfg/version.yaml
"""

import sys
import os
import argparse
from pathlib import Path
from datetime import datetime

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


class VersionManager:
    """Manages version information for PaperKit"""
    
    def __init__(self, config_path=None):
        """Initialize the version manager"""
        if config_path is None:
            # Find the .paperkit directory
            script_dir = Path(__file__).parent
            paperkit_root = script_dir.parent.parent
            config_path = paperkit_root / ".paperkit" / "_cfg" / "version.yaml"
        
        self.config_path = Path(config_path)
        self.version_data = None
        
        if self.config_path.exists():
            self.load()
    
    def load(self):
        """Load version data from YAML file"""
        try:
            with open(self.config_path, 'r') as f:
                self.version_data = yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading version config: {e}", file=sys.stderr)
            sys.exit(1)
    
    def save(self):
        """Save version data to YAML file"""
        try:
            with open(self.config_path, 'w') as f:
                yaml.dump(self.version_data, f, default_flow_style=False, sort_keys=False)
        except Exception as e:
            print(f"Error saving version config: {e}", file=sys.stderr)
            sys.exit(1)
    
    def get_version(self):
        """Get the current version string"""
        if not self.version_data:
            return "unknown"
        return self.version_data.get('version', {}).get('current', 'unknown')
    
    def get_full_info(self):
        """Get all version information"""
        if not self.version_data:
            return {}
        return self.version_data.get('version', {})
    
    def set_version(self, version_string, release_type=None, update_date=True):
        """
        Set a new version
        
        Args:
            version_string: Version string (e.g., "alpha-1.3.0")
            release_type: Optional release type (alpha, beta, rc, stable)
            update_date: Whether to update the release date
        """
        if not self.version_data:
            self.version_data = {'version': {}}
        
        version = self.version_data.setdefault('version', {})
        
        # Parse version string
        version['current'] = version_string
        version.setdefault('release', {})['name'] = version_string
        
        if update_date:
            today = datetime.now().strftime("%Y-%m-%d")
            version['release']['date'] = today
            version.setdefault('metadata', {})['lastUpdated'] = today
        
        if release_type:
            version['release']['type'] = release_type
        
        # Try to parse semantic version components
        try:
            # Handle format like "alpha-1.2.0" or "1.2.0"
            parts = version_string.split('-')
            if len(parts) == 2:
                prerelease, semver = parts
                version.setdefault('components', {})['prerelease'] = prerelease
            else:
                semver = version_string
            
            # Parse major.minor.patch
            major, minor, patch = semver.split('.')
            components = version.setdefault('components', {})
            components['major'] = int(major)
            components['minor'] = int(minor)
            components['patch'] = int(patch)
        except:
            pass  # If parsing fails, just keep the version string
        
        self.save()
    
    def bump_version(self, part='patch'):
        """
        Bump version by incrementing major, minor, or patch
        
        Args:
            part: Which part to bump ('major', 'minor', or 'patch')
        """
        if not self.version_data:
            print("Error: No version data loaded", file=sys.stderr)
            sys.exit(1)
        
        version = self.version_data.get('version', {})
        components = version.get('components', {})
        
        major = components.get('major', 1)
        minor = components.get('minor', 0)
        patch = components.get('patch', 0)
        prerelease = components.get('prerelease', 'alpha')
        
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
        
        new_version = f"{prerelease}-{major}.{minor}.{patch}"
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
        import json
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
