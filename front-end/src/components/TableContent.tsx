type Props = {
  title: string;
  value: string;
  normalRange: string;
  unit: string;
};

function TableContent({ title, value, normalRange, unit }: Props) {
  const [min, max] = normalRange.split(" - ").map(Number);
  Number(value) >= min && Number(value) <= max;

  return (
    <>
      <tr className="item-row-table">
        <td className="px-5 py-5 border-b  text-center  border-gray-200 bg-white text-base">
          <p className="text-gray-900 whitespace-no-wrap">{title}</p>
        </td>
        <td className="px-5 py-5 border-b  text-center border-gray-200 bg-white text-base">
          <span
            className={`relative inline-block w-full px-3 py-1 font-semibold  leading-tight ${
              Number(value) >= min && Number(value) <= max
                ? "text-green-900"
                : "text-red-800"
            }`}
          >
            <span
              aria-hidden
              className={`absolute inset-0  rounded-xl ${
                Number(value) >= min && Number(value) <= max
                  ? "bg-green-900/20"
                  : "bg-red-800/20"
              }`}
            ></span>
            <span className="relative">{value}</span>
          </span>
        </td>
        <td className="px-5 py-5 border-b  text-center border-gray-200 bg-white text-base">
          <p className="text-gray-900 whitespace-no-wrap">{normalRange}</p>
        </td>
        <td className="px-5 py-5 border-b  text-center border-gray-200 bg-white text-base">
          <p className="text-gray-600 whitespace-no-wrap">{unit}</p>
        </td>
      </tr>
    </>
  );
}

export default TableContent;
