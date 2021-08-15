package main

import (
	"fmt"
	"log"
	"os"

	"github.com/pelletier/go-toml"
)

type TestPlugin struct {
	Foo string
	Bar string
}

func main() {
	fmt.Println("Hello world")
	config, err := toml.LoadFile("./config.toml")
	if err != nil {
		log.Fatalf("Error %s", err)
	}

	add := config.Get("grpc.address")
	config.Set("grpc.address", fmt.Sprintf("%s.real", add))

	config.Set("plugins.tanium.real_sock", "fsa")
	config.Set("plugins.tanium.proxy_sock", "fsa")

	src, err := os.OpenFile("./new.toml", os.O_RDWR, 0644)
	if err != nil {
		log.Fatal(err)
	}
	defer src.Close()


	config.WriteTo(src)
}
