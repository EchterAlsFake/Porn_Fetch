package main

import (
	"database/sql"

	"github.com/mattn/go-sqlite3"
	"github.com/pocketbase/dbx"
)

// Use SQLite compiled against Android's libc. The default modernc driver uses
// raw Linux syscalls, including lstat on amd64, which Android seccomp forbids.
func init() {
	sql.Register("pornfetch_sqlite3", &sqlite3.SQLiteDriver{
		ConnectHook: func(conn *sqlite3.SQLiteConn) error {
			// Keep PocketBase's defaults on every pooled connection. Set the busy
			// timeout before WAL so opening concurrent connections waits for locks.
			_, err := conn.Exec(`
				PRAGMA busy_timeout = 10000;
				PRAGMA journal_mode = WAL;
				PRAGMA journal_size_limit = 200000000;
				PRAGMA synchronous = NORMAL;
				PRAGMA foreign_keys = ON;
				PRAGMA temp_store = MEMORY;
				PRAGMA cache_size = -32000;
			`, nil)
			return err
		},
	})
	dbx.BuilderFuncMap["pornfetch_sqlite3"] = dbx.BuilderFuncMap["sqlite3"]
}

func connectDatabase(path string) (*dbx.DB, error) {
	return dbx.Open("pornfetch_sqlite3", path)
}
