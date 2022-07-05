// Parser for the packets. Each port indicates something.
function decodeUplink(input) {
  let res = {data: {bytes: input.bytes} , warnings: [] , errors: []};
  
  switch(input.fPort){
    //for sent strings
    case 1:
      res.data.texto = deBytesAString(input.bytes).slice(0,-1);
      break;
      
    case 2:
      //for the simple 3 pin temp sensor
      res.data.long = byteArrayToLong(res.data.bytes);
      res.data.grados = deVoltiosAGrados(res.data.long);
      break;
    
    case 3:
      //for the 4 pin humidity and temp sensor
      input.bytes.reverse();
      res.data.grados = aFloat(input.bytes.slice(0,4));
      res.data.humedad = aFloat(input.bytes.slice(-4));
      break;
      
    case 4:
      //for the 4 pin humidity and temp sensor
      res.data.grados = sflt162f((input.bytes[1] << 8) + input.bytes[0])*100;
      res.data.humedad = sflt162f((input.bytes[3] << 8) + input.bytes[2])*100;
      break;
    case 6:
      //simply sending an int of the power used 
      res.data.pow = byteArrayToLong(res.data.bytes);
      break;
    default:
      
      //gps parse of data
      res.data.pow = byteArrayToLong(res.data.bytes.slice(0,1));
      res.data.lng = aFloat2(res.data.bytes.slice(1,5));
      res.data.lat = aFloat2(res.data.bytes.slice(5,10));
      break;
    
  }
  
  return res;
}


byteArrayToLong = function(byteArray) {
    var value = 0;
    for ( var i = byteArray.length - 1; i >= 0; i--) {
        value = (value * 256) + byteArray[i];
    }

    return value;
};

deVoltiosAGrados = function (entero){
  return (entero * 0.322 -50)
}
aFloat = function (array){
let buf = new ArrayBuffer(4);
let view = new DataView(buf);
array.forEach(function (b, i) {
    view.setUint8(i, b);
});
return view.getFloat32(0);
}
aFloat2 = function (array){
array = array.reverse();
let buf = new ArrayBuffer(4);
let view = new DataView(buf);
array.forEach(function (b, i) {
    view.setUint8(i, b);
});
return view.getFloat32(0);
}
deBytesAString = function (bytes) {
  return String.fromCharCode(...bytes)
}

function sflt162f(rawSflt16)
    {
    // rawSflt16 is the 2-byte number decoded from wherever;
    // it's in range 0..0xFFFF
    // bit 15 is the sign bit
    // bits 14..11 are the exponent
    // bits 10..0 are the the mantissa. Unlike IEEE format,
    // the msb is explicit; this means that numbers
    // might not be normalized, but makes coding for
    // underflow easier.
    // As with IEEE format, negative zero is possible, so
    // we special-case that in hopes that JavaScript will
    // also cooperate.
    //
    // The result is a number in the open interval (-1.0, 1.0);
    //

    // throw away high bits for repeatability.
    rawSflt16 &= 0xFFFF;

    // special case minus zero:
    if (rawSflt16 == 0x8000)
        return -0.0;

    // extract the sign.
    var sSign = ((rawSflt16 & 0x8000) !== 0) ? -1 : 1;

    // extract the exponent
    var exp1 = (rawSflt16 >> 11) & 0xF;

    // extract the "mantissa" (the fractional part)
    var mant1 = (rawSflt16 & 0x7FF) / 2048.0;

    // convert back to a floating point number. We hope
    // that Math.pow(2, k) is handled efficiently by
    // the JS interpreter! If this is time critical code,
    // you can replace by a suitable shift and divide.
    var f_unscaled = sSign * mant1 * Math.pow(2, exp1 - 15);

    return f_unscaled;
    }
