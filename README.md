# mkpipe-extractor-sqlite

SQLite extractor plugin for [MkPipe](https://github.com/mkpipe-etl/mkpipe). Reads SQLite database tables via JDBC.

## Documentation

For more detailed documentation, please visit the [GitHub repository](https://github.com/mkpipe-etl/mkpipe).

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

---

## Connection Configuration

```yaml
connections:
  sqlite_source:
    variant: sqlite
    database: /full/path/to/mydb.db
```

---

## Table Configuration

```yaml
pipelines:
  - name: sqlite_to_pg
    source: sqlite_source
    destination: pg_target
    tables:
      - name: users
        target_name: stg_users
        replication_method: full
```

### Incremental Replication

```yaml
      - name: events
        target_name: stg_events
        replication_method: incremental
        iterate_column: updated_at
        iterate_column_type: datetime
```

### Custom SQL

```yaml
      - name: events
        target_name: stg_events
        replication_method: full
        custom_query: "SELECT id, user_id, event_type FROM events WHERE {query_filter}"
```

---

## Performance Notes

- SQLite is a file-based database and does not support concurrent connections — parallel JDBC reads (`partitions_count`) are not meaningful and may cause lock contention.
- For large SQLite databases, keep `fetchsize` moderate (10,000–50,000).
- SQLite is best suited for small-to-medium datasets (< a few hundred MB). For large analytical workloads, consider migrating to a proper RDBMS.

---

## All Table Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `name` | string | required | SQLite table name |
| `target_name` | string | required | Destination table name |
| `replication_method` | `full` / `incremental` | `full` | Replication strategy |
| `iterate_column` | string | — | Column used for incremental watermark |
| `iterate_column_type` | `int` / `datetime` | — | Type of `iterate_column` |
| `fetchsize` | int | `100000` | Rows per JDBC fetch |
| `custom_query` | string | — | Override SQL with `{query_filter}` placeholder |
| `custom_query_file` | string | — | Path to SQL file (relative to `sql/` dir) |
| `tags` | list | `[]` | Tags for selective pipeline execution |
| `pass_on_error` | bool | `false` | Skip table on error instead of failing |



