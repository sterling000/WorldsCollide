#!/usr/bin/env python3
"""
Seed Analysis Script for WorldsCollide Randomizer

Analyzes spoiler logs to calculate progression metrics with proper character gating,
specifically looking at the number of checks required to reach the "Unlock Final Kefka" 
objective (6 characters + 9 espers minimum).
"""

import os
import re
import glob
import statistics
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Dict, List, Tuple, Set, Optional

@dataclass
class EventReward:
    event_name: str
    reward: str
    reward_type: str  # 'CHARACTER', 'ESPER', 'ITEM'
    gated_by: Optional[str] = None  # Character required to access this event

@dataclass
class SeedAnalysis:
    seed_name: str
    starting_characters: Set[str]
    events: List[EventReward]
    checks_to_6_chars: int  # meaningful checks only (char/esper rewards)
    checks_to_9_espers: int  # meaningful checks only (char/esper rewards)
    checks_to_unlock_kefka: int  # max(6_chars, 9_espers) - meaningful checks only
    character_progression: List[str]
    esper_progression: List[str]
    is_completable: bool
    total_available_chars: int
    total_available_espers: int
    # New fields for tracking item checks encountered
    item_checks_to_6_chars: int  # item checks encountered while getting 6 chars
    item_checks_to_9_espers: int  # item checks encountered while getting 9 espers
    item_checks_to_unlock: int  # item checks encountered to unlock kefka
    total_checks_to_unlock: int  # meaningful + item checks combined
    item_percentage: float  # percentage of total checks that were items

class CharacterGateMapping:
    """Maps events to their character requirements by analyzing event files"""
    
    def __init__(self):
        self.gate_mapping = {}
        self._build_character_gate_mapping()
    
    def _build_character_gate_mapping(self):
        """Build character gate mapping from event files"""
        # Known character gate mappings based on event file analysis
        # This should be expanded by scanning all event files
        self.gate_mapping = {
            # Character-gated events
            'South Figaro': 'CELES',
            'Opera House': 'CELES', 
            'Magitek Factory': 'CELES',
            'Zone Eater': 'GOGO',
            'Mt. Kolts': 'SABIN',
            'Lete River': 'TERRA',
            'Imperial Camp': 'CYAN',
            'Doma WOB': 'CYAN',
            'Doma WOR': 'CYAN',
            'Phantom Train': 'SABIN',
            'Veldt': 'GAU',
            'Veldt Cave WOR': 'SHADOW',
            'Burning House': 'STRAGO',
            'Kohlingen': 'SETZER',
            'Phoenix Cave': 'LOCKE',
            'Mt. Zozo': 'TERRA',
            'Esper Mountain': 'RELM',
            'Tzen': None,
            'Coliseum': None,
            'Owzer Mansion': 'RELM',
            'Fanatic\'s Tower': 'STRAGO',
            'Ebot\'s Rock': 'STRAGO',
            'Umaro\'s Cave': 'UMARO',
            'Baren Falls': 'SABIN',
            'Serpent Trench': 'GAU',
            'Floating Continent': 'SHADOW',  # Usually accessible but may have reqs
            
            # Events with no character gates (always accessible if you meet chars_required)
            'Narshe Battle': None,
            'Start': None,
            'Whelk': "TERRA",
            'Narshe Moogle Defense': "MOG",
            'Ancient Castle': "EDGAR",  # May depend on Edgar for figaro castle access
            'Tritoch': None,
            'Sealed Gate': "TERRA",
            'Daryl\'s Tomb': "SETZER",
            'Auction House': None,
            'Collapsing House': "SABIN",
            'Doom Gaze': None,
            'Kefka\'s Tower': None,
            '8 Dragons': None,
            'Lone Wolf': "MOG",
        }

