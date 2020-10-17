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

const TotalDataSizeInGB = 0.5
const Loop = 10
const URL = "pulsar://localhost:6650"

type Tester struct {
	testConfig TestConfig
	client     *pulsar.Client
	producers  []pulsar.Producer

	message    []byte
	msgCounter MsgCounter
	InsertLogs []InsertLog
}

type TestConfig struct {
	PulsarUrl    string
	PulsarTopic  string
	LogWritePath string

	ProducerNum       int
	TopicNum          int
	Dim               int
	TotalDataSizeInGB float32
}

type MsgCounter struct {
	InsertCounter int
	InsertTime    time.Time
}

type InsertLog struct {
	TopicNum               int
	ProducerNum            int
	VectorDim              int
	MsgLength              int
	DurationInMilliseconds int64
	SpeedInCounter         float64
	SpeedInBytes           float64
}

func (t *Tester) InitClient() {
	client, err := pulsar.NewClient(pulsar.ClientOptions{
		URL: t.testConfig.PulsarUrl,
	})
	if err != nil {
		log.Fatalf("Could not instantiate Pulsar client: %v", err)
	}

	t.client = &client
}

func (t *Tester) InitProducer() {
	topicsPerProducer := t.testConfig.ProducerNum / t.testConfig.TopicNum
	for i := 0; i < t.testConfig.TopicNum; i++ {
		for j := 0; j < topicsPerProducer; j++ {
			producer, err := (*t.client).CreateProducer(pulsar.ProducerOptions{
				Topic: t.testConfig.PulsarTopic + strconv.FormatInt(int64(i), 10),
			})
			if err != nil {
				log.Fatalf("Could not instantiate Pulsar client: %v", err)
			}
			t.producers = append(t.producers, producer)
		}
	}
}

func (t *Tester) GenerateMessage() {
	vec := make([]float32, 0)
	t.message = make([]byte, 0)

	for i := 0; i < t.testConfig.Dim; i++ {
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
	speedInBytes := float64(length*t.testConfig.Dim*4) / duration.Seconds()

	insertLog := InsertLog{
		TopicNum:               t.testConfig.TopicNum,
		ProducerNum:            t.testConfig.ProducerNum,
		VectorDim:              t.testConfig.Dim,
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
	t.producers = make([]pulsar.Producer, 0)
	(*t.client).Close()
	t.client = nil
}

func (t *Tester) Run() {
	t.GenerateMessage()

	totalDataSize := int(t.testConfig.TotalDataSizeInGB * 1024 * 1024 * 1024)
	dataSizePerMsg := t.testConfig.Dim * 4
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

func (t *Tester) RunTest(topicNum int, producerNum int, dim int) {
	t.testConfig.TopicNum = topicNum
	t.testConfig.ProducerNum = producerNum
	t.testConfig.Dim = dim

	t.InitClient()
	t.InitProducer()

	fmt.Println("test topicNum:", topicNum, "producerNum:", producerNum, "dim:", dim)
	t.Run()

	t.Close()
}

func TestTopicsNum() {
	conf := TestConfig{
		PulsarUrl:    URL,
		PulsarTopic:  "my-test",
		LogWritePath: "/tmp/throughput_topic_test.txt",

		TotalDataSizeInGB: TotalDataSizeInGB,
	}

	tester := Tester{
		testConfig: conf,
	}

	for i := 0; i < Loop; i++{
		tester.RunTest(int(math.Pow(2, float64(i))), 1024, 512)
	}

	tester.WriteLog()
}

func TestProducersNum() {
	conf := TestConfig{
		PulsarUrl:    URL,
		PulsarTopic:  "my-test",
		LogWritePath: "/tmp/throughput_topic_test.txt",

		TotalDataSizeInGB: TotalDataSizeInGB,
	}

	tester := Tester{
		testConfig: conf,
	}

	for i := 0; i < Loop; i++{
		tester.RunTest(1, int(math.Pow(2, float64(i))), 512)
	}
}

func TestDims() {
	conf := TestConfig{
		PulsarUrl:    URL,
		PulsarTopic:  "my-test",
		LogWritePath: "/tmp/throughput_topic_test.txt",

		TotalDataSizeInGB: TotalDataSizeInGB,
	}

	tester := Tester{
		testConfig: conf,
	}

	for i := 0; i < Loop; i++{
		tester.RunTest(1024, 1024, int(math.Pow(2, float64(i))))
	}
}

func main() {
	TestTopicsNum()
}
