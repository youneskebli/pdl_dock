import { useCallback, useEffect, useState } from "react";
import TableContent from "./TableContent";
import axios from "axios";

interface Cell {
  title: string;
  value: string;
  normalRange: string;
  unit: string;
}

interface Data {
    category: string,
    cells: Cell[]
}
const Data = {
  results: {
    category: "Laboratory",
    cells: [
        {
            title: "Sodium",
            value: "110.00",
            normalRange: "136.00-145.00",
            unit: "mEq/L"
        },
        {
            title: "Potassium",
            value: "8.00",
            normalRange: "3.50 - 5.10",
            unit: "mEq/L"
        },
        {
            title: "Chloride",
            value: "99.00",
            normalRange: "98.00 -107.00",
            unit: "mEq/L"
        },
        {
            title: "Bicarbonate",
            value: "25.00",
            normalRange: "22.00-28.00",
            unit: "mEq/L"
        },
        {
            title: "Calcium",
            value: "18.00",
            normalRange: "8.6 - 10.2",
            unit: "mg/dL"
        },
        {
            title: "Magnesium",
            value: "1.9",
            normalRange: "1.8 - 2.3",
            unit: "mg/dL"
        }
    ]
}
};

function Table() {
  const [data, setData] = useState<Data | null>();
  const [loading, setLoading] = useState(false);
  const [FetchData, setFetchData] = useState(false);

  const handleFetchData = useCallback(async () => {
    try {
      setLoading(true);
      const response = await axios.get("http://192.168.100.14:8081/structureocr?image=./image.jpeg");
      // const jsonArray = JSON.parse(response.data);
      setData(response.data);
      console.log(response.data)
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }, [FetchData]);
  useEffect(() => {
    if (FetchData) {
      handleFetchData();
    }
  }, [FetchData, handleFetchData]);
  if (loading) {
    return (
      <div className="w-full h-screen flex items-center justify-center">
        <p>...loading</p>
      </div>
    );
  }
  return (
    <main className="w-10/12 mx-auto h-full   ">
        <button
          onClick={() => setFetchData(true)}
          className="border border-gray-500 text-gray-500 rounded-lg max-w-[180px] px-4 py-2 hover:underline"
        >
          Get Data{" "}
      </button>
      {/* <button onClick={fetchData}>Get Data </button> */}
      <h1 className=" w-full    capitalize text-3xl font-bold leading-tight  text-[#2b2a2a]  ">
        {data && data?.category}
      </h1>
      <div className="inline-block min-w-full py-2 align-middle md:px-6 lg:px-8">
        <table className="mt-10   min-w-full leading-normal  ">
          <thead className="border-y border-y-slate-300 ">
            <tr className="text-slate-400 font-normal">
              <th
                scope="col"
                className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-center text-lg font-semibold text-gray-700 uppercase tracking-wider"
              >
                Title
              </th>
              <th
                scope="col"
                className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-center text-lg font-semibold text-gray-700 uppercase tracking-wider"
              >
                Value
              </th>
              <th
                scope="col"
                className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-center text-lg font-semibold text-gray-700 uppercase tracking-wider"
              >
                Normal range
              </th>
              <th
                scope="col"
                className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-center text-lg font-semibold text-gray-700 uppercase tracking-wider"
              >
                Unit
              </th>
            </tr>
          </thead>

          <tbody className="w-full h-full divide-y divide-slate-100 bg-white overflow-hidden">
            {Array.isArray(data?.cells) && data?.cells.map((item, index) => (
              <TableContent key={index} {...item} />
            ))}
          </tbody>
        </table>
      </div>
    </main>
  );
}

export default Table;
