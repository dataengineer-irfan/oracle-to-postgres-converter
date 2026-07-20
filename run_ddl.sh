#!/bin/bash
for f in /tmp/ddl/*.sql; do
    if [ "$f" != "/tmp/ddl/all_fk_constraints.sql" ]; then
        psql -U postgres -d postgres -f "$f" > /dev/null 2>&1
    fi
done
psql -U postgres -d postgres -f /tmp/ddl/all_fk_constraints.sql > /dev/null 2>&1
