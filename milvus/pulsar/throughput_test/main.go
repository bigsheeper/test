package main

import (
	"context"
	"encoding/binary"
	"encoding/json"
	"fmt"
	"github.com/apache/pulsar-client-go/pulsar"
	"log"
	"math"
	"math/rand"
	"os"
	"strconv"
	"sync"
	"time"
)

type Tester struct {
	testConfig TestConfig
	client     *pulsar.Client
	producers  []pulsar.Producer

	CurrentDim int

	message    []byte
	msgCounter MsgCounter
	InsertLogs []InsertLog
}

type TestConfig struct {
	PulsarUrl    string
	PulsarTopic  string
	LogWritePath string

	ProducerNum       int
	VectorDims        []int
	TotalDataSizeInGB float32
}

type MsgCounter struct {
	InsertCounter int
	InsertTime    time.Time
}

type InsertLog struct {
	VectorDim              int
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
	for i := 0; i < t.testConfig.ProducerNum; i++ {
		producer, err := (*t.client).CreateProducer(pulsar.ProducerOptions{
			Topic: t.testConfig.PulsarTopic + strconv.FormatInt(int64(i), 10),
		})
		if err != nil {
			log.Fatalf("Could not instantiate Pulsar client: %v", err)
		}
		t.producers = append(t.producers, producer)
	}
}

func (t *Tester) GenerateMessage() {
	vec := make([]float32, 0)
	t.message = make([]byte, 0)

	for i := 0; i < t.CurrentDim; i++ {
		vec = append(vec, rand.Float32())
	}

	for _, ele := range vec {
		buf := make([]byte, 4)
		binary.LittleEndian.PutUint32(buf, math.Float32bits(ele))
		t.message = append(t.message, buf...)
	}
}

func (t *Tester) GenerateLog(length int) {
	t.msgCounter.InsertCounter += length
	timeNow := time.Now()
	duration := timeNow.Sub(t.msgCounter.InsertTime)
	speedInCounter := float64(length) / duration.Seconds()
	speedInBytes := float64(length*t.CurrentDim*4) / duration.Seconds()

	insertLog := InsertLog{
		VectorDim:              t.CurrentDim,
		MsgLength:              length,
		DurationInMilliseconds: duration.Milliseconds(),
		SpeedInCounter:         speedInCounter,
		SpeedInBytes:           speedInBytes,
	}

	t.InsertLogs = append(t.InsertLogs, insertLog)
	t.msgCounter.InsertTime = timeNow
	fmt.Println(insertLog)
}

func (t *Tester) WriteLog() {
	fileName := t.testConfig.LogWritePath
	fileName += "throughput_test_result_"
	fileName += strconv.FormatInt(int64(t.testConfig.TotalDataSizeInGB), 10)
	fileName += "_" + strconv.FormatInt(int64(t.testConfig.ProducerNum), 10)
	fileName += ".txt"

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

func (t *Tester) sendMsg(wg *sync.WaitGroup, index int) {
	if _, err := t.producers[index].Send(context.Background(), &pulsar.ProducerMessage{
		Payload: t.message,
	}); err != nil {
		log.Fatal(err)
	}
	wg.Done()
}

func (t *Tester) Close() {
	for i := 0; i < t.testConfig.ProducerNum; i++ {
		t.producers[i].Close()
	}
	(*t.client).Close()
}

func (t *Tester) Run(dim int) {
	t.CurrentDim = dim
	t.GenerateMessage()

	totalDataSize := int(t.testConfig.TotalDataSizeInGB * 1024 * 1024 * 1024)
	dataSizePerMsg := dim * 4
	sendTimes := totalDataSize / (dataSizePerMsg)

	t.msgCounter.InsertTime = time.Now()

	count := 0
	for {
		if count >= sendTimes {
			break
		}
		wg := sync.WaitGroup{}
		wg.Add(t.testConfig.ProducerNum)
		count += t.testConfig.ProducerNum
		for i := 0; i < t.testConfig.ProducerNum; i++ {
			go t.sendMsg(&wg, i)
		}
		wg.Wait()
	}

	t.GenerateLog(count)
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
		LogWritePath:      "/tmp/",
		ProducerNum:       1024,
		VectorDims:        vectorDims,
		TotalDataSizeInGB: 8,
	}

	tester := Tester{
		testConfig: conf,
	}

	tester.InitClient()
	tester.InitProducer()

	for _, dim := range tester.testConfig.VectorDims {
		fmt.Println("test dim", dim)
		tester.Run(dim)
	}

	tester.WriteLog()
	tester.Close()
}
