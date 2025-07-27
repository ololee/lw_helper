const fs = require('fs');
const path = require('path');

function read7BitEncodedInt(dataBuffer, offset)
{
    let result = 0;
    let offsetLen = 0;
    let bitsRead = 0;

    while (true)
    {
        if (bitsRead >= 35) throw new Error("Invalid 7-bit encoded integer.");

        const byte = dataBuffer.readInt8(offset++);
        offsetLen++;
        result |= (byte & 0x7F) << bitsRead;
        bitsRead += 7;

        if ((byte & 0x80) === 0) break;
    }

    return {
        offsetLen: offsetLen,
        contentLength: result,
    };
}

function extractFiles(scriptFile)
{
    const dataBuffer = fs.readFileSync(scriptFile);

    var offset = 0;
    dataBuffer.readInt32LE(offset);

    offset += 4;
    dataBuffer.readInt32LE(offset);
    offset += 4;
    var version = dataBuffer.readInt32LE(offset);
    offset += 4;
    var count = dataBuffer.readInt32LE(offset);
    offset += 4;
    for (var i = 0; i < count; i++)
    {
        var encodeInfo = read7BitEncodedInt(dataBuffer, offset);
        offset += encodeInfo.offsetLen;
        var nameLength = encodeInfo.contentLength;
        const name = dataBuffer.slice(offset, offset + nameLength).toString('utf-8');
        offset += nameLength;
        
        var contentLength = dataBuffer.readInt32LE(offset);
        offset += 4;
        
        var content = dataBuffer.slice(offset, offset + contentLength);
        offset += contentLength;

        var saveFileName = "export/" + name;
        const directory = path.dirname(saveFileName);
        fs.mkdirSync(directory, {recursive: true});
        fs.writeFileSync("export/" + name, content);
        console.log(`Extracted: ${name}`);
    }
}

const scriptFile = 'LWScripts.data';
extractFiles(scriptFile);
