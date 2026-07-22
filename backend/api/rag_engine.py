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
        self.table_owners = {} # Maps table_name -> schema/owner
        self.joins = [] # List of (source_table, source_col, target_table, target_col)
        self.valid_values = {} # Maps table_name -> {col_name -> [valid_values]}
        self.scenarios = [] # List of scenarios from knowledgebase
        
        # Load ODM first to build the LDM -> Table mapping
        self._load_odm(odm_path)
        self._load_glossary(glossary_path)
        self._load_postgres_schema()
        self._load_valid_values()
        self._load_scenarios()
        
    def _load_scenarios(self):
        import json
        kb_path = Path(__file__).parent.parent / "knowledgebase" / "provider_scenarios.json"
        if kb_path.exists():
            try:
                with open(kb_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.scenarios = data.get("scenarios", [])
            except Exception as e:
                print(f"Failed to load scenarios JSON: {e}")
                
    def retrieve_relevant_scenarios(self, prompt: str) -> str:
        """Returns a string containing matching business scenarios for the prompt."""
        if not self.scenarios:
            return ""
            
        prompt_lower = prompt.lower()
        matches = []
        for s in self.scenarios:
            name_words = set(s.get("name", "").lower().split())
            if any(w in prompt_lower for w in name_words if len(w) > 3):
                matches.append(s)
                
        if not matches:
            return ""
            
        output = "MATCHING BUSINESS WORKFLOW SCENARIOS:\n"
        for idx, s in enumerate(matches[:2]): # Max 2 scenarios to save context
            output += f"Scenario: {s.get('name')}\n"
            output += f"Tables Involved: {', '.join(s.get('related_tables', []))}\n"
            output += f"Required Insert Sequence:\n"
            for step in s.get("insert_sequence", []):
                output += f"  - {step}\n"
            output += f"Business Validations:\n"
            for val in s.get("business_validations", []):
                output += f"  - {val}\n"
            output += "\n"
        return output

    def _load_valid_values(self):
        import json
        analysis_path = Path(__file__).parent.parent.parent / "temp" / "data_analysis.json"
        if analysis_path.exists():
            try:
                with open(analysis_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for table, stats in data.items():
                        self.valid_values[table] = {}
                        for col, col_data in stats.get("columns", {}).items():
                            if col_data.get("type") == "categorical":
                                self.valid_values[table][col] = col_data.get("values", [])
            except Exception as e:
                print(f"Failed to load data analysis JSON: {e}")
        
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
                        self.table_owners[t_name] = "provider"
                        
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
                        self.table_owners[table_name] = tbl.get("owner", "").lower()
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
        table_scores = {}
        
        def add_score(t, points):
            if t not in table_scores:
                table_scores[t] = 0
            table_scores[t] += points
            
        # 0. DIRECT MATCH (Highest Priority): If the user literally types the table name!
        for t in self.odm_tables:
            if t in prompt_lower:
                add_score(t, 100)
                
        # If we found direct matches, just return them! No need to guess.
        if table_scores and any(s >= 100 for s in table_scores.values()):
            top = sorted(table_scores.items(), key=lambda x: (-x[1], x[0]))
            return [t for t, s in top][:8]
        
        # 1. Match against Business Glossary terms (+5 points)
        for term, tables in self.glossary.items():
            if term in prompt_lower:
                for t in tables:
                    add_score(t, 5)
                    
        # 2. Match against Table names directly and their descriptions
        for t in self.odm_tables:
            core_name = re.sub(r"_(tb|tn|tx)$", "", t)
            core_name_spaces = core_name.replace("_", " ")
            if core_name in prompt_lower or core_name_spaces in prompt_lower:
                add_score(t, 5)
                
            # Full text search on description as fallback (+1 point per keyword)
            desc = self.table_descriptions.get(t, "")
            # Removed 'type', 'code' from stop words so they can match descriptions like 'Provider Type Table'
            stop_words = {"create", "generate", "record", "records", "table", "tables", "with", "that", "this", "some", "from", "where", "delete", "update", "select", "insert", "number", "date", "name"}
            words = [w for w in prompt_lower.split() if len(w) >= 4 and w not in stop_words]
            for w in words:
                if w in desc:
                    add_score(t, 1)
                    
        if not table_scores:
            return []
            
        # Ensure deterministic order, sort by score descending, then alphabetical
        matched_list = sorted(table_scores.items(), key=lambda x: (-x[1], x[0]))
        matched_tables = [t for t, s in matched_list]
        
        # Prioritize the core Provider table so it is chosen by the LLM or fallback
        if "p_dtl_tb" in matched_tables:
            matched_tables.remove("p_dtl_tb")
            matched_tables.insert(0, "p_dtl_tb")
            
        # TUNE: Limit context window bloat by strictly capping matched tables
        return matched_tables[:8]

    def retrieve_schema_context(self, matched_tables: list[str]) -> str:
        """Returns a formatted string containing exact columns and their business descriptions for the LLM."""
        if not matched_tables:
            return ""
        
        context = "Exact columns from the Enterprise Data Dictionary for the relevant tables:\n"
        for t in matched_tables:
            cols = self.table_columns.get(t, [])
            if cols:
                col_strs = []
                for c in cols:
                    c_name = c['name']
                    c_desc = c['desc']
                    
                    # Inject valid values if we have them
                    valid_vals = self.valid_values.get(t, {}).get(c_name)
                    if valid_vals:
                        formatted_vals = [f"'{v}'" if isinstance(v, str) else str(v) for v in valid_vals]
                        val_str = f"MUST BE ONE OF: [{', '.join(formatted_vals)}]"
                        c_desc = f"{c_desc} - {val_str}" if c_desc else val_str
                        
                    col_strs.append(f"{c_name} ({c_desc})" if c_desc else c_name)
                    
                context += f"- Table {t}: {', '.join(col_strs)}\n"
        return context

    def retrieve_join_context(self, matched_tables: list[str]) -> str:
        if len(matched_tables) < 2:
            return ""
            
        join_rules = []
        for src_tbl, src_col, tgt_tbl, tgt_col in self.joins:
            if src_tbl in matched_tables and tgt_tbl in matched_tables:
                src_owner = self.table_owners.get(src_tbl, "")
                tgt_owner = self.table_owners.get(tgt_tbl, "")
                if src_owner in ["reference", "referance"] or tgt_owner in ["reference", "referance"]:
                    join_rules.append(f"Left Join {src_tbl} and {tgt_tbl} ON {src_tbl}.{src_col} = {tgt_tbl}.{tgt_col}")
                else:
                    join_rules.append(f"Join {src_tbl} and {tgt_tbl} ON {src_tbl}.{src_col} = {tgt_tbl}.{tgt_col}")
                
        if join_rules:
            return "EXPLICIT DATABASE JOIN RULES (CRITICAL):\n" + "\n".join(f"- {r}" for r in join_rules)
        return ""

# Singleton instance initialized lazily
_engine = None

def get_rag_engine() -> RAGEngine:
    global _engine
    if _engine is None:
        base_dir = Path(__file__).parent.parent.parent
        _engine = RAGEngine(
            base_dir / "_Input" / "provider_business_glossary.yaml",
            base_dir / "_Input" / "provider_odm.yaml"
        )
    return _engine
