
/**
 * ajax 请求模块
 */

const { encryptPublicLong } = require('./jsencrypt');
const { hex_md5 } = require('./md5');

// 字符串转base64
var signKey = 'u*afNnLWi6g78K0dlOyIB9KHTfQmVPhvB';

var createEncrypt = function (data) {
    var pubKey = '-----BEGIN PUBLIC KEY-----'
    pubKey += 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDRRnWUDiF+c/LKNmsROebjTlIH'
    pubKey += '4uBWPytFYeNKV0kNfor1l6DFI7stvq1w5XIa+MBDniGOrHH4R3c8NcnHbTf2kHMD'
    pubKey += 'nLFUqRYHLNt8ytEC0S9vvMNxsJPskPhuV3rs2F/QOkRqtapXuEFkF2k083Oa4bBX'
    pubKey += 'TnpKvIxP0Hkrrqa/WQIDAQAB'
    pubKey += '-----END PUBLIC KEY-----'
    var dataStr = JSON.stringify(data);
    var encrypted = encryptPublicLong(dataStr, pubKey)
    return encrypted
};
var createSign = function (oParam) {
    if (!oParam) {
        return null
    }
    var keyValue = ''
    Object.keys(oParam).forEach(function (key) {
        keyValue += (key + oParam[key])
    });
    keyValue += signKey
    var md5Value = hex_md5(keyValue)
    return md5Value
}
/**
 * 请求方法
 * type 请求类型
 * url 请求地址
 * data 请求的数据
 * success 请求成功回调
 * error 请求失败回调
 */
function createData(data) {
    var newParam = {}
    if (data) {
        data['is_release'] = 0;
        newParam.d = createEncrypt(data)
    } else {
        data["is_release"] = 1;
    }
    newParam.t = parseInt(new Date().getTime() / 1000)

    newParam.sign = createSign(newParam)

    newParam = JSON.stringify(newParam);

    return newParam
}

console.log(createData({
    "city": "长沙市",
    "province": "湖南省",
    "dealer_type": "0",
    "lat": "28.2348894",
    "lon": "112.9454732",
    "site_id": "aGqZxcudmMbFb8eem5SXZWOalZafasRql2xpcpual8Zwlp0="
}))