class SpoilerLogParser:
    """Parse WorldsCollide spoiler logs to extract event reward information"""
    
    # Known character names from FF6
    CHARACTERS = {
        'TERRA', 'LOCKE', 'CYAN', 'SHADOW', 'EDGAR', 'SABIN', 'CELES', 'STRAGO',
        'RELM', 'SETZER', 'MOG', 'GAU', 'GOGO', 'UMARO'
    }
    
    # Known esper names
    ESPERS = {
        'RAMUH', 'SHIVA', 'IFRIT', 'SIREN', 'TERRATO', 'SHOAT', 'MADUIN', 
        'BISMARK', 'STRAY', 'PALIDOR', 'TRITOCH', 'ODIN', 'RAIDEN', 'BAHAMUT',
        'ALEXANDR', 'CRUSADER', 'RAGNAROK', 'KIRIN', 'ZONSEEK', 'CARBUNKL',
        'PHANTOM', 'SRAPHIM', 'GOLEM', 'UNICORN', 'FENRIR', 'STARLET',
        'PHOENIX', 'ZONESEEK'  # Alternative spelling
    }
    
    def __init__(self):
        self.gate_mapping = CharacterGateMapping()
    
    def parse_spoiler_log(self, log_path: str) -> SeedAnalysis:
        """Parse a single spoiler log file"""
        seed_name = os.path.basename(log_path).replace('.txt', '')
        
        with open(log_path, 'r') as f:
            content = f.read()
        
        # Parse starting characters
        starting_characters = self._parse_starting_characters(content)
        
        # Parse events and rewards
        events = self._parse_events_section(content)
        
        # Calculate progression with character gating
        analysis = self._calculate_gated_progression(seed_name, starting_characters, events)
        return analysis
    
    def _parse_starting_characters(self, content: str) -> Set[str]:
        """Extract starting characters from the Start event"""
        starting_chars = set()
        
        # Look for the Start event in Events section
        start_match = re.search(r'^Start\s+(.+)$', content, re.MULTILINE)
        if start_match:
            start_rewards = start_match.group(1).strip()
            # Parse multiple characters if comma-separated
            rewards = [r.strip() for r in start_rewards.split(',')]
            for reward in rewards:
                if reward.upper() in self.CHARACTERS:
                    starting_chars.add(reward.upper())
        
        return starting_chars
    
    def _parse_events_section(self, content: str) -> List[EventReward]:
        """Parse the events section to extract event -> reward mappings"""
        events = []
        
        # Find the Events section
        events_match = re.search(r'---- Events ----\s*\n(.*?)(?=\n----|\Z)', content, re.DOTALL)
        if not events_match:
            events_match = re.search(r'Events.*?\n(.*?)(?=\n----|$)', content, re.DOTALL)
        
        if events_match:
            events_section = events_match.group(1)
            lines = events_section.split('\n')
            
            for line in lines:
                # CRITICAL FIX: Skip indented detail lines (auction house details, battle changes, etc.)
                # Only parse lines that start at column 0 (true event rewards)
                if line.startswith('    ') or line.startswith('\t'):
                    continue
                
                line = line.strip()
                if not line or line.startswith('-'):
                    continue
                    
                # Parse event -> reward format
                # Handle complex multi-line formats and simple ones
                parts = re.split(r'\s{2,}', line, 1)  # Split on 2+ spaces
                if len(parts) >= 2:
                    event_name = parts[0].strip()
                    rewards_str = parts[1].strip()
                    
                    # Get character gate for this event
                    gated_by = self.gate_mapping.gate_mapping.get(event_name)
                    
                    # Handle multiple rewards separated by commas, but preserve parenthetical pricing info
                    # Use regex to split on commas that are NOT inside parentheses
                    rewards = re.split(r',(?![^()]*\))', rewards_str)
                    for reward in rewards:
                        reward = reward.strip()
                        if reward:  # Skip empty rewards
                            # Clean up reward string - remove auction house pricing info
                            reward = re.sub(r'\s*\(\d+,?\d*\)', '', reward)  # Remove (10,000) etc.
                            if reward:  # Check again after cleanup
                                reward_type = self._classify_reward(reward)
                                events.append(EventReward(event_name, reward, reward_type, gated_by))
        
        return events
    
    def _classify_reward(self, reward: str) -> str:
        """Classify a reward as CHARACTER, ESPER, or ITEM"""
        reward_upper = reward.upper()
        
        if reward_upper in self.CHARACTERS:
            return 'CHARACTER'
        elif reward_upper.endswith(' (ESPER)'):
            # Handle special case: "Ragnarok (Esper)" should be classified as ESPER
            # Strip the " (Esper)" suffix and check if the base name is in ESPERS
            base_reward = reward_upper.replace(' (ESPER)', '')
            if base_reward in self.ESPERS:
                return 'ESPER'
            else:
                return 'ITEM'
        elif reward_upper == 'RAGNAROK':
            # Special case: "Ragnarok" without "(Esper)" suffix should be treated as ITEM
            # since the esper version would have the "(Esper)" suffix
            return 'ITEM'
        elif reward_upper in self.ESPERS:
            return 'ESPER'
        else:
            return 'ITEM'
    
    def _calculate_gated_progression(self, seed_name: str, starting_chars: Set[str], 
                                   events: List[EventReward]) -> SeedAnalysis:
        """Calculate progression using character gating and pathfinding"""
        
        # Track what we have
        available_chars = starting_chars.copy()
        available_espers = 0
        characters_found = len(starting_chars)
        espers_found = 0
        
        # Track progression - separate meaningful vs item checks
        meaningful_checks_completed = 0  # Only char/esper rewards
        total_checks_completed = 0  # All checks including items
        item_checks_completed = 0  # Item checks only
        
        meaningful_checks_to_6_chars = 0
        meaningful_checks_to_9_espers = 0
        item_checks_to_6_chars = 0
        item_checks_to_9_espers = 0
        
        character_progression = []
        esper_progression = []
        
        # Create a queue of available events (BFS for optimal progression)
        remaining_events = events.copy()
        
        # Process events in order, but only those we can access
        while remaining_events and (characters_found < 6 or espers_found < 9):
            made_progress = False
            
            # Look for events we can complete
            for i, event in enumerate(remaining_events):
                can_complete = True
                
                # Check if we have the required character
                if event.gated_by and event.gated_by not in available_chars:
                    can_complete = False
                
                if can_complete:
                    # Complete this event - track both meaningful and total checks
                    total_checks_completed += 1
                    remaining_events.pop(i)
                    made_progress = True
                    
                    if event.reward_type == 'CHARACTER':
                        meaningful_checks_completed += 1
                        characters_found += 1
                        available_chars.add(event.reward.upper())
                        character_progression.append(f"Meaningful Check {meaningful_checks_completed}: {event.event_name} -> {event.reward}")
                        if characters_found == 6 and meaningful_checks_to_6_chars == 0:
                            meaningful_checks_to_6_chars = meaningful_checks_completed
                            item_checks_to_6_chars = item_checks_completed
                            
                    elif event.reward_type == 'ESPER':
                        meaningful_checks_completed += 1
                        espers_found += 1
                        esper_progression.append(f"Meaningful Check {meaningful_checks_completed}: {event.event_name} -> {event.reward}")
                        if espers_found == 9 and meaningful_checks_to_9_espers == 0:
                            meaningful_checks_to_9_espers = meaningful_checks_completed
                            item_checks_to_9_espers = item_checks_completed
                    
                    else:  # ITEM reward
                        item_checks_completed += 1
                    
                    break  # Restart the loop to recheck all events
            
            if not made_progress:
                # We're stuck - can't complete any more events
                break
        
        # Count total available rewards
        total_chars = len([e for e in events if e.reward_type == 'CHARACTER']) + len(starting_chars)
        total_espers = len([e for e in events if e.reward_type == 'ESPER'])
        
        # Set impossible values if we never reached targets
        if meaningful_checks_to_6_chars == 0:
            meaningful_checks_to_6_chars = 999
        if meaningful_checks_to_9_espers == 0:
            meaningful_checks_to_9_espers = 999
            
        meaningful_checks_to_unlock_kefka = max(meaningful_checks_to_6_chars, meaningful_checks_to_9_espers)
        is_completable = (meaningful_checks_to_unlock_kefka < 999 and 
                         total_chars >= 6 and total_espers >= 9)
        
        # Calculate item check stats for the final unlock path
        final_item_checks = max(item_checks_to_6_chars, item_checks_to_9_espers)
        final_total_checks = meaningful_checks_to_unlock_kefka + final_item_checks if meaningful_checks_to_unlock_kefka < 999 else 999
        item_percentage = (final_item_checks / final_total_checks * 100) if final_total_checks > 0 and meaningful_checks_to_unlock_kefka < 999 else 0
        
        return SeedAnalysis(
            seed_name=seed_name,
            starting_characters=starting_chars,
            events=events,
            checks_to_6_chars=meaningful_checks_to_6_chars,
            checks_to_9_espers=meaningful_checks_to_9_espers,
            checks_to_unlock_kefka=meaningful_checks_to_unlock_kefka,
            character_progression=character_progression,
            esper_progression=esper_progression,
            is_completable=is_completable,
            total_available_chars=total_chars,
            total_available_espers=total_espers,
            item_checks_to_6_chars=item_checks_to_6_chars,
            item_checks_to_9_espers=item_checks_to_9_espers,
            item_checks_to_unlock=final_item_checks,
            total_checks_to_unlock=final_total_checks,
            item_percentage=item_percentage
        )

