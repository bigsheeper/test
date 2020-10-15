package main

import (
	"context"
	"encoding/json"
	"fmt"
	"github.com/apache/pulsar/pulsar-client-go/pulsar"
	"log"
	"math"
	"os"
	"sync"
	"time"
)

type Tester struct {
	testConfig TestConfig
	client     *pulsar.Client
	producer   *pulsar.Producer

	message    []byte
	msgCounter MsgCounter
	InsertLogs []InsertLog
}

type TestConfig struct {
	PulsarUrl    string
	PulsarTopic  string
	LogWritePath string

	VectorDims        []int
	TotalDataSizeInGB int
}

type MsgCounter struct {
	InsertCounter int
	InsertTime    time.Time
}

type InsertLog struct {
	VectorDim              int
	TotalDataSizeInGB      int
	MsgLength              int
	DurationInMilliseconds int64
	SpeedInCounter         float64
	SpeedInBytes           float64
}

func (t *Tester) InitClient() {
	client, err := pulsar.NewClient(pulsar.ClientOptions{
		URL: "pulsar://localhost:6650",
	})
	if err != nil {
		log.Fatalf("Could not instantiate Pulsar client: %v", err)
	}

	t.client = &client
}

func (t *Tester) InitProducer() {
	producer, err := (*t.client).CreateProducer(pulsar.ProducerOptions{
		Topic: "my-topic",
	})

	if err != nil {
		log.Fatalf("Could not instantiate Pulsar client: %v", err)
	}

	t.producer = &producer
}

func (t *Tester) InitMessage() {

}

func (t *Tester) GenerateLog(length int, dim int) {
	t.msgCounter.InsertCounter += length
	timeNow := time.Now()
	duration := timeNow.Sub(t.msgCounter.InsertTime)
	speedInCounter := float64(length) / duration.Seconds()
	speedInBytes := float64(length*dim*4) / duration.Seconds()

	insertLog := InsertLog{
		VectorDim:              dim,
		TotalDataSizeInGB:      t.testConfig.TotalDataSizeInGB,
		MsgLength:              length,
		DurationInMilliseconds: duration.Milliseconds(),
		SpeedInCounter:         speedInCounter,
		SpeedInBytes:           speedInBytes,
	}

	t.InsertLogs = append(t.InsertLogs, insertLog)
	t.msgCounter.InsertTime = timeNow
}

func (t *Tester) WriteLog() {
	fileName := t.testConfig.LogWritePath

	f, err := os.OpenFile(fileName, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		log.Fatal(err)
	}

	// write logs
	for _, insertLog := range t.InsertLogs {
		insertLogJson, err := json.Marshal(&insertLog)
		if err != nil {
			log.Fatal(err)
		}

		writeString := string(insertLogJson) + "\n"
		fmt.Println(writeString)

		_, err2 := f.WriteString(writeString)
		if err2 != nil {
			log.Fatal(err2)
		}
	}

	// reset InsertLogs buffer
	t.InsertLogs = make([]InsertLog, 0)

	err = f.Close()
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("write log done")
}

func (t *Tester) sendMsg(wg *sync.WaitGroup) {
	if err := (*t.producer).Send(context.Background(), pulsar.ProducerMessage{
		Payload: t.message,
	}); err != nil {
		log.Fatal(err)
	}
	wg.Done()
}

func (t *Tester) Close() {
	err := (*t.producer).Close()
	if err != nil {
		log.Fatal(err)
	}
	err = (*t.client).Close()
	if err != nil {
		log.Fatal(err)
	}
}

func (t *Tester) Run(dim int) {
	totalDataSize := t.testConfig.TotalDataSizeInGB * 1024 * 1024 * 1024
	dataSizePerMsg := dim * 4
	sendTimes := totalDataSize / dataSizePerMsg

	t.msgCounter.InsertTime = time.Now()

	wg := sync.WaitGroup{}
	wg.Add(sendTimes)

	for i := 0; i < sendTimes; i++ {
		go t.sendMsg(&wg)
	}

	wg.Wait()

	t.GenerateLog(sendTimes, dim)
}

func main() {
	vectorDims := []int{
		int(math.Pow(2, 5)),
		int(math.Pow(2, 7)),
		int(math.Pow(2, 9)),
		int(math.Pow(2, 11)),
		int(math.Pow(2, 13)),
		int(math.Pow(2, 15)),
		int(math.Pow(2, 17)),
		int(math.Pow(2, 19)),
		int(math.Pow(2, 21)),
	}

	conf := TestConfig{
		PulsarUrl:         "pulsar://localhost:6650",
		PulsarTopic:       "my-test",
		LogWritePath:      "/tmp/throughput/test_result.txt",
		VectorDims:        vectorDims,
		TotalDataSizeInGB: 1,
	}

	tester := Tester{
		testConfig: conf,
	}

	tester.InitClient()
	tester.InitProducer()
	tester.InitMessage()

	for _, dim := range tester.testConfig.VectorDims {
		fmt.Println("test dim", dim)
		tester.Run(dim)
	}

	tester.Close()
}
