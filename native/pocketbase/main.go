// PocketBase's Android runtime, loaded in-process by Python through ctypes.
package main

/*
#include <stdlib.h>
*/
import "C"

import (
	"context"
	"encoding/json"
	"fmt"
	"net"
	"net/http"
	"sync"
	"time"
	"unsafe"

	"github.com/pocketbase/pocketbase/apis"
	"github.com/pocketbase/pocketbase/core"
	_ "github.com/pocketbase/pocketbase/migrations"
	"github.com/pocketbase/pocketbase/plugins/jsvm"
)

var lock sync.Mutex
var application *core.BaseApp
var server *http.Server

func result(url string, err error) *C.char {
	value := map[string]string{"endpoint": url}
	if err != nil {
		value["error"] = err.Error()
	}
	data, _ := json.Marshal(value)
	return C.CString(string(data))
}

//export PFStart
func PFStart(dataDir, migrationsDir, email, password *C.char) *C.char {
	lock.Lock()
	defer lock.Unlock()
	if application != nil {
		return result("", fmt.Errorf("PocketBase is already running"))
	}
	app := core.NewBaseApp(core.BaseAppConfig{DataDir: C.GoString(dataDir), DBConnect: connectDatabase})
	if err := jsvm.Register(app, jsvm.Config{MigrationsDir: C.GoString(migrationsDir), HooksFilesPattern: `a^`}); err != nil {
		return result("", err)
	}
	if err := app.Bootstrap(); err != nil {
		app.ClearBootstrap()
		return result("", err)
	}
	fail := func(err error) *C.char { app.ClearBootstrap(); return result("", err) }
	if err := app.RunAllMigrations(); err != nil {
		return fail(err)
	}
	account, err := app.FindAuthRecordByEmail("_superusers", C.GoString(email))
	if err != nil {
		collection, err := app.FindCollectionByNameOrId("_superusers")
		if err != nil {
			return fail(err)
		}
		account = core.NewRecord(collection)
		account.SetEmail(C.GoString(email))
	}
	account.SetPassword(C.GoString(password))
	if err := app.Save(account); err != nil {
		return fail(err)
	}
	router, err := apis.NewRouter(app)
	if err != nil {
		return fail(err)
	}
	mux, err := router.BuildMux()
	if err != nil {
		return fail(err)
	}
	listener, err := net.Listen("tcp4", "127.0.0.1:0")
	if err != nil {
		return fail(err)
	}
	server = &http.Server{Handler: mux, ReadHeaderTimeout: 10 * time.Second}
	application = app
	endpoint := "http://" + listener.Addr().String()
	go server.Serve(listener)
	return result(endpoint, nil)
}

//export PFStop
func PFStop() *C.char {
	lock.Lock()
	defer lock.Unlock()
	if application == nil {
		return result("", nil)
	}
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	err := server.Shutdown(ctx)
	if err != nil {
		server.Close()
	}
	if closeErr := application.ClearBootstrap(); err == nil {
		err = closeErr
	}
	application, server = nil, nil
	return result("", err)
}

//export PFFree
func PFFree(pointer unsafe.Pointer) { C.free(pointer) }

func main() {}
