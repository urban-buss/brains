---
applyTo: "**/writer.py,**/query.py,**/validate.py,**/exceptions.py"
---
# Shared Protocols — Writer & Query Contracts

Every brain implements a **writer** (Parquet I/O) and a **query layer** (DuckDB read-only access). These modules are intentionally duplicated (per ADR-004) but must follow the same contract so that:

- Bug fixes port between brains in < 5 minutes.
- New brains can be scaffolded from the pattern.
- A future `brainlib` extraction (if 3+ brains) has a stable interface.

---

## WriterProtocol

### Required module-level constant

```python
SCHEMAS: dict[str, pa.Schema]
```

The **single source of truth** for every entity's Parquet column layout. All writes enforce this schema; any mismatch triggers a migration.

### Required functions

| Function | Signature | Contract |
|----------|-----------|----------|
| **write** | `(entity: str, rows: list[dict], output_dir: Path) → Path` | Overwrite the entity's Parquet file. Enforce schema from `SCHEMAS[entity]`. Return the written path. |
| **append** | `(entity: str, rows: list[dict], output_dir: Path) → None` | Read existing → concat → write. Deduplicate by primary key if applicable. |
| **read** | `(entity: str, output_dir: Path) → list[dict] | pa.Table` | Read and return all rows. Return type may vary (list[dict] or Arrow Table). |

### Schema versioning sidecar

Each brain persists a `.schema_version.json` alongside its Parquet files:

```json
{
  "schema_hash": "<deterministic hash of SCHEMAS>",
  "generated_at": "ISO-8601 timestamp"
}
```

- `compute_schema_hash()` → `str` — deterministic fingerprint of `SCHEMAS`.
- On connection open or write, compare stored hash to current. Raise `DataStaleError` on mismatch (triggers migration).

### Naming flexibility

The actual function names may differ (`write_parquet` vs `write_table`). The contract is the **shape**: `(entity, data, output_dir) → result`.

---

## QueryProtocol

### SQL validation — `validate_sql(sql: str)`

Every brain's query layer MUST reject:

1. **Empty or whitespace-only** SQL.
2. **Multiple statements** (`;` separator).
3. **DDL/DML at start**: `INSERT`, `UPDATE`, `DELETE`, `DROP`, `CREATE`, `ALTER`, `TRUNCATE`.
4. **Non-SELECT start**: must begin with `SELECT` or `WITH`.
5. **Forbidden keywords anywhere** (after stripping comments):
   ```
   COPY | ATTACH | DETACH | PRAGMA | LOAD | INSTALL
   GRANT | REVOKE | EXEC | EXECUTE
   ```
6. **Forbidden filesystem functions** (after stripping comments):
   ```
   read_parquet | read_csv | read_csv_auto | read_json | read_json_auto
   parquet_scan | parquet_metadata | parquet_schema | query
   ```

Comment stripping before checks 5–6:
```python
no_comments = re.sub(r"--[^\n]*", "", sql)
no_comments = re.sub(r"/\*.*?\*/", "", no_comments, flags=re.DOTALL)
```

Return contract: either `→ None` (raises on failure) or `→ str` (returns cleaned SQL). Both are acceptable.

### Connection management

| Capability | Contract |
|------------|----------|
| **Create/get** | Accept `output_dir: Path`, return a DuckDB connection with entity views registered. |
| **View registration** | Each entity in `SCHEMAS` gets a `CREATE VIEW` backed by `read_parquet(path)`. |
| **Invalidation** | `invalidate_connection(output_dir)` — close and evict cached connection (call after writes). |
| **Thread safety** | Connection cache access SHOULD be protected by a lock. |

### Query execution

| Capability | Contract |
|------------|----------|
| **execute** | Accept SQL + optional row limit. Return results (format varies: markdown, list[dict], structured tuple). |
| **Error handling** | Catch DuckDB errors, wrap in `QueryError` with actionable messages. |

---

## Exceptions

Both brains define these in `exceptions.py`:

| Exception | Meaning |
|-----------|---------|
| `QueryError` | SQL validation failure or DuckDB execution error. |
| `DataStaleError` | Schema mismatch or missing Parquet files. |

Brain-specific exceptions (e.g., `WineNotFoundError`, `RecipeNotFoundError`) extend beyond this base set.

---

## Porting checklist

When fixing a bug in one brain's writer or query layer, check:

1. Does the same pattern exist in the other brain?
2. Is the fix applicable (same contract point)?
3. Port it, adapt naming, add a test.

Key diff points for manual comparison:
- `cellarbrain/src/cellarbrain/writer.py` ↔ `recipebrain/src/recipebrain/writer.py`
- `cellarbrain/src/cellarbrain/query.py` (lines 150–180: patterns, 416–460: validate_sql)
- `recipebrain/src/recipebrain/query.py` (lines 32–45: patterns, 96–120: validate_sql)