def analyze_seeds(seeds_dir: str = "seeds") -> Dict[str, any]:
    """Analyze all seed spoiler logs in the given directory"""
    parser = SpoilerLogParser()
    analyses = []
    
    # Find all .txt files in seeds directory
    log_files = glob.glob(os.path.join(seeds_dir, "*.txt"))
    
    if not log_files:
        print(f"No .txt files found in {seeds_dir} directory!")
        print("Make sure to run wc_batch.py with -slog flag to generate spoiler logs.")
        return {"error": "No spoiler logs found"}
    
    print(f"Found {len(log_files)} spoiler log files to analyze...")
    
    for log_file in log_files:
        try:
            analysis = parser.parse_spoiler_log(log_file)
            analyses.append(analysis)
            status = "✓" if analysis.is_completable else "✗"
            print(f"{status} {analysis.seed_name}: {analysis.checks_to_unlock_kefka} checks "
                  f"({len(analysis.starting_characters)} start chars, "
                  f"{analysis.total_available_chars}/{analysis.total_available_espers} total)")
        except Exception as e:
            print(f"Error analyzing {log_file}: {e}")
            import traceback
            traceback.print_exc()
    
    return generate_statistical_report(analyses)

def generate_statistical_report(analyses: List[SeedAnalysis]) -> Dict[str, any]:
    """Generate comprehensive statistical analysis"""
    
    # Filter completable vs incomplete
    completable = [a for a in analyses if a.is_completable]
    incomplete = [a for a in analyses if not a.is_completable]
    
    if not analyses:
        return {"error": "No seeds analyzed!"}
    
    if not completable:
        return {
            "error": "No completable seeds found!",
            "total_seeds": len(analyses),
            "incomplete_details": [(a.seed_name, len(a.starting_characters), 
                                   a.total_available_chars, a.total_available_espers) 
                                  for a in incomplete]
        }
    
    # Extract progression data
    kefka_checks = [a.checks_to_unlock_kefka for a in completable]
    char_checks = [a.checks_to_6_chars for a in completable]
    esper_checks = [a.checks_to_9_espers for a in completable]
    
    # Calculate statistics
    report = {
        "total_seeds": len(analyses),
        "completable_seeds": len(completable),
        "incomplete_seeds": len(incomplete),
        "incomplete_rate": len(incomplete) / len(analyses) * 100,
        
        "kefka_unlock_stats": {
            "mean": statistics.mean(kefka_checks),
            "median": statistics.median(kefka_checks),
            "std_dev": statistics.stdev(kefka_checks) if len(kefka_checks) > 1 else 0,
            "min": min(kefka_checks),
            "max": max(kefka_checks),
            "percentile_95": sorted(kefka_checks)[int(0.95 * len(kefka_checks))],
            "percentile_80": sorted(kefka_checks)[int(0.80 * len(kefka_checks))],
            "percentile_20": sorted(kefka_checks)[int(0.20 * len(kefka_checks))],
        },
        
        "target_analysis": {
            "under_20_checks": len([c for c in kefka_checks if c < 20]) / len(kefka_checks) * 100,
            "under_18_checks": len([c for c in kefka_checks if c < 18]) / len(kefka_checks) * 100,
            "under_16_checks": len([c for c in kefka_checks if c < 16]) / len(kefka_checks) * 100,
            "over_22_checks": len([c for c in kefka_checks if c > 22]) / len(kefka_checks) * 100,
            "over_24_checks": len([c for c in kefka_checks if c >= 24]) / len(kefka_checks) * 100,
        },
        
        "character_vs_esper": {
            "chars_limiting_factor": len([a for a in completable if a.checks_to_6_chars > a.checks_to_9_espers]),
            "espers_limiting_factor": len([a for a in completable if a.checks_to_9_espers > a.checks_to_6_chars]),
            "tied": len([a for a in completable if a.checks_to_6_chars == a.checks_to_9_espers]),
        },
        
        "starting_character_analysis": {
            "avg_starting_chars": statistics.mean([len(a.starting_characters) for a in completable]),
            "starting_char_distribution": {}
        },
        
        "detailed_data": {
            "kefka_checks": kefka_checks,
            "character_checks": char_checks,
            "esper_checks": esper_checks,
        },
        
        "progression_paths": {
            "character_paths": [analysis.character_progression for analysis in completable],
            "esper_paths": [analysis.esper_progression for analysis in completable],
            "seed_names": [analysis.seed_name for analysis in completable]
        },
        
        "item_check_analysis": {
            "avg_item_checks": statistics.mean([a.item_checks_to_unlock for a in completable]),
            "avg_item_percentage": statistics.mean([a.item_percentage for a in completable]),
            "avg_total_checks": statistics.mean([a.total_checks_to_unlock for a in completable]),
            "item_check_range": {
                "min": min([a.item_checks_to_unlock for a in completable]),
                "max": max([a.item_checks_to_unlock for a in completable])
            }
        },
        
        "incomplete_seeds_details": [(a.seed_name, len(a.starting_characters), 
                                     a.total_available_chars, a.total_available_espers) 
                                    for a in incomplete]
    }
    
    return report

