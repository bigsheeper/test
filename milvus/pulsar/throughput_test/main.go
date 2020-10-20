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

const TestTimes = 10
const TotalDataSizeInGB = 0.5
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

func (t *Tester) WriteLog(insertLogs []InsertLog) {
	fileName := t.testConfig.LogWritePath

	f, err := os.OpenFile(fileName, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		log.Fatal(err)
	}

	// write logs
	for _, insertLog := range insertLogs {
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
	// t.InsertLogs = make([]InsertLog, 0)

	err = f.Close()
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("write log done")
}

func (t *Tester) WriteSymbol(s string) {
	fileName := t.testConfig.LogWritePath

	f, err := os.OpenFile(fileName, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		log.Fatal(err)
	}

	_, err2 := f.WriteString(s + "\n")
	if err2 != nil {
		log.Fatal(err2)
	}

	err = f.Close()
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("write symbol done")
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

// return [Average, Max, Min] InsertLog
func GetStatisticTestResult(insertLogs []InsertLog) (InsertLog, InsertLog, InsertLog) {
	var totalDuration int64 = 0
	var totalSpeedInCounter float64 = 0
	var totalSpeedInBytes float64 = 0

	var maxInsert = InsertLog{
		SpeedInBytes: -1,
	}
	var minInsert = InsertLog{
		SpeedInBytes: math.MaxFloat64,
	}

	for _, insertLog := range insertLogs {
		totalDuration += insertLog.DurationInMilliseconds
		totalSpeedInCounter += insertLog.SpeedInCounter
		totalSpeedInBytes += insertLog.SpeedInBytes
		// max
		if insertLog.SpeedInBytes > maxInsert.SpeedInBytes {
			maxInsert = insertLog
		}
		// min
		if insertLog.SpeedInBytes < minInsert.SpeedInBytes {
			minInsert = insertLog
		}
	}

	avg := InsertLog{
		TopicNum: insertLogs[0].TopicNum,
		ProducerNum: insertLogs[0].ProducerNum,
		VectorDim: insertLogs[0].VectorDim,
		MsgLength: insertLogs[0].MsgLength,
		DurationInMilliseconds: totalDuration / int64(len(insertLogs)),
		SpeedInCounter: totalSpeedInCounter / float64(len(insertLogs)),
		SpeedInBytes: totalSpeedInBytes / float64(len(insertLogs)),
	}

	return avg, maxInsert, minInsert
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

	tester.WriteSymbol("-------------- begin test --------------")
	avgInsertLogs := make([]InsertLog, 0)
	maxInsertLogs := make([]InsertLog, 0)
	minInsertLogs := make([]InsertLog, 0)
	for i := 0; i < 10; i++{
		tester.InsertLogs = make([]InsertLog, 0)
		for j := 0; j < TestTimes; j++ {
			tester.RunTest(int(math.Pow(2, float64(i))), 512, 512)
		}
		var avg, max, min = GetStatisticTestResult(tester.InsertLogs)
		avgInsertLogs = append(avgInsertLogs, avg)
		maxInsertLogs = append(maxInsertLogs, max)
		minInsertLogs = append(minInsertLogs, min)
	}

	tester.WriteSymbol("*************** total result average ***************")
	tester.WriteLog(avgInsertLogs)

	tester.WriteSymbol("*************** total result max ***************")
	tester.WriteLog(maxInsertLogs)

	tester.WriteSymbol("*************** total result min ***************")
	tester.WriteLog(minInsertLogs)
}

func TestProducersNum() {
	conf := TestConfig{
		PulsarUrl:    URL,
		PulsarTopic:  "my-test",
		LogWritePath: "/tmp/throughput_producer_test.txt",

		TotalDataSizeInGB: TotalDataSizeInGB,
	}

	tester := Tester{
		testConfig: conf,
	}

	tester.WriteSymbol("-------------- begin test --------------")
	avgInsertLogs := make([]InsertLog, 0)
	maxInsertLogs := make([]InsertLog, 0)
	minInsertLogs := make([]InsertLog, 0)
	for i := 7; i < 14; i++{
		tester.InsertLogs = make([]InsertLog, 0)
		for j := 0; j < TestTimes; j++ {
			tester.RunTest(4, int(math.Pow(2, float64(i))), 512)
		}
		var avg, max, min = GetStatisticTestResult(tester.InsertLogs)
		avgInsertLogs = append(avgInsertLogs, avg)
		maxInsertLogs = append(maxInsertLogs, max)
		minInsertLogs = append(minInsertLogs, min)
	}

	tester.WriteSymbol("*************** total result average ***************")
	tester.WriteLog(avgInsertLogs)

	tester.WriteSymbol("*************** total result max ***************")
	tester.WriteLog(maxInsertLogs)

	tester.WriteSymbol("*************** total result min ***************")
	tester.WriteLog(minInsertLogs)
}

func TestDims() {
	conf := TestConfig{
		PulsarUrl:    URL,
		PulsarTopic:  "my-test",
		LogWritePath: "/tmp/throughput_dim_benchmark.txt",

		TotalDataSizeInGB: TotalDataSizeInGB,
	}

	tester := Tester{
		testConfig: conf,
	}

	tester.WriteSymbol("-------------- begin test --------------")
	avgInsertLogs := make([]InsertLog, 0)
	maxInsertLogs := make([]InsertLog, 0)
	minInsertLogs := make([]InsertLog, 0)
	for i := 5; i < 20; i++{
		tester.InsertLogs = make([]InsertLog, 0)
		for j := 0; j < TestTimes; j++ {
			tester.RunTest(128, 256, int(math.Pow(2, float64(i))))
		}
		tester.WriteSymbol("-------------- dim " + strconv.FormatInt(int64(math.Pow(2, float64(i))), 10) + " --------------")
		tester.WriteLog(tester.InsertLogs)
		var avg, max, min = GetStatisticTestResult(tester.InsertLogs)
		avgInsertLogs = append(avgInsertLogs, avg)
		maxInsertLogs = append(maxInsertLogs, max)
		minInsertLogs = append(minInsertLogs, min)
	}

	tester.WriteSymbol("*************** total result average ***************")
	tester.WriteLog(avgInsertLogs)

	tester.WriteSymbol("*************** total result max ***************")
	tester.WriteLog(maxInsertLogs)

	tester.WriteSymbol("*************** total result min ***************")
	tester.WriteLog(minInsertLogs)
}

func main() {
	//TestTopicsNum()
	//TestProducersNum()
	TestDims()
}
