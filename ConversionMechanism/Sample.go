
package main
import (
	"encoding/json"
	"fmt"
	"strconv"
	"github.com/hyperledger/fabric/core/chaincode/shim"
	pb "github.com/hyperledger/fabric/protos/peer"
)
type Sample struct{}
type SampleStruct1 struct {
	Value1 string `json:"value1"`
	Value2 int    `json:"value2"`
	Value3 string `json:"value3"`
}
type SampleStruct2 struct {
	Value4 string `json:"value4"`
	Value5 bool   `json:"value5"`
}
type IndepentedStruct struct {
	Value6 bool    `json:"value6"`
	Value7 float64 `json:"value7"`
	Value8 string  `json:"value8"`
}
func (c *Sample) Init(stub shim.ChaincodeStubInterface) pb.Response {
	return shim.Success(nil)
}
func (c *Sample) Invoke(stub shim.ChaincodeStubInterface) pb.Response {
	function, args := stub.GetFunctionAndParameters()
	switch function {
	case "setSampleStruct1SampleStruct2":
		return c.setSampleStruct1SampleStruct2(stub, args)
	case "setIndepentedStruct":
		return c.setIndepentedStruct(stub, args)
	case "updateSampleStruct1":
		return c.updateSampleStruct1(stub, args)
	case "updateIndepentedStruct":
		return c.updateIndepentedStruct(stub, args)
	}
	return shim.Error("Received unknown function invocation")
}
func (c *Sample) setSampleStruct1SampleStruct2(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	var err error
	value1 := args[0]
	value2, err := strconv.Atoi(args[1])
	value3 := args[2]
	value4 := args[3]
	value5, err := strconv.ParseBool(args[4])
	sampleStruct2 := &SampleStruct2{value4, value5}
	sampleStruct1 := &SampleStruct1{value1, value2, value3}
	sampleStruct1JSONasBytes, err := json.Marshal(sampleStruct1)
	if err != nil {
		return shim.Error(err.Error())
	}
	sampleStruct2JSONasBytes, err := json.Marshal(sampleStruct2)
	if err != nil {
		return shim.Error(err.Error())
	}
	err = stub.PutState(value1, sampleStruct1JSONasBytes)
	if err != nil {
		return shim.Error(err.Error())
	}
	err = stub.PutState(value4, sampleStruct2JSONasBytes)
	if err != nil {
		return shim.Error(err.Error())
	}
	return shim.Success(nil)
}

func (c *Sample) updateSampleStruct1(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	var err error
	value1 := args[0]
	value3 := args[1]
	InfoBytes, err := stub.GetState(value1)
	if err != nil {
		return shim.Error("Failed to get info:" + err.Error())
	} else if InfoBytes == nil {
		return shim.Error("Not found")
	}
	sampleStruct1 := SampleStruct1{}
	err = json.Unmarshal(InfoBytes, &sampleStruct1)
	if err != nil {
		return shim.Error(err.Error())
	}
	sampleStruct1.Value3 = value3
	sampleStruct1InfoJSONasBytes, _ := json.Marshal(sampleStruct1)
	err = stub.PutState(value1, sampleStruct1InfoJSONasBytes)
	if err != nil {
		return shim.Error(err.Error())
	}
	fmt.Println("- Update info (success)")
	return shim.Success(nil)
}
func (c *Sample) setIndepentedStruct(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	var err error
	value6, err := strconv.ParseBool(args[0])
	value7, err := strconv.ParseFloat(args[1], 64)
	value8 := args[2]
	indepentedStruct := &IndepentedStruct{value6, value7, value8}
	indepentedStructJSONasBytes, err := json.Marshal(indepentedStruct)
	if err != nil {
		return shim.Error(err.Error())
	}
	err = stub.PutState(value8, indepentedStructJSONasBytes)
	if err != nil {
		return shim.Error(err.Error())
	}
	return shim.Success(nil)
}
func (c *Sample) updateIndepentedStruct(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	var err error
	value6, err := strconv.ParseBool(args[0])
	value7, err := strconv.ParseFloat(args[1], 64)
	value8 := args[2]
	InfoBytes, err := stub.GetState(value8)
	if err != nil {
		return shim.Error("Failed to get info:" + err.Error())
	} else if InfoBytes == nil {
		return shim.Error("Not found")
	}
	indepentedStruct := IndepentedStruct{}
	err = json.Unmarshal(InfoBytes, &indepentedStruct)
	if err != nil {
		return shim.Error(err.Error())
	}
	indepentedStruct.Value6 = value6
	indepentedStruct.Value7 = value7
	indepentedStructInfoJSONasBytes, _ := json.Marshal(indepentedStruct)
	err = stub.PutState(value8, indepentedStructInfoJSONasBytes)
	if err != nil {
		return shim.Error(err.Error())
	}
	fmt.Println("- Update info (success)")
	return shim.Success(nil)
}
func main() {
	err := shim.Start(new(Sample))
	if err != nil {
		fmt.Printf("Error starting chaincode sample: %s", err)
	}
}
