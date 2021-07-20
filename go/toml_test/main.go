package main

import (
	"fmt"
	"log"
	"os"

	"github.com/BurntSushi/toml"
	containerd_config "github.com/containerd/containerd/services/server/config"
)

type TestPlugin struct {
	Foo string
	Bar string
}

func main() {
	fmt.Println("Hello world")

	var config containerd_config.Config

	_, err := toml.DecodeFile("./config.toml", &config)
	if err != nil {
		log.Fatal(err)
	}

	// rewrite the grpc.address
	config.GRPC.Address = "/foo/bar/baz"

	// stash hints to the new stuff in the plugins.footest
	config.Plugins["footest"] = TestPlugin{
		Foo: "foo",
		Bar: "bar",
	}

	src, err := os.OpenFile("./new.toml", os.O_RDWR, 0644)
	if err != nil {
		log.Fatal(err)
	}
	defer src.Close()

	toml.NewEncoder(src).Encode(config)
}
