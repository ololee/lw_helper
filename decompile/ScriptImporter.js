const fs = require('fs');
const path = require('path');
const crc32 = require('crc').crc32;

function getAllFiles(dirPath)
{
    let fileList = [];
    const files = fs.readdirSync(dirPath);
    let directoryList = [];

    files.forEach((file) => 
    {
        const fullPath = path.join(dirPath, file);

        const stat = fs.statSync(fullPath);

        if (stat.isDirectory())
        {
            //fileList = fileList.concat(getAllFiles(fullPath));
            directoryList.push(fullPath);
        }
        else
        {
            fileList.push(fullPath);
        }
    });

    directoryList.forEach((directory) =>
    {
        fileList = fileList.concat(getAllFiles(directory));
    });

    return fileList;
}

function write7BitEncodedInt(bufferArray, value)
{
    while (value >= 0x80)
    {
        bufferArray.push(Buffer.from([value | 0x80]));
        value >>= 7;
    }
    bufferArray.push(Buffer.from([value]));
}

function writeBinaryString(bufferArray, str)
{
    const encoder = new TextEncoder();
    const encodedString = encoder.encode(str);
    write7BitEncodedInt(bufferArray, encodedString.length);
    bufferArray.push(Buffer.from(encodedString));
}

function createBinaryFile(inputDir, inputBinaryFile, outputBinaryFile)
{
    const dataBuffer = fs.readFileSync(inputBinaryFile);

    const bufferArray = [];
    var magic = dataBuffer.readInt32LE(0);
    var tmpVal = dataBuffer.readInt32LE(4);
    var version = dataBuffer.readInt32LE(8);

    const fileList = getAllFiles(inputDir);
    const headerBuffer = Buffer.alloc(12);
    headerBuffer.writeInt32LE(magic, 0);
    headerBuffer.writeInt32LE(tmpVal, 4);
    headerBuffer.writeInt32LE(version, 8);
    bufferArray.push(headerBuffer);

    const fileCountBuffer = Buffer.alloc(4);
    fileCountBuffer.writeInt32LE(fileList.length, 0);
    bufferArray.push(fileCountBuffer);
    var count = 0;

    fileList.forEach((filePath) =>
    {
        var fileName = path.relative(inputDir, filePath);
        fileName = fileName.replace(/\\/g, '/');
        const fileContent = fs.readFileSync(filePath);

        writeBinaryString(bufferArray, fileName);

        const contentLengthBuffer = Buffer.alloc(4);
        contentLengthBuffer.writeInt32LE(fileContent.length, 0);
        bufferArray.push(contentLengthBuffer);

        bufferArray.push(fileContent);

        console.log(`${count} pushed.`);
    });

    const finalBuffer = Buffer.concat(bufferArray);
    fs.writeFileSync(outputBinaryFile, finalBuffer);

    console.log(`Binary file created at: ${outputBinaryFile}`);
}

function createCrcSizeFile(outputBinaryFile, outputCrcFile)
{
    const dataBuffer = fs.readFileSync(outputBinaryFile);

    const length = dataBuffer.length;
    const bufferCrc32 = crc32(dataBuffer);

    const outputContent = `${length}|${bufferCrc32}`;
    fs.writeFileSync(outputCrcFile, outputContent);
    console.log(`Crc32 result exported to: ${outputCrcFile}`);
}

const inputDirectory = './export';
const inputBinaryFile = 'LWScripts.data';
const outputBinaryFile = 'LWScriptsNew.data';
const outputCrcFile = 'LWScriptsNew.txt';

if (!fs.existsSync(inputDirectory))
{
    console.error(`Input director "${inputDirectory}" does not exist.`);
    process.exit(1);
}

createBinaryFile(inputDirectory, inputBinaryFile, outputBinaryFile);
createCrcSizeFile(outputBinaryFile, outputCrcFile);
