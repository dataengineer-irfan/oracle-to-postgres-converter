import yaml
import re
from pathlib import Path
import psycopg
import sys

# Import DB_CONFIG; we need to append the root dir to sys.path to find config.py
root_dir = Path(__file__).parent.parent
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))
from config import DB_CONFIG

class RAGEngine:
    def __init__(self, glossary_path: Path, odm_path: Path):
        self.glossary = {}
        self.odm_tables = set()
        self.ldm_to_tables = {} # Maps LDM entity name -> List of physical tables
        self.table_descriptions = {} # Maps table_name -> description
        self.table_columns = {} # Maps table_name -> list of {name, desc}
        self.joins = [] # List of (source_table, source_col, target_table, target_col)
        
        # Load ODM first to build the LDM -> Table mapping
        self._load_odm(odm_path)
        self._load_glossary(glossary_path)
        self._load_postgres_schema()
        
    def _load_postgres_schema(self):
        """Fetches table columns directly from Postgres for tables NOT in the ODM."""
        try:
            with psycopg.connect(**DB_CONFIG) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT table_name, column_name 
                        FROM information_schema.columns 
                        WHERE table_schema = 'provider'
                        ORDER BY table_name, ordinal_position;
                    """)
                    for row in cur.fetchall():
                        t_name = row[0].lower()
                        c_name = row[1].lower()
                        
                        self.odm_tables.add(t_name)
                        
                        if t_name not in self.table_columns:
                            self.table_columns[t_name] = []
                            
                        # Only add if we didn't already get this column from the ODM
                        existing = [c["name"] for c in self.table_columns[t_name]]
                        if c_name not in existing:
                            self.table_columns[t_name].append({"name": c_name, "desc": f"Postgres column {c_name}"})
        except Exception as e:
            print(f"Failed to load schema from Postgres: {e}")

    def _load_odm(self, path: Path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                for tbl in data.get("tables", []):
                    table_name = tbl.get("table_name", "").lower()
                    if table_name:
                        self.odm_tables.add(table_name)
                        desc = tbl.get("description", "").lower()
                        self.table_descriptions[table_name] = desc
                        
                        columns = []
                        for col in tbl.get("columns", []):
                            col_name = col.get("column_name", "").lower()
                            col_desc = col.get("description", "").strip()
                            references = col.get("references", "")
                            
                            if references:
                                parts = references.lower().split('.')
                                if len(parts) >= 2:
                                    target_table = parts[-2]
                                    target_col = parts[-1]
                                    self.joins.append((table_name, col_name, target_table, target_col))
                                    
                            if col_name:
                                columns.append({"name": col_name, "desc": col_desc})
                        self.table_columns[table_name] = columns
                        
                    ldm_entity = tbl.get("maps_to_ldm_entity", "")
                    if ldm_entity:
                        ldm_lower = ldm_entity.lower()
                        if ldm_lower not in self.ldm_to_tables:
                            self.ldm_to_tables[ldm_lower] = []
                        self.ldm_to_tables[ldm_lower].append(table_name)
        except Exception:
            pass

    def _load_glossary(self, path: Path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                for term in data.get("terms", []):
                    term_name = term.get("term", "").lower()
                    
                    related_ldms = term.get("related_ldm_entities", [])
                    resolved_tables = []
                    for ldm in related_ldms:
                        resolved_tables.extend(self.ldm_to_tables.get(ldm.lower(), []))
                        
                    self.glossary[term_name] = resolved_tables
        except Exception:
            pass

    def retrieve_context(self, prompt: str) -> list[str]:
        prompt_lower = prompt.lower()
        matched_tables = set()
        
        # 0. DIRECT MATCH (Highest Priority): If the user literally types the table name!
        for t in self.odm_tables:
            if t in prompt_lower:
                matched_tables.add(t)
                
        # If we found direct matches, just return them! No need to guess.
        if matched_tables:
            return sorted(list(matched_tables))[:3]
        
        # 1. Match against Business Glossary terms
        for term, tables in self.glossary.items():
            if term in prompt_lower:
                for t in tables:
                    matched_tables.add(t)
                    
        # 2. Match against Table names directly and their descriptions
        for t in self.odm_tables:
            core_name = re.sub(r"_(tb|tn|tx)$", "", t)
            core_name_spaces = core_name.replace("_", " ")
            if core_name in prompt_lower or core_name_spaces in prompt_lower:
                matched_tables.add(t)
                
            # Full text search on description as fallback (with strict stop words)
            desc = self.table_descriptions.get(t, "")
            # Filter out extreme common SQL words
            stop_words = {"create", "generate", "record", "records", "table", "tables", "with", "that", "this", "some", "from", "where", "delete", "update", "select", "insert", "number", "code", "date", "name", "type"}
            words = [w for w in prompt_lower.split() if len(w) > 4 and w not in stop_words]
            for w in words:
                if w in desc:
                    matched_tables.add(t)
                
        # Ensure deterministic order, with core tables prioritized
        matched_list = sorted(list(matched_tables))
        
        # Prioritize the core Provider table so it is chosen by the LLM or fallback
        if "p_dtl_tb" in matched_list:
            matched_list.remove("p_dtl_tb")
            matched_list.insert(0, "p_dtl_tb")
            
        # TUNE: Limit context window bloat by strictly capping matched tables to top 3
        return matched_list[:3]

    def retrieve_schema_context(self, matched_tables: list[str]) -> str:
        """Returns a formatted string containing exact columns and their business descriptions for the LLM."""
        if not matched_tables:
            return ""
        
        context = "Exact columns from the Enterprise Data Dictionary for the relevant tables:\n"
        for t in matched_tables:
            cols = self.table_columns.get(t, [])
            if cols:
                col_strs = [f"{c['name']} ({c['desc']})" if c['desc'] else c['name'] for c in cols]
                context += f"- Table {t}: {', '.join(col_strs)}\n"
        return context

    def retrieve_join_context(self, matched_tables: list[str]) -> str:
        if len(matched_tables) < 2:
            return ""
            
        join_rules = []
        for src_tbl, src_col, tgt_tbl, tgt_col in self.joins:
            if src_tbl in matched_tables and tgt_tbl in matched_tables:
                join_rules.append(f"Join {src_tbl} and {tgt_tbl} ON {src_tbl}.{src_col} = {tgt_tbl}.{tgt_col}")
                
        if join_rules:
            return "EXPLICIT DATABASE JOIN RULES (CRITICAL):\n" + "\n".join(f"- {r}" for r in join_rules)
        return ""

# Singleton instance initialized lazily
_engine = None

def get_rag_engine() -> RAGEngine:
    global _engine
    if _engine is None:
        base_dir = Path(__file__).parent.parent
        _engine = RAGEngine(
            base_dir / "_Input" / "provider_business_glossary.yaml",
            base_dir / "_Input" / "provider_odm.yaml"
        )
    return _engine
