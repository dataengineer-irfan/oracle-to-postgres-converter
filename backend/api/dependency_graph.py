from typing import List
import sys
from pathlib import Path

# Add parent directory to sys.path to allow importing from the existing project
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from generation.data_generator import PROVIDER_FK_MAP
except ImportError:
    PROVIDER_FK_MAP = {}

def resolve_dependencies(tables: List[str]) -> List[str]:
    """
    Given a list of target tables, recursively traverses the PROVIDER_FK_MAP
    to find all parent tables required to satisfy foreign key constraints.
    Returns the complete list of tables needed.
    """
    if not PROVIDER_FK_MAP:
        return tables
        
    required_tables = set(tables)
    
    # Build adjacency list for parent lookups: child -> set(parents)
    deps = {}
    for (child_tbl, _), (parent_tbl, _) in PROVIDER_FK_MAP.items():
        if child_tbl not in deps:
            deps[child_tbl] = set()
        deps[child_tbl].add(parent_tbl)
        
    # BFS or DFS to find all ancestors
    queue = list(required_tables)
    while queue:
        current = queue.pop(0)
        parents = deps.get(current, set())
        for p in parents:
            if p not in required_tables:
                required_tables.add(p)
                queue.append(p)
                
    # Sort them topologically or alphabetically for the UI
    # The actual topological sorting for execution happens inside DataGenerator
    return sorted(list(required_tables))