def print_report(report: Dict[str, any]):
    """Print a formatted analysis report"""
    if "error" in report:
        print(f"\n❌ ERROR: {report['error']}")
        if "incomplete_details" in report:
            print(f"\nIncomplete seeds analysis:")
            for seed_name, start_chars, total_chars, total_espers in report["incomplete_details"]:
                print(f"   {seed_name}: {start_chars} start, {total_chars} chars, {total_espers} espers available")
        return
    
    print("\n" + "="*80)
    print("WORLDSCOLLIDIS SEED PROGRESSION ANALYSIS")
    print("="*80)
    
    print(f"\n📊 SAMPLE SIZE")
    print(f"Total Seeds Analyzed: {report['total_seeds']}")
    print(f"Completable Seeds: {report['completable_seeds']}")
    print(f"Incomplete Seeds: {report['incomplete_seeds']} ({report['incomplete_rate']:.1f}%)")
    
    if report['incomplete_seeds'] > 0:
        print(f"\n⚠️  INCOMPLETE SEEDS DETAILS:")
        for seed_name, start_chars, total_chars, total_espers in report['incomplete_seeds_details']:
            print(f"   {seed_name}: {start_chars} start chars, {total_chars} total chars, {total_espers} espers")
    
    # Progression Paths Details
    if 'progression_paths' in report:
        print(f"\n🛤️  PROGRESSION PATHS ANALYSIS")
        paths = report['progression_paths']
        seed_names = paths['seed_names']
        char_paths = paths['character_paths']
        esper_paths = paths['esper_paths']
        
        for i, seed_name in enumerate(seed_names[:3]):  # Show first 3 seeds as examples
            print(f"\n   {seed_name}:")
            if i < len(char_paths) and char_paths[i]:
                print(f"     Characters: {' → '.join(char_paths[i][:6])}{'...' if len(char_paths[i]) > 6 else ''}")
            if i < len(esper_paths) and esper_paths[i]:
                print(f"     Espers: {' → '.join(esper_paths[i][:6])}{'...' if len(esper_paths[i]) > 6 else ''}")
        
        if len(seed_names) > 3:
            print(f"   ... and {len(seed_names) - 3} more seeds (see JSON report for full paths)")
    
    stats = report['kefka_unlock_stats']
    print(f"\n🎯 UNLOCK FINAL KEFKA STATISTICS (Gated Analysis)")
    print(f"Mean checks: {stats['mean']:.1f}")
    print(f"Median checks: {stats['median']:.1f}")
    print(f"Standard deviation: {stats['std_dev']:.1f}")
    print(f"Range: {stats['min']} - {stats['max']} checks")
    print(f"95th percentile: {stats['percentile_95']} checks")
    print(f"80th percentile: {stats['percentile_80']} checks")
    
    targets = report['target_analysis']
    print(f"\n🎯 TARGET ANALYSIS")
    print(f"Under 16 checks (ideal): {targets['under_16_checks']:.1f}%")
    print(f"Under 18 checks (target 80%): {targets['under_18_checks']:.1f}%")
    print(f"Under 20 checks (target 95%): {targets['under_20_checks']:.1f}%")
    print(f"Over 22 checks (outliers): {targets['over_22_checks']:.1f}%")
    print(f"Over 24 checks (discouraged): {targets['over_24_checks']:.1f}%")
    
    limiting = report['character_vs_esper']
    print(f"\n⚖️  LIMITING FACTOR ANALYSIS")
    print(f"Characters are limiting factor: {limiting['chars_limiting_factor']} seeds")
    print(f"Espers are limiting factor: {limiting['espers_limiting_factor']} seeds")
    print(f"Tied (same check count): {limiting['tied']} seeds")
    
    # Item Check Analysis
    if 'item_check_analysis' in report:
        items = report['item_check_analysis']
        print(f"\n🎁 ITEM CHECK ANALYSIS")
        print(f"Average meaningful checks (char/esper only): {stats['mean']:.1f}")
        print(f"Average item checks encountered: {items['avg_item_checks']:.1f}")
        print(f"Average total checks (meaningful + items): {items['avg_total_checks']:.1f}")
        print(f"Average item percentage: {items['avg_item_percentage']:.1f}%")
        print(f"Item check range: {items['item_check_range']['min']} - {items['item_check_range']['max']}")
    
    # Assessment
    print(f"\n📋 ASSESSMENT")
    if targets['over_24_checks'] > 1:
        print(f"❌ FAIL: {targets['over_24_checks']:.1f}% of seeds require 24+ checks (target: <1%)")
    else:
        print(f"✅ PASS: {targets['over_24_checks']:.1f}% of seeds require 24+ checks (target: <1%)")
        
    if targets['under_20_checks'] < 95:
        print(f"❌ FAIL: {targets['under_20_checks']:.1f}% under 20 checks (target: 95%)")
    else:
        print(f"✅ PASS: {targets['under_20_checks']:.1f}% under 20 checks (target: 95%)")
        
    if targets['under_18_checks'] < 80:
        print(f"❌ FAIL: {targets['under_18_checks']:.1f}% under 18 checks (target: 80%)")
    else:
        print(f"✅ PASS: {targets['under_18_checks']:.1f}% under 18 checks (target: 80%)")
    
    if report['incomplete_rate'] > 0:
        print(f"❌ CRITICAL: {report['incomplete_rate']:.1f}% of seeds are incompletable!")

def main():
    """Main analysis function"""
    print("WorldsCollide Seed Progression Analysis")
    print("======================================")
    print("Analyzing character gating and optimal progression paths...")
    
    # Check if seeds directory exists
    seeds_dir = "seeds"
    if not os.path.exists(seeds_dir):
        print(f"Error: {seeds_dir} directory not found!")
        print("Please run wc_batch.py first to generate seeds with -slog flag.")
        return
    
    # Analyze seeds
    report = analyze_seeds(seeds_dir)
    
    # Print results
    print_report(report)
    
    # Save detailed report
    import json
    with open('seed_analysis_report.json', 'w') as f:
        json.dump(report, f, indent=2, default=str)  # default=str handles sets
    print(f"\n📄 Detailed report saved to: seed_analysis_report.json")

if __name__ == "__main__":
    main()