# AWS Pulsar Throughput Test Result

向量维度由 2^5 ~ 2^19 进行测试，每个维度测试 1 次。

```txt
单机测试结果：
{"VectorDim":32,"MsgLength":8388608,"DurationInMilliseconds":113166,"SpeedInCounter":74126.09050189823,"SpeedInBytes":9488139.584242973}
{"VectorDim":128,"MsgLength":2097152,"DurationInMilliseconds":33220,"SpeedInCounter":63128.01316450618,"SpeedInBytes":32321542.740227163}
{"VectorDim":512,"MsgLength":524288,"DurationInMilliseconds":27533,"SpeedInCounter":19041.50924438171,"SpeedInBytes":38997010.93249374}
{"VectorDim":2048,"MsgLength":131072,"DurationInMilliseconds":24322,"SpeedInCounter":5388.826035731458,"SpeedInBytes":44145262.88471211}
{"VectorDim":8192,"MsgLength":32768,"DurationInMilliseconds":22361,"SpeedInCounter":1465.3552005280612,"SpeedInBytes":48016759.21090351}
{"VectorDim":32768,"MsgLength":8192,"DurationInMilliseconds":17656,"SpeedInCounter":463.9641695387589,"SpeedInBytes":60812711.629784204}
{"VectorDim":131072,"MsgLength":2048,"DurationInMilliseconds":21539,"SpeedInCounter":95.08132921562999,"SpeedInBytes":49849999.93180422}
{"VectorDim":524288,"MsgLength":1024,"DurationInMilliseconds":39228,"SpeedInCounter":26.103693273537992,"SpeedInBytes":54743412.55598675}

 
2 节点测试结果：
{"VectorDim":32,"MsgLength":8388608,"DurationInMilliseconds":119577,"SpeedInCounter":70151.9387383627,"SpeedInBytes":8979448.158510426}
{"VectorDim":128,"MsgLength":2097152,"DurationInMilliseconds":36464,"SpeedInCounter":57512.02704498223,"SpeedInBytes":29446157.8470309}
{"VectorDim":512,"MsgLength":524288,"DurationInMilliseconds":18211,"SpeedInCounter":28788.94084820994,"SpeedInBytes":58959750.857133955}
{"VectorDim":2048,"MsgLength":131072,"DurationInMilliseconds":16400,"SpeedInCounter":7991.933528423567,"SpeedInBytes":65469919.46484586}
{"VectorDim":8192,"MsgLength":32768,"DurationInMilliseconds":16251,"SpeedInCounter":2016.287549659065,"SpeedInBytes":66069710.42722824}
{"VectorDim":32768,"MsgLength":8192,"DurationInMilliseconds":37069,"SpeedInCounter":220.992628350191,"SpeedInBytes":28965945.783116236}
{"VectorDim":131072,"MsgLength":2048,"DurationInMilliseconds":32068,"SpeedInCounter":63.86260830549822,"SpeedInBytes":33482399.18327305}
{"VectorDim":524288,"MsgLength":1024,"DurationInMilliseconds":77451,"SpeedInCounter":13.221178983724862,"SpeedInBytes":27726821.94807656}
```
