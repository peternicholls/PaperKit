#!/usr/bin/env python3
"""
Agent Format Migration Script

Converts agent definitions from old format (MD with frontmatter) to new format
(YAML metadata + MD instructions without frontmatter).

Usage:
    python3 migrate-agent-format.py [--dry-run] [--verbose]

Options:
    --dry-run   Show what would be changed without making changes
    --verbose   Show detailed output

Exit codes:
    0 = Migration successful (or nothing to migrate)
    1 = Migration errors occurred
"""

import sys
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import re


# Color codes for terminal output
class Colors:
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'
    BOLD = '\033[1m'


def color(text: str, color_code: str) -> str:
    """Wrap text in color codes."""
    return f"{color_code}{text}{Colors.NC}"


def find_project_root() -> Optional[Path]:
    """Find the project root by looking for .paperkit/ directory."""
    current = Path.cwd()
    for path in [current] + list(current.parents):
        if (path / ".paperkit").is_dir():
            return path
    return None


def extract_frontmatter(content: str) -> Tuple[Optional[str], str]:
    """
    Extract YAML frontmatter from markdown content.
    
    Returns:
        Tuple of (frontmatter_yaml, content_without_frontmatter)
    """
    lines = content.split('\n')
    
    # Check for frontmatter start
    if not lines or lines[0].strip() != '---':
        return None, content
    
    # Find the closing ---
    end_idx = None
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == '---':
            end_idx = i
            break
    
    if end_idx is None:
        return None, content
    
    # Extract frontmatter and remaining content
    frontmatter = '\n'.join(lines[1:end_idx])
    remaining = '\n'.join(lines[end_idx + 1:]).lstrip('\n')
    
    return frontmatter, remaining


def check_for_frontmatter(md_path: Path) -> bool:
    """Check if a markdown file has YAML frontmatter."""
    try:
        content = md_path.read_text(encoding='utf-8')
        frontmatter, _ = extract_frontmatter(content)
        return frontmatter is not None
    except Exception:
        return False


def find_agents_with_frontmatter(project_root: Path) -> List[Tuple[Path, str]]:
    """Find all MD agent files that still have YAML frontmatter."""
    agents_with_fm = []
    
    agent_dirs = [
        project_root / ".paperkit/core/agents",
        project_root / ".paperkit/specialist/agents"
    ]
    
    for agent_dir in agent_dirs:
        if not agent_dir.is_dir():
            continue
        
        for md_file in agent_dir.glob("*.md"):
            content = md_file.read_text(encoding='utf-8')
            frontmatter, _ = extract_frontmatter(content)
            if frontmatter:
                agents_with_fm.append((md_file, frontmatter))
    
    return agents_with_fm


def migrate_agent(md_path: Path, yaml_dir: Path, dry_run: bool = False, verbose: bool = False) -> bool:
    """
    Migrate a single agent from frontmatter format to YAML + MD format.
    
    Returns True if migration successful, False otherwise.
    """
    try:
        import yaml
    except ImportError:
        print(color("Error: pyyaml package required. Install with: pip install pyyaml", Colors.RED))
        return False
    
    try:
        content = md_path.read_text(encoding='utf-8')
        frontmatter_str, md_content = extract_frontmatter(content)
        
        if not frontmatter_str:
            if verbose:
                print(color(f"  {md_path.name}: No frontmatter found", Colors.YELLOW))
            return True
        
        # Parse frontmatter
        frontmatter = yaml.safe_load(frontmatter_str)
        agent_name = frontmatter.get('name', md_path.stem)
        yaml_path = yaml_dir / f"{agent_name}.yaml"
        
        if verbose:
            print(f"  Processing: {md_path.name}")
            print(f"    Agent name: {agent_name}")
            print(f"    YAML target: {yaml_path.name}")
        
        if dry_run:
            print(color(f"  [DRY RUN] Would migrate: {md_path.name}", Colors.CYAN))
            print(f"    → Create/update: {yaml_path}")
            print(f"    → Remove frontmatter from: {md_path}")
            return True
        
        # Check if YAML already exists
        if yaml_path.exists():
            print(color(f"  {yaml_path.name} already exists - skipping YAML creation", Colors.YELLOW))
        else:
            # Write YAML file
            with open(yaml_path, 'w') as f:
                yaml.dump(frontmatter, f, default_flow_style=False, sort_keys=False)
            print(color(f"  ✓ Created: {yaml_path.name}", Colors.GREEN))
        
        # Update MD file (remove frontmatter)
        md_path.write_text(md_content, encoding='utf-8')
        print(color(f"  ✓ Updated: {md_path.name} (removed frontmatter)", Colors.GREEN))
        
        return True
        
    except Exception as e:
        print(color(f"  ✗ Error migrating {md_path.name}: {e}", Colors.RED))
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Migrate agent definitions from frontmatter to YAML format"
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be changed without making changes'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed output'
    )
    
    args = parser.parse_args()
    
    project_root = find_project_root()
    if not project_root:
        print(color("Error: Could not find PaperKit project root", Colors.RED))
        sys.exit(1)
    
    print(color("╔═══════════════════════════════════════════════════╗", Colors.CYAN))
    print(color("║       Agent Format Migration Script               ║", Colors.CYAN))
    print(color("╚═══════════════════════════════════════════════════╝", Colors.CYAN))
    print(color(f"Project: {project_root}", Colors.BLUE))
    
    if args.dry_run:
        print(color("\n[DRY RUN MODE - No changes will be made]\n", Colors.YELLOW))
    
    # Find agents with frontmatter
    print(color("\nScanning for agents with frontmatter...", Colors.BOLD))
    agents = find_agents_with_frontmatter(project_root)
    
    if not agents:
        print(color("\n✓ No agents with frontmatter found. Migration not needed.", Colors.GREEN))
        sys.exit(0)
    
    print(f"\nFound {len(agents)} agent(s) with frontmatter:\n")
    for md_path, _ in agents:
        print(f"  - {md_path.relative_to(project_root)}")
    
    # Migrate each agent
    print(color("\nMigrating agents...", Colors.BOLD))
    yaml_dir = project_root / ".paperkit/_cfg/agents"
    
    success_count = 0
    fail_count = 0
    
    for md_path, _ in agents:
        if migrate_agent(md_path, yaml_dir, args.dry_run, args.verbose):
            success_count += 1
        else:
            fail_count += 1
    
    # Summary
    print(color("\n" + "=" * 50, Colors.BOLD))
    print(color("SUMMARY", Colors.BOLD))
    print("=" * 50)
    print(f"  Processed: {len(agents)}")
    print(f"  Successful: {color(str(success_count), Colors.GREEN)}")
    print(f"  Failed: {color(str(fail_count), Colors.RED if fail_count > 0 else Colors.GREEN)}")
    
    if args.dry_run:
        print(color("\n[DRY RUN] No changes were made. Run without --dry-run to apply changes.", Colors.YELLOW))
    
    if fail_count > 0:
        print(color("\n⚠ Migration completed with errors", Colors.YELLOW))
        sys.exit(1)
    else:
        print(color("\n✓ Migration completed successfully", Colors.GREEN))
        sys.exit(0)


if __name__ == "__main__":
    main()
