const decodeToStr = function (arr) {
  let decoder = new TextDecoder("utf-8");
  str = decoder.decode(new Uint8Array(arr));
  arr.splice(0, arr.length);
  return str;
};

function processString(str, success, failed) {
  let i = 0;
  while (i < str.length) {
    // 检查是否为转义序列（\开头后跟三个数字）
    if (
      str[i] === "\\" &&
      /[0-9]/.test(str[i + 1]) &&
      /[0-9]/.test(str[i + 2]) &&
      /[0-9]/.test(str[i + 3])
    ) {
      // 条件A：处理转义序列
      const code = parseInt(str.slice(i + 1, i + 4), 10);
      success && success(code);
      i += 4; // 跳过 \ddd
    } else {
      // 条件B：处理普通字符
      failed && failed(str[i]);
      i++; // 移动到下一个字符
    }
  }
};

function toNormalStr(input)
{
	let finalStr = "";
	let tmpArr = [];
	processString(input,(code)=>{
		tmpArr.push(code);
		if(tmpArr.length === 3)
		{
			finalStr += decodeToStr(tmpArr);
		}
	},(s)=>{
		finalStr += s;
	});
	return finalStr;
}


globalThis.decodeToStr = decodeToStr;
globalThis.processString = processString;
globalThis.toNormalStr = toNormalStr;
